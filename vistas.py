from flask import render_template_string, url_for

def registrar_rutas(app):
    @app.route('/')
    def inicio():
        # Usamos render_template_string para poder enlazar la carpeta static correctamente
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAMU - Acceso</title>
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

                /* Contenedor principal de la animación */
                #splash-container {
                    text-align: center;
                    width: 100%;
                    max-width: 400px;
                    padding: 20px;
                }

                /* Estilo del Video / Logo */
                .video-logo {
                    width: 160px;
                    border-radius: 50%;
                    box-shadow: 0px 15px 25px rgba(0,0,0,0.15); /* Sombra elegante abajo */
                    transition: transform 1s cubic-bezier(0.25, 1, 0.5, 1);
                    background-color: #ffffff; /* Fondo blanco por si el video es transparente */
                }
                
                /* Clase para cuando el logo sube */
                .video-logo.move-up {
                    transform: translateY(-30px) scale(0.85);
                }

                /* Texto SAMU */
                .brand-samu {
                    font-size: 2.8rem;
                    font-weight: 700;
                    color: #1d1d1f;
                    opacity: 0;
                    transform: translateY(20px);
                    transition: all 1s ease;
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
                    padding: 12px 40px;
                    border-radius: 30px;
                    border: none;
                    font-weight: 600;
                    letter-spacing: 1px;
                    margin-top: 20px;
                    display: none; /* Oculto al inicio */
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                }
                .btn-comenzar:hover {
                    transform: scale(1.05);
                }

                /* Panel de Login que se desliza */
                #login-box {
                    display: none;
                    background: #ffffff;
                    padding: 35px 30px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.08);
                    margin-top: 15px;
                    text-align: left;
                }
                .form-control {
                    background-color: #f5f5f7;
                    border: none;
                    border-radius: 12px;
                    padding: 14px;
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
                <div class="text-muted small mb-2" id="subtitle" style="opacity: 0; transition: 1s;">PANEL PRINCIPAL</div>
                
                <button class="btn-comenzar mx-auto" id="btnComenzar">COMENZAR</button>

                <div id="login-box">
                    <h5 class="mb-4 text-center fw-bold" style="color: #1d1d1f;">Ingreso al Sistema</h5>
                    <div class="mb-3">
                        <label class="form-label small text-muted">Usuario</label>
                        <input type="text" class="form-control" placeholder="Ej: Administrador">
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
                const subtitle = document.getElementById('subtitle');
                const btnComenzar = document.getElementById('btnComenzar');
                const loginBox = document.getElementById('login-box');

                // Motor de la animación principal
                function ejecutarAnimacion() {
                    video.classList.add('move-up');
                    brandName.classList.add('show');
                    subtitle.style.opacity = '1';
                    
                    // Mostramos el botón después de que el logo sube
                    setTimeout(() => {
                        $(btnComenzar).fadeIn(600);
                    }, 500);
                }

                // Disparador 1: Cuando el video termina de reproducirse
                video.onended = ejecutarAnimacion;

                // Disparador 2 (Seguro de vida): Si el video falla o no existe, 
                // arrancamos la animación a los 2.5 segundos de todas formas.
                setTimeout(() => {
                    if (!brandName.classList.contains('show')) {
                        ejecutarAnimacion();
                    }
                }, 2500);

                // Acción al presionar COMENZAR
                btnComenzar.addEventListener('click', function() {
                    $(this).fadeOut(200);
                    $(subtitle).slideUp(200);
                    
                    // Desliza el panel de ingreso hacia abajo
                    setTimeout(() => {
                        $(loginBox).slideDown(600);
                    }, 300);
                });
            </script>
        </body>
        </html>
        """)
