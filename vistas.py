from flask import render_template_string, url_for

def registrar_rutas(app):
    @app.route('/')
    def inicio():
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAMU - Panel Principal</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #f5f5f7;
                    margin: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    overflow-x: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                #splash-container {
                    text-align: center;
                    width: 100%;
                    max-width: 400px;
                    padding: 20px;
                }

                /* Video / Logo */
                .video-logo {
                    width: 140px;
                    border-radius: 50%;
                    box-shadow: 0px 10px 20px rgba(0,0,0,0.12);
                    transition: transform 0.4s ease-in-out;
                    background-color: #ffffff;
                }
                
                .video-logo.move-up {
                    transform: translateY(-15px) scale(0.9);
                }

                /* Texto SAMU */
                .brand-samu {
                    font-size: 2.8rem;
                    font-weight: 700;
                    color: #1d1d1f;
                    opacity: 0;
                    transform: translateY(10px);
                    transition: all 0.4s ease-in-out;
                    margin-top: 5px;
                    letter-spacing: 0.05em;
                }
                .brand-samu.show {
                    opacity: 1;
                    transform: translateY(0);
                }

                /* Botón Comenzar */
                .btn-comenzar {
                    background-color: #1d1d1f;
                    color: white;
                    padding: 12px 50px;
                    border-radius: 30px;
                    border: none;
                    font-weight: 600;
                    letter-spacing: 1px;
                    margin: 20px auto 10px auto;
                    display: none; 
                    box-shadow: 0 8px 15px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                    text-transform: uppercase;
                }
                .btn-comenzar:hover {
                    transform: scale(1.03);
                }

                /* Texto Panel Principal abajo */
                .panel-principal-text {
                    font-size: 0.85rem;
                    color: #86868b;
                    letter-spacing: 3px;
                    text-transform: uppercase;
                    font-weight: 500;
                    opacity: 0;
                    transition: opacity 0.4s ease-in-out;
                    margin-top: 5px;
                }

                /* Tarjeta de Login Deslizable */
                #login-box {
                    display: none;
                    background: #ffffff;
                    padding: 30px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.06);
                    margin-top: 20px;
                    text-align: left;
                }
                .form-control {
                    background-color: #f5f5f7;
                    border: none;
                    border-radius: 12px;
                    padding: 12px;
                }
                .form-control:focus {
                    background-color: #ffffff;
                    border: 2px solid #0071e3;
                    box-shadow: none;
                }
            </style>
        </head>
        <body>

            <div id="splash-container">
                <video id="logoVideo" class="video-logo" autoplay muted playsinline>
                    <source src="{{ url_for('static', filename='logo_s.mp4') }}" type="video/mp4">
                </video>
                
                <div class="brand-samu" id="brandName">SAMU</div>
                
                <button class="btn-comenzar" id="btnComenzar">COMENZAR</button>
                
                <div class="panel-principal-text" id="panelLabel">PANEL PRINCIPAL</div>

                <div id="login-box">
                    <h5 class="mb-4 text-center fw-bold" style="color: #1d1d1f;">Ingreso al Sistema</h5>
                    <div class="mb-3">
                        <label class="form-label small text-muted">Usuario</label>
                        <input type="text" class="form-control" placeholder="Introducir usuario">
                    </div>
                    <div class="mb-4">
                        <label class="form-label small text-muted">Contraseña</label>
                        <input type="password" class="form-control" placeholder="••••••••">
                    </div>
                    <button class="btn w-100" style="background-color: #0071e3; color: white; border-radius: 12px; padding: 12px; font-weight: 500;">Ingresar</button>
                    <div class="text-center mt-3">
                        <a href="#" class="text-decoration-none small" style="color: #0071e3;">¿Olvidaste tu contraseña?</a>
                    </div>
                </div>
            </div>

            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                const video = document.getElementById('logoVideo');
                const brandName = document.getElementById('brandName');
                const panelLabel = document.getElementById('panelLabel');
                const btnComenzar = document.getElementById('btnComenzar');
                const loginBox = document.getElementById('login-box');

                // Acción de transición ultra rápida
                function iniciarPlataforma() {
                    video.classList.add('move-up');
                    brandName.classList.add('show');
                    
                    setTimeout(() => {
                        panelLabel.style.opacity = '1';
                        $(btnComenzar).fadeIn(300);
                    }, 200);
                }

                // Disparador inmediato al terminar el video
                video.onended = iniciarPlataforma;

                // Seguro de aceleración extrema: si el video no responde en 500ms, fuerza la carga
                setTimeout(() => {
                    if (!brandName.classList.contains('show')) {
                        iniciarPlataforma();
                    }
                }, 500);

                // Evento al presionar COMENZAR
                btnComenzar.addEventListener('click', function() {
                    $(this).fadeOut(150);
                    $(panelLabel).fadeOut(150);
                    
                    setTimeout(() => {
                        $(loginBox).slideDown(400); // Deslizamiento fluido hacia abajo
                    }, 200);
                });
            </script>
        </body>
        </html>
        """)
