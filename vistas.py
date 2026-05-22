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
                /* Variables para rastrear la posición fluida del mouse */
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
                    /* El fondo base real de la página es blanco puro */
                    background-color: #ffffff; 
                }

                /* --- CAPA DE COLORES (Que será "espantada" por el mouse) --- */
                .color-layer {
                    position: fixed;
                    top: 0; left: 0; width: 100vw; height: 100vh;
                    z-index: -1;
                    overflow: hidden;
                    background: #ffffff;
                    
                    /* LA MAGIA: Una máscara que oculta los colores justo donde está el mouse */
                    -webkit-mask-image: radial-gradient(circle 35vmax at var(--x) var(--y), transparent 0%, rgba(0,0,0,1) 40%);
                    mask-image: radial-gradient(circle 35vmax at var(--x) var(--y), transparent 0%, rgba(0,0,0,1) 40%);
                }

                .blob {
                    position: absolute;
                    border-radius: 50%;
                    filter: blur(120px);
                }

                /* Luz Azul vibrante pero suave */
                .blob-blue {
                    width: 70vw; height: 70vw;
                    background: #0ea5e9; 
                    opacity: 0.35; 
                    top: -10%; left: -10%;
                    animation: flotar 20s infinite ease-in-out alternate;
                }

                /* Luz Rosada un poco más clara y elegante */
                .blob-pink {
                    width: 70vw; height: 70vw;
                    background: #f9a8d4; /* Rosado más claro */
                    opacity: 0.35; 
                    bottom: -10%; right: -10%;
                    animation: flotar 25s infinite ease-in-out alternate-reverse;
                }

                @keyframes flotar {
                    0% { transform: translate(0, 0) scale(1); }
                    50% { transform: translate(8%, 5%) scale(1.1); }
                    100% { transform: translate(-5%, 8%) scale(0.95); }
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
                    filter: drop-shadow(0px 15px 30px rgba(0, 0, 0, 0.08));
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

                .btn-comenzar {
                    background: #0f172a;
                    color: #ffffff;
                    padding: 16px 40px;
                    border-radius: 16px;
                    border: none;
                    font-size: 1.2rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
                    transition: all 0.3s ease;
                    width: 90%;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                }
                .btn-comenzar:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 30px rgba(15, 23, 42, 0.25);
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

                /* --- LOGIN LIMPIO --- */
                #login-box {
                    display: none; 
                    width: 90%;
                    background: rgba(255, 255, 255, 0.85);
                    backdrop-filter: blur(25px);
                    -webkit-backdrop-filter: blur(25px);
                    padding: 35px 30px;
                    border-radius: 24px;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
                    text-align: left;
                    margin-bottom: 20px;
                    border: 1px solid rgba(255, 255, 255, 1);
                }

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
                    margin-top: 10px;
                    box-shadow: 0 8px 20px rgba(14, 165, 233, 0.2);
                }
                .btn-ingresar:hover { filter: brightness(1.1); }

                @media (max-width: 576px) {
                    .logo-img { width: 160px !important; }
                    .brand-samu { font-size: 3.8rem !important; }
                    .btn-comenzar { font-size: 1.05rem; padding: 14px 30px; }
                    .btn-panel { font-size: 0.9rem; padding: 12px 30px; }
                    #login-box { padding: 30px 25px; }
                    
                    /* En celulares, como no hay mouse, anulamos la máscara para que se vea el color suavemente */
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
                // --- MOTOR DEL MOUSE FLUIDO (ESPANTA LOS COLORES) ---
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
                        // Interpolación para que la máscara se mueva suavemente detrás del mouse
                        curX += (tgX - curX) * 0.05;
                        curY += (tgY - curY) * 0.05;
                        
                        document.documentElement.style.setProperty('--x', Math.round(curX) + 'px');
                        document.documentElement.style.setProperty('--y', Math.round(curY) + 'px');
                        
                        requestAnimationFrame(animate);
                    }
                    animate();
                }

                // --- SECUENCIA DE ANIMACIÓN ---
                window.onload = function() {
                    setTimeout(() => { document.getElementById('logoImg').classList.add('fade-in'); }, 300);
                    setTimeout(() => { document.getElementById('logoImg').classList.add('move-up-logo'); }, 1200);
                    setTimeout(() => { document.getElementById('brandName').classList.add('fade-in'); }, 1800);
                    setTimeout(() => { document.getElementById('brandGroup').classList.add('move-up-group'); }, 2800);
                    setTimeout(() => { document.getElementById('actionArea').classList.add('show'); }, 3500);
                };

                $('#btnComenzar').click(function() {
                    $(this).slideUp(300);
                    setTimeout(() => { $('#login-box').slideDown(500); }, 300);
                });
            </script>
        </body>
        </html>
        """)
