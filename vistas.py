def registrar_rutas(app):
    @app.route('/')
    def inicio():
        # Retorna una página web completamente en blanco
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
                }
            </style>
        </head>
        <body>
            </body>
        </html>
        """
