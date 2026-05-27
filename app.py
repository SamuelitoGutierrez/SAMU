import os
import importlib
from flask import Flask, session, request, redirect, url_for, render_template_string, Blueprint
from mod_07_almacen import mod_07_bp

def crear_servidor_samu():
    app = Flask(__name__)
    
    # Llave maestra para encriptar las sesiones de los usuarios
    app.secret_key = 'samu_2026_highway_super_secret_key'

    # =====================================================================
    # 1. AUTO-DESCUBRIMIENTO DE MÓDULOS (BLUEPRINTS DINÁMICOS)
    # =====================================================================
    print("Iniciando Motor SAMU...")
    print("Buscando módulos en el sistema...")

    # Registro directo del Modulo 7 para que funcione aunque este servidor
    # cargue solo los archivos vistas_*.py por auto-descubrimiento.
    app.register_blueprint(mod_07_bp)
    print(" [+] Módulo conectado: mod_07_almacen -> (Ruta: /almacen)")
    
    # Escanea todos los archivos en el directorio actual
    for archivo in os.listdir('.'):
        # Solo procesa los archivos que son vistas (interfaces)
        if archivo.startswith('vistas_') and archivo.endswith('.py'):
            nombre_modulo = archivo[:-3] # Quita el '.py'
            try:
                # Importa el archivo automáticamente
                modulo = importlib.import_module(nombre_modulo)
                
                # Busca cualquier Blueprint dentro del archivo y lo registra
                for atributo_nombre in dir(modulo):
                    atributo = getattr(modulo, atributo_nombre)
                    if isinstance(atributo, Blueprint):
                        app.register_blueprint(atributo)
                        print(f" [+] Módulo conectado: {nombre_modulo} -> (Ruta: {atributo.url_prefix})")
            except Exception as e:
                print(f" [!] Error al cargar {nombre_modulo}: {e}")

    # =====================================================================
    # 2. EL GUARDIÁN GLOBAL DE PERMISOS (MATRIZ DE ACCESO)
    # =====================================================================
    @app.before_request
    def verificar_seguridad():
        # A. Rutas libres donde CUALQUIERA puede entrar sin iniciar sesión
        rutas_libres = [
            'inicio.panel_principal', # El Mega-Menú visual que creamos
            'login.mostrar_login',    # La pantalla de login
            'static'                  # Imágenes, CSS, logos
        ]

        # Si el endpoint es libre o no existe, déjalo pasar
        if request.endpoint in rutas_libres or not request.endpoint:
            return

        # B. Verificación de Sesión (¿Está logueado?)
        if 'usuario_id' not in session:
            # Si no está logueado y trata de entrar a un lugar privado, lo manda al login
            return redirect(url_for('inicio.panel_principal', modo='visual'))

        # C. Matriz de Permisos por Rol
        rol_usuario = session.get('rol')
        ruta_actual = request.endpoint # Ejemplo: 'cuaderno.residencia'

        # El Administrador tiene control absoluto, no se le bloquea nada
        if rol_usuario == 'Admin':
            return 

        # Reglas para Ingeniero Residente / Supervisor
        if rol_usuario in ['Ingeniero', 'Residente', 'Supervisor']:
            # Solo puede acceder a las vistas que empiecen con estos nombres:
            modulos_permitidos = ['cuaderno.', 'avance.', 'personal.', 'inicio.']
            if not any(ruta_actual.startswith(m) for m in modulos_permitidos):
                return generar_pantalla_bloqueo()

        # Reglas para el Encargado de Maquinaria
        if rol_usuario == 'Maquinaria':
            modulos_permitidos = ['mecanico.', 'inicio.']
            if not any(ruta_actual.startswith(m) for m in modulos_permitidos):
                return generar_pantalla_bloqueo()
                
        # Reglas para Almacenero
        if rol_usuario == 'Almacenero':
            modulos_permitidos = ['almacen.', 'inicio.']
            if not any(ruta_actual.startswith(m) for m in modulos_permitidos):
                return generar_pantalla_bloqueo()

    # =====================================================================
    # 3. INTERFACES DE ERROR ELEGANTES
    # =====================================================================
    def generar_pantalla_bloqueo():
        return render_template_string("""
        <div style="font-family: 'Inter', sans-serif; text-align: center; margin-top: 20vh; color: #1d1d1f;">
            <h1 style="font-size: 4rem; margin-bottom: 0;">403</h1>
            <h2>Acceso Restringido</h2>
            <p style="color: #86868b;">Tu rol actual no tiene privilegios para operar este módulo.</p>
            <a href="/" style="padding: 10px 20px; background: #0066cc; color: white; text-decoration: none; border-radius: 20px;">Volver al Panel</a>
        </div>
        """), 403

    @app.errorhandler(404)
    def pagina_no_encontrada(e):
        return render_template_string("""
        <div style="font-family: 'Inter', sans-serif; text-align: center; margin-top: 20vh; color: #1d1d1f;">
            <h1 style="font-size: 4rem; margin-bottom: 0;">404</h1>
            <h2>Módulo no encontrado</h2>
            <p style="color: #86868b;">El sistema SAMU no pudo encontrar la ruta solicitada.</p>
        </div>
        """), 404

    return app

# =====================================================================
# ARRANQUE DEL SERVIDOR
# =====================================================================
if __name__ == '__main__':
    app = crear_servidor_samu()
    # Ejecuta el servidor en todas las interfaces de red para Coolify
    app.run(debug=True, host='0.0.0.0', port=5000)
