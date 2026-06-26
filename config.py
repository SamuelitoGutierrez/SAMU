"""Configuración central — SAMU-GLOBAL KITS."""
import os
from datetime import timedelta


def _env(nombre, default=None):
    valor = os.environ.get(nombre)
    if valor not in (None, ""):
        return valor
    return default


def obtener_secret_key():
    clave = _env("SECRET_KEY")
    entorno = (_env("ENTORNO", "produccion") or "produccion").lower()
    fallback = "samu-global-kits-produccion-cambiar-esta-clave-ya"
    if not clave:
        if entorno in ("produccion", "production"):
            print("AVISO: SECRET_KEY no definida — usando clave temporal. Configúrala en Coolify.")
            return fallback
        return "solo-desarrollo-no-usar-en-produccion"
    if len(clave) < 16:
        print("AVISO: SECRET_KEY muy corta — usa al menos 32 caracteres en producción.")
    return clave


class Config:
    NOMBRE_APP = "SAMU-GLOBAL KITS"
    ENTORNO = _env("ENTORNO", "produccion")

    SECRET_KEY = obtener_secret_key()

    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _env("SESSION_COOKIE_SECURE", "0") in ("1", "true", "yes")

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    DB_HOST = _env("DB_HOST", "localhost")
    DB_NAME = _env("DB_NAME", "samu")
    DB_USER = _env("DB_USER", "postgres")
    DB_PASSWORD = _env("DB_PASSWORD", "")
    DB_PORT = int(_env("DB_PORT", "5432") or "5432")

    STORAGE_DOCUMENTS = _env("STORAGE_DOCUMENTS", "/app/storage/documents")

    PUBLIC_URL = (_env("PUBLIC_URL", "http://85.31.62.90:3000") or "").rstrip("/")
    PORT = int(_env("PORT", "3000") or "3000")

    LOGIN_USER = _env("LOGIN_USER", "admin")
    LOGIN_PASSWORD = _env("LOGIN_PASSWORD", "admin123")
    LOGIN_NOMBRE = _env("LOGIN_NOMBRE", "Administrador")
