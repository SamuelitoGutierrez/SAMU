from flask import Blueprint, render_template_string, request, session

# Creamos el Blueprint para el módulo de Inicio / Panel Principal
inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/panel')
def panel_principal():
    # Simulador de estados para que puedas probar ambos modos fácilmente.
    # Si entras a /panel?modo=visual -> Verás el modo restringido
    # Si entras a /panel?modo=auth -> Verás el modo liberado
    modo = request.args.get('modo', 'visual')
    
    # Datos simulados de la sesión
    rol_usuario = session.get('rol', 'Invitado' if modo == 'visual' else 'Ing. Residente')
    nombre_usuario = session.get('nombre', 'Visitante' if modo == 'visual' else 'Samuel Gutierrez')

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SAMU - Panel Principal</title>
        
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Bauhaus+93&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --apple-bg: #fbfbfd;
                --apple-text: #1d1d1f;
                --apple-gray: #86868b;
                --apple-blue: #0066cc;
                --nav-height: 48px;
            }

            body {
                margin: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: var(--apple-bg);
                color: var(--apple-text);
                -webkit-font-smoothing: antialiased;
            }

            /* --- NAVBAR ESTILO APPLE (VIDRIO ESMERILADO) --- */
            .apple-nav {
                position: fixed;
                top: 0;
                width: 100%;
                height: var(--nav-height);
                background: rgba(255, 255, 255, 0.72);
                backdrop-filter: saturate(180%) blur(20px);
                -webkit-backdrop-filter: saturate(180%) blur(20px);
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                z-index: 9999;
                display: flex;
                justify-content: center;
                transition: background 0.3s ease;
            }

            .nav-content {
                width: 100%;
                max-width: 980px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0 20px;
                height: 100%;
            }

            /* Logo SAMU en la barra */
            .nav-brand {
                font-family: 'Bauhaus 93', sans-serif;
                font-size: 1.2rem;
                color: var(--apple-text);
                text-decoration: none;
                letter-spacing: 1px;
                transition: opacity 0.2s;
            }
            .nav-brand:hover { opacity: 0.7; }

            /* Enlaces de la barra */
            .nav-links {
                display: flex;
                gap: 35px;
                height: 100%;
            }
            .nav-item {
                font-size: 0.75rem;
                font-weight: 400;
                color: rgba(0, 0, 0, 0.8);
                text-decoration: none;
                display: flex;
                align-items: center;
                height: 100%;
                cursor: pointer;
                transition: color 0.2s;
            }
            .nav-item:hover { color: #000; }

            /* Perfil de Usuario */
            .nav-profile {
                font-size: 0.75rem;
                color: var(--apple-gray);
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .nav-profile i { font-size: 1.1rem; color: var(--apple-text); }

            /* --- MEGA MENÚ DESPLEGABLE (PANEL DE CRISTAL) --- */
            .mega-menu {
                position: fixed;
                top: var(--nav-height);
                left: 0;
                width: 100%;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: saturate(180%) blur(30px);
                -webkit-backdrop-filter: saturate(180%) blur(30px);
                border-bottom: 1px solid rgba(0, 0, 0, 0.08);
                box-shadow: 0 10px 30px rgba(0,0,0,0.04);
                overflow: hidden;
                z-index: 9998;
                
                /* Animación de apertura ultra fluida (CSS Grid) */
                display: grid;
                grid-template-rows: 0fr;
                transition: grid-template-rows 0.4s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.3s ease;
                opacity: 0;
            }
            
            .mega-menu.active {
                grid-template-rows: 1fr;
                opacity: 1;
            }

            .mega-content {
                min-height: 0;
                width: 100%;
                max-width: 980px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                opacity: 0;
                transform: translateY(-10px);
                transition: opacity 0.3s ease 0.1s, transform 0.4s cubic-bezier(0.25, 1, 0.5, 1) 0.1s;
            }
            
            .mega-menu.active .mega-content {
                opacity: 1;
                transform: translateY(0);
                padding-top: 35px;
                padding-bottom: 45px;
            }

            /* Paneles de contenido (se intercambian con fade) */
            .submenu-panel {
                display: none;
                width: 100%;
                animation: fadeIn 0.3s ease;
            }
            .submenu-panel.active {
                display: flex;
                gap: 60px;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateX(-5px); }
                to { opacity: 1; transform: translateX(0); }
            }

            /* Columnas dentro del Mega-Menú */
            .mega-column {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .mega-title {
                font-size: 0.75rem;
                color: var(--apple-gray);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 10px;
                font-weight: 500;
            }
            .mega-link {
                font-size: 1.4rem; /* Links grandes a la izquierda (Estilo Apple) */
                font-weight: 600;
                color: var(--apple-text);
                text-decoration: none;
                transition: color 0.2s;
            }
            .mega-link:hover { color: var(--apple-blue); }
            
            .mega-sublink {
                font-size: 0.85rem; /* Links pequeños a la derecha */
                font-weight: 500;
                color: var(--apple-text);
                text-decoration: none;
                transition: color 0.2s;
            }
            .mega-sublink:hover { color: var(--apple-blue); }

            /* --- TOAST DE ACCESO RESTRINGIDO --- */
            .toast-acceso {
                position: fixed;
                bottom: 40px;
                left: 50%;
                transform: translateX(-50%) translateY(100px);
                background: rgba(29, 29, 31, 0.9);
                backdrop-filter: blur(10px);
                color: white;
                padding: 12px 24px;
                border-radius: 30px;
                font-size: 0.9rem;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 10px;
                opacity: 0;
                transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
                z-index: 10000;
            }
            .toast-acceso.show {
                transform: translateX(-50%) translateY(0);
                opacity: 1;
            }

            /* Contenido de la página de fondo */
            .page-content {
                padding-top: 100px;
                text-align: center;
            }
            
            /* Indicador del Modo Actual */
            .modo-badge {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 20px;
            }
            .badge-visual { background: #f2f2f7; color: var(--apple-gray); }
            .badge-auth { background: #e8f2fc; color: var(--apple-blue); }

        </style>
    </head>
    <body data-modo="{{ modo }}">

        <nav class="apple-nav" id="appleNav">
            <div class="nav-content">
                <a href="#" class="nav-brand">SAMU</a>
                
                <div class="nav-links">
                    <span class="nav-item" data-target="cuaderno">Cuaderno de Obra</span>
                    <span class="nav-item" data-target="personal">Control del Personal</span>
                    <span class="nav-item" data-target="equipo">Equipo Mecánico</span>
                    <span class="nav-item" data-target="almacen">Almacén</span>
                    <span class="nav-item" data-target="avance">Avance de Obra</span>
                    <span class="nav-item" data-target="sistema">Sistema</span>
                </div>

                <div class="nav-profile">
                    {{ nombre_usuario }}
                    <i class="bi bi-person-circle"></i>
                </div>
            </div>
        </nav>

        <div class="mega-menu" id="megaMenu">
            <div class="mega-content">
                
                <div class="submenu-panel" id="panel-cuaderno">
                    <div class="mega-column" style="width: 300px;">
                        <span class="mega-title">Módulos de Registro</span>
                        <a href="#" class="mega-link samu-action">Residencia</a>
                        <a href="#" class="mega-link samu-action">Supervisión</a>
                    </div>
                    <div class="mega-column">
                        <span class="mega-title">Más para Cuaderno</span>
                        <a href="#" class="mega-sublink samu-action">Análisis de Residencia</a>
                        <a href="#" class="mega-sublink samu-action">Análisis de Supervisión</a>
                        <a href="#" class="mega-sublink samu-action">Exportar Partes Diarios</a>
                    </div>
                </div>

                <div class="submenu-panel" id="panel-personal">
                    <div class="mega-column" style="width: 300px;">
                        <span class="mega-title">Gestión Humana</span>
                        <a href="#" class="mega-link samu-action">Registro de Personal</a>
                        <a href="#" class="mega-link samu-action">Personal en Obra</a>
                        <a href="#" class="mega-link samu-action">Asistencias</a>
                    </div>
                    <div class="mega-column">
                        <span class="mega-title">Documentación</span>
                        <a href="#" class="mega-sublink samu-action">Sistema de Papeletas</a>
                        <a href="#" class="mega-sublink samu-action">Análisis de Asistencias</a>
                        <a href="#" class="mega-sublink samu-action">Reporte de Tareos</a>
                    </div>
                </div>

                <div class="submenu-panel" id="panel-equipo">
                    <div class="mega-column" style="width: 300px;">
                        <span class="mega-title">Control de Flota</span>
                        <a href="#" class="mega-link samu-action">Maquinaria y Vehículos</a>
                        <a href="#" class="mega-link samu-action">Operativos México Chico</a>
                        <a href="#" class="mega-link samu-action">Horas Máquina</a>
                    </div>
                    <div class="mega-column">
                        <span class="mega-title">Abastecimiento</span>
                        <a href="#" class="mega-sublink samu-action">Combustible a Equipo</a>
                        <a href="#" class="mega-sublink samu-action">Análisis Horas Máquina</a>
                        <a href="#" class="mega-sublink samu-action">Rendimiento por KM</a>
                    </div>
                </div>

                <div class="submenu-panel" id="panel-almacen">
                    <div class="mega-column" style="width: 300px;">
                        <span class="mega-title">Inventario</span>
                        <a href="#" class="mega-link samu-action">Materiales Generales</a>
                        <a href="#" class="mega-link samu-action">Combustible Principal</a>
                    </div>
                    <div class="mega-column">
                        <span class="mega-title">Reportes</span>
                        <a href="#" class="mega-sublink samu-action">Análisis de Stock</a>
                        <a href="#" class="mega-sublink samu-action">Ingresos y Salidas</a>
                    </div>
                </div>

                <div class="submenu-panel" id="panel-avance">
                    <div class="mega-column" style="width: 300px;">
                        <span class="mega-title">Ejecución Técnica</span>
                        <a href="#" class="mega-link samu-action">Partidas y Metrados</a>
                        <a href="#" class="mega-link samu-action">Actividades Diarias</a>
                        <a href="#" class="mega-link samu-action">Topografía</a>
                    </div>
                    <div class="mega-column">
                        <span class="mega-title">Métricas</span>
                        <a href="#" class="mega-sublink samu-action">Análisis de Metrados</a>
                        <a href="#" class="mega-sublink samu-action">Curva S del Proyecto</a>
                    </div>
                </div>

                <div class="submenu-panel" id="panel-sistema">
                    <div class="mega-column" style="width: 300px;">
                        <span class="mega-title">Administración</span>
                        <a href="#" class="mega-link samu-action">Gestión de Usuarios</a>
                        <a href="#" class="mega-link samu-action">Roles y Permisos</a>
                    </div>
                    <div class="mega-column">
                        <span class="mega-title">Seguridad</span>
                        <a href="#" class="mega-sublink samu-action">Actividad del Sistema</a>
                        <a href="#" class="mega-sublink samu-action">Configuración Global</a>
                    </div>
                </div>

            </div>
        </div>

        <div class="toast-acceso" id="toastAcceso">
            <i class="bi bi-lock-fill"></i> Acceso restringido. Inicie sesión para operar.
        </div>

        <div class="page-content">
            <h1 style="font-size: 3.5rem; font-weight: 600; letter-spacing: -1.5px; margin-bottom: 0;">Centro de Comando</h1>
            <p style="font-size: 1.2rem; color: var(--apple-gray); margin-top: 10px;">Gestión inteligente para la carretera PU N-110.</p>
            
            <div class="modo-badge {{ 'badge-visual' if modo == 'visual' else 'badge-auth' }}">
                MODO ACTUAL: {{ 'VISUAL (SOLO LECTURA)' if modo == 'visual' else 'AUTORIZADO (OPERATIVO)' }}
            </div>
            
            <p style="margin-top: 30px; font-size: 0.9rem; color: #a1a1a6;">
                Pasa el cursor por el menú superior para desplegar las herramientas de SAMU. <br>
                Cambia la URL a <b>/panel?modo=auth</b> para probar el estado liberado.
            </p>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const navItems = document.querySelectorAll('.nav-item');
                const megaMenu = document.getElementById('megaMenu');
                const appleNav = document.getElementById('appleNav');
                const panels = document.querySelectorAll('.submenu-panel');
                const enlacesSamu = document.querySelectorAll('.samu-action');
                const toastAcceso = document.getElementById('toastAcceso');
                const modoActual = document.body.getAttribute('data-modo');
                
                let timeoutId;

                // 1. LÓGICA DE APERTURA DEL MEGA MENÚ (Súper fluido)
                navItems.forEach(item => {
                    item.addEventListener('mouseenter', function() {
                        clearTimeout(timeoutId); // Cancela el cierre si se iba a cerrar
                        
                        const targetPanel = this.getAttribute('data-target');
                        
                        // Ocultar todos los paneles y mostrar solo el que toca
                        panels.forEach(p => p.classList.remove('active'));
                        document.getElementById('panel-' + targetPanel).classList.add('active');
                        
                        // Desplegar el menú
                        megaMenu.classList.add('active');
                        appleNav.style.background = 'rgba(255, 255, 255, 1)'; // Barra solida al abrir
                    });
                });

                // 2. LÓGICA DE CIERRE
                // Si el mouse sale de la barra de navegación Y del mega menú, se cierra
                function cerrarMenu() {
                    timeoutId = setTimeout(() => {
                        megaMenu.classList.remove('active');
                        appleNav.style.background = 'rgba(255, 255, 255, 0.72)';
                    }, 100); // 100ms de gracia para no cerrarlo por accidente
                }

                appleNav.addEventListener('mouseleave', cerrarMenu);
                megaMenu.addEventListener('mouseleave', cerrarMenu);
                
                // Si el mouse vuelve a entrar al menú mientras se estaba cerrando, cancelamos el cierre
                megaMenu.addEventListener('mouseenter', () => clearTimeout(timeoutId));


                // 3. LÓGICA DE PROTECCIÓN (VISUAL VS AUTORIZADO)
                enlacesSamu.forEach(enlace => {
                    enlace.addEventListener('click', function(e) {
                        e.preventDefault(); // Detenemos la navegación por ahora
                        
                        if (modoActual === 'visual') {
                            // Mostrar Toast de Acceso Denegado
                            toastAcceso.classList.add('show');
                            setTimeout(() => toastAcceso.classList.remove('show'), 3000);
                        } else {
                            // En el futuro, aquí irá la redirección real: window.location.href = this.href;
                            alert("¡Acceso Autorizado! Dirigiendo al módulo...");
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    """)
