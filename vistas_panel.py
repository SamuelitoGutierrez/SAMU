"""Panel principal y API de datos persistentes."""
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from store import cargar_dato, guardar_dato

panel_bp = Blueprint("panel", __name__)


def _requiere_sesion():
    if not session.get("usuario_id"):
        session["despues_login"] = request.full_path
        return redirect(url_for("login.iniciar_sesion"))
    return None


@panel_bp.route("/panel")
def inicio():
    redir = _requiere_sesion()
    if redir:
        return redir
    return render_template(
        "blank.html",
        usuario=session.get("nombre") or session.get("usuario", ""),
    )


@panel_bp.route("/api/datos", methods=["GET", "POST"])
def api_datos():
    redir = _requiere_sesion()
    if redir:
        return jsonify({"ok": False, "message": "No autenticado"}), 401

    uid = session["usuario_id"]
    clave = request.args.get("clave") or (request.get_json(silent=True) or {}).get("clave") or "panel"

    if request.method == "GET":
        datos, err = cargar_dato(uid, clave)
        if err:
            return jsonify({"ok": False, "message": err}), 500
        return jsonify({"ok": True, "clave": clave, "datos": datos})

    payload = request.get_json(silent=True) or {}
    valor = payload.get("datos", payload.get("valor", {}))
    ok, err = guardar_dato(uid, clave, valor)
    if not ok:
        return jsonify({"ok": False, "message": err}), 500
    return jsonify({"ok": True, "message": "Guardado"})
