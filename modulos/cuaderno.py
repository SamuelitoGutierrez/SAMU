# modulos/cuaderno.py
from flask import Blueprint, render_template
from navbar import obtener_datos_navbar

cuaderno_bp = Blueprint('cuaderno', __name__)

@cuaderno_bp.route('/cuaderno')
def index():
    # Obtienes el contexto del menú para esta página
    context = obtener_datos_navbar()
    return render_template('lobby_cuaderno.html', **context)
