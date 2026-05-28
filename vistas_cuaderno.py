# =========================================================
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
        "avance_porcentaje": 38.5,
        "ultimo_asiento": 88,
        "llenado_ultimo": 82,
        "firmados": 76,
        "observaciones": 5
    }

    asientos = [
        {"dia": 24, "numero": 84, "estado": "Firmado", "avance": 100, "supervisor": "Ing. Supervisor", "observacion": "Asiento conforme y firmado."},
        {"dia": 25, "numero": 85, "estado": "Firmado", "avance": 100, "supervisor": "Ing. Supervisor", "observacion": "Sin observaciones."},
        {"dia": 26, "numero": 86, "estado": "Observado", "avance": 72, "supervisor": "Ing. Supervisor", "observacion": "Precisar metrados ejecutados en partidas de drenaje."},
        {"dia": 27, "numero": 87, "estado": "Pendiente", "avance": 64, "supervisor": "-", "observacion": "Pendiente de revisión por supervisión."},
        {"dia": 28, "numero": 88, "estado": "En redacción", "avance": 82, "supervisor": "-", "observacion": "Último asiento registrado por residencia."}
    ]

    rol_usuario = session.get('rol', '')

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

            .dashboard-grid {
                display: grid;
                grid-template-columns: 1.15fr 0.85fr;
                gap: 22px;
                margin-bottom: 34px;
            }

            .glass-panel {
                background: rgba(255,255,255,0.72);
                border: 1px solid rgba(255,255,255,0.92);
                backdrop-filter: blur(24px);
                border-radius: 28px;
                padding: 22px;
                box-shadow: 0 18px 45px rgba(15,23,42,0.06);
            }

            .panel-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 14px;
                margin-bottom: 18px;
            }

            .panel-head h3 {
                margin: 0;
                font-size: 17px;
                font-weight: 800;
                letter-spacing: -0.3px;
            }

            .status-pill {
                border-radius: 999px;
                padding: 7px 11px;
                font-size: 11px;
                font-weight: 800;
                background: #eff6ff;
                color: #075985;
            }

            .last-seat {
                display: grid;
                grid-template-columns: auto 1fr;
                gap: 18px;
                align-items: center;
            }

            .seat-number {
                width: 94px;
                height: 94px;
                border-radius: 28px;
                display: grid;
                place-items: center;
                background: linear-gradient(135deg, #0f172a, #0263a0);
                color: #fff;
                box-shadow: 0 18px 36px rgba(2,99,160,0.22);
            }

            .seat-number strong { font-size: 30px; line-height: 1; }
            .seat-number span { font-size: 10px; font-weight: 800; text-transform: uppercase; opacity: 0.75; }

            .progress-soft {
                height: 12px;
                border-radius: 999px;
                background: #e2e8f0;
                overflow: hidden;
                margin: 10px 0 8px;
            }

            .progress-soft > div {
                height: 100%;
                border-radius: 999px;
                background: linear-gradient(90deg, #0263a0, #38bdf8);
            }

            .calendar-grid {
                display: grid;
                grid-template-columns: repeat(7, minmax(0, 1fr));
                gap: 8px;
            }

            .cal-day {
                position: relative;
                border: 1px solid #e2e8f0;
                border-radius: 15px;
                min-height: 52px;
                background: rgba(255,255,255,0.86);
                display: grid;
                place-items: center;
                font-size: 12px;
                font-weight: 800;
                color: #64748b;
                cursor: default;
                transition: all 0.22s ease;
            }

            .cal-day.has-seat {
                color: #0f172a;
                background: #f8fafc;
                border-color: #dbeafe;
                cursor: pointer;
            }

            .cal-day.signed { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }
            .cal-day.observed { background: #fff7ed; border-color: #fed7aa; color: #9a3412; }
            .cal-day.pending { background: #eff6ff; border-color: #bfdbfe; color: #075985; }

            .cal-day:hover {
                transform: translateY(-3px) scale(1.06);
                box-shadow: 0 16px 30px rgba(15,23,42,0.14);
                z-index: 5;
            }

            .cal-tooltip {
                position: absolute;
                left: 50%;
                bottom: calc(100% + 10px);
                transform: translateX(-50%) translateY(8px);
                width: 230px;
                padding: 12px;
                border-radius: 18px;
                background: rgba(15,23,42,0.94);
                color: #fff;
                box-shadow: 0 18px 38px rgba(15,23,42,0.26);
                opacity: 0;
                pointer-events: none;
                transition: .2s ease;
                text-align: left;
                font-size: 11px;
                font-weight: 600;
            }

            .cal-day:hover .cal-tooltip {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }

            .observation-list {
                display: grid;
                gap: 10px;
            }

            .postit {
                border: 1px solid #fde68a;
                border-radius: 18px;
                background: linear-gradient(135deg, #fef9c3, #fff7ed);
                padding: 13px;
                cursor: pointer;
                transition: .22s ease;
                box-shadow: 0 10px 22px rgba(202,138,4,.10);
            }

            .postit:hover {
                transform: translateY(-2px) rotate(-.5deg);
                box-shadow: 0 18px 32px rgba(202,138,4,.16);
            }

            .postit strong { display: block; font-size: 12px; margin-bottom: 4px; color: #78350f; }
            .postit p { margin: 0; font-size: 12px; color: #92400e; line-height: 1.45; }

            .supervisor-tools {
                display: grid;
                gap: 10px;
            }

            .supervisor-note {
                border: 1px solid #dbeafe;
                border-radius: 18px;
                background: #f8fafc;
                padding: 12px;
                min-height: 96px;
                resize: vertical;
                outline: none;
                font-size: 13px;
            }

            .tool-row {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }

            .tool-btn {
                border: none;
                border-radius: 999px;
                padding: 10px 14px;
                font-size: 12px;
                font-weight: 800;
                color: #fff;
                background: linear-gradient(135deg, #0f172a, #0263a0);
                box-shadow: 0 12px 26px rgba(2,99,160,.16);
            }

            .tool-btn.warn { background: linear-gradient(135deg, #b45309, #f59e0b); }
            .tool-btn.ok { background: linear-gradient(135deg, #166534, #22c55e); }

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
                .dashboard-grid {
                    grid-template-columns: 1fr;
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

                <div class="dashboard-grid">
                    <div class="glass-panel">
                        <div class="panel-head">
                            <h3><i class="bi bi-journal-check me-2"></i>Estado del último asiento</h3>
                            <span class="status-pill">Asiento N° {{ estadisticas.ultimo_asiento }}</span>
                        </div>
                        <div class="last-seat">
                            <div class="seat-number">
                                <div class="text-center"><span>N°</span><br><strong>{{ estadisticas.ultimo_asiento }}</strong></div>
                            </div>
                            <div>
                                <div class="d-flex justify-content-between align-items-center">
                                    <strong>Porcentaje de llenado</strong>
                                    <span class="fw-bold text-primary">{{ estadisticas.llenado_ultimo }}%</span>
                                </div>
                                <div class="progress-soft"><div style="width: {{ estadisticas.llenado_ultimo }}%;"></div></div>
                                <p class="text-muted small mb-0">Último asiento registrado por residencia. Supervisión puede revisar, observar o firmar sin modificar el contenido principal.</p>
                            </div>
                        </div>
                    </div>

                    <div class="glass-panel">
                        <div class="panel-head">
                            <h3><i class="bi bi-shield-check me-2"></i>Supervisión</h3>
                            <span class="status-pill">{{ estadisticas.firmados }} firmados</span>
                        </div>
                        <div class="supervisor-tools">
                            <textarea class="supervisor-note" id="notaSupervisor" placeholder="Escribir post-it u observación de supervisión..."></textarea>
                            <div class="tool-row">
                                <button type="button" class="tool-btn warn" onclick="agregarPostItSupervisor()"><i class="bi bi-sticky me-1"></i>Agregar post-it</button>
                                <button type="button" class="tool-btn" onclick="resaltarAsientoDemo()"><i class="bi bi-highlighter me-1"></i>Resaltar</button>
                                <button type="button" class="tool-btn ok" onclick="firmarAsientoDemo()"><i class="bi bi-pen me-1"></i>Firmar asiento</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <div class="glass-panel">
                        <div class="panel-head">
                            <h3><i class="bi bi-calendar3 me-2"></i>Calendario de asientos</h3>
                            <span class="status-pill">Mayo 2026</span>
                        </div>
                        <div class="calendar-grid">
                            {% for d in range(1, 32) %}
                                {% set asiento = (asientos | selectattr('dia', 'equalto', d) | list | first) %}
                                {% if asiento %}
                                    <div class="cal-day has-seat {% if asiento.estado == 'Firmado' %}signed{% elif asiento.estado == 'Observado' %}observed{% else %}pending{% endif %}" onclick="irAAsiento({{ asiento.numero }})">
                                        {{ d }}
                                        <div class="cal-tooltip">
                                            <b>Asiento N° {{ asiento.numero }}</b><br>
                                            Estado: {{ asiento.estado }}<br>
                                            Avance: {{ asiento.avance }}%<br>
                                            Supervisor: {{ asiento.supervisor }}<br>
                                            <span>{{ asiento.observacion }}</span>
                                        </div>
                                    </div>
                                {% else %}
                                    <div class="cal-day">{{ d }}</div>
                                {% endif %}
                            {% endfor %}
                        </div>
                    </div>

                    <div class="glass-panel">
                        <div class="panel-head">
                            <h3><i class="bi bi-stickies me-2"></i>Observaciones activas</h3>
                            <span class="status-pill">{{ estadisticas.observaciones }} observaciones</span>
                        </div>
                        <div class="observation-list" id="listaObservaciones">
                            {% for asiento in asientos if asiento.estado != 'Firmado' %}
                                <div class="postit" onclick="irAAsiento({{ asiento.numero }})">
                                    <strong>Asiento N° {{ asiento.numero }} · {{ asiento.estado }}</strong>
                                    <p>{{ asiento.observacion }}</p>
                                </div>
                            {% endfor %}
                        </div>
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

        <script>
            const nombreSupervisor = "{{ nombre_completo }}";

            function irAAsiento(numero) {
                const destino = `/residencia?asiento=${numero}`;
                window.location.href = destino;
            }

            function agregarPostItSupervisor() {
                const nota = document.getElementById('notaSupervisor');
                const texto = (nota.value || '').trim();
                if (!texto) return;
                const lista = document.getElementById('listaObservaciones');
                const item = document.createElement('div');
                item.className = 'postit';
                item.innerHTML = `<strong>Post-it · ${nombreSupervisor}</strong><p>${texto}</p>`;
                lista.prepend(item);
                nota.value = '';
            }

            function resaltarAsientoDemo() {
                alert('Modo resaltado preparado para supervisión. Al conectar persistencia, se guardará por asiento y usuario.');
            }

            function firmarAsientoDemo() {
                alert('Asiento marcado como firmado por supervisión. Esta acción quedará persistida al conectar base de datos.');
            }
        </script>

    </body>
    </html>
    """, estadisticas=estadisticas, asientos=asientos, rol_usuario=rol_usuario, menu_superior=menu_superior)
