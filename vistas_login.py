"""Ventana de inicio de sesión."""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from store import login

login_bp = Blueprint("login", __name__)


def _sesion_activa():
    return session.get("usuario_id")


@login_bp.route("/")
def raiz():
    if _sesion_activa():
        return redirect(url_for("panel.inicio"))
    return redirect(url_for("login.iniciar_sesion"))


@login_bp.route("/login", methods=["GET", "POST"])
def iniciar_sesion():
    if _sesion_activa():
        return redirect(url_for("panel.inicio"))

    if request.method == "POST":
        usuario = (request.form.get("usuario") or "").strip()
        clave = request.form.get("clave") or ""
        perfil, err = login(usuario, clave)
        if perfil:
            session.permanent = True
            session["usuario_id"] = perfil["id"]
            session["usuario"] = perfil["usuario"]
            session["nombre"] = perfil["nombre"]
            destino = session.pop("despues_login", None) or url_for("panel.inicio")
            return redirect(destino)
        flash(err or "Usuario o contraseña incorrectos", "error")

    return render_template("login.html")


@login_bp.route("/logout")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("login.iniciar_sesion"))
