import os
import importlib
from flask import Flask, session, request, redirect, url_for, render_template_string, Blueprint

def iniciar_servidor_samu():
    aplicacion = Flask(__name__)
    aplicacion.secret_key = 'samu_2026_highway_super_secret_key'

    print("==================================================")
    print(" INICIANDO CEREBRO GLOBAL SAMU 2026 ")
    print("==================================================")

    # 1. LISTA MAESTRA DE MÓDULOS
    todos_los_modulos = [
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
        "vistas_combustible_almacen", "vistas_combustible_equipo", "vistas_horas_maquina",
        "vistas_inicio", "vistas_login", "vistas_maquinaria", "vistas_mensajes_panel",
        "vistas_navbar", "vistas_notificaciones", "vistas_operativos_maquinaria",
        "vistas_papeleta", "vistas_partidas_metrados", "vistas_perfil",
        "vistas_personal_obra", "vistas_recuperacion_password", "vistas_registro_personal",
        "vistas_residencia", "vistas_supervision", "vistas_topografia"
    ]

    print("Cargando y enlazando todo el ecosistema de SAMU...")
    for nombre_modulo in todos_los_modulos:
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
            pass
        except Exception as e:
            print(f" [!] Alerta en {nombre_modulo}.py: {str(e)}")

    print("==================================================")

    # 2. SISTEMA GLOBAL DE PERMISOS
    @aplicacion.before_request
    def guardian_de_accesos():
        rutas_libres = ['login.mostrar_login', 'inicio.panel_principal', 'static']
        if request.endpoint in rutas_libres or not request.endpoint:
            return

        if 'usuario_id' not in session:
            return redirect(url_for('login.mostrar_login'))

        rol = session.get('rol')
        ruta = request.endpoint 

        if rol == 'Admin':
            return 

        if rol in ['Ingeniero', 'Residente', 'Supervisor']:
            if not any(ruta.startswith(m) for m in ['cuaderno.', 'personal.', 'avance.', 'inicio.']):
                return generar_error_403()
                
        elif rol == 'Maquinaria':
            if not any(ruta.startswith(m) for m in ['mecanico.', 'inicio.']):
                return generar_error_403()

    # 3. INTERFACES DE ERROR
    def generar_error_403():
        return render_template_string("""
        <div style="font-family: 'Inter', Arial, sans-serif; text-align: center; margin-top: 20vh;">
            <h1 style="font-size: 5rem; color: #1d1d1f; font-weight: 600; letter-spacing: -2px;">403</h1>
            <h2 style="color: #1d1d1f; font-weight: 500;">Acceso Restringido</h2>
            <p style="color: #86868b;">Tu credencial actual no tiene permisos para este módulo.</p>
            <a href="/panel" style="display: inline-block; margin-top: 15px; padding: 10px 20px; background: #000; color: white; text-decoration: none; border-radius: 20px; font-size: 0.9rem;">Volver al Panel</a>
        </div>
        """), 403

    @aplicacion.errorhandler(404)
    def error_404(e):
        return render_template_string("""
        <div style="font-family: 'Inter', Arial, sans-serif; text-align: center; margin-top: 20vh;">
            <h1 style="font-size: 5rem; color: #1d1d1f; font-weight: 600; letter-spacing: -2px;">404</h1>
            <h2 style="color: #1d1d1f; font-weight: 500;">Módulo Inactivo</h2>
            <p style="color: #86868b;">El sistema SAMU detecta que este archivo aún no tiene interfaz.</p>
            <a href="/panel" style="display: inline-block; margin-top: 15px; padding: 10px 20px; background: #000; color: white; text-decoration: none; border-radius: 20px; font-size: 0.9rem;">Volver al Panel</a>
        </div>
        """), 404

    return aplicacion

# --- ¡ESTA ES LA CLAVE PARA QUE EL SERVIDOR NO SE CAIGA (502) ---
# Declaramos 'app' de forma global para que el servidor en la nube lo reconozca
app = iniciar_servidor_samu()

if __name__ == '__main__':
    # Usamos el puerto dinámico del servidor, o 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
