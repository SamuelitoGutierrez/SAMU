# =========================================================
# navbar.py
# SAMU Ingeniería — Lógica dinámica del navbar
# =========================================================

try:
    from vistas_navbar import HTML_NAVBAR
except ImportError:
    HTML_NAVBAR = ""

def obtener_navbar(es_admin, nombre_usuario):
    """
    Toma la plantilla HTML_NAVBAR y reemplaza las variables
    dinámicas según la sesión del usuario actual.
    """
    admin_js = 'true' if es_admin else 'false'
    
    # CORRECCIÓN DE ESTADO DE SESIÓN
    if not nombre_usuario or nombre_usuario == 'Visitante':
        # Muestra "INICIAR SESIÓN" como un enlace que lleva al Login
        html_usuario = '<a href="/" style="color: #1d1d1f; text-decoration: none; cursor: pointer; transition: opacity 0.2s;" onmouseover="this.style.opacity=0.6" onmouseout="this.style.opacity=1">INICIAR SESIÓN</a> <i class="bi bi-person-circle ms-2" style="font-size: 1.3rem; color: #1d1d1f;"></i>'
    else:
        # Muestra el nombre real del usuario autenticado (ej: SAMU)
        html_usuario = f'<span style="color: #1d1d1f;">{nombre_usuario}</span> <i class="bi bi-person-circle ms-2" style="font-size: 1.3rem; color: #1d1d1f;"></i>'
    
    # Inyectamos los datos en la plantilla HTML
    html_final = HTML_NAVBAR.replace("{HTML_USUARIO}", html_usuario).replace("{ADMIN_JS}", admin_js)
    
    return html_final
