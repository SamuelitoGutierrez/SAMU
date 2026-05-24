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
    # Convertimos el booleano de Python a sintaxis de JavaScript
    admin_js = 'true' if es_admin else 'false'
    
    # Inyectamos los datos en la plantilla HTML
    html_final = HTML_NAVBAR.replace("{NOMBRE_USUARIO}", nombre_usuario).replace("{ADMIN_JS}", admin_js)
    
    return html_final
