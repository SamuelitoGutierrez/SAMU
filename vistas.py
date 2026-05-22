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
            <title>SAMU - Acceso al Sistema</title>
            
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
            
            <style>
                /* Fondo Oscuro Elegante y tipografía Bauhaus 93 */
                body {
                    /* Degradado radial profundo (Azul oscuro a negro) */
                    background: radial-gradient(circle at top center, #1e293b 0%, #0f172a 50%, #020617 100%);
                    margin: 0;
                    font-family: 'Bauhaus 93', 'Arial Rounded MT Bold', sans-serif;
                    overflow: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #ffffff;
                }

                .main-wrapper {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%;
                    max-width: 420px;
                    position: relative;
                }

                /* --- GRUPO DE MARCA --- */
                .brand-group {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    transform: translateY(12vh);
                    transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
                    z-index: 2;
                }
                
                .brand-group.move-up-group {
                    transform: translateY(-4vh);
                }

                /* Logo Grande con resplandor */
                .logo-img {
                    width: 250px;
                    opacity: 0;
                    transform: translateY(0);
                    /* Sombra brillante para que resalte en el fondo oscuro */
                    filter: drop-shadow(0px 0px 20px rgba(56, 189, 248, 0.4));
                    transition: opacity 1.2s ease, transform 1s ease;
                }
                .logo-img.fade-in {
                    opacity: 1;
                }
                .logo-img.move-up-logo {
                    transform: translateY(-15px);
                }

                /* Texto SAMU en Bauhaus 93 */
                .brand-samu {
                    font-size: 4.8rem;
                    color: #ffffff;
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.08em;
                    text-shadow: 0px 10px 20px rgba(0,0,0,0.5); /* Sombra para dar volumen */
                    transition: opacity 1.2s ease;
                }
                .brand-samu.fade-in {
                    opacity: 1;
                }

                /* --- ÁREA DE ACCIÓN --- */
                .action-area {
                    width: 100%;
                    opacity: 0;
                    visibility: hidden;
                    transform: translateY(20px);
                    transition: all 1s ease;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-top: 15px;
                }
                .action-area.show {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0);
                }

                /* Botones con estilo moderno/oscuro */
                .btn-comenzar {
                    background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
                    color: #ffffff;
                    padding: 16px 40px;
                    border-radius: 12px;
                    border: none;
                    font-size: 1.2rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 25px rgba(14, 165, 233, 0.3);
                    transition: all 0.3s ease;
                    width: 90%;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                }
                .btn-comenzar:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 30px rgba(14, 165, 233, 0.5);
                }
                .btn-comenzar i {
                    margin-left: 10px;
                    font-size: 1.2rem;
                }

                .btn-panel {
                    background-color: rgba(255, 255, 255, 0.05);
                    color: #94a3b8;
                    border: 2px solid #334155;
                    padding: 14px 40px;
                    border-radius: 12px;
                    font-size: 1rem;
                    letter-spacing: 1.5px;
                    width: 90%;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                }
                .btn-panel:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: #ffffff;
                    border-color: #64748b;
                }

                /* Tarjeta de Login (Efecto Cristal / Glassmorphism) */
                #login-box {
                    display: none; 
                    width: 90%;
                    background: rgba(30, 41, 59, 0.7); /* Fondo semi transparente */
                    backdrop-filter: blur(12px); /* Desenfoca lo que hay detrás */
                    -webkit-backdrop-filter: blur(12px);
                    padding: 35px 30px;
                    border-radius: 15px;
                    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
                    text-align: left;
                    margin-bottom: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1); /* Borde brillante sutil */
                }

                .form-label {
                    font-size: 1rem;
                    color: #cbd5e1;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }

                /* Campos de texto oscuros */
                .form-control {
                    background-color: rgba(15, 23, 42, 0.6);
                    border: 1px solid #334155;
                    border-radius: 8px;
                    padding: 14px 15px;
                    font-family: 'Arial Rounded MT Bold', sans-serif; /* Más legible para escribir */
                    font-size: 1rem;
                    color: #ffffff;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background-color: rgba(15, 23, 42, 0.9);
                    border-color: #0ea5e9;
                    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2);
                    color: #ffffff;
                }
                .form-control::placeholder {
                    color: #64748b;
                }

                .btn-ingresar {
                    background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
                    color: white;
                    border-radius: 8px;
                    padding: 14px;
                    font-size: 1.1rem;
                    letter-spacing: 1px;
                    border: none;
                    text-transform: uppercase;
                    transition: opacity 0.3s ease;
                    margin-top: 10px;
                }
                .btn-ingresar:hover {
                    opacity: 0.9;
                }
            </style>
        </head>
        <body>

            <div class="main-wrapper">
                
                <div class="brand-group" id="brandGroup">
                    <img id="logoImg" src="{{ url_for('static', filename='logo_s.png') }}" class="logo-img" alt="Logo SAMU">
                    <div class="brand-samu" id="brandName">SAMU</div>
                </div>
                
                <div class="action-area" id="actionArea">
                    
                    <button class="btn-comenzar" id="btnComenzar">
                        COMENZAR <i class="bi bi-arrow-right"></i>
                    </button>

                    <div id="login-box">
                        <h4 class="mb-4 text-center" style="color: #ffffff; font-size: 1.8rem; letter-spacing: 2px;">INGRESO SEGURO</h4>
                        <div class="mb-3">
                            <label class="form-label">Usuario</label>
                            <input type="text" class="form-control" placeholder="Ej: Administrador">
                        </div>
                        <div class="mb-4">
                            <label class="form-label">Contraseña</label>
                            <input type="password" class="form-control" placeholder="••••••••">
                        </div>
                        <button class="btn w-100 btn-ingresar">Ingresar</button>
                    </div>

                    <button class="btn-panel" id="btnPanel">
                        PANEL PRINCIPAL
                    </button>
                    
                </div>
            </div>

            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                window.onload = function() {
                    setTimeout(() => {
                        document.getElementById('logoImg').classList.add('fade-in');
                    }, 300);

                    setTimeout(() => {
                        document.getElementById('logoImg').classList.add('move-up-logo');
                    }, 1200);

                    setTimeout(() => {
                        document.getElementById('brandName').classList.add('fade-in');
                    }, 1800);

                    setTimeout(() => {
                        document.getElementById('brandGroup').classList.add('move-up-group');
                    }, 2800);

                    setTimeout(() => {
                        document.getElementById('actionArea').classList.add('show');
                    }, 3500);
                };

                $('#btnComenzar').click(function() {
                    $(this).slideUp(300);
                    
                    setTimeout(() => {
                        $('#login-box').slideDown(500);
                    }, 300);
                });
            </script>
        </body>
        </html>
        """)
