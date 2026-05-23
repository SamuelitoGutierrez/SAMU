from flask import Blueprint, render_template_string, request, redirect, url_for, session

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def mostrar_login():
    error = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        # --- CUENTA MAESTRA DEL DUEÑO (SAMU) ---
        if usuario == 'SAMU' and password == '716285':
            session['usuario_id'] = 1
            session['nombre'] = 'SAMU - Dirección'
            session['rol'] = 'Admin' # Rol de dueño
            return redirect(url_for('inicio.panel_principal'))
        else:
            error = "Credenciales incorrectas."

    # Usamos el mismo diseño fluido que ya perfeccionamos
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU - Ingreso</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <style>
            :root { --x: 50vw; --y: 50vh; }
            body { margin: 0; font-family: 'Bauhaus 93', 'Arial Rounded MT Bold', sans-serif; overflow: hidden; height: 100vh; display: flex; justify-content: center; align-items: center; background-color: #ffffff; }
            .color-layer { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: #ffffff; -webkit-mask-image: radial-gradient(circle 40vmax at var(--x) var(--y), transparent 0%, rgba(0,0,0,1) 90%); }
            .blob { position: absolute; border-radius: 50%; filter: blur(90px); }
            .blob-blue { width: 60vw; height: 60vw; background: #0ea5e9; opacity: 0.25; top: -10%; left: -10%; animation: mov 18s infinite ease-in-out; }
            .blob-pink { width: 60vw; height: 60vw; background: #f9a8d4; opacity: 0.20; bottom: -10%; right: -10%; animation: mov 22s infinite ease-in-out reverse; }
            @keyframes mov { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(10vw, 5vh) scale(1.1); } }
            .main-wrapper { width: 100%; max-width: 400px; text-align: center; z-index: 10; }
            #login-box { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px); padding: 35px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.05); }
            .form-control { border-radius: 12px; padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; }
            .btn-ingresar { background: #000; color: #fff; width: 100%; padding: 14px; border-radius: 12px; border: none; font-weight: bold; margin-top: 10px; }
            .nav-btn { background: none; border: 2px solid #000; color: #000; width: 100%; padding: 12px; border-radius: 12px; margin-top: 15px; font-weight: bold; text-decoration: none; display: block; }
        </style>
    </head>
    <body>
        <div class="color-layer"><div class="blob blob-blue"></div><div class="blob blob-pink"></div></div>
        <div class="main-wrapper">
            <img src="/static/logo_s.png" style="width: 180px; margin-bottom: 20px;">
            <div id="login-box">
                <form method="POST">
                    <h4 class="mb-4">INGRESO</h4>
                    {% if error %}<div class="alert alert-danger py-2" style="font-size: 0.8rem;">{{ error }}</div>{% endif %}
                    <input type="text" name="usuario" class="form-control mb-3" placeholder="Usuario" required>
                    <input type="password" name="password" class="form-control mb-4" placeholder="Contraseña" required>
                    <button type="submit" class="btn-ingresar">INGRESAR</button>
                </form>
                <a href="/panel" class="nav-btn">PANEL PRINCIPAL</a>
            </div>
        </div>
        <script>
            window.addEventListener('mousemove', (e) => {
                document.documentElement.style.setProperty('--x', e.clientX + 'px');
                document.documentElement.style.setProperty('--y', e.clientY + 'px');
            });
        </script>
    </body>
    </html>
    """, error=error)
