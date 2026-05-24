# main.py — El Cerebro de la Operación
from flask import Flask
from vistas_login import login_bp
from modulos.residencia import residencia_bp

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Aquí el CEO "registra" a sus departamentos (Blueprints)
app.register_blueprint(login_bp)
app.register_blueprint(residencia_bp)

if __name__ == '__main__':
    # Aquí es donde realmente se "enciende" la maquinaria
    app.run(debug=True, host='0.0.0.0', port=3000)
