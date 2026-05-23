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
            <title>SAMU</title> <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
            
            <style>
                /* Variables para el mouse */
                :root {
                    --x: 50vw;
                    --y: 50vh;
                }

                body {
                    margin: 0;
                    font-family: 'Bauhaus 93', 'Arial Rounded MT Bold', sans-serif;
                    overflow: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #0f172a;
                    background-color: #ffffff; 
                }

                /* --- CAPA DE COLORES Y MÁSCARA --- */
                .color-layer {
                    position: fixed;
                    top: 0; left: 0; width: 100vw; height: 100vh;
                    z-index: -1;
                    overflow: hidden;
                    background: #ffffff;
                    
                    -webkit-mask-image: radial-gradient(circle 35vmax at var(--x) var(--y), transparent 0%, rgba(0,0,0,1) 90%);
                    mask-image: radial-gradient(circle 35vmax at var(--x) var(--y), transparent 0%, rgba(0,0,0,1) 90%);
                }

                .blob {
                    position: absolute;
                    border-radius: 50%;
                    filter: blur(100px);
                }

                .blob-blue {
                    width: 55vw; height: 55vw;
                    background: #0ea5e9; 
                    opacity: 0.25; 
                    top: -5%; left: -5%;
                    animation: flotar 25s infinite ease-in-out alternate;
                }

                .blob-pink {
                    width: 55vw; height: 55vw;
                    background: #f9a8d4; 
                    opacity: 0.20; 
                    bottom: -5%; right: -5%;
                    animation: flotar 30s infinite ease-in-out alternate-reverse;
                }

                @keyframes flotar {
                    0% { transform: translate(0, 0) scale(1); }
                    50% { transform: translate(5%, 3%) scale(1.05); }
                    100% { transform: translate(-3%, 5%) scale(0.98); }
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

                .brand-group {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    transform: translateY(12vh);
                    transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
                }
                
                .brand-group.move-up-group { transform: translateY(-2vh); }

                .logo-img {
                    width: 250px;
                    opacity: 0;
                    transform: translateY(0);
                    filter: drop-shadow(0px 15px 30px rgba(0, 0, 0, 0.05));
                    transition: opacity 1.2s ease, transform 1s ease;
                }
                .logo-img.fade-in { opacity: 1; }
                .logo-img.move-up-logo { transform: translateY(-15px); }

                .brand-samu {
                    font-size: 5rem;
                    color: #0f172a;
                    opacity: 0;
                    margin-top: 5px;
                    letter-spacing: 0.08em;
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

                /* BOTONES Y MÓDULOS */
                .btn-comenzar {
                    background: #0f172a;
                    color: #ffffff;
                    padding: 16px 40px;
                    border-radius: 16px;
                    border: none;
                    font-size: 1.2rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1);
                    transition: all 0.3s ease;
                    width: 90%;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                }
                .btn-comenzar:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 30px rgba(15, 23, 42, 0.2);
                    background: #1e293b;
                }
                .btn-comenzar i { margin-left: 10px; font-size: 1.2rem; }

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
                    background-color: #f1f5f9;
                    color: #0f172a;
                    border-color: #94a3b8;
                }

                /* LOGIN LIMPIO */
                #login-wrapper {
                    display: none; 
                    width: 100%;
                }

                #login-box {
                    width: 90%;
                    margin: 0 auto 20px auto;
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(25px);
                    -webkit-backdrop-filter: blur(25px);
                    padding: 35px 30px;
                    border-radius: 24px;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.06);
                    text-align: left;
                    border: 1px solid rgba(0, 0, 0, 0.04);
                }

                .btn-volver {
                    background: none;
                    border: none;
                    color: #94a3b8;
                    font-size: 1.4rem;
                    padding: 0;
                    cursor: pointer;
                    transition: color 0.3s ease;
                }
                .btn-volver:hover { color: #0f172a; }

                .form-label {
                    font-size: 0.95rem;
                    color: #64748b;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    margin-bottom: 8px;
                    font-family: 'Arial Rounded MT Bold', sans-serif;
                }

                .form-control {
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 14px 15px;
                    font-family: 'Arial', sans-serif;
                    font-size: 1rem;
                    color: #0f172a;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background-color: #ffffff;
                    border: 1px solid #3b82f6;
                    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
                }
                .form-control::placeholder { color: #94a3b8; }

                .btn-ingresar {
                    background: linear-gradient(90deg, #0ea5e9 0%, #3b82f6 100%);
                    color: white;
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 1.1rem;
                    letter-spacing: 2px;
                    border: none;
                    text-transform: uppercase;
                    transition: filter 0.3s ease;
                    margin-top: 15px;
                    box-shadow: 0 8px 20px rgba(14, 165, 233, 0.2);
                }
                .btn-ingresar:hover { filter: brightness(1.1); }

                /* =========================================
                   AJUSTES REDUCIDOS PARA CELULAR
                   ========================================= */
                @media (max-width: 576px) {
                    .logo-img { width: 130px !important; } /* Logo más chico */
                    .brand-samu { font-size: 3.2rem !important; margin-top: 0 !important; } /* Letra más chica */
                    
                    .btn-comenzar { 
                        font-size: 1rem; 
                        padding: 12px 25px; 
                        border-radius: 12px; 
                        margin-bottom: 15px;
                    }
                    .btn-panel { 
                        font-size: 0.85rem; 
                        padding: 12px 25px; 
                        border-radius: 12px;
                    }
                    
                    #login-box { 
                        padding: 25px 20px; 
                        border-radius: 16px;
                    }
                    .form-control { font-size: 0.95rem; padding: 12px; }
                    .btn-ingresar { font-size: 1rem; padding: 12px; }
                    
                    .color-layer {
                        -webkit-mask-image: none;
                        mask-image: none;
                        opacity: 0.5;
                    }
                }
            </style>
        </head>
        <body>

            <div class="color-layer">
                <div class="blob blob-pink"></div>
                <div class="blob blob-blue"></div>
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

                    <div id="login-wrapper">
                        <div id="login-box">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <button class="btn-volver" id="btnVolver" title="Retroceder"><i class="bi bi-arrow-left"></i></button>
                                <h4 class="m-0 text-center flex-grow-1" style="color: #0f172a; font-size: 1.5rem; letter-spacing: 2px; transform: translateX(-10px);">INGRESO</h4>
                            </div>
                            
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
                    </div>

                    <button class="btn-panel" id="btnPanel">
                        PANEL PRINCIPAL
                    </button>
                    
                </div>
            </div>

            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                // --- MOTOR DEL MOUSE ---
                let curX = window.innerWidth / 2;
                let curY = window.innerHeight / 2;
                let tgX = curX;
                let tgY = curY;

                if (window.matchMedia("(pointer: fine)").matches) {
                    window.addEventListener('mousemove', (e) => {
                        tgX = e.clientX;
                        tgY = e.clientY;
                    });

                    function animate() {
                        curX += (tgX - curX) * 0.05;
                        curY += (tgY - curY) * 0.05;
                        document.documentElement.style.setProperty('--x', Math.round(curX) + 'px');
                        document.documentElement.style.setProperty('--y', Math.round(curY) + 'px');
                        requestAnimationFrame(animate);
                    }
                    animate();
                }

                // --- ANIMACIÓN INICIAL ---
                window.onload = function() {
                    setTimeout(() => { document.getElementById('logoImg').classList.add('fade-in'); }, 300);
                    setTimeout(() => { document.getElementById('logoImg').classList.add('move-up-logo'); }, 1200);
                    setTimeout(() => { document.getElementById('brandName').classList.add('fade-in'); }, 1800);
                    setTimeout(() => { document.getElementById('brandGroup').classList.add('move-up-group'); }, 2800);
                    setTimeout(() => { document.getElementById('actionArea').classList.add('show'); }, 3500);
                };

                // --- TRANSICIÓN PERFECTA SIN RECORTES ---
                const btnComenzar = $('#btnComenzar');
                const loginWrapper = $('#login-wrapper');

                // Al hacer clic en Comenzar
                btnComenzar.click(function() {
                    // Primero desvanece el botón sin achicarlo (evita el recorte visual)
                    $(this).fadeOut(200, function() {
                        // Una vez oculto, desglosa el cuadro de login suavemente
                        loginWrapper.slideDown(400);
                    });
                });

                // Al hacer clic en Retroceder
                $('#btnVolver').click(function(e) {
                    e.preventDefault();
                    // Primero recoge el cuadro de login
                    loginWrapper.slideUp(350, function() {
                        // Una vez recogido, hace reaparecer el botón
                        btnComenzar.fadeIn(300);
                    });
                });
            </script>
        </body>
        </html>
        """)
