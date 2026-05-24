# navbar.py
from flask import session

def obtener_datos_navbar():
    # Aquí defines toda tu estructura de navegación centralizada
    nombre = session.get('nombre', 'Visitante')
    is_admin = session.get('rol') == 'Admin'
    
    # Definimos los módulos del sistema aquí
    menu_data = [
        {"label": "Cuaderno de Obra", "url": "/cuaderno"},
        {"label": "Control del Personal", "url": "/personal"},
        {"label": "Equipo Mecánico", "url": "/maquinaria"},
        {"label": "Almacén", "url": "/almacen"},
        {"label": "Avance de Obra", "url": "/avance"},
        {"label": "Sistema", "url": "/sistema"}
    ]
    
    return {
        "menu_items": menu_data,
        "usuario": nombre,
        "es_admin": is_admin
    }
