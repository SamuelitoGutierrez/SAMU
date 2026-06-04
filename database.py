import os
from urllib.parse import quote_plus

import psycopg2
from psycopg2 import pool

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv(encoding="utf-8")


def valor_env(nombre, requerido=True, respaldo=None):
    valor = os.environ.get(nombre)
    if valor not in (None, ""):
        return valor
    if respaldo is not None:
        return respaldo
    if requerido:
        raise RuntimeError(f"Variable de entorno obligatoria no configurada: {nombre}")
    return ""


DB_CONFIG = {
    "host": valor_env("DB_HOST"),
    "database": valor_env("DB_NAME"),
    "user": valor_env("DB_USER"),
    "password": valor_env("DB_PASSWORD"),
    "port": int(valor_env("DB_PORT", requerido=False, respaldo="5432")),
}

DATABASE_URL = (
    f"postgresql://{DB_CONFIG['user']}:{quote_plus(DB_CONFIG['password'])}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

_connection_pool = None


def init_connection_pool(minconn=None, maxconn=None):
    """Inicializa el pool de conexiones a PostgreSQL."""
    global _connection_pool
    minconn = int(valor_env("DB_MIN_CONN", str(minconn or 1)))
    maxconn = int(valor_env("DB_MAX_CONN", str(maxconn or 30)))

    if _connection_pool is None:
        if DATABASE_URL:
            _connection_pool = pool.ThreadedConnectionPool(minconn, maxconn, dsn=DATABASE_URL)
        else:
            _connection_pool = pool.ThreadedConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                **DB_CONFIG,
            )

    return _connection_pool


def get_connection():
    """Obtiene una conexion disponible desde el pool."""
    connection_pool = init_connection_pool()
    try:
        return connection_pool.getconn()
    except pool.PoolError as exc:
        raise RuntimeError(
            "No hay conexiones PostgreSQL disponibles en el pool. "
            "Aumente DB_MAX_CONN o revise que las conexiones se liberen correctamente. "
            f"Detalle: {exc}"
        ) from exc


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
