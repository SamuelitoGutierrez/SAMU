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
                body {
                    margin: 0;
                    font-family: 'Bauhaus 93', 'Arial Rounded MT Bold', sans-serif;
                    overflow: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #0f172a;
                    background-color: #ffffff; /* Base blanca */
                }

                /* --- FONDO DINÁMICO ESTILO AURORA / LUZ --- */
                .bg-mesh {
                    position: fixed;
                    top: 0; left: 0; width: 100vw; height: 100vh;
                    z-index: -1;
                    overflow: hidden;
                }
                .blob {
                    position: absolute;
                    border-radius: 50%;
                    filter: blur(100px); /* Difumina las esferas para crear ondas de luz */
                    opacity: 0.6;
                    animation: flotar 20s infinite ease-in-out alternate;
                }
                .blob-1 {
                    width: 55vw; height: 55vw;
                    background: #00c3ff; /* Cyan brillante */
                    top: -15%; left: -10%;
                    animation-duration: 18s;
                }
                .blob-2 {
                    width: 65vw; height: 65vw;
                    background: #e0f2fe; /* Azul muy muy claro */
                    bottom: -20%; right: -10%;
                    animation-duration: 22s;
                    animation-direction: alternate-reverse;
                }
                .blob-3 {
                    width: 45vw; height: 45vw;
                    background: #7dd3fc; /* Azul cielo suave */
                    top: 40%; left: 50%;
                    animation-duration: 25s;
                }

                @keyframes flotar {
                    0% { transform: translate(0, 0) scale(1); }
                    50% { transform: translate(8%, 12%) scale(1.1); }
                    100% { transform: translate(-8%, 5%) scale(0.95); }
                }

                /* --- ESTRUCTURA PRINCIPAL --- */
                .main-wrapper {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%;
                    max-width: 420px;
                    position: relative;
                    z-index: 10;
                }

                /* --- GRUPO DE MARCA --- */
                .brand-group {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    transform: translateY(12vh);
                    transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
                }
                
                .brand-group.move-up-group {
                    transform: translateY(-2vh);
                }

                /* Logo */
                .logo-img {
                    width: 250px; /* Tamaño PC */
                    opacity: 0;
                    transform: translateY(0);
                    filter: drop-shadow(0px 15px 25px rgba(0, 195, 255, 0.2));
                    transition: opacity 1.2s ease, transform 1s ease;
                }
                .logo-img.fade-in { opacity: 1; }
                .logo-img.move-up-logo { transform: translateY(-15px); }

                /* Texto SAMU */
                .brand-samu {
                    font-size: 5rem; /* Tamaño PC */
                    color: #0f172a; /* Azul marino casi negro */
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.08em;
                    text-shadow: 0px 10px 30px rgba(0, 195, 255, 0.3);
                    transition: opacity 1.2s ease;
                }
                .brand-samu.fade-in { opacity: 1; }

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

                /* Botón COMENZAR */
                .btn-comenzar {
                    background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
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
                }
                .btn-comenzar i { margin-left: 10px; font-size: 1.2rem; }

                /* Botón PANEL PRINCIPAL */
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

                /* --- LOGIN CON EFECTO CRISTAL (Glassmorphism Claro) --- */
                #login-box {
                    display: none; 
                    width: 90%;
                    background: rgba(255, 255, 255, 0.7); /* Blanco semi-transparente */
                    backdrop-filter: blur(20px); /* Desenfoque intenso */
                    -webkit-backdrop-filter: blur(20px);
                    padding: 35px 30px;
                    border-radius: 24px;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08); /* Sombra elegante */
                    text-align: left;
                    margin-bottom: 20px;
                    border: 1px solid rgba(255, 255, 255, 1);
                }

                .form-label {
                    font-size: 0.95rem;
                    color: #475569;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    margin-bottom: 8px;
                    font-family: 'Arial Rounded MT Bold', sans-serif;
                }

                /* Casillas de texto claras */
                .form-control {
                    background-color: rgba(241, 245, 249, 0.8);
                    border: 1px solid rgba(226, 232, 240, 0.8);
                    border-radius: 12px;
                    padding: 14px 15px;
                    font-family: 'Arial', sans-serif;
                    font-size: 1rem;
                    color: #0f172a;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background-color: #ffffff;
                    border: 1px solid #00c3ff;
                    box-shadow: 0 0 0 4px rgba(0, 195, 255, 0.15);
                    color: #0f172a;
                }
                .form-control::placeholder { color: #94a3b8; }

                .btn-ingresar {
                    background: linear-gradient(90deg, #0073ff 0%, #00c3ff 100%);
                    color: white;
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 1.1rem;
                    letter-spacing: 2px;
                    border: none;
                    text-transform: uppercase;
                    transition: filter 0.3s ease;
                    margin-top: 10px;
                    box-shadow: 0 8px 20px rgba(0, 195, 255, 0.3);
                }
                .btn-ingresar:hover { filter: brightness(1.1); }

                /* =========================================
                   REGLAS PARA CELULARES (ADAPTACIÓN MÓVIL)
                   ========================================= */
                @media (max-width: 576px) {
                    .logo-img {
                        width: 150px !important; /* Logo más pequeño en celular */
                    }
                    .brand-samu {
                        font-size: 3.5rem !important; /* Letra más pequeña */
                    }
                    .btn-comenzar {
                        font-size: 1rem;
                        padding: 14px 30px;
                    }
                    .btn-panel {
                        font-size: 0.9rem;
                        padding: 12px 30px;
                    }
                    #login-box {
                        padding: 30px 25px; /* Menos padding lateral para que encaje mejor */
                    }
                }
            </style>
        </head>
        <body>

            <div class="bg-mesh">
                <div class="blob blob-1"></div>
                <div class="blob blob-2"></div>
                <div class="blob blob-3"></div>
            </div>

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
                        <h4 class="mb-4 text-center" style="color: #0f172a; font-size: 1.6rem; letter-spacing: 2px;">INGRESO</h4>
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
