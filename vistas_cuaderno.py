# =========================================================
# vistas_cuaderno.py
# Módulo: Cuaderno de Obra Digital (Lobby + Autoapertura)
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for, request
from navbar import obtener_navbar

cuaderno_bp = Blueprint('cuaderno', __name__)

# Registramos las 3 rutas para que el cerebro (main.py) sepa manejarlas
@cuaderno_bp.route('/cuaderno')
@cuaderno_bp.route('/residencia')
@cuaderno_bp.route('/supervision')
def panel_cuaderno():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Visitante')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    # Detectar por dónde entró el usuario para auto-expandir la ventana
    ruta_actual = request.path
    modo_auto = 'ninguno'
    if '/residencia' in ruta_actual:
        modo_auto = 'residencia'
    elif '/supervision' in ruta_actual:
        modo_auto = 'supervision'

    estadisticas = { "total_asientos": 87, "dias_lluvia": 14, "consultas_pendientes": 3, "avance_porcentaje": 38.5 }
    historial_asientos = [
        {"numero": 87, "fecha": "23/May/2026", "resumen": "Paralización en Frente 02 por falla en Excavadora CAT 336."},
        {"numero": 86, "fecha": "22/May/2026", "resumen": "Colocación de subbase granular KM 12+400 al KM 13+100."}
    ]

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Cuaderno de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Bauhaus+93&display=swap" rel="stylesheet">
        
        <style>
            :root { --apple-text: #1d1d1f; --apple-gray: #86868b; --glass-bg: rgba(255, 255, 255, 0.6); --glass-border: rgba(255, 255, 255, 0.8); }
            body { margin: 0; font-family: 'Inter', sans-serif; background-color: #fbfbfd; color: var(--apple-text); overflow-x: hidden; min-height: 100vh; }
            .dynamic-bg { position: fixed; inset: 0; z-index: -2; background: #fbfbfd; overflow: hidden;}
            .bg-blob { position: absolute; border-radius: 50%; filter: blur(120px); pointer-events: none; }
            .blob-navy { width: 55vw; height: 55vw; background: #0f172a; opacity: 0.20; top: -10%; left: -10%; animation: movAzul 22s infinite ease-in-out; }
            .blob-pink { width: 50vw; height: 50vw; background: #f9a8d4; opacity: 0.20; bottom: -15%; right: -10%; animation: movRosa 26s infinite ease-in-out reverse; }
            @keyframes movAzul { 0%, 100% { transform: translate(0,0) scale(1); } 50% { transform: translate(8vw,6vh) scale(1.1); } }
            @keyframes movRosa { 0%, 100% { transform: translate(0,0) scale(1); } 50% { transform: translate(-6vw,-8vh) scale(1.15); } }

            .view-section { position: absolute; top: 0; left: 0; width: 100%; min-height: 100vh; padding: 100px 20px 40px; transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1); }
            #dashboardView { opacity: 1; transform: scale(1); z-index: 10; }
            #workspaceView { opacity: 0; transform: translateY(50px) scale(0.95); z-index: 5; pointer-events: none; display: none; }
            
            .view-hidden-up { opacity: 0 !important; transform: translateY(-50px) scale(0.95) !important; pointer-events: none; }
            .view-active { opacity: 1 !important; transform: translateY(0) scale(1) !important; pointer-events: auto !important; display: block !important; z-index: 20 !important;}

            .main-container { max-width: 1000px; margin: 0 auto; }
            .project-title { text-align: center; margin-bottom: 40px; }
            .project-title h1 { font-size: 34px; font-weight: 700; letter-spacing: -1px; margin-bottom: 4px; }
            .project-title p { color: var(--apple-gray); font-size: 15px; margin: 0; }
            .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 40px; }
            .stat-card { background: var(--glass-bg); border: 1px solid var(--glass-border); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); padding: 20px; border-radius: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
            .stat-card label { font-size: 11px; color: var(--apple-gray); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
            .stat-card .value { font-size: 28px; font-weight: 700; letter-spacing: -0.5px; color: #000; margin-top: 5px; }

            .portals-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
            .portal-card { background: rgba(255,255,255,0.7); border: 1px solid rgba(255,255,255,0.9); backdrop-filter: blur(30px); border-radius: 30px; padding: 50px 40px; text-align: center; cursor: pointer; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
            .portal-card:hover { transform: translateY(-5px) scale(1.02); background: #ffffff; border-color: #0066cc; box-shadow: 0 20px 40px rgba(0,102,204,0.1); }
            .portal-icon { font-size: 48px; color: #0066cc; margin-bottom: 20px; }
            .portal-title { font-size: 24px; font-weight: 700; margin-bottom: 10px; }
            .portal-desc { font-size: 14px; color: var(--apple-gray); }

            .workspace-container { max-width: 1300px; margin: 0 auto; }
            .btn-back { background: none; border: none; font-size: 14px; font-weight: 600; color: #0066cc; margin-bottom: 20px; cursor: pointer; display: flex; align-items: center; gap: 8px;}
            .btn-back:hover { text-decoration: underline; }
            .workspace-split { display: grid; grid-template-columns: 320px 1fr; gap: 24px; align-items: start; }
            
            .timeline-wrapper, .canvas-wrapper { background: var(--glass-bg); border: 1px solid var(--glass-border); backdrop-filter: blur(25px); border-radius: 24px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.02); }
            .timeline-wrapper { max-height: calc(100vh - 180px); overflow-y: auto; }
            .timeline-title { font-size: 12px; font-weight: 700; color: var(--apple-gray); text-transform: uppercase; margin-bottom: 15px; }
            .timeline-item { background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.8); padding: 15px; border-radius: 16px; margin-bottom: 12px; cursor: pointer; transition: 0.2s; }
            .timeline-item:hover { background: #fff; border-color: #cbd5e1; }
            .timeline-item strong { color: #0066cc; display: block; font-size: 13px; margin-bottom: 4px; }
            .timeline-item p { font-size: 12px; color: #334155; margin: 0; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

            .form-section-title { font-size: 13px; font-weight: 700; color: #000; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 1px solid rgba(0,0,0,0.08); text-transform: uppercase; margin-top: 25px;}
            .form-label { font-size: 12px; font-weight: 600; color: var(--apple-gray); margin-bottom: 8px; }
            .form-select, .form-control { border-radius: 14px; border: 1px solid #e2e8f0; padding: 14px; font-size: 14px; background: rgba(255,255,255,0.7); transition: all 0.2s; }
            .form-select:focus, .form-control:focus { background: #ffffff; border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.1); outline: none; }

            .slider-container { width: 100%; max-width: 450px; margin: 40px auto 10px auto; position: relative; }
            .slider-track { width: 100%; height: 60px; background: rgba(0,0,0,0.04); border: 1px solid rgba(0,0,0,0.03); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; user-select: none; }
            .slider-text { font-size: 13px; font-weight: 600; color: #4b5563; text-transform: uppercase; pointer-events: none; z-index: 1; }
            .slider-handle { width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; cursor: grab; z-index: 2; transition: left 0.1s ease-out; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            .slider-handle:active { cursor: grabbing; background: #0066cc; }
            .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}

        <div class="dynamic-bg"><div class="bg-blob blob-navy"></div><div class="bg-blob blob-pink"></div></div>

        <div class="view-section" id="dashboardView">
            <div class="main-container">
                <div class="project-title">
                    <h1>Carretera PU N-110</h1>
                    <p>Asiruni — Rosaspata — Huayrapata &bull; Cuaderno de Obra Digital</p>
                </div>

                <div class="stats-grid">
                    <div class="stat-card"><label>Asientos Totales</label><div class="value">{{ estadisticas.total_asientos }}</div></div>
                    <div class="stat-card"><label>Días Impactados</label><div class="value">{{ estadisticas.dias_lluvia }}</div></div>
                    <div class="stat-card"><label>Consultas Pendientes</label><div class="value" style="color: #dc2626;">{{ estadisticas.consultas_pendientes }}</div></div>
                    <div class="stat-card"><label>Avance Físico</label><div class="value">{{ estadisticas.avance_porcentaje }}%</div></div>
                </div>

                <div class="portals-grid">
                    <div class="portal-card" onclick="abrirWorkspace('residencia')">
                        <div class="portal-icon"><i class="bi bi-journal-richtext"></i></div>
                        <div class="portal-title">Residencia de Obra</div>
                        <div class="portal-desc">Aperturar asientos legales y registrar avances diarios.</div>
                    </div>
                    <div class="portal-card" onclick="abrirWorkspace('supervision')">
                        <div class="portal-icon"><i class="bi bi-shield-check"></i></div>
                        <div class="portal-title">Supervisión de Obra</div>
                        <div class="portal-desc">Control, absolución de consultas y órdenes técnicas.</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="view-section" id="workspaceView">
            <div class="workspace-container">
                <button class="btn-back" onclick="volverDashboard()">
                    <i class="bi bi-arrow-left"></i> Volver al Menú Central del Cuaderno
                </button>

                <div class="workspace-split">
                    <div class="timeline-wrapper">
                        <div class="timeline-title">Historial de Folios</div>
                        {% for asiento in historial_asientos %}
                        <div class="timeline-item">
                            <strong>Asiento N° {{ asiento.numero }} &bull; {{ asiento.fecha }}</strong>
                            <p>{{ asiento.resumen }}</p>
                        </div>
                        {% endfor %}
                    </div>

                    <div class="canvas-wrapper">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h3 class="m-0" style="font-weight: 700; letter-spacing: -0.5px;">Asiento N° {{ estadisticas.total_asientos + 1 }}</h3>
                            <span class="badge bg-dark py-2 px-3" style="font-size: 12px; border-radius: 8px;" id="etiquetaModo">Residencia</span>
                        </div>
                        <p style="color: var(--apple-gray); font-size: 14px; margin-bottom: 25px;">Modo Borrador &bull; Guardado automático local</p>

                        <form id="formLegalObra" onsubmit="event.preventDefault();">
                            <div class="form-section-title" style="margin-top: 0;">1. Condiciones del Entorno</div>
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <label class="form-label">Estado Climático Dominante</label>
                                    <select class="form-select" required>
                                        <option value="soleado">Soleado / Despejado</option>
                                        <option value="nublado">Nublado</option>
                                        <option value="lluvia">Lluvia Intensa (Paralización)</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Impacto Operativo</label>
                                    <select class="form-select" required>
                                        <option value="normal">Trabajo Normal (100%)</option>
                                        <option value="parcial">Restricción Parcial</option>
                                    </select>
                                </div>
                            </div>

                            <div class="form-section-title">2. Trabajos Ejecutados y Metrados</div>
                            <div class="mb-4">
                                <textarea class="form-control" rows="5" placeholder="Describa progresivas, frentes activos y requerimientos técnicos..." required></textarea>
                            </div>

                            <div class="form-section-title" style="color: #dc2626;">3. Firma Inmutable</div>
                            <div class="slider-container">
                                <div class="slider-track" id="sliderTrack">
                                    <div class="slider-progress" id="sliderProgress"></div>
                                    <div class="slider-text" id="sliderText">Deslizar para Firmar Asiento</div>
                                    <div class="slider-handle" id="sliderHandle"><i class="bi bi-chevron-right" style="font-size: 1.2rem;"></i></div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <script>
            const dashboardView = document.getElementById('dashboardView');
            const workspaceView = document.getElementById('workspaceView');
            const etiquetaModo = document.getElementById('etiquetaModo');
            
            // Lógica de Auto-Apertura
            const modoAuto = "{{ modo_auto }}";
            
            if (modoAuto !== 'ninguno') {
                // Configura la transición instantánea para saltar el lobby
                dashboardView.style.transition = 'none';
                workspaceView.style.transition = 'none';
                
                dashboardView.classList.add('view-hidden-up');
                workspaceView.style.display = 'block';
                workspaceView.classList.add('view-active');
                
                if (modoAuto === 'residencia') {
                    etiquetaModo.textContent = 'Residencia de Obra';
                    etiquetaModo.className = 'badge bg-primary py-2 px-3';
                } else {
                    etiquetaModo.textContent = 'Supervisión de Obra';
                    etiquetaModo.className = 'badge bg-success py-2 px-3';
                }
                
                // Restaura las transiciones suaves después del renderizado inicial
                setTimeout(() => {
                    dashboardView.style.transition = 'all 0.6s cubic-bezier(0.25, 1, 0.5, 1)';
                    workspaceView.style.transition = 'all 0.6s cubic-bezier(0.25, 1, 0.5, 1)';
                    calcularLimites();
                }, 100);
            }

            function abrirWorkspace(modo) {
                if (modo === 'residencia') {
                    etiquetaModo.textContent = 'Residencia de Obra';
                    etiquetaModo.className = 'badge bg-primary py-2 px-3';
                } else {
                    etiquetaModo.textContent = 'Supervisión de Obra';
                    etiquetaModo.className = 'badge bg-success py-2 px-3';
                }

                dashboardView.classList.add('view-hidden-up');
                workspaceView.style.display = 'block'; 
                
                setTimeout(() => {
                    workspaceView.classList.add('view-active');
                    calcularLimites(); 
                }, 50);
            }

            function volverDashboard() {
                // Al volver, cambiamos la URL en el navegador para no recargar en bucle
                window.history.pushState({}, '', '/cuaderno');
                
                workspaceView.classList.remove('view-active');
                setTimeout(() => {
                    workspaceView.style.display = 'none';
                    dashboardView.classList.remove('view-hidden-up');
                }, 400);
            }

            // Motor Slider iPhone
            const handle = document.getElementById('sliderHandle'), track = document.getElementById('sliderTrack');
            const progress = document.getElementById('sliderProgress'), text = document.getElementById('sliderText');
            let isDragging = false, startX = 0, maxSlide = 0;

            function calcularLimites() { maxSlide = track.clientWidth - handle.clientWidth - 8; }
            window.addEventListener('resize', calcularLimites);

            handle.addEventListener('mousedown', (e) => { isDragging = true; startX = e.clientX - handle.offsetLeft; calcularLimites(); });
            document.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                let left = e.clientX - startX;
                if (left < 4) left = 4;
                if (left > maxSlide) left = maxSlide;
                handle.style.left = left + 'px'; progress.style.width = (left + 26) + 'px';
                if (left >= maxSlide - 2) { isDragging = false; sellarAsientoLegal(); }
            });
            document.addEventListener('mouseup', () => {
                if (!isDragging) return;
                isDragging = false;
                handle.style.transition = 'left 0.3s ease'; progress.style.transition = 'width 0.3s ease';
                handle.style.left = '4px'; progress.style.width = '0px';
                setTimeout(() => { handle.style.transition = 'none'; progress.style.transition = 'none'; }, 300);
            });

            function sellarAsientoLegal() {
                handle.style.left = maxSlide + 'px'; progress.style.width = '100%'; handle.style.background = '#00875a';
                handle.innerHTML = '<i class="bi bi-check-lg" style="color:#fff;"></i>'; text.textContent = "ASIENTO FIRMADO"; text.style.color = "#00875a";
                
                setTimeout(() => {
                    alert("Documento sellado e ingresado al sistema.");
                    volverDashboard();
                    setTimeout(() => {
                        handle.style.transition = 'none'; progress.style.transition = 'none';
                        handle.style.left = '4px'; progress.style.width = '0px'; handle.style.background = '#000';
                        handle.innerHTML = '<i class="bi bi-chevron-right" style="color:#fff; font-size: 1.2rem;"></i>';
                        text.textContent = "Deslizar para Firmar Asiento"; text.style.color = "#4b5563";
                    }, 600);
                }, 600);
            }
        </script>
    </body>
    </html>
    """, estadisticas=estadisticas, historial_asientos=historial_asientos, menu_superior=menu_superior, modo_auto=modo_auto)
