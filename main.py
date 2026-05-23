import os
import importlib
from flask import Flask, session, request, redirect, url_for, render_template_string, Blueprint

def iniciar_servidor_samu():
    app = Flask(__name__)
    app.secret_key = 'samu_2026_highway_super_secret_key'

    print("==================================================")
    print(" INICIANDO CEREBRO SAMU 2026 ")
    print("==================================================")

    # 1. LISTA MAESTRA DE TODOS TUS PYS
    # El sistema recorrerá esto y conectará lo que ya exista.
    # Lo que aún no exista (archivos vacíos), lo ignorará sin causar errores,
    # y cuando los crees, los conectará automáticamente.
    todos_los_modulos = [
        "vistas_activar_cuenta", "vistas_actividades", "vistas_almacen_materiales",
        "vistas_analisis_actividades", "vistas_analisis_almacen_materiales",
        "vistas_analisis_asistencias", "vistas_analisis_combustible_almacen",
        "vistas_analisis_combustible_equipo", "vistas_analisis_horas_maquina",
        "vistas_analisis_maquinaria", "vistas_analisis_operativos_maquinaria",
        "vistas_analisis_papeletas", "vistas_analisis_partidas_metrados",
        "vistas_analisis_personal_obra", "vistas_analisis_registro_personal",
        "vistas_analisis_residencia", "vistas_analisis_supervicion",
        "vistas_anaslisis_registro_personal", "vistas_asistencias",
        "vistas_busqueda_global", "vistas_chat", "vistas_combustible_almacen",
        "vistas_combustible_equipo", "vistas_horas_maquina", "vistas_inicio",
        "vistas_login", "vistas_maquinaria", "vistas_mensajes_panel",
        "vistas_navbar", "vistas_notificaciones", "vistas_operativos_maquinaria",
        "vistas_papeleta", "vistas_partidas_metrados", "vistas_perfil",
        "vistas_personal_obra", "vistas_recuperacion_password",
        "vistas_registro_personal", "vistas_residencia", "vistas_supervision",
        "vistas_topografia"
    ]

    print("Cargando módulos de vistas...")
    for nombre_modulo in todos_los_modulos:
        try:
            # Intenta importar el archivo .py
            modulo = importlib.import_module(nombre_modulo)
            
            # Busca si dentro del archivo hay un "Blueprint" y lo conecta
            modulo_conectado = False
            for atributo_nombre in dir(modulo):
                atributo = getattr(modulo, atributo_nombre)
                if isinstance(atributo, Blueprint):
                    app.register_blueprint(atributo)
                    modulo_conectado = True
                    print(f" [OK] Conectado: {nombre_modulo}.py")
            
            if not modulo_conectado:
                print(f" [INFO] {nombre_modulo}.py existe, pero aún no tiene código de Blueprint.")
                
        except ModuleNotFoundError:
            # Si el archivo aún no lo has creado, no pasa nada, el servidor sigue funcionando
            pass
        except Exception as e:
            print(f" [ERROR] Problema en {nombre_modulo}.py: {str(e)}")

    print("==================================================")

    # 2. SISTEMA GLOBAL DE PERMISOS (NUNCA MÁS TENDRÁS QUE TOCAR ESTO)
    @app.before_request
    def guardian_de_accesos():
        # A. Rutas que no requieren contraseña (El login y archivos estáticos)
        if request.endpoint in ['login.mostrar_login', 'static'] or not request.endpoint:
            return

        # B. ¿El usuario inició sesión?
        if 'usuario_id' not in session:
            # Si quiere entrar a una ruta y no está logueado, lo mandamos al login
            return redirect(url_for('login.mostrar_login'))

        # C. MATRIZ DE PERMISOS
        rol = session.get('rol')

        # --- PERMISO ABSOLUTO PARA EL DUEÑO (TÚ) ---
        if rol == 'Admin':
            return # 'return' vacío significa: "Déjalo pasar a donde quiera"

        # --- PERMISOS PARA OTROS ROLES (Se restringe según el inicio del endpoint) ---
        ruta = request.endpoint 
        
        if rol in ['Ingeniero', 'Residente']:
            # Solo acceden a cuaderno, personal, avance y el panel de inicio
            if not any(ruta.startswith(m) for m in ['cuaderno.', 'personal.', 'avance.', 'inicio.']):
                return generar_error_403()
                
        elif rol == 'Maquinaria':
            if not any(ruta.startswith(m) for m in ['mecanico.', 'inicio.']):
                return generar_error_403()

    # 3. INTERFACES DE ERROR ESTILO APPLE
    def generar_error_403():
        return render_template_string("""
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 20vh;">
            <h1 style="font-size: 4rem; color: #1d1d1f;">403</h1>
            <h2 style="color: #1d1d1f;">Acceso Restringido</h2>
            <p style="color: #86868b;">No tienes permisos para ver este módulo.</p>
        </div>
        """), 403

    @app.errorhandler(404)
    def error_404(e):
        return render_template_string("""
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 20vh;">
            <h1 style="font-size: 4rem; color: #1d1d1f;">404</h1>
            <h2 style="color: #1d1d1f;">Módulo en Construcción</h2>
            <p style="color: #86868b;">Este archivo .py aún no ha sido creado o registrado.</p>
        </div>
        """), 404

    return app

if __name__ == '__main__':
    app = iniciar_servidor_samu()
    # Arrancamos el servidor de forma local/producción
    app.run(debug=True, host='0.0.0.0', port=5000)
