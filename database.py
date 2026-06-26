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


def env(nombre, requerido=True, default=None):
    valor = os.environ.get(nombre)
    if valor not in (None, ""):
        return valor
    if default is not None:
        return default
    if requerido:
        raise RuntimeError(f"Variable de entorno obligatoria: {nombre}")
    return ""


DB = {
    "host": env("DB_HOST"),
    "database": env("DB_NAME"),
    "user": env("DB_USER"),
    "password": env("DB_PASSWORD"),
    "port": int(env("DB_PORT", requerido=False, default="5432")),
}

DATABASE_URL = (
    f"postgresql://{DB['user']}:{quote_plus(DB['password'])}"
    f"@{DB['host']}:{DB['port']}/{DB['database']}"
)

_pool = None


def pool_db():
    global _pool
    if _pool is None:
        minc = int(env("DB_MIN_CONN", requerido=False, default="1"))
        maxc = int(env("DB_MAX_CONN", requerido=False, default="20"))
        _pool = pool.ThreadedConnectionPool(minc, maxc, dsn=DATABASE_URL)
    return _pool


def conexion():
    try:
        return pool_db().getconn()
    except pool.PoolError as e:
        raise RuntimeError(f"Pool de conexiones agotado: {e}") from e


def liberar(conn):
    if conn and _pool:
        pool_db().putconn(conn)
