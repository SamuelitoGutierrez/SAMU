import os
import importlib
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, session, request, redirect, url_for, render_template_string, Blueprint
from mod_07_almacen import mod_07_bp

def iniciar_servidor_samu():
    aplicacion = Flask(__name__)
    aplicacion.secret_key = 'samu_2026_highway_super_secret_key'

    print("==================================================")
    print(" INICIANDO CEREBRO GLOBAL SAMU 2026 ")
    print("==================================================")

    # 1. LISTA MAESTRA DE ABSOLUTAMENTE TODOS LOS MÓDULOS
    todos_los_modulos = [
        # --- Módulos Modulares del Cuaderno de Obra ---
        "mod_01_jornal", "mod_02_personal", "mod_03_partidas", "mod_04_mayor_metrado",
        "mod_05_sub_partidas", "mod_06_actividades", "mod_07_almacen", "mod_08_maquinaria",
        "mod_09_herramientas", "mod_10_ocurrencias",
        
        # --- Módulos Originales del Sistema ---
        "activar_cuenta", "actividad_sistema", "actividades", "almacen_materiales",
        "analisis_actividades", "analisis_almacen_materiales", "analisis_asistencias",
        "analisis_combustible_almacen", "analisis_combustible_equipo", "analisis_horas_maquina",
        "analisis_maquinaria", "analisis_operativos_maquinaria", "analisis_papeletas",
        "analisis_partidas_metrados", "analisis_personal_obra", "analisis_residencia",
        "analisis_supervicion", "anaslisis_registro_personal", "asistencias",
        "busqueda_global", "chat", "combustible_almacen", "combustible_equipo",
        "horas_maquina", "inicio", "layout_base", "login", "maquinaria",
        "mensajes_enlaces", "mensajes_estado", "mensajes_panel", "mensajes_sonidos",
        "mensajes_utils", "navbar", "notificaciones", "notificador_email",
        "notificador_sms", "operativos_maquinaria", "papeleta", "partidas_metrados",
        "perfil", "personal_obra", "recuperacion_password", "registrador_modulos",
        "registro_personal", "residencia", "samu_crud", "supervision", "topografia",
        "ui_base", "utilidades_seguridad", "vistas", "vistas_activar_cuenta",
        "vistas_actividades", "vistas_almacen_materiales", "vistas_analisis_actividades",
        "vistas_analisis_almacen_materiales", "vistas_analisis_asistencias",
        "vistas_analisis_combustible_almacen", "vistas_analisis_combustible_equipo",
        "vistas_analisis_horas_maquina", "vistas_analisis_maquinaria",
        "vistas_analisis_operativos_maquinaria", "vistas_analisis_papeletas",
        "vistas_analisis_partidas_metrados", "vistas_analisis_personal_obra",
        "vistas_analisis_registro_personal", "vistas_analisis_residencia",
        "vistas_analisis_supervicion", "vistas_anaslisis_registro_personal",
        "vistas_asistencias", "vistas_busqueda_global", "vistas_chat",
        "vistas_combustible_almacen", "vistas_combustible_equipo", "vistas_cuaderno", 
        "vistas_horas_maquina", "vistas_inicio", "vistas_login", "vistas_maquinaria", 
        "vistas_mensajes_panel", "vistas_navbar", "vistas_notificaciones", 
        "vistas_operativos_maquinaria", "vistas_papeleta", "vistas_partidas_metrados", 
        "vistas_perfil", "vistas_personal_obra", "vistas_recuperacion_password", 
        "vistas_registro_personal", "vistas_residencia", "vistas_supervision", "vistas_topografia"
    ]

    # Registro explicito del Modulo 7 - Movimientos de Almacen.
    aplicacion.register_blueprint(mod_07_bp)
    modulos_registrados_directamente = {"mod_07_almacen"}

    print("Cargando y enlazando todo el ecosistema de SAMU...")
    for nombre_modulo in todos_los_modulos:
        if nombre_modulo in modulos_registrados_directamente:
            print(f" [VISTA OK] Conectado: {nombre_modulo}.py")
            continue

        try:
            modulo = importlib.import_module(nombre_modulo)
            es_vista = False
            for atributo_nombre in dir(modulo):
                atributo = getattr(modulo, atributo_nombre)
                if isinstance(atributo, Blueprint):
                    aplicacion.register_blueprint(atributo)
                    es_vista = True
                    print(f" [VISTA OK] Conectado: {nombre_modulo}.py")
            
            if not es_vista:
                print(f" [LÓGICA OK] Cargado en memoria: {nombre_modulo}.py")
                
        except ModuleNotFoundError:
            pass # Si el archivo no existe aún, sigue adelante sin romper el servidor
        except Exception as e:
            print(f" [!] Alerta en {nombre_modulo}.py: {str(e)}")

    print("==================================================")

    # 2. SISTEMA GLOBAL DE PERMISOS
    @aplicacion.before_request
    def guardian_de_accesos():
        # Añadida la ruta base del panel a las rutas libres verificadas por el guardián
        rutas_libres = ['login.mostrar_login', 'static']
        
        if request.endpoint in rutas_libres or not request.endpoint:
            return

        if 'usuario_id' not in session:
            return redirect(url_for('login.mostrar_login'))

        rol = session.get('rol')
        ruta = request.endpoint 

        # Acceso total para el dueño/administrador
        if rol == 'Admin':
            return 

        # Restricciones de otros roles
        if rol in ['Ingeniero', 'Residente', 'Supervisor']:
            # Se ha añadido 'mod_' para dar permisos a los nuevos micromódulos del cuaderno
            if not any(ruta.startswith(m) for m in ['cuaderno.', 'residencia.', 'supervision.', 'personal.', 'avance.', 'inicio.', 'mod_']):
                return generar_error_403()
                
        elif rol == 'Maquinaria':
            if not any(ruta.startswith(m) for m in ['mecanico.', 'inicio.']):
                return generar_error_403()

        elif rol == 'Almacenero':
            if not any(ruta.startswith(m) for m in ['almacen.', 'inicio.']):
                return generar_error_403()

    # 3. INTERFACES DE ERROR ESTILO APPLE
    def generar_error_403():
        return render_template_string("""
        <div style="font-family: 'Inter', Arial, sans-serif; text-align: center; margin-top: 20vh; background: #fbfbfd; height: 100vh; overflow: hidden; margin: 0; padding-top: 20vh;">
            <h1 style="font-size: 6rem; color: #1d1d1f; font-weight: 700; letter-spacing: -3px; margin: 0;">403</h1>
            <h2 style="color: #1d1d1f; font-weight: 500; font-size: 24px;">Acceso Restringido</h2>
            <p style="color: #86868b; margin-bottom: 25px;">Tu credencial actual no tiene permisos para este módulo.</p>
            <a href="/panel" style="display: inline-block; padding: 12px 25px; background: #0f172a; color: white; text-decoration: none; border-radius: 20px; font-size: 14px; transition: 0.3s;">Volver al Panel</a>
        </div>
        """), 403

    @aplicacion.errorhandler(404)
    def error_404(e):
        return render_template_string("""
        <div style="font-family: 'Inter', Arial, sans-serif; text-align: center; margin-top: 20vh; background: #fbfbfd; height: 100vh; overflow: hidden; margin: 0; padding-top: 20vh;">
            <h1 style="font-size: 6rem; color: #1d1d1f; font-weight: 700; letter-spacing: -3px; margin: 0;">404</h1>
            <h2 style="color: #1d1d1f; font-weight: 500; font-size: 24px;">Módulo Inactivo</h2>
            <p style="color: #86868b; margin-bottom: 25px;">El sistema SAMU detecta que este archivo aún no tiene interfaz o está en construcción.</p>
            <a href="/panel" style="display: inline-block; padding: 12px 25px; background: #0f172a; color: white; text-decoration: none; border-radius: 20px; font-size: 14px; transition: 0.3s;">Volver al Panel Central</a>
        </div>
        """), 404

    return aplicacion

# ==============================================================================
# DECLARACIÓN GLOBAL (LA CLAVE PARA EL DESPLIEGUE EN LA NUBE Y EVITAR EL 502)
# ==============================================================================
# La variable 'app' TIENE que estar expuesta en la raíz del archivo para WSGI
app = iniciar_servidor_samu()

if __name__ == '__main__':
    # Capturamos el puerto que asigne tu servidor en la nube,
    # o usamos el 3000/5000 por defecto para pruebas locales.
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, host='0.0.0.0', port=port)
