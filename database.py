import os
from pathlib import Path
from urllib.parse import quote_plus

import psycopg2
from psycopg2 import pool

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv(encoding="utf-8")


def _cargar_env_manual():
    ruta = Path(__file__).resolve().with_name(".env")
    if not ruta.exists():
        return
    for enc in ("utf-8", "latin-1"):
        try:
            lineas = ruta.read_text(encoding=enc).splitlines()
            break
        except UnicodeDecodeError:
            continue
    else:
        return
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        k, v = linea.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_cargar_env_manual()


def env(nombre, default=None):
    valor = os.environ.get(nombre)
    if valor not in (None, ""):
        return valor
    return default


def db_config():
    """Lee configuración DB solo cuando se necesita (no rompe el arranque)."""
    return {
        "host": env("DB_HOST", "localhost"),
        "database": env("DB_NAME", "samu"),
        "user": env("DB_USER", "postgres"),
        "password": env("DB_PASSWORD", ""),
        "port": int(env("DB_PORT", "5432") or "5432"),
    }


def database_url():
    c = db_config()
    if not c["password"]:
        return None
    return (
        f"postgresql://{c['user']}:{quote_plus(c['password'])}"
        f"@{c['host']}:{c['port']}/{c['database']}"
    )


_pool = None
ULTIMO_ERROR_CONEXION = ""


def pool_db():
    global _pool, ULTIMO_ERROR_CONEXION
    if _pool is not None:
        return _pool
    url = database_url()
    if not url:
        ULTIMO_ERROR_CONEXION = "DB_PASSWORD o credenciales no configuradas"
        raise RuntimeError(ULTIMO_ERROR_CONEXION)
    try:
        minc = int(env("DB_MIN_CONN", "1") or "1")
        maxc = int(env("DB_MAX_CONN", "20") or "20")
        _pool = pool.ThreadedConnectionPool(minc, maxc, dsn=url)
        return _pool
    except Exception as exc:
        ULTIMO_ERROR_CONEXION = str(exc)
        raise


def conexion():
    return pool_db().getconn()


def liberar(conn):
    if conn and _pool:
        _pool.putconn(conn)


def error_conexion():
    return ULTIMO_ERROR_CONEXION or "Error de conexión PostgreSQL"
