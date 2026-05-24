# =========================================================
# vistas_cuaderno.py
# Módulo: Cuaderno de Obra Digital - Completo y Responsivo
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for, request
from navbar import obtener_navbar

cuaderno_bp = Blueprint('cuaderno', __name__)

@cuaderno_bp.route('/cuaderno')
@cuaderno_bp.route('/residencia')
@cuaderno_bp.route('/supervision')
def panel_cuaderno():
    if 'usuario_id' not in session: 
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Visitante')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    ruta_actual = request.path
    modo_auto = 'ninguno'
    if '/residencia' in ruta_actual: 
        modo_auto = 'residencia'
    elif '/supervision' in ruta_actual: 
        modo_auto = 'supervision'

    estadisticas = { 
        "total_asientos": 87, 
        "dias_lluvia": 14, 
        "consultas_pendientes": 3, 
        "avance_porcentaje": 38.5 
    }
    
    historial_asientos = [
        {"numero": 87, "fecha": "23/May/2026", "resumen": "Paralización Frente 02 por falla en Excavadora CAT 336."}, 
        {"numero": 86, "fecha": "22/May/2026", "resumen": "Colocación de subbase granular KM 12+400."}
    ]

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Cuaderno de Obra</title>
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
            
            /* --- FONDO ANIMADO --- */
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

            /* --- TRANSICIONES DE VISTA --- */
            .view-section { 
                position: absolute; 
                top: 0; 
                left: 0; 
                width: 100%; 
                min-height: 100vh; 
                padding: 90px 20px 40px; 
                transition: all 0.5s ease; 
            }
            
            #dashboardView { 
                opacity: 1; 
                transform: scale(1); 
                z-index: 10; 
            }
            
            #workspaceView { 
                opacity: 0; 
                transform: translateY(30px) scale(0.98); 
                z-index: 5; 
                pointer-events: none; 
                display: none; 
            }
            
            .view-hidden-up { 
                opacity: 0 !important; 
                transform: translateY(-30px) scale(0.98) !important; 
                pointer-events: none; 
            }
            
            .view-active { 
                opacity: 1 !important; 
                transform: translateY(0) scale(1) !important; 
                pointer-events: auto !important; 
                display: block !important; 
                z-index: 20 !important;
            }

            /* --- CSS GRID LOBBY --- */
            .main-container { 
                max-width: 1000px; 
                margin: 0 auto; 
            }
            
            .project-title { 
                text-align: center; 
                margin-bottom: 30px; 
            }
            
            .project-title h1 { 
                font-size: 28px; 
                font-weight: 700; 
                letter-spacing: -1px; 
                margin-bottom: 4px; 
            }
            
            .project-title p { 
                color: var(--apple-gray); 
                font-size: 14px; 
                margin: 0; 
            }
            
            .stats-grid { 
                display: grid; 
                grid-template-columns: repeat(4, 1fr); 
                gap: 12px; 
                margin-bottom: 30px; 
            }
            
            .stat-card { 
                background: var(--glass-bg); 
                border: 1px solid var(--glass-border); 
                backdrop-filter: blur(15px); 
                -webkit-backdrop-filter: blur(15px); 
                padding: 15px; 
                border-radius: 16px; 
                text-align: center; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.02); 
            }
            
            .stat-card label { 
                font-size: 10px; 
                color: var(--apple-gray); 
                text-transform: uppercase; 
                font-weight: 600; 
            }
            
            .stat-card .value { 
                font-size: 24px; 
                font-weight: 700; 
                color: #000; 
                margin-top: 2px; 
            }

            .portals-grid { 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 20px; 
            }
            
            .portal-card { 
                background: rgba(255,255,255,0.7); 
                border: 1px solid rgba(255,255,255,0.9); 
                backdrop-filter: blur(20px); 
                -webkit-backdrop-filter: blur(20px); 
                border-radius: 24px; 
                padding: 40px 20px; 
                text-align: center; 
                cursor: pointer; 
                transition: transform 0.3s; 
            }
            
            .portal-card:active { 
                transform: scale(0.97); 
                background: #f8fafc; 
            } 
            
            .portal-icon { 
                font-size: 40px; 
                color: #0066cc; 
                margin-bottom: 15px; 
            }
            
            .portal-title { 
                font-size: 20px; 
                font-weight: 700; 
                margin-bottom: 8px; 
            }
            
            .portal-desc { 
                font-size: 13px; 
                color: var(--apple-gray); 
            }

            /* --- CSS GRID WORKSPACE --- */
            .workspace-container { 
                max-width: 1300px; 
                margin: 0 auto; 
            }
            
            .btn-back { 
                background: none; 
                border: none; 
                font-size: 14px; 
                font-weight: 600; 
                color: #0066cc; 
                margin-bottom: 15px; 
                padding: 0; 
                cursor: pointer; 
                display: flex; 
                align-items: center; 
                gap: 5px;
            }
            
            .workspace-split { 
                display: grid; 
                grid-template-columns: 300px 1fr; 
                gap: 20px; 
                align-items: start; 
            }
            
            .timeline-wrapper, .canvas-wrapper { 
                background: var(--glass-bg); 
                border: 1px solid var(--glass-border); 
                backdrop-filter: blur(20px); 
                -webkit-backdrop-filter: blur(20px); 
                border-radius: 20px; 
                padding: 20px; 
            }
            
            .form-section-title { 
                font-size: 12px; 
                font-weight: 700; 
                color: #000; 
                margin-bottom: 12px; 
                padding-bottom: 6px; 
                border-bottom: 1px solid rgba(0,0,0,0.08); 
                text-transform: uppercase; 
                margin-top: 20px;
            }
            
            .form-label { 
                font-size: 12px; 
                font-weight: 600; 
                color: var(--apple-gray); 
                margin-bottom: 6px; 
            }
            
            .form-select, .form-control { 
                border-radius: 12px; 
                padding: 12px; 
                font-size: 14px; 
                background: rgba(255,255,255,0.8); 
                border: 1px solid #e2e8f0; 
            }

            /* --- SLIDER RESPONSIVO --- */
            .slider-container { 
                width: 100%; 
                margin: 30px auto 10px auto; 
                position: relative; 
            }
            
            .slider-track { 
                width: 100%; 
                height: 56px; 
                background: rgba(0,0,0,0.04); 
                border-radius: 30px; 
                position: relative; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                overflow: hidden; 
                user-select: none; 
                touch-action: none; 
            }
            
            .slider-text { 
                font-size: 12px; 
                font-weight: 600; 
                color: #4b5563; 
                text-transform: uppercase; 
                pointer-events: none; 
                z-index: 1; 
            }
            
            .slider-handle { 
                width: 48px; 
                height: 48px; 
                background: #000; 
                color: #fff; 
                border-radius: 50%; 
                position: absolute; 
                left: 4px; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                cursor: grab; 
                z-index: 2; 
                touch-action: none; 
            }
            
            .slider-progress { 
                position: absolute; 
                left: 0; 
                top: 0; 
                height: 100%; 
                background: rgba(0, 102, 204, 0.1); 
                width: 0; 
                pointer-events: none; 
            }

            /* --- MEDIA QUERIES (MAGIA MÓVIL) --- */
            @media (max-width: 991px) { 
                .stats-grid { grid-template-columns: repeat(2, 1fr); }
                .workspace-split { grid-template-columns: 1fr; }
                .timeline-wrapper { max-height: 200px; order: 2; overflow-y: auto;} 
                .canvas-wrapper { order: 1; } 
            }
            
            @media (max-width: 576px) { 
                .view-section { padding: 80px 15px 30px; }
                .portals-grid { grid-template-columns: 1fr; } 
                .stats-grid { grid-template-columns: 1fr 1fr; }
                .project-title h1 { font-size: 24px; }
                .portal-card { padding: 30px 20px; }
                .slider-text { font-size: 10px; } 
            }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}
        
        <div class="dynamic-bg">
            <div class="bg-blob blob-navy"></div>
            <div class="bg-blob blob-pink"></div>
        </div>

        <div class="view-section" id="dashboardView">
            <div class="main-container">
                <div class="project-title">
                    <h1>Carretera PU N-110</h1>
                    <p>Cuaderno de Obra Digital</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <label>Asientos</label>
                        <div class="value">{{ estadisticas.total_asientos }}</div>
                    </div>
                    <div class="stat-card">
                        <label>Días Lluvia</label>
                        <div class="value">{{ estadisticas.dias_lluvia }}</div>
                    </div>
                    <div class="stat-card">
                        <label>Consultas</label>
                        <div class="value" style="color: #dc2626;">{{ estadisticas.consultas_pendientes }}</div>
                    </div>
                    <div class="stat-card">
                        <label>Avance</label>
                        <div class="value">{{ estadisticas.avance_porcentaje }}%</div>
                    </div>
                </div>
                
                <div class="portals-grid">
                    <div class="portal-card" onclick="abrirWorkspace('residencia')">
                        <div class="portal-icon"><i class="bi bi-journal-richtext"></i></div>
                        <div class="portal-title">Residencia</div>
                        <div class="portal-desc">Aperturar asientos legales diarios.</div>
                    </div>
                    <div class="portal-card" onclick="abrirWorkspace('supervision')">
                        <div class="portal-icon"><i class="bi bi-shield-check"></i></div>
                        <div class="portal-title">Supervisión</div>
                        <div class="portal-desc">Control y absolución de consultas.</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="view-section" id="workspaceView">
            <div class="workspace-container">
                <button class="btn-back" onclick="volverDashboard()">
                    <i class="bi bi-arrow-left"></i> Volver al Menú
                </button>

                <div class="workspace-split">
                    <div class="timeline-wrapper">
                        <div class="timeline-title">Historial Rápido</div>
                        {% for asiento in historial_asientos %}
                        <div class="timeline-item">
                            <strong>N° {{ asiento.numero }} - {{ asiento.fecha }}</strong>
                            <p>{{ asiento.resumen }}</p>
                        </div>
                        {% endfor %}
                    </div>

                    <div class="canvas-wrapper">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h3 class="m-0" style="font-weight: 700; font-size: 1.2rem;">Asiento N° {{ estadisticas.total_asientos + 1 }}</h3>
                            <span class="badge bg-dark py-2 px-3" style="font-size: 11px;" id="etiquetaModo">Residencia</span>
                        </div>
                        
                        <form id="formLegalObra" onsubmit="event.preventDefault();">
                            <div class="form-section-title">1. Clima y Operatividad</div>
                            <div class="row g-2 mb-3"> 
                                <div class="col-sm-6">
                                    <select class="form-select" required>
                                        <option value="soleado">Soleado / Despejado</option>
                                        <option value="lluvia">Lluvia Intensa</option>
                                    </select>
                                </div>
                                <div class="col-sm-6">
                                    <select class="form-select" required>
                                        <option value="normal">Trabajo Normal (100%)</option>
                                        <option value="parcial">Paralización Parcial</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="form-section-title">2. Trabajos y Metrados</div>
                            <div class="mb-3">
                                <textarea class="form-control" rows="4" placeholder="Progresivas, frentes activos..." required></textarea>
                            </div>

                            <div class="slider-container">
                                <div class="slider-track" id="sliderTrack">
                                    <div class="slider-progress" id="sliderProgress"></div>
                                    <div class="slider-text" id="sliderText">Deslizar para Firmar</div>
                                    <div class="slider-handle" id="sliderHandle"><i class="bi bi-chevron-right"></i></div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // --- LÓGICA DE AUTO-APERTURA ---
            const dashboardView = document.getElementById('dashboardView');
            const workspaceView = document.getElementById('workspaceView');
            const etiquetaModo = document.getElementById('etiquetaModo');
            const modoAuto = "{{ modo_auto }}";
            
            if (modoAuto !== 'ninguno') {
                dashboardView.style.transition = 'none'; 
                workspaceView.style.transition = 'none';
                dashboardView.classList.add('view-hidden-up'); 
                workspaceView.style.display = 'block'; 
                workspaceView.classList.add('view-active');
                
                etiquetaModo.textContent = modoAuto === 'residencia' ? 'Residencia de Obra' : 'Supervisión de Obra';
                etiquetaModo.className = modoAuto === 'residencia' ? 'badge bg-primary py-2 px-3' : 'badge bg-success py-2 px-3';
                
                setTimeout(() => { 
                    dashboardView.style.transition = 'all 0.5s ease'; 
                    workspaceView.style.transition = 'all 0.5s ease'; 
                    calcularLimites(); 
                }, 100);
            }

            function abrirWorkspace(modo) {
                etiquetaModo.textContent = modo === 'residencia' ? 'Residencia de Obra' : 'Supervisión de Obra';
                etiquetaModo.className = modo === 'residencia' ? 'badge bg-primary py-2 px-3' : 'badge bg-success py-2 px-3';
                dashboardView.classList.add('view-hidden-up'); 
                workspaceView.style.display = 'block'; 
                
                setTimeout(() => { 
                    workspaceView.classList.add('view-active'); 
                    window.scrollTo(0, 0); 
                    calcularLimites(); 
                }, 50);
            }

            function volverDashboard() {
                window.history.pushState({}, '', '/cuaderno');
                workspaceView.classList.remove('view-active');
                setTimeout(() => { 
                    workspaceView.style.display = 'none'; 
                    dashboardView.classList.remove('view-hidden-up'); 
                    window.scrollTo(0, 0); 
                }, 400);
            }

            // --- LÓGICA DEL SLIDER (MOUSE + TÁCTIL) ---
            const handle = document.getElementById('sliderHandle');
            const track = document.getElementById('sliderTrack');
            const progress = document.getElementById('sliderProgress');
            const text = document.getElementById('sliderText');
            
            let isDragging = false, startX = 0, maxSlide = 0;

            function calcularLimites() { 
                maxSlide = track.clientWidth - handle.clientWidth - 8; 
            }
            window.addEventListener('resize', calcularLimites);

            function startDrag(clientX) { 
                isDragging = true; 
                startX = clientX - handle.offsetLeft; 
                calcularLimites(); 
            }
            
            function onDrag(clientX) {
                if (!isDragging) return;
                let left = clientX - startX;
                if (left < 4) left = 4; 
                if (left > maxSlide) left = maxSlide;
                
                handle.style.left = left + 'px'; 
                progress.style.width = (left + 26) + 'px';
                
                if (left >= maxSlide - 2) { 
                    isDragging = false; 
                    sellar(); 
                }
            }
            
            function stopDrag() {
                if (!isDragging) return; 
                isDragging = false;
                handle.style.transition = 'left 0.3s ease'; 
                progress.style.transition = 'width 0.3s ease';
                handle.style.left = '4px'; 
                progress.style.width = '0px';
                
                setTimeout(() => { 
                    handle.style.transition = 'none'; 
                    progress.style.transition = 'none'; 
                }, 300);
            }

            // Eventos Desktop
            handle.addEventListener('mousedown', (e) => startDrag(e.clientX));
            document.addEventListener('mousemove', (e) => onDrag(e.clientX));
            document.addEventListener('mouseup', stopDrag);
            
            // Eventos Celular
            handle.addEventListener('touchstart', (e) => startDrag(e.touches[0].clientX), {passive: true});
            document.addEventListener('touchmove', (e) => { 
                if(isDragging) onDrag(e.touches[0].clientX); 
            }, {passive: false});
            document.addEventListener('touchend', stopDrag);

            function sellar() {
                handle.style.left = maxSlide + 'px'; 
                progress.style.width = '100%'; 
                handle.style.background = '#00875a';
                handle.innerHTML = '<i class="bi bi-check-lg" style="color:#fff;"></i>'; 
                text.textContent = "FIRMADO"; 
                text.style.color = "#00875a";
                
                setTimeout(() => {
                    alert("Documento sellado e ingresado."); 
                    volverDashboard();
                    setTimeout(() => {
                        handle.style.transition = 'none'; 
                        progress.style.transition = 'none'; 
                        handle.style.left = '4px'; 
                        progress.style.width = '0px'; 
                        handle.style.background = '#000';
                        handle.innerHTML = '<i class="bi bi-chevron-right" style="color:#fff;"></i>'; 
                        text.textContent = "Deslizar para Firmar"; 
                        text.style.color = "#4b5563";
                    }, 600);
                }, 600);
            }
        </script>
    </body>
    </html>
    """, estadisticas=estadisticas, historial_asientos=historial_asientos, menu_superior=menu_superior, modo_auto=modo_auto)
