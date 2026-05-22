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
            
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
            
            <style>
                body {
                    background: radial-gradient(circle at center, #ffffff 0%, #f4f6f9 60%, #e8edf2 100%);
                    margin: 0;
                    font-family: 'Playfair Display', serif; /* Letra clásica aplicada a todo */
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
                    max-width: 400px;
                    position: relative;
                }

                /* --- GRUPO DE MARCA (Logo + SAMU) --- */
                .brand-group {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    transform: translateY(10vh); /* Empieza un poco abajo */
                    transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
                    z-index: 2;
                }
                
                /* Movimiento del bloque completo hacia arriba */
                .brand-group.move-up-group {
                    transform: translateY(-5vh);
                }

                /* 1. Logo */
                .logo-img {
                    width: 200px;
                    opacity: 0;
                    transform: translateY(0);
                    filter: drop-shadow(0px 10px 20px rgba(0,0,0,0.08));
                    transition: opacity 1.2s ease, transform 1s ease;
                }
                .logo-img.fade-in {
                    opacity: 1;
                }
                .logo-img.move-up-logo {
                    transform: translateY(-15px); /* Pequeño salto inicial del logo */
                }

                /* 2. Texto SAMU */
                .brand-samu {
                    font-size: 4rem;
                    font-weight: 800;
                    color: #1a1e24;
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.15em;
                    transition: opacity 1.2s ease;
                }
                .brand-samu.fade-in {
                    opacity: 1;
                }

                /* --- ÁREA DE ACCIÓN (Botones y Login) --- */
                .action-area {
                    width: 100%;
                    opacity: 0; /* Oculto al inicio */
                    visibility: hidden;
                    transform: translateY(20px);
                    transition: all 1s ease;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-top: 20px;
                }
                .action-area.show {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0);
                }

                /* Botones Clásicos */
                .btn-comenzar {
                    background-color: #1a1e24;
                    color: #ffffff;
                    padding: 16px 40px;
                    border-radius: 4px; /* Bordes menos redondeados, más clásicos */
                    border: none;
                    font-weight: 600;
                    font-size: 1.1rem;
                    letter-spacing: 2px;
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
                    border: 1px solid #cdd4dc;
                    padding: 14px 40px;
                    border-radius: 4px;
                    font-weight: 600;
                    font-size: 0.95rem;
                    letter-spacing: 2px;
                    width: 90%;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                }
                .btn-panel:hover {
                    background-color: #ffffff;
                    color: #1a1e24;
                    border-color: #a0abb8;
                }

                /* Tarjeta de Login (Elegante y minimalista) */
                #login-box {
                    display: none; /* Oculto inicialmente, manejado por jQuery */
                    width: 90%;
                    background: #ffffff;
                    padding: 40px 30px;
                    border-radius: 4px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.06);
                    text-align: left;
                    margin-bottom: 20px;
                    border-top: 3px solid #1a1e24; /* Detalle elegante en la parte superior */
                }

                .form-label {
                    font-weight: 600;
                    font-size: 0.9rem;
                    color: #4a5360;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }

                .form-control {
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 2px;
                    padding: 12px 15px;
                    font-family: 'Playfair Display', serif;
                    font-style: italic; /* Toque clásico en el texto de entrada */
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
                    border-radius: 2px;
                    padding: 14px;
                    font-weight: 600;
                    letter-spacing: 2px;
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
                        <h4 class="mb-4 text-center fw-bold" style="color: #1a1e24; font-size: 1.5rem; letter-spacing: 1px;">Ingreso Seguro</h4>
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
                    // 1. Aparece el Logo
                    setTimeout(() => {
                        document.getElementById('logoImg').classList.add('fade-in');
                    }, 300);

                    // 2. El logo sube sutilmente para hacerle espacio a SAMU
                    setTimeout(() => {
                        document.getElementById('logoImg').classList.add('move-up-logo');
                    }, 1200);

                    // 3. Aparece la palabra SAMU
                    setTimeout(() => {
                        document.getElementById('brandName').classList.add('fade-in');
                    }, 1800);

                    // 4. Todo el bloque (Logo + SAMU) sube hacia la parte superior
                    setTimeout(() => {
                        document.getElementById('brandGroup').classList.add('move-up-group');
                    }, 2800);

                    // 5. Aparecen los botones en el espacio que quedó abajo
                    setTimeout(() => {
                        document.getElementById('actionArea').classList.add('show');
                    }, 3500);
                };

                // Lógica de interacción fluida
                $('#btnComenzar').click(function() {
                    // Oculta el botón COMENZAR deslizándolo hacia arriba
                    $(this).slideUp(300);
                    
                    // Muestra el Login deslizándolo hacia abajo, 
                    // empujando naturalmente a PANEL PRINCIPAL
                    setTimeout(() => {
                        $('#login-box').slideDown(500);
                    }, 300);
                });
            </script>
        </body>
        </html>
        """)
