\# =========================================================
# vistas_cuaderno.py
# Módulo: Cuaderno de Obra Digital - Lobby Central (Responsivo)
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar

cuaderno_bp = Blueprint('cuaderno', __name__)

# NOTA IMPORTANTE: Ahora SOLO maneja la ruta /cuaderno. 
# Esto permite que vistas_residencia.py funcione correctamente sin interferencias.
@cuaderno_bp.route('/cuaderno')
def panel_cuaderno():
    # Validación de sesión de usuario
    if 'usuario_id' not in session: 
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Visitante')
    
    # Obtenemos la barra de navegación superior renderizada
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    # Datos estadísticos para el panel gerencial
    estadisticas = { 
        "total_asientos": 88, 
        "dias_lluvia": 14, 
        "consultas_pendientes": 3, 
        "avance_porcentaje": 38.5 
    }

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Lobby del Cuaderno de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
            :root { 
                --apple-text: #1d1d1f; 
                --apple-gray: #86868b; 
                --glass-bg: rgba(255, 255, 255, 0.6); 
                --glass-border: rgba(255, 255, 255, 0.8); 
            }
            
            body { 
                margin: 0; 
                font-family: 'Inter', sans-serif; 
                background-color: #fbfbfd; 
                color: var(--apple-text); 
                overflow-x: hidden; 
                min-height: 100vh; 
            }
            
            /* --- FONDO ANIMADO AL 20% --- */
            .dynamic-bg { 
                position: fixed; 
                inset: 0; 
                z-index: -2; 
                background: #fbfbfd; 
                overflow: hidden;
            }
            
            .bg-blob { 
                position: absolute; 
                border-radius: 50%; 
                filter: blur(90px); 
                pointer-events: none; 
            }
            
            .blob-navy { 
                width: 70vw; 
                height: 70vw; 
                max-width: 600px; 
                max-height: 600px; 
                background: #0f172a; 
                opacity: 0.15; 
                top: -10%; 
                left: -10%; 
                animation: movAzul 20s infinite alternate; 
            }
            
            .blob-pink { 
                width: 70vw; 
                height: 70vw; 
                max-width: 600px; 
                max-height: 600px; 
                background: #f9a8d4; 
                opacity: 0.15; 
                bottom: -10%; 
                right: -10%; 
                animation: movRosa 24s infinite alternate; 
            }
            
            @keyframes movAzul { 100% { transform: translate(10vw,10vh) scale(1.1); } }
            @keyframes movRosa { 100% { transform: translate(-10vw,-10vh) scale(1.1); } }

            /* --- CONTENEDOR PRINCIPAL LOBBY --- */
            .view-section { 
                width: 100%; 
                min-height: 100vh; 
                padding: 100px 20px 40px; 
            }
            
            .main-container { 
                max-width: 1000px; 
                margin: 0 auto; 
            }
            
            .project-title { 
                text-align: center; 
                margin-bottom: 40px; 
            }
            
            .project-title h1 { 
                font-size: 32px; 
                font-weight: 700; 
                letter-spacing: -1px; 
                margin-bottom: 6px; 
            }
            
            .project-title p { 
                color: var(--apple-gray); 
                font-size: 15px; 
                margin: 0; 
            }
            
            /* --- DASHBOARD ESTADÍSTICO --- */
            .stats-grid { 
                display: grid; 
                grid-template-columns: repeat(4, 1fr); 
                gap: 16px; 
                margin-bottom: 40px; 
            }
            
            .stat-card { 
                background: var(--glass-bg); 
                border: 1px solid var(--glass-border); 
                backdrop-filter: blur(20px); 
                -webkit-backdrop-filter: blur(20px); 
                padding: 18px; 
                border-radius: 18px; 
                text-align: center; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.02); 
                transition: transform 0.3s;
            }
            
            .stat-card:hover { 
                transform: translateY(-2px); 
            }
            
            .stat-card label { 
                font-size: 11px; 
                color: var(--apple-gray); 
                text-transform: uppercase; 
                font-weight: 600; 
                letter-spacing: 0.5px;
            }
            
            .stat-card .value { 
                font-size: 26px; 
                font-weight: 700; 
                color: #000; 
                margin-top: 5px; 
                letter-spacing: -0.5px;
            }

            /* --- PORTALES DE ACCESO DIRECTO --- */
            .portals-grid { 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 30px; 
            }
            
            /* Convertido a diseño de botón/enlace real */
            .portal-card { 
                background: rgba(255,255,255,0.7); 
                border: 1px solid rgba(255,255,255,0.9); 
                backdrop-filter: blur(25px); 
                -webkit-backdrop-filter: blur(25px); 
                border-radius: 30px; 
                padding: 50px 30px; 
                text-align: center; 
                cursor: pointer; 
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
                box-shadow: 0 10px 30px rgba(0,0,0,0.03); 
                text-decoration: none;
                color: inherit;
                display: block;
            }
            
            .portal-card:hover { 
                transform: translateY(-5px) scale(1.02); 
                background: #ffffff; 
                border-color: #0066cc; 
                box-shadow: 0 20px 40px rgba(0,102,204,0.1); 
            }
            
            .portal-card:active { 
                transform: scale(0.98); 
                background: #f8fafc; 
            } 
            
            .portal-icon { 
                font-size: 45px; 
                color: #0066cc; 
                margin-bottom: 20px; 
            }
            
            .portal-title { 
                font-size: 24px; 
                font-weight: 700; 
                margin-bottom: 10px; 
                letter-spacing: -0.5px;
            }
            
            .portal-desc { 
                font-size: 14px; 
                color: var(--apple-gray); 
                line-height: 1.4;
            }

            /* --- MEDIA QUERIES (RESPONSIVO MÓVIL Y TABLET) --- */
            @media (max-width: 991px) { 
                .stats-grid { 
                    grid-template-columns: repeat(2, 1fr); 
                }
            }
            
            @media (max-width: 576px) { 
                .view-section { 
                    padding: 90px 15px 30px; 
                }
                .portals-grid { 
                    grid-template-columns: 1fr; 
                    gap: 20px;
                } 
                .stats-grid { 
                    grid-template-columns: 1fr 1fr; 
                    gap: 12px;
                }
                .project-title h1 { 
                    font-size: 26px; 
                }
                .portal-card { 
                    padding: 35px 20px; 
                    border-radius: 24px;
                }
                .stat-card .value {
                    font-size: 22px;
                }
                .stat-card {
                    padding: 12px;
                }
            }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}
        
        <div class="dynamic-bg">
            <div class="bg-blob blob-navy"></div>
            <div class="bg-blob blob-pink"></div>
        </div>

        <div class="view-section">
            <div class="main-container">
                
                <div class="project-title">
                    <h1>Carretera PU N-110</h1>
                    <p>Tramo: Asiruni — Rosaspata — Huayrapata &bull; Cuaderno de Obra Digital</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <label>Asientos Totales</label>
                        <div class="value">{{ estadisticas.total_asientos }}</div>
                    </div>
                    <div class="stat-card">
                        <label>Días de Lluvia</label>
                        <div class="value">{{ estadisticas.dias_lluvia }}</div>
                    </div>
                    <div class="stat-card">
                        <label>Consultas Pendientes</label>
                        <div class="value" style="color: #dc2626;">{{ estadisticas.consultas_pendientes }}</div>
                    </div>
                    <div class="stat-card">
                        <label>Avance Físico</label>
                        <div class="value">{{ estadisticas.avance_porcentaje }}%</div>
                    </div>
                </div>
                
                <div class="portals-grid">
                    <a href="/residencia" class="portal-card">
                        <div class="portal-icon"><i class="bi bi-journal-richtext"></i></div>
                        <div class="portal-title">Residencia de Obra</div>
                        <div class="portal-desc">Aperturar asientos legales, registrar avances diarios, control de metrados y ocurrencias.</div>
                    </a>
                    
                    <a href="/supervision" class="portal-card">
                        <div class="portal-icon"><i class="bi bi-shield-check"></i></div>
                        <div class="portal-title">Supervisión de Obra</div>
                        <div class="portal-desc">Control técnico, absolución de consultas, emisión de órdenes y verificaciones de terreno.</div>
                    </a>
                </div>

            </div>
        </div>

    </body>
    </html>
    """, estadisticas=estadisticas, menu_superior=menu_superior)
