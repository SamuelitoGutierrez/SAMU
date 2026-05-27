import os

import psycopg2
from psycopg2 import pool


DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "database": os.environ.get("DB_NAME", "postgres"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "port": int(os.environ.get("DB_PORT", "5432")),
}

_connection_pool = None


def init_connection_pool(minconn=1, maxconn=10):
    """Inicializa el pool de conexiones a PostgreSQL."""
    global _connection_pool

    if _connection_pool is None:
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
