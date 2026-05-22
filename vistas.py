def registrar_rutas(app):
    @app.route('/')
    def inicio():
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAMU - Panel Principal</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #f8f9fa;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                    overflow: hidden;
                    font-family: 'Segoe UI', sans-serif;
                }

                .main-container {
                    text-align: center;
                    width: 100%;
                    max-width: 450px;
                    z-index: 10;
                }

                /* Video con Sombra */
                .video-logo {
                    width: 180px;
                    border-radius: 50%;
                    filter: drop-shadow(0px 15px 10px rgba(0,0,0,0.3)); /* Sombra abajo */
                    transition: all 1s ease-in-out;
                }

                .video-logo.move-up {
                    transform: translateY(-20px) scale(0.8);
                }

                /* Textos iniciales */
                .brand-samu {
                    font-size: 3rem;
                    font-weight: bold;
                    color: #1a2a6c;
                    opacity: 0;
                    transition: 1s;
                    margin-top: 10px;
                }

                .btn-comenzar {
                    display: none; /* Se activa por JS */
                    margin: 20px auto;
                    padding: 12px 40px;
                    border-radius: 30px;
                    font-weight: bold;
                }

                .panel-text {
                    font-size: 0.9rem;
                    color: #6c757d;
                    letter-spacing: 3px;
                    text-transform: uppercase;
                    opacity: 0;
                    transition: 1.5s;
                }

                /* Contenedor del Login (Oculto al inicio) */
                #loginSection {
                    display: none;
                    margin-top: 20px;
                }

                /* Animaciones de entrada */
                .show { opacity: 1 !important; }
            </style>
        </head>
        <body>

            <div class="main-container">
                <video id="logoVideo" class="video-logo" autoplay muted playsinline>
                    <source src="/static/logo_s.mp4" type="video/mp4">
                    Tu navegador no soporta videos.
                </video>

                <div class="brand-samu" id="brandName">SAMU</div>
                
                <button class="btn btn-primary btn-comenzar shadow" id="btnComenzar">COMENZAR</button>
                
                <div class="panel-text" id="panelLabel">PANEL PRINCIPAL</div>

                <div id="loginSection" class="card shadow-lg border-0 rounded-4 overflow-hidden">
                    <div class="card-body p-4">
                        <h5 class="text-center mb-4 text-primary">Ingreso al Sistema</h5>
                        <div class="mb-3 text-start">
                            <label class="form-label small">Usuario</label>
                            <input type="text" class="form-control" placeholder="Ej: Ingeniero_Puno">
                        </div>
                        <div class="mb-3 text-start">
                            <label class="form-label small">Contraseña</label>
                            <input type="password" class="form-control" placeholder="••••••••">
                        </div>
                        <button class="btn btn-dark w-100 rounded-3 mb-3">INGRESAR</button>
                        <div class="text-center">
                            <a href="#" class="text-decoration-none small text-muted">¿Olvidaste tu contraseña?</a>
                        </div>
                    </div>
                </div>
            </div>

            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                const video = document.getElementById('logoVideo');
                
                // Cuando el video termina
                video.onended = function() {
                    video.classList.add('move-up');
                    document.getElementById('brandName').classList.add('show');
                    document.getElementById('panelLabel').classList.add('show');
                    
                    // Mostrar botón COMENZAR suavemente
                    setTimeout(() => {
                        $("#btnComenzar").fadeIn();
                    }, 500);
                };

                // Acción del botón COMENZAR
                $("#btnComenzar").click(function() {
                    $(this).fadeOut(300);
                    $("#panelLabel").fadeOut(300);
                    
                    setTimeout(() => {
                        $("#loginSection").slideDown(800); // Efecto de deslizamiento hacia abajo
                    }, 400);
                });
            </script>
        </body>
        </html>
        """
