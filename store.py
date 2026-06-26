"""Datos persistentes — SAMU-GLOBAL KITS."""
import json
import os

from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from database import conexion, error_conexion, liberar

ULTIMO_ERROR = ""


def _fila_dict(cur, row):
    if not row:
        return None
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))


def ultimo_error():
    return ULTIMO_ERROR or "Error de base de datos"


def hash_clave(texto):
    return generate_password_hash(texto, method="scrypt")


def verificar_clave(hash_almacenado, texto_plano):
    if not hash_almacenado:
        return False
    if hash_almacenado.startswith(("scrypt:", "pbkdf2:", "argon2:")):
        return check_password_hash(hash_almacenado, texto_plano)
    return hash_almacenado == texto_plano


def _migrar_clave_si_plana(cur, usuario_id, hash_almacenado, texto_plano):
    if hash_almacenado.startswith(("scrypt:", "pbkdf2:", "argon2:")):
        return
    if hash_almacenado == texto_plano:
        cur.execute(
            "UPDATE usuarios SET clave = %s WHERE id = %s",
            (hash_clave(texto_plano), usuario_id),
        )


def init_db():
    global ULTIMO_ERROR
    conn = None
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                usuario VARCHAR(80) UNIQUE NOT NULL,
                clave VARCHAR(255) NOT NULL,
                nombre VARCHAR(160) NOT NULL,
                rol VARCHAR(40) NOT NULL DEFAULT 'comite',
                activo BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )
        cur.execute("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS rol VARCHAR(40) NOT NULL DEFAULT 'comite'")
        cur.execute("ALTER TABLE usuarios ALTER COLUMN clave TYPE VARCHAR(255)")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS datos_usuario (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                clave VARCHAR(120) NOT NULL,
                valor JSONB NOT NULL DEFAULT '{}'::jsonb,
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                UNIQUE (usuario_id, clave)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS documentos (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
                tipo VARCHAR(40) NOT NULL,
                nombre_archivo VARCHAR(255) NOT NULL,
                ruta VARCHAR(500) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )
        cur.execute("SELECT 1 FROM usuarios LIMIT 1")
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO usuarios (usuario, clave, nombre, rol) VALUES (%s, %s, %s, %s)",
                (
                    Config.LOGIN_USER,
                    hash_clave(Config.LOGIN_PASSWORD),
                    Config.LOGIN_NOMBRE,
                    "admin",
                ),
            )
        conn.commit()
        return True
    except Exception as exc:
        ULTIMO_ERROR = str(exc) or error_conexion()
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            liberar(conn)


def login(usuario, clave):
    if not init_db():
        return None, ultimo_error()
    conn = None
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, usuario, nombre, clave, rol FROM usuarios
            WHERE LOWER(usuario) = LOWER(%s) AND activo = TRUE
            LIMIT 1
            """,
            (usuario.strip(),),
        )
        fila = cur.fetchone()
        if not fila:
            return None, "Usuario o contraseña incorrectos"
        perfil = _fila_dict(cur, fila)
        if not verificar_clave(perfil.pop("clave"), clave):
            return None, "Usuario o contraseña incorrectos"
        _migrar_clave_si_plana(cur, perfil["id"], fila[3], clave)
        conn.commit()
        return perfil, None
    except Exception as exc:
        if conn:
            conn.rollback()
        return None, str(exc)
    finally:
        if conn:
            liberar(conn)


def guardar_dato(usuario_id, clave, valor):
    if not init_db():
        return False, ultimo_error()
    conn = None
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO datos_usuario (usuario_id, clave, valor, updated_at)
            VALUES (%s, %s, %s::jsonb, NOW())
            ON CONFLICT (usuario_id, clave) DO UPDATE SET
                valor = EXCLUDED.valor,
                updated_at = NOW()
            """,
            (usuario_id, clave, json.dumps(valor)),
        )
        conn.commit()
        return True, None
    except Exception as exc:
        if conn:
            conn.rollback()
        return False, str(exc)
    finally:
        if conn:
            liberar(conn)


def cargar_dato(usuario_id, clave):
    if not init_db():
        return None, ultimo_error()
    conn = None
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT valor FROM datos_usuario
            WHERE usuario_id = %s AND clave = %s LIMIT 1
            """,
            (usuario_id, clave),
        )
        row = cur.fetchone()
        if not row:
            return {}, None
        valor = row[0]
        if isinstance(valor, str):
            valor = json.loads(valor)
        return valor or {}, None
    except Exception as exc:
        return None, str(exc)
    finally:
        if conn:
            liberar(conn)


def ruta_documentos():
    path = Config.STORAGE_DOCUMENTS
    os.makedirs(path, exist_ok=True)
    return path
