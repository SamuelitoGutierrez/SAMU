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
                /* Fondo claro y luminoso */
                body {
                    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
                    margin: 0;
                    /* Fuente principal Bauhaus 93, con alternativas limpias por si acaso */
                    font-family: 'Bauhaus 93', 'Arial Rounded MT Bold', sans-serif;
                    overflow: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #1e293b;
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

                /* Logo con sombra suave clara */
                .logo-img {
                    width: 250px;
                    opacity: 0;
                    transform: translateY(0);
                    filter: drop-shadow(0px 15px 25px rgba(0,0,0,0.08));
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
                    color: #0f172a;
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.05em;
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

                /* Botones elegantes y sólidos */
                .btn-comenzar {
                    background-color: #0f172a;
                    color: #ffffff;
                    padding: 16px 40px;
                    border-radius: 16px;
                    border: none;
                    font-size: 1.2rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.2);
                    transition: all 0.3s ease;
                    width: 90%;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                }
                .btn-comenzar:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 30px rgba(15, 23, 42, 0.3);
                    background-color: #1e293b;
                }
                .btn-comenzar i {
                    margin-left: 10px;
                    font-size: 1.2rem;
                }

                .btn-panel {
                    background-color: transparent;
                    color: #64748b;
                    border: 2px solid #cbd5e1;
                    padding: 14px 40px;
                    border-radius: 16px;
                    font-size: 1rem;
                    letter-spacing: 1.5px;
                    width: 90%;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                }
                .btn-panel:hover {
                    background-color: #ffffff;
                    color: #0f172a;
                    border-color: #94a3b8;
                }

                /* --- NUEVO CUADRO DE LOGIN ELEGANTE --- */
                #login-box {
                    display: none; 
                    width: 90%;
                    background: #ffffff;
                    padding: 40px 35px;
                    border-radius: 24px; /* Bordes más redondeados */
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05); /* Sombra súper difuminada y suave */
                    text-align: left;
                    margin-bottom: 20px;
                    border: 1px solid rgba(0, 0, 0, 0.03);
                }

                .form-label {
                    font-size: 0.95rem;
                    color: #64748b;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    margin-bottom: 8px;
                    font-family: 'Arial Rounded MT Bold', sans-serif; /* Para que sea más legible */
                }

                /* Casillas de texto minimalistas */
                .form-control {
                    background-color: #f8fafc; /* Gris perlado muy claro */
                    border: 1px solid transparent;
                    border-radius: 12px;
                    padding: 15px;
                    font-family: 'Arial', sans-serif; /* Letra estándar para leer bien lo que se escribe */
                    font-size: 1rem;
                    color: #0f172a;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background-color: #ffffff;
                    border: 1px solid #3b82f6;
                    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); /* Resplandor azul al hacer clic */
                }
                .form-control::placeholder {
                    color: #cbd5e1;
                }

                .btn-ingresar {
                    background-color: #0ea5e9;
                    color: white;
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 1.2rem;
                    letter-spacing: 2px;
                    border: none;
                    text-transform: uppercase;
                    transition: background-color 0.3s ease;
                    margin-top: 15px;
                    box-shadow: 0 8px 15px rgba(14, 165, 233, 0.2);
                }
                .btn-ingresar:hover {
                    background-color: #0284c7;
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
                        <h4 class="mb-4 text-center" style="color: #0f172a; font-size: 1.8rem; letter-spacing: 2px;">INGRESO</h4>
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
