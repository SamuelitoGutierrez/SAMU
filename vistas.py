def registrar_rutas(app):
    @app.route('/')
    def inicio():
        # Retorna la página con un título grande y centrado
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>SAMU</title>
            <style>
                body { 
                    background-color: #ffffff; /* Fondo blanco */
                    margin: 0; 
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh; /* Ocupa toda la altura de la pantalla */
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                h1 {
                    font-size: 6rem; /* Tamaño gigante del texto */
                    color: #2c3e50; /* Un tono gris azulado oscuro y elegante */
                    text-transform: uppercase;
                    letter-spacing: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Bienvenido a SAMU</h1>
        </body>
        </html>
        """
