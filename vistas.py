def registrar_rutas(app):
    @app.route('/')
    def inicio():
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAMU - Sistema de Gestión</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #f5f5f7; /* Gris muy sutil y elegante */
                    margin: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    overflow-x: hidden;
                }

                /* --- 1. PANTALLA DE CARGA (SPLASH) --- */
                #splash-screen {
                    position: fixed;
                    top: 0; left: 0; width: 100%; height: 100vh;
                    background-color: #f5f5f7;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    z-index: 9999;
                    transition: opacity 1s ease-in-out;
                }
                .video-logo {
                    width: 150px;
                    border-radius: 50%;
                    box-shadow: 0px 20px 30px rgba(0,0,0,0.12);
                    transition: transform 1s cubic-bezier(0.25, 1, 0.5, 1);
                }
                .video-logo.move-up {
                    transform: translateY(-40px) scale(0.85);
                }
                .brand-samu {
                    font-size: 2.5rem;
                    font-weight: 600;
                    color: #1d1d1f;
                    opacity: 0;
                    transform: translateY(20px);
                    transition: all 1s ease;
                    margin-top: 10px;
                    letter-spacing: 0.05em;
                }
                .brand-samu.show {
                    opacity: 1;
                    transform: translateY(0);
                }

                /* --- 2. PORTAL PRINCIPAL (VITRINA) --- */
                #main-portal {
                    display: none;
                    padding: 60px 20px;
                    max-width: 1000px;
                    margin: 0 auto;
                    opacity: 0;
                    transition: opacity 1.5s ease-in;
                }
                .portal-header {
                    text-align: center;
                    margin-bottom: 50px;
                }
                .portal-title {
                    font-size: 3.5rem;
                    font-weight: 700;
                    color: #1d1d1f;
                    letter-spacing: -0.02em;
                }
                .portal-subtitle {
                    font-size: 1.2rem;
                    color: #86868b;
                    margin-top: 5px;
                }
                
                /* Tarjetas de Módulos Bloqueados */
                .modulo-card {
                    background: #ffffff;
                    border-radius: 20px;
                    padding: 40px 30px;
                    text-align: center;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
                    height: 100%;
                    cursor: not-allowed;
                    position: relative;
                    overflow: hidden;
                }
                .modulo-card::after {
                    content: '🔒 Acceso Restringido';
                    position: absolute;
                    bottom: -50px;
                    left: 0;
                    width: 100%;
                    background: rgba(29, 29, 31, 0.95);
                    color: white;
                    padding: 12px 0;
                    font-size: 0.9rem;
                    font-weight: 500;
                    transition: bottom 0.3s ease;
                }
                .modulo-card:hover::after {
                    bottom: 0; /* Sube el candado al pasar el mouse */
                }
                .modulo-icon {
                    font-size: 3.5rem;
                    margin-bottom: 15px;
                }
                .modulo-title {
                    font-weight: 600;
                    font-size: 1.2rem;
                    color: #1d1d1f;
                }

                /* --- 3. FORMULARIO DE INGRESO --- */
                #login-section {
                    display: none;
                    max-width: 380px;
                    margin: 20px auto 0;
                    background: #ffffff;
                    padding: 40px;
                    border-radius: 24px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
                }
                .form-control {
                    background-color: #f5f5f7;
                    border: none;
                    border-radius: 12px;
                    padding: 15px;
                    margin-bottom: 15px;
                }
                .form-control:focus {
                    background-color: #ffffff;
                    border: 2px solid #0071e3;
                    box-shadow: none;
                }
                .btn-ingresar {
                    background-color: #0071e3;
                    color: white;
                    border-radius: 20px;
                    padding: 12px;
                    font-weight: 500;
                    width: 100%;
                    border: none;
                    margin-top: 10px;
                    transition: background-color 0.2s;
                }
                .btn-ingresar:hover {
                    background-color: #0077ED;
                }
                .btn-comenzar-flotante {
                    position: fixed;
                    bottom: 40px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: #1d1d1f;
                    color: white;
                    padding: 15px 40px;
                    border-radius: 30px;
                    font-weight: 600;
                    letter-spacing: 1px;
                    border: none;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                    z-index: 1000;
                    display: none;
                    transition: transform 0.2s;
                }
                .btn-comenzar-flotante:hover {
                    transform: translateX(-50%) scale(1.05);
                }
            </style>
        </head>
        <body>

            <div id="splash-screen">
                <video id="logoVideo" class="video-logo" autoplay muted playsinline>
                    <source src="/static/logo_s.mp4" type="video/mp4">
                </video>
                <div class="brand-samu" id="brandName">SAMU</div>
            </div>

            <button class="btn-comenzar-flotante" id="btnComenzar">INICIAR SESIÓN</button>

            <div id="main-portal">
                <div class="portal-header">
                    <h1 class="portal-title">Sistema de Gestión</h1>
                    <p class="portal-subtitle">Proyecto Carretera PU N-110</p>
                </div>

                <div id="login-section">
                    <h4 class="text-center mb-4 fw-bold" style="color: #1d1d1f;">Acceso Seguro</h4>
                    <form>
                        <input type="text" class="form-control" placeholder="Usuario Institucional" required>
                        <input type="password" class="form-control" placeholder="Contraseña" required>
                        <button type="button" class="btn-ingresar">Continuar</button>
                        <div class="text-center mt-4">
                            <a href="#" class="text-decoration-none" style="color: #0071e3; font-size: 0.85rem;">¿Olvidaste tu contraseña?</a>
                        </div>
                    </form>
                </div>

                <div class="row g-4 mt-2" id="modulos-grid">
                    <div class="col-md-4">
                        <div class="modulo-card">
                            <div class="modulo-icon">📘</div>
                            <div class="modulo-title">Cuaderno de Obra</div>
                            <p class="text-muted small mt-2">Registros y reportes diarios</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="modulo-card">
                            <div class="modulo-icon">👷</div>
                            <div class="modulo-title">Personal de Obra</div>
                            <p class="text-muted small mt-2">Asistencias y jornales</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="modulo-card">
                            <div class="modulo-icon">🚜</div>
                            <div class="modulo-title">Maquinaria</div>
                            <p class="text-muted small mt-2">Control de horas y combustible</p>
                        </div>
                    </div>
                </div>
            </div>

            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                const video = document.getElementById('logoVideo');
                const splashScreen = document.getElementById('splash-screen');
                const mainPortal = document.getElementById('main-portal');
                const btnComenzar = document.getElementById('btnComenzar');
                const modulosGrid = document.getElementById('modulos-grid');
                const loginSection = document.getElementById('login-section');

                // 1. Cuando el video termina
                video.onended = function() {
                    video.classList.add('move-up');
                    document.getElementById('brandName').classList.add('show');
                    
                    // 2. Desvanecer splash y mostrar portal
                    setTimeout(() => {
                        splashScreen.style.opacity = '0';
                        
                        setTimeout(() => {
                            splashScreen.style.display = 'none';
                            mainPortal.style.display = 'block';
                            
                            // Fade-in del portal y botón
                            setTimeout(() => {
                                mainPortal.style.opacity = '1';
                                $(btnComenzar).fadeIn(800);
                            }, 50);
                        }, 1000);
                    }, 1500);
                };

                // 3. Acción del botón INICIAR SESIÓN
                btnComenzar.addEventListener('click', function() {
                    $(this).fadeOut(300);
                    $(modulosGrid).slideUp(600);
                    
                    // Deslizar login hacia abajo
                    setTimeout(() => {
                        $(loginSection).slideDown(600);
                    }, 400);
                });
            </script>
        </body>
        </html>
        """
