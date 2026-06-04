import os
import sys
from urllib.parse import quote_plus

import psycopg2

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv(encoding="utf-8")


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
    f"postgresql://{DB_CONFIG['user']}:{quote_plus(DB_CONFIG['password'])}"
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


MIGRACIONES = [
    # Tabla principal de Residencia.
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS tipo VARCHAR(40) NOT NULL DEFAULT 'Residente'",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS estado VARCHAR(40) NOT NULL DEFAULT 'Borrador'",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS avance INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS bloqueado BOOLEAN NOT NULL DEFAULT FALSE",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS firmado_por VARCHAR(160)",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS firmado_en TIMESTAMP",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS contenido TEXT",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS observaciones TEXT",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS personal_gastos_generales JSONB NOT NULL DEFAULT '[]'::jsonb",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW()",
    "ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW()",

    # Tabla del flujo del Inspector / Supervisión.
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS numero INTEGER",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS residencia_numero INTEGER",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS fecha DATE",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS estado VARCHAR(40) NOT NULL DEFAULT 'borrador_inspector'",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS contenido TEXT",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS firmado_por VARCHAR(160)",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS firmado_en TIMESTAMP",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS personal_supervision JSONB NOT NULL DEFAULT '[]'::jsonb",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS partidas_ejecutadas TEXT",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS almacen_ingreso TEXT",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS almacen_salida TEXT",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS maquinaria TEXT",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS ocurrencias TEXT",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW()",
    "ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW()",

    # Compatibilidad con instalaciones antiguas donde residencia_numero era obligatorio.
    "ALTER TABLE cuaderno_inspector_asientos ALTER COLUMN residencia_numero DROP NOT NULL",
    "ALTER TABLE cuaderno_inspector_asientos ALTER COLUMN estado SET DEFAULT 'borrador_inspector'",
]


def conectar():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    return psycopg2.connect(**DB_CONFIG)


def main():
    conn = None
    try:
        conn = conectar()
        conn.autocommit = False
        with conn.cursor() as cur:
            for sql in MIGRACIONES:
                print(f"Ejecutando: {sql}")
                cur.execute(sql)
        conn.commit()
        print("Migracion completada correctamente. No se eliminaron ni modificaron datos existentes.")
        return 0
    except Exception as exc:
        if conn:
            conn.rollback()
        print(f"Error ejecutando migracion: {exc}", file=sys.stderr)
        return 1
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
