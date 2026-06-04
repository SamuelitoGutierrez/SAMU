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


DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "database": os.environ.get("DB_NAME", "samu"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", "AQUI_VA_LA_CLAVE"),
    "port": int(os.environ.get("DB_PORT", "5432")),
}

DEFAULT_DATABASE_URL = "postgresql://postgres:AQUI_VA_LA_CLAVE@localhost:5432/samu"
LOCAL_DATABASE_URL = (
    f"postgresql://{quote_plus(DB_CONFIG['user'])}:{quote_plus(DB_CONFIG['password'])}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("SQLALCHEMY_DATABASE_URI") or LOCAL_DATABASE_URL or DEFAULT_DATABASE_URL

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
