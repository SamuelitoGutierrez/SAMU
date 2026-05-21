from flask import Flask
import vistas

# Inicializamos la plataforma
app = Flask(__name__)

# Conectamos nuestro archivo de vistas para mostrar la ventana
vistas.registrar_rutas(app)

# Dejaremos personal_obra.py vacío por ahora hasta confirmar que esto enciende.

if __name__ == '__main__':
    # Le decimos que arranque en el puerto 3000 para que Coolify lo detecte
    app.run(host='0.0.0.0', port=3000)
