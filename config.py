"""Configuración central — SAMU-GLOBAL KITS."""
import os
from datetime import timedelta


def _env(nombre, default=None, requerido=False):
    valor = os.environ.get(nombre)
    if valor not in (None, ""):
        return valor
    if default is not None:
        return default
    if requerido:
        raise RuntimeError(f"Variable de entorno obligatoria: {nombre}")
    return ""


def obtener_secret_key():
    clave = _env("SECRET_KEY")
    placeholder = "cambiar_clave_secreta_en_coolify"
    entorno = _env("ENTORNO", default="desarrollo").lower()
    if not clave or clave == placeholder:
        if entorno in ("produccion", "production"):
            raise RuntimeError(
                "SECRET_KEY no configurada. Defínela en Coolify antes de desplegar."
            )
        return "solo-desarrollo-no-usar-en-produccion"
    if len(clave) < 32:
        raise RuntimeError("SECRET_KEY debe tener al menos 32 caracteres.")
    return clave


class Config:
    NOMBRE_APP = "SAMU-GLOBAL KITS"
    ENTORNO = _env("ENTORNO", default="desarrollo")
    SECRET_KEY = obtener_secret_key()

    # Sesiones seguras
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _env("SESSION_COOKIE_SECURE", "0") in ("1", "true", "yes")

    # CSRF (Flask-WTF)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Base de datos
    DB_HOST = _env("DB_HOST", requerido=True)
    DB_NAME = _env("DB_NAME", requerido=True)
    DB_USER = _env("DB_USER", requerido=True)
    DB_PASSWORD = _env("DB_PASSWORD", requerido=True)
    DB_PORT = int(_env("DB_PORT", default="5432"))

    # Almacenamiento persistente de PDFs y anexos (volumen Docker)
    STORAGE_DOCUMENTS = _env("STORAGE_DOCUMENTS", default="/app/storage/documents")

    PUBLIC_URL = _env("PUBLIC_URL", default="http://85.31.62.90:3000").rstrip("/")

    LOGIN_USER = _env("LOGIN_USER", default="admin")
    LOGIN_PASSWORD = _env("LOGIN_PASSWORD", default="admin123")
    LOGIN_NOMBRE = _env("LOGIN_NOMBRE", default="Administrador")
