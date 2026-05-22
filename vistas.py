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
                /* ANIMACIÓN DEL FONDO DINÁMICO */
                @keyframes gradienteDinamico {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                body {
                    /* Degradado mezclando los colores de tu imagen: Azul profundo, cyan neón, y toques violetas */
                    background: linear-gradient(-45deg, #050b14, #0a1128, #113154, #09091c, #004d7a);
                    background-size: 400% 400%;
                    animation: gradienteDinamico 15s ease infinite;
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

                /* Logo con resplandor neón */
                .logo-img {
                    width: 250px;
                    opacity: 0;
                    transform: translateY(0);
                    filter: drop-shadow(0px 0px 25px rgba(0, 195, 255, 0.4));
                    transition: opacity 1.2s ease, transform 1s ease;
                }
                .logo-img.fade-in {
                    opacity: 1;
                }
                .logo-img.move-up-logo {
                    transform: translateY(-15px);
                }

                /* Texto SAMU */
                .brand-samu {
                    font-size: 5rem;
                    color: #ffffff;
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.08em;
                    text-shadow: 0px 10px 30px rgba(0, 195, 255, 0.6);
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

                /* Botón COMENZAR vibrante */
                .btn-comenzar {
                    background: linear-gradient(90deg, #0073ff 0%, #00c3ff 100%);
                    color: #ffffff;
                    padding: 16px 40px;
                    border-radius: 16px;
                    border: none;
                    font-size: 1.2rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 30px rgba(0, 195, 255, 0.4);
                    transition: all 0.3s ease;
                    width: 90%;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                }
                .btn-comenzar:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 40px rgba(0, 195, 255, 0.6);
                }
                .btn-comenzar i {
                    margin-left: 10px;
                    font-size: 1.2rem;
                }

                .btn-panel {
                    background-color: transparent;
                    color: #b0c4de;
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    padding: 14px 40px;
                    border-radius: 16px;
                    font-size: 1rem;
                    letter-spacing: 1.5px;
                    width: 90%;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                }
                .btn-panel:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: #ffffff;
                    border-color: #ffffff;
                }

                /* --- LOGIN CON EFECTO CRISTAL (Glassmorphism) --- */
                #login-box {
                    display: none; 
                    width: 90%;
                    background: rgba(255, 255, 255, 0.05); /* Blanco súper transparente */
                    backdrop-filter: blur(16px); /* Desenfoque del fondo */
                    -webkit-backdrop-filter: blur(16px);
                    padding: 40px 35px;
                    border-radius: 24px;
                    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
                    text-align: left;
                    margin-bottom: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.15); /* Borde luminoso */
                }

                .form-label {
                    font-size: 0.95rem;
                    color: #e2e8f0;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    margin-bottom: 8px;
                    font-family: 'Arial Rounded MT Bold', sans-serif;
                }

                /* Casillas de texto adaptadas al diseño oscuro */
                .form-control {
                    background-color: rgba(0, 0, 0, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    padding: 15px;
                    font-family: 'Arial', sans-serif;
                    font-size: 1rem;
                    color: #ffffff;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background-color: rgba(0, 0, 0, 0.4);
                    border: 1px solid #00c3ff;
                    box-shadow: 0 0 0 4px rgba(0, 195, 255, 0.2);
                    color: #ffffff;
                }
                .form-control::placeholder {
                    color: #94a3b8;
                }

                .btn-ingresar {
                    background: linear-gradient(90deg, #0073ff 0%, #00c3ff 100%);
                    color: white;
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 1.2rem;
                    letter-spacing: 2px;
                    border: none;
                    text-transform: uppercase;
                    transition: background-color 0.3s ease;
                    margin-top: 15px;
                    box-shadow: 0 8px 20px rgba(0, 195, 255, 0.3);
                }
                .btn-ingresar:hover {
                    filter: brightness(1.2);
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
                        <h4 class="mb-4 text-center" style="color: #ffffff; font-size: 1.8rem; letter-spacing: 2px;">INGRESO</h4>
                        <div class="mb-3">
                            <label class="form-label">Usuario</label>
                            <input type="text" class="form-control" placeholder="Escribe tu usuario">
                        </div>
                        <div class="mb-4">
                            <label class="form-label">Contraseña</label>
                            <input type="password" class="form-control" placeholder="••••••••">
                        </div>
                        <button class="btn w-100 btn-ingresar">Entrar</button>
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
