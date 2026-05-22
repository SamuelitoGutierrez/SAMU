from flask import Flask, session, redirect, url_for, request
import vistas
# Aquí iremos importando los demás módulos conforme los vayamos armando:
# import cuaderno_obra
# import personal_obra
# import maquinaria

app = Flask(__name__)

# La "Llave Maestra" para encriptar las sesiones de los usuarios
app.secret_key = 'samu_pun110_seguro_2026'

# Damos los permisos registrando las rutas de todos los archivos .py
vistas.registrar_rutas(app)
# cuaderno_obra.registrar_rutas(app)
# personal_obra.registrar_rutas(app)
# maquinaria.registrar_rutas(app)

# --- EL CANDADO DE SEGURIDAD ---
@app.before_request
def verificar_seguridad():
    # Solo permitimos ver la página de inicio, el proceso de login y los videos/fotos (static)
    rutas_publicas = ['inicio', 'login', 'static']
    
    # Si intentan forzar la entrada a un módulo operativo sin sesión, se bloquea y los devuelve al inicio
    if request.endpoint and request.endpoint not in rutas_publicas and 'usuario_autenticado' not in session:
        # Por ahora está comentado para no generar bucles hasta que conectemos la base de datos de usuarios
        # return redirect(url_for('inicio'))
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
