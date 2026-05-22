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
                /* Aplicamos la fuente Arial Rounded MT Bold a todo el sistema */
                body {
                    background: radial-gradient(circle at center, #ffffff 0%, #f4f6f9 60%, #e8edf2 100%);
                    margin: 0;
                    font-family: 'Arial Rounded MT Bold', 'Helvetica Rounded', Arial, sans-serif; 
                    overflow: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .main-wrapper {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%;
                    max-width: 420px; /* Un poco más de margen para el logo grande */
                    position: relative;
                }

                /* --- GRUPO DE MARCA (Logo + SAMU) --- */
                .brand-group {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    transform: translateY(12vh); /* Inicia acomodado para el nuevo tamaño */
                    transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
                    z-index: 2;
                }
                
                .brand-group.move-up-group {
                    transform: translateY(-4vh);
                }

                /* 1. Logo (Ahora mucho más grande) */
                .logo-img {
                    width: 250px; /* Aumentado de 200px a 250px */
                    opacity: 0;
                    transform: translateY(0);
                    filter: drop-shadow(0px 12px 25px rgba(0,0,0,0.1));
                    transition: opacity 1.2s ease, transform 1s ease;
                }
                .logo-img.fade-in {
                    opacity: 1;
                }
                .logo-img.move-up-logo {
                    transform: translateY(-15px);
                }

                /* 2. Texto SAMU */
                .brand-samu {
                    font-size: 4.2rem;
                    color: #1a1e24;
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.05em; /* Ligeramente más junto para combinar con Arial Rounded */
                    transition: opacity 1.2s ease;
                }
                .brand-samu.fade-in {
                    opacity: 1;
                }

                /* --- ÁREA DE ACCIÓN (Botones y Login) --- */
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

                /* Botones */
                .btn-comenzar {
                    background-color: #1a1e24;
                    color: #ffffff;
                    padding: 16px 40px;
                    border-radius: 12px; /* Bordes redondeados haciendo juego con la letra */
                    border: none;
                    font-size: 1.1rem;
                    letter-spacing: 1px;
                    box-shadow: 0 10px 25px rgba(26, 30, 36, 0.15);
                    transition: all 0.3s ease;
                    width: 90%;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                }
                .btn-comenzar:hover {
                    background-color: #2c333d;
                    box-shadow: 0 12px 30px rgba(26, 30, 36, 0.25);
                }
                .btn-comenzar i {
                    margin-left: 10px;
                    font-size: 1.1rem;
                }

                .btn-panel {
                    background-color: transparent;
                    color: #5a6473;
                    border: 2px solid #cdd4dc;
                    padding: 14px 40px;
                    border-radius: 12px;
                    font-size: 0.95rem;
                    letter-spacing: 1px;
                    width: 90%;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                }
                .btn-panel:hover {
                    background-color: #ffffff;
                    color: #1a1e24;
                    border-color: #a0abb8;
                }

                /* Tarjeta de Login */
                #login-box {
                    display: none; 
                    width: 90%;
                    background: #ffffff;
                    padding: 35px 30px;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
                    text-align: left;
                    margin-bottom: 20px;
                    border-top: 4px solid #1a1e24; 
                }

                .form-label {
                    font-size: 0.95rem;
                    color: #4a5360;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                }

                .form-control {
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 12px 15px;
                    font-family: 'Arial Rounded MT Bold', 'Helvetica Rounded', Arial, sans-serif;
                    font-size: 1rem;
                    color: #1a1e24;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background-color: #ffffff;
                    border-color: #1a1e24;
                    box-shadow: none;
                }

                .btn-ingresar {
                    background-color: #1a1e24;
                    color: white;
                    border-radius: 8px;
                    padding: 14px;
                    font-size: 1.05rem;
                    letter-spacing: 1px;
                    border: none;
                    text-transform: uppercase;
                    transition: background-color 0.3s ease;
                }
                .btn-ingresar:hover {
                    background-color: #313944;
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
                        <h4 class="mb-4 text-center" style="color: #1a1e24; font-size: 1.5rem; letter-spacing: 1px;">INGRESO SEGURO</h4>
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
