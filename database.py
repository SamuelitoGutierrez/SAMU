import os
from urllib.parse import quote_plus

import psycopg2
from psycopg2 import pool

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()


def valor_env(nombre, respaldo):
    valor = os.environ.get(nombre)
    return valor if valor not in (None, "") else respaldo


DB_CONFIG = {
    "host": valor_env("DB_HOST", "localhost"),
    "database": valor_env("DB_NAME", "samu"),
    "user": valor_env("DB_USER", "postgres"),
    "password": valor_env("DB_PASSWORD", "PON_TU_CLAVE_AQUI"),
    "port": int(valor_env("DB_PORT", "5432")),
}

DEFAULT_DATABASE_URL = "postgresql://postgres:PON_TU_CLAVE_AQUI@localhost:5432/samu"
LOCAL_DATABASE_URL = (
    f"postgresql://{quote_plus(DB_CONFIG['user'])}:{quote_plus(DB_CONFIG['password'])}"
    f"@localhost:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)


def normalizar_database_url(url):
    if not url:
        return url
    return (
        url.replace("@postgresql:", "@localhost:")
        .replace("@postgresql/", "@localhost/")
    )


DATABASE_URL = normalizar_database_url(
    os.environ.get("DATABASE_URL") or os.environ.get("SQLALCHEMY_DATABASE_URI") or LOCAL_DATABASE_URL or DEFAULT_DATABASE_URL
)

_connection_pool = None


def init_connection_pool(minconn=1, maxconn=10):
    """Inicializa el pool de conexiones a PostgreSQL."""
    global _connection_pool

    if _connection_pool is None:
        if DATABASE_URL:
            _connection_pool = pool.SimpleConnectionPool(minconn, maxconn, dsn=DATABASE_URL)
        else:
            _connection_pool = pool.SimpleConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                **DB_CONFIG,
            )

    return _connection_pool


def get_connection():
    """Obtiene una conexion disponible desde el pool."""
    connection_pool = init_connection_pool()
    return connection_pool.getconn()


def release_connection(connection):
    """Devuelve una conexion al pool."""
    if _connection_pool is not None and connection is not None:
        _connection_pool.putconn(connection)


def close_all_connections():
    """Cierra todas las conexiones abiertas en el pool."""
    global _connection_pool

    if _connection_pool is not None:
        _connection_pool.closeall()
        _connection_pool = None
