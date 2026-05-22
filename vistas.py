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
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap" rel="stylesheet">
            
            <style>
                body {
                    background-color: #f5f5f7;
                    margin: 0;
                    font-family: 'Montserrat', sans-serif; /* Aplicando la nueva letra */
                    overflow-x: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                #splash-container {
                    text-align: center;
                    width: 100%;
                    max-width: 420px;
                    padding: 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }

                /* 1. Logo Transparente */
                .logo-img {
                    width: 130px;
                    opacity: 0; /* Oculto al inicio para el desvanecimiento */
                    filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.1)); /* Sombra suave sin círculo blanco */
                    transform: translateY(20px);
                    transition: opacity 1.2s ease, transform 1s cubic-bezier(0.25, 1, 0.5, 1);
                }
                
                /* Estado 2: Desvanecer (Aparece) */
                .logo-img.fade-in {
                    opacity: 1;
                    transform: translateY(0);
                }
                
                /* Estado 3: Subir */
                .logo-img.move-up {
                    transform: translateY(-20px) scale(0.9);
                }

                /* Texto SAMU */
                .brand-samu {
                    font-size: 3rem;
                    font-weight: 800;
                    color: #1d1d1f;
                    opacity: 0;
                    transform: translateY(20px);
                    transition: all 1s ease;
                    margin-top: -10px;
                    letter-spacing: 0.1em;
                }
                .brand-samu.show {
                    opacity: 1;
                    transform: translateY(-10px); /* Sube junto con el logo */
                }

                /* Contenedor de Botones */
                .botones-container {
                    display: none; /* Ocultos hasta que termine la animación */
                    width: 100%;
                    margin-top: 10px;
                }

                /* Botón Comenzar */
                .btn-comenzar {
                    background-color: #1d1d1f;
                    color: white;
                    padding: 14px 40px;
                    border-radius: 30px;
                    border: none;
                    font-weight: 600;
                    font-size: 0.95rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                    transition: all 0.3s ease;
                    width: 80%;
                    margin-bottom: 15px;
                }
                .btn-comenzar:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 25px rgba(0,0,0,0.15);
                    background-color: #333336;
                }
                .btn-comenzar i {
                    margin-left: 8px;
                    font-size: 1.1rem;
                    transition: margin-left 0.3s ease;
                }
                .btn-comenzar:hover i {
                    margin-left: 15px; /* La flecha se mueve al pasar el mouse */
                }

                /* Botón Panel Principal */
                .btn-panel {
                    background-color: transparent;
                    color: #86868b;
                    border: 1px solid #d2d2d7;
                    padding: 12px 40px;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 0.85rem;
                    letter-spacing: 1px;
                    width: 80%;
                    transition: all 0.3s ease;
                }
                .btn-panel:hover {
                    background-color: #e8e8ed;
                    color: #1d1d1f;
                }

                /* Tarjeta de Login */
                #login-box {
                    display: none;
                    background: #ffffff;
                    padding: 35px;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
                    width: 100%;
                    text-align: left;
                }
                .form-control {
                    background-color: #f5f5f7;
                    border: none;
                    border-radius: 12px;
                    padding: 14px;
                    font-family: 'Montserrat', sans-serif;
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
                <img id="logoImg" src="{{ url_for('static', filename='logo_s.png') }}" class="logo-img" alt="Logo">
                
                <div class="brand-samu" id="brandName">SAMU</div>
                
                <div class="botones-container" id="botonesContainer">
                    <button class="btn-comenzar" id="btnComenzar">
                        COMENZAR <i class="bi bi-arrow-right"></i>
                    </button>
                    <br>
                    <button class="btn-panel" id="btnPanel">
                        PANEL PRINCIPAL
                    </button>
                </div>

                <div id="login-box">
                    <h5 class="mb-4 text-center fw-bold" style="color: #1d1d1f;">Acceso Seguro</h5>
                    <div class="mb-3">
                        <label class="form-label small text-muted fw-bold">Usuario</label>
                        <input type="text" class="form-control" placeholder="Introducir usuario">
                    </div>
                    <div class="mb-4">
                        <label class="form-label small text-muted fw-bold">Contraseña</label>
                        <input type="password" class="form-control" placeholder="••••••••">
                    </div>
                    <button class="btn w-100" style="background-color: #0071e3; color: white; border-radius: 12px; padding: 14px; font-weight: 600; letter-spacing: 1px;">Ingresar</button>
                </div>
            </div>

            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                const logoImg = document.getElementById('logoImg');
                const brandName = document.getElementById('brandName');
                const botonesContainer = document.getElementById('botonesContainer');
                const btnComenzar = document.getElementById('btnComenzar');
                const btnPanel = document.getElementById('btnPanel');
                const loginBox = document.getElementById('login-box');

                // Secuencia de animación tipo presentación
                window.onload = function() {
                    // 1. Desvanecer el logo (Aparece suavemente)
                    setTimeout(() => {
                        logoImg.classList.add('fade-in');
                    }, 200);

                    // 2. El logo sube y SAMU aparece desde abajo
                    setTimeout(() => {
                        logoImg.classList.add('move-up');
                        brandName.classList.add('show');
                    }, 1400);

                    // 3. Aparecen los botones
                    setTimeout(() => {
                        $(botonesContainer).fadeIn(600);
                    }, 2000);
                };

                // Acción al presionar COMENZAR (Muestra el Login)
                btnComenzar.addEventListener('click', function() {
                    $(botonesContainer).fadeOut(200);
                    
                    setTimeout(() => {
                        $(loginBox).slideDown(500);
                    }, 250);
                });
            </script>
        </body>
        </html>
        """)
