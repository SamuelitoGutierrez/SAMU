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
            
            <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
            
            <style>
                body {
                    /* Degradado radial: Blanco al centro, azul muy ligero hacia los bordes */
                    background: radial-gradient(circle at center, #ffffff 0%, #f0f4f8 60%, #e4edf5 100%);
                    margin: 0;
                    font-family: 'Outfit', sans-serif; /* Letra moderna para UI */
                    overflow: hidden;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                /* Contenedor central elevado */
                .main-wrapper {
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    /* Inicia ligeramente más arriba del centro absoluto */
                    transform: translateY(-5vh); 
                    transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
                    width: 100%;
                    max-width: 400px;
                }
                
                /* Subida más pronunciada */
                .main-wrapper.move-up {
                    transform: translateY(-18vh);
                }

                .logo-img {
                    width: 220px; 
                    opacity: 0;
                    filter: drop-shadow(0px 12px 20px rgba(13, 110, 253, 0.1)); /* Sombra con un toque azul */
                    transition: opacity 1.5s ease;
                }
                .logo-img.fade-in {
                    opacity: 1;
                }

                /* SAMU con tipografía Cinzel (Monumental) */
                .brand-samu {
                    font-family: 'Cinzel', serif;
                    font-size: 4.5rem;
                    font-weight: 800;
                    color: #0f172a; /* Azul-grisáceo muy oscuro */
                    opacity: 0;
                    margin-top: 0px;
                    letter-spacing: 0.12em;
                    transition: opacity 1.5s ease;
                }
                .brand-samu.fade-in {
                    opacity: 1;
                }

                .action-area {
                    position: absolute;
                    top: 100%; 
                    width: 100%;
                    margin-top: 35px;
                }

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

                .btn-comenzar {
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                    color: white;
                    padding: 16px 40px;
                    border-radius: 30px;
                    border: none;
                    font-weight: 600;
                    font-size: 1.05rem;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 20px rgba(15, 23, 42, 0.2);
                    transition: all 0.3s ease;
                    width: 85%;
                    margin-bottom: 15px;
                }
                .btn-comenzar:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 25px rgba(15, 23, 42, 0.3);
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
                    color: #64748b;
                    border: 1px solid #cbd5e1;
                    padding: 14px 40px;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 0.9rem;
                    letter-spacing: 1.5px;
                    width: 85%;
                    transition: all 0.3s ease;
                }
                .btn-panel:hover {
                    background-color: #f8fafc;
                    color: #0f172a;
                    border-color: #94a3b8;
                }

                #login-box {
                    opacity: 0;
                    visibility: hidden;
                    transform: translateY(-20px);
                    transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1);
                    position: absolute;
                    width: 100%;
                    top: 0;
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    padding: 40px 35px;
                    border-radius: 24px;
                    box-shadow: 0 25px 50px rgba(15, 23, 42, 0.08);
                    text-align: left;
                    border: 1px solid rgba(255, 255, 255, 0.5);
                }
                #login-box.show {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0);
                }

                .form-control {
                    background-color: #f1f5f9;
                    border: 1px solid transparent;
                    border-radius: 14px;
                    padding: 15px;
                    font-family: 'Outfit', sans-serif;
                    font-weight: 400;
                    transition: all 0.3s ease;
                }
                .form-control:focus {
                    background-color: #ffffff;
                    border: 1px solid #3b82f6;
                    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
                }
            </style>
        </head>
        <body>

            <div class="main-wrapper" id="mainWrapper">
                
                <img id="logoImg" src="{{ url_for('static', filename='logo_s.png') }}" class="logo-img" alt="Logo SAMU">
                
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
                        <h5 class="mb-4 text-center fw-bold" style="color: #0f172a; font-family: 'Cinzel', serif;">Acceso Seguro</h5>
                        <div class="mb-3">
                            <label class="form-label small text-muted fw-bold">Usuario</label>
                            <input type="text" class="form-control" placeholder="Introducir usuario">
                        </div>
                        <div class="mb-4">
                            <label class="form-label small text-muted fw-bold">Contraseña</label>
                            <input type="password" class="form-control" placeholder="••••••••">
                        </div>
                        <button class="btn w-100" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border-radius: 14px; padding: 15px; font-weight: 600; letter-spacing: 1px; border: none; box-shadow: 0 8px 15px rgba(37, 99, 235, 0.2);">Ingresar</button>
                    </div>

                </div>
            </div>

            <script>
                const logoImg = document.getElementById('logoImg');
                const brandName = document.getElementById('brandName');
                const mainWrapper = document.getElementById('mainWrapper');
                const botonesContainer = document.getElementById('botonesContainer');
                const btnComenzar = document.getElementById('btnComenzar');
                const loginBox = document.getElementById('login-box');

                window.onload = function() {
                    setTimeout(() => {
                        logoImg.classList.add('fade-in');
                    }, 200);

                    setTimeout(() => {
                        brandName.classList.add('fade-in');
                    }, 1000);

                    setTimeout(() => {
                        mainWrapper.classList.add('move-up');
                        botonesContainer.classList.add('show');
                    }, 2000);
                };

                btnComenzar.addEventListener('click', function() {
                    botonesContainer.classList.remove('show');
                    
                    setTimeout(() => {
                        loginBox.classList.add('show');
                    }, 400); 
                });
            </script>
        </body>
        </html>
        """)
