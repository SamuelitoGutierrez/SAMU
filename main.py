"""
SAMU-GLOBAL KITS — Punto de entrada Flask.
Seguridad: CSRF, sesiones firmadas, SECRET_KEY obligatoria en producción.
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv(encoding="utf-8")

from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect

from config import Config
from store import init_db, ultimo_error
from vistas_login import login_bp
from vistas_panel import panel_bp

csrf = CSRFProtect()


def crear_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Carpeta persistente para cotizaciones, boletas y PDF (volumen Coolify)
    docs = Path(app.config["STORAGE_DOCUMENTS"])
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "cotizaciones").mkdir(exist_ok=True)
    (docs / "boletas").mkdir(exist_ok=True)
    (docs / "anexos").mkdir(exist_ok=True)

    csrf.init_app(app)
    app.register_blueprint(login_bp)
    app.register_blueprint(panel_bp)
    csrf.exempt(app.view_functions["panel.api_datos"])

    @app.route("/health")
    def health():
        db_ok = init_db()
        return jsonify({
            "ok": True,
            "app": Config.NOMBRE_APP,
            "db": db_ok,
            "storage": str(docs),
            "error_db": None if db_ok else ultimo_error(),
        })

    return app


app = crear_app()


if __name__ == "__main__":
    if init_db():
        print(f"[{Config.NOMBRE_APP}] Base de datos lista.")
    else:
        print(f"AVISO DB: {ultimo_error()}")
    print(f"Almacén documentos: {Config.STORAGE_DOCUMENTS}")
    print(f"URL pública → {Config.PUBLIC_URL}/login")
    port = int(os.environ.get("PORT", 3000))
    debug = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
