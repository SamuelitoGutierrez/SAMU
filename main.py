from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('blank.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f'Servidor activo → http://localhost:{port}/')
    app.run(host='0.0.0.0', port=port, debug=True)