def registrar_rutas(app):
    @app.route('/')
    def inicio():
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAMU - Acceso</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #f4f7f6; /* Fondo gris muy claro y elegante */
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                    overflow: hidden; /* Evita que la pantalla se mueva durante la animación */
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                
                /* Contenedor principal */
                .splash-container {
                    text-align: center;
                    position: relative;
                    width: 100%;
                    max-width: 400px;
                    padding: 20px;
                }

                /* Diseño de la S inicial */
                .logo-s {
                    font-size: 7rem;
                    font-weight: 800;
                    color: #0d6efd; /* Azul profesional */
                    position: absolute;
                    top: 50vh; /* Centrado verticalmente al inicio */
                    left: 50%;
                    transform: translate(-50%, -50%);
                    transition: all 1s ease-in-out; /* La magia del movimiento fluido */
                    margin: 0;
                }

                /* Clase que se activa para subir la S */
                .logo-s.move-up {
                    top: 0; 
                    position: relative;
                    transform: translate(-50%, 0);
                    font-size: 4rem; /* Se hace un poco más pequeña al subir */
                }

                /* Diseño del texto SAMU */
                .brand-name {
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #2c3e50;
                    opacity: 0; /* Invisible al inicio */
                    transform: translateY(20px); /* Ligeramente abajo al inicio */
                    transition: all 1s ease-in-out;
                    margin-top: -10px;
                    letter-spacing: 2px;
                }

                /* Clase que se activa para mostrar SAMU */
                .brand-name.show {
                    opacity: 1;
                    transform: translateY(0);
                }

                /* Diseño de la tarjeta de Iniciar Sesión */
                .login-container {
                    opacity: 0; /* Invisible al inicio */
                    transform: translateY(20px);
                    transition: all 1s ease-in-out;
                    margin-top: 30px;
                }

                /* Clase que se activa para mostrar el Login */
                .login-container.show {
                    opacity: 1;
                    transform: translateY(0);
                }
            </style>
        </head>
        <body>
            <div class="splash-container">
                <div class="logo-s" id="logo">S</div>
                
                <div class="brand-name" id="brand">SAMU</div>
                
                <div class="login-container" id="loginForm">
                    <div class="card shadow-lg border-0 rounded-4">
                        <div class="card-body p-4 p-sm-5">
                            <h5 class="card-title text-center mb-4 text-muted">Iniciar Sesión</h5>
                            <form>
                                <div class="mb-3">
                                    <input type="text" class="form-control form-control-lg" placeholder="Usuario" required>
                                </div>
                                <div class="mb-4">
                                    <input type="password" class="form-control form-control-lg" placeholder="Contraseña" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold">Ingresar</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                document.addEventListener("DOMContentLoaded", () => {
                    // Paso 1: Espera 1 segundo y sube la "S"
                    setTimeout(() => {
                        document.getElementById("logo").classList.add("move-up");
                    }, 1000); 

                    // Paso 2: A la par que la "S" sube, aparece "SAMU"
                    setTimeout(() => {
                        document.getElementById("brand").classList.add("show");
                    }, 1400); 

                    // Paso 3: Un segundo después, aparece suavemente el Login
                    setTimeout(() => {
                        document.getElementById("loginForm").classList.add("show");
                    }, 2200); 
                });
            </script>
        </body>
        </html>
        """
