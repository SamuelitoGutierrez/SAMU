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
                    font-family: 'Montserrat', sans-serif;
                    overflow: hidden; /* Evita cualquier salto o barra de desplazamiento */
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                /* Contenedor central animado */
                .main-wrapper {
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    transform: translateY(40px); /* Empieza un poco más abajo */
                    transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
                    width: 100%;
                    max-width: 400px;
                }
                
                /* Clase que hace que todo el bloque suba suavemente */
                .main-wrapper.move-up {
                    transform: translateY(-50px);
                }

                /* 1. Logo mucho más grande */
                .logo-img {
                    width: 220px; /* Aumentado de 130px a 220px */
                    opacity: 0;
                    filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.1));
                    transition: opacity 1.5s ease;
                }
                .logo-img.fade-in {
                    opacity: 1;
                }

                /* 2. Texto SAMU mucho más grande */
                .brand-samu {
                    font-size: 4rem; /* Aumentado de 3rem a 4rem */
                    font-weight: 800;
                    color: #1d1d1f;
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.1em;
                    transition: opacity 1.5s ease;
                }
                .brand-samu.fade-in {
                    opacity: 1;
                }

                /* 3. Área de acciones estática (No empuja nada) */
                .action-area {
                    position: absolute;
                    top: 100%; /* Siempre se ubica exactamente debajo de SAMU */
                    width: 100%;
                    margin-top: 30px;
                }

                /* Contenedor de Botones */
                .botones-container {
                    opacity: 0;
                    visibility: hidden;
                    transition: opacity 0.8s ease;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    position: absolute;
                    width: 100%;
                    top: 0;
                }
                .botones-container.show {
                    opacity: 1;
                    visibility: visible;
                }

                /* Diseño de Botones */
                .btn-comenzar {
                    background-color: #1d1d1f;
                    color: white;
                    padding: 15px 40px;
                    border-radius: 30px;
                    border: none;
                    font-weight: 600;
                    font-size: 1rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                    transition: all 0.3s ease;
                    width: 85%;
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
                    margin-left: 15px;
                }

                .btn-panel {
                    background-color: transparent;
                    color: #86868b;
                    border: 1px solid #d2d2d7;
                    padding: 12px 40px;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 0.85rem;
                    letter-spacing: 1px;
                    width: 85%;
                    transition: all 0.3s ease;
                }
                .btn-panel:hover {
                    background-color: #e8e8ed;
                    color: #1d1d1f;
                }

                /* 4. Tarjeta de Login (Oculta al inicio) */
                #login-box {
                    opacity: 0;
                    visibility: hidden;
                    transform: translateY(-20px); /* Preparado para deslizarse hacia abajo */
                    transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1);
                    position: absolute;
                    width: 100%;
                    top: 0;
                    background: #ffffff;
                    padding: 35px 30px;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
                    text-align: left;
                }
                #login-box.show {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0); /* Se desliza a su posición original */
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

            <div class="main-wrapper" id="mainWrapper">
                
                <img id="logoImg" src="{{ url_for('static', filename='logo_s.png') }}" class="logo-img" alt="Logo">
                
                <div class="brand-samu" id="brandName">SAMU</div>
                
                <div class="action-area">
                    
                    <div class="botones-container" id="botonesContainer">
                        <button class="btn-comenzar" id="btnComenzar">
                            COMENZAR <i class="bi bi-arrow-right"></i>
                        </button>
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
            </div>

            <script>
                // Variables de los elementos
                const logoImg = document.getElementById('logoImg');
                const brandName = document.getElementById('brandName');
                const mainWrapper = document.getElementById('mainWrapper');
                const botonesContainer = document.getElementById('botonesContainer');
                const btnComenzar = document.getElementById('btnComenzar');
                const loginBox = document.getElementById('login-box');

                // Secuencia exacta y fluida
                window.onload = function() {
                    // 1. Aparece el Logo
                    setTimeout(() => {
                        logoImg.classList.add('fade-in');
                    }, 200);

                    // 2. Aparece SAMU (sin saltos, solo se desvanece)
                    setTimeout(() => {
                        brandName.classList.add('fade-in');
                    }, 1000);

                    // 3. Todo sube suavemente y aparecen los botones
                    setTimeout(() => {
                        mainWrapper.classList.add('move-up');
                        botonesContainer.classList.add('show');
                    }, 2000);
                };

                // Acción al presionar COMENZAR
                btnComenzar.addEventListener('click', function() {
                    // Desaparecen los botones
                    botonesContainer.classList.remove('show');
                    
                    // Se desliza el login hacia abajo en el mismo lugar
                    setTimeout(() => {
                        loginBox.classList.add('show');
                    }, 400); // Espera a que los botones desaparezcan para evitar cruces
                });
            </script>
        </body>
        </html>
        """)
