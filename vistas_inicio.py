from flask import Blueprint, render_template_string, session
from navbar import obtener_navbar

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/panel')
def panel_principal():
    es_admin = session.get('rol') == 'Admin'
    nombre = session.get('nombre', 'Visitante')

    # Traemos el Mega-Menú desde navbar.py
    menu_superior = obtener_navbar(es_admin, nombre)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU - Panel Central</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Bauhaus+93&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0; font-family: 'Inter', sans-serif; background-color: #fbfbfd;
                color: #1d1d1f; overflow-x: hidden;
            }
            .hero-section { padding-top: 180px; text-align: center; }
            .badge-status { padding: 6px 16px; border-radius: 20px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
            .bg-visual { background: #f2f2f7; color: #86868b; }
            .bg-admin { background: #000; color: #fff; }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}

        <div class="hero-section">
            <h1 style="font-size: 56px; font-weight: 600; letter-spacing: -1.2px;">Panel Central 2026</h1>
            <p style="font-size: 21px; color: #86868b;">Gestión de frentes para la carretera PU N-110.</p>
            <span class="badge-status {{ 'bg-admin' if es_admin else 'bg-visual' }}">
                {{ 'Modo Administrativo: Full Acceso' if es_admin else 'Modo Lectura: Vista Previa' }}
            </span>
        </div>

    </body>
    </html>
    """, menu_superior=menu_superior, es_admin=es_admin)
