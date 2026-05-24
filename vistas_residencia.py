# =========================================================
# vistas_residencia.py
# SAMU Ingeniería — Espacio de Trabajo de Residencia de Obra
# Cumple con la Directiva N° 009-2020-OSCE/CD
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar

residencia_bp = Blueprint('residencia', __name__)

@residencia_bp.route('/residencia')
def espacio_residencia():
    # Verificación de seguridad legal básica
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Samuel Gutierrez')

    # Importamos e inyectamos el menú maestro plano estilo Apple
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    # DATOS ESTADÍSTICOS DINÁMICOS (Listos para conectar con consultas SQL de base de datos)
    estadisticas = {
        "total_asientos": 45,
        "dias_lluvia": 14,
        "consultas_pendientes": 3,
        "avance_porcentaje": 38.5
    }

    # ASIENTOS DE PRUEBA PARA LA LÍNEA DE TIEMPO (Historial legal inmutable)
    historial_asientos = [
        {"numero": 45, "fecha": "22/May/2026", "tipo": "Ocurrencia", "resumen": "Se registra paralización parcial en Frente 02 por falla mecánica en Excavadora CAT 336."},
        {"numero": 44, "fecha": "21/May/2026", "tipo": "Avance Normal", "resumen": "Continuación de colocación de subbase granular entre las progresivas KM 12+400 al KM 13+100."},
        {"numero": 43, "fecha": "20/May/2026", "tipo": "Consulta Técnica", "resumen": "Se formula consulta técnica sobre la reubicación de la alcantarilla TMC en el KM 14+250."},
        {"numero": 42, "fecha": "19/May/2026", "tipo": "Avance Normal", "resumen": "Trabajos de excavación en roca fija para ensanche de plataforma en Frente 01."}
    ]

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Residencia de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Bauhaus+93&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --apple-text: #1d1d1f;
                --apple-gray: #86868b;
                --glass-bg: rgba(255, 255, 255, 0.45);
                --glass-border: rgba(255, 255, 255, 0.6);
            }

            body {
                margin: 0; font-family: 'Inter', sans-serif; background-color: #fbfbfd;
                color: var(--apple-text); overflow-x: hidden; min-height: 100vh;
            }

            /* --- CAPAS DE GRADIENTES DINÁMICOS ANIMADOS (OPACIDAD AL 20%) --- */
            .dynamic-bg { position: fixed; inset: 0; z-index: -2; overflow: hidden; background: #fbfbfd; }
            .bg-blob { position: absolute; border-radius: 50%; filter: blur(120px); pointer-events: none; }
            
            /* Azul marino profundo a un 20% de impacto */
            .blob-navy {
                width: 55vw; height: 55vw; background: #0f172a; opacity: 0.12;
                top: -10%; left: -10%; animation: movAzulMarino 22s infinite ease-in-out;
            }
            /* Rosado Apple elegante a un 20% de impacto */
            .blob-pink {
                width: 50vw; height: 50vw; background: #f9a8d4; opacity: 0.14;
                bottom: -15%; right: -10%; animation: movRosado 26s infinite ease-in-out reverse;
            }

            @keyframes movAzulMarino {
                0%, 100% { transform: translate(0, 0) scale(1); }
                50% { transform: translate(8vw, 6vh) scale(1.1); }
            }
            @keyframes movRosado {
                0%, 100% { transform: translate(0, 0) scale(1); }
                50% { transform: translate(-6vw, -8vh) scale(1.15); }
            }

            .main-container { max-width: 1200px; margin: 0 auto; padding: 90px 20px 40px 20px; }
            .project-title h1 { font-size: 32px; font-weight: 700; letter-spacing: -0.8px; margin-bottom: 4px; }
            .project-title p { color: var(--apple-gray); font-size: 16px; margin-bottom: 25px; }

            /* --- DASHBOARD DE ESTADÍSTICAS GERENCIALES --- */
            .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }
            .stat-card {
                background: var(--glass-bg); border: 1px solid var(--glass-border);
                backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                padding: 18px 20px; border-radius: 18px; transition: transform 0.3s;
            }
            .stat-card:hover { transform: translateY(-2px); }
            .stat-card label { font-size: 11px; color: var(--apple-gray); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; display: block; margin-bottom: 4px; }
            .stat-card .value { font-size: 26px; font-weight: 700; letter-spacing: -0.5px; color: #000; }

            /* --- ENTORNO DE TRABAJO DIVIDIDO (SPLIT-VIEW 30/70) --- */
            .workspace-split { display: grid; grid-template-columns: 320px 1fr; gap: 24px; align-items: start; }
            
            /* Línea de tiempo (Izquierda) */
            .timeline-wrapper {
                background: var(--glass-bg); border: 1px solid var(--glass-border);
                backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                border-radius: 24px; padding: 20px; max-height: calc(100vh - 300px); overflow-y: auto;
            }
            .timeline-title { font-size: 13px; font-weight: 700; color: var(--apple-gray); text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px; }
            .timeline-item {
                padding: 12px; border-radius: 14px; background: rgba(255,255,255,0.4);
                border: 1px solid rgba(255,255,255,0.5); cursor: pointer; transition: all 0.2s; margin-bottom: 10px;
            }
            .timeline-item:hover { background: #ffffff; border-color: #cbd5e1; }
            .timeline-header { display: flex; justify-content: space-between; font-size: 11px; font-weight: 600; margin-bottom: 4px; }
            .timeline-asiento { color: #0066cc; }
            .timeline-fecha { color: var(--apple-gray); }
            .timeline-item p { font-size: 12px; margin: 0; color: #334155; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

            /* Lienzo de Trabajo Principal (Derecha) */
            .canvas-wrapper {
                background: var(--glass-bg); border: 1px solid var(--glass-border);
                backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                border-radius: 24px; padding: 35px; min-height: 480px;
                display: flex; flex-direction: column; justify-content: center; align-items: center;
                position: relative; transition: all 0.4s ease;
            }

            /* --- BOTÓN WOW: APERTURAR ASIENTO --- */
            .btn-apertura-wow {
                background: rgba(255, 255, 255, 0.7); border: 1px solid rgba(255, 255, 255, 0.8);
                padding: 40px 60px; border-radius: 24px; font-size: 22px; font-weight: 600;
                color: #000; letter-spacing: -0.5px; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 20px rgba(0,0,0,0.02); text-align: center;
            }
            .btn-apertura-wow:hover {
                transform: scale(1.02); background: #ffffff;
                border-color: #0066cc; box-shadow: 0 15px 35px rgba(0, 102, 204, 0.08);
            }
            .btn-apertura-wow span { display: block; font-size: 13px; color: var(--apple-gray); font-weight: 400; margin-top: 8px; letter-spacing: 0px; }

            /* --- LIENZO DE REDACCIÓN FORMULARIO (OCULTO AL INICIO) --- */
            .form-lienzo { width: 100%; display: none; }
            .form-section-title { font-size: 14px; font-weight: 600; color: #000; margin-bottom: 15px; padding-bottom: 6px; border-bottom: 1px solid rgba(0,0,0,0.06); text-transform: uppercase; letter-spacing: 0.5px; }
            .form-label { font-size: 12px; font-weight: 500; color: var(--apple-gray); margin-bottom: 6px; }
            .form-select, .form-control {
                border-radius: 12px; border: 1px solid #e2e8f0; padding: 12px;
                font-size: 14px; background: rgba(255,255,255,0.7); transition: all 0.2s;
            }
            .form-select:focus, .form-control:focus {
                background: #ffffff; border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.1); outline: none;
            }

            /* --- IPHONE SLIDER PARA FIRMAR Y CERRAR --- */
            .slider-container { width: 100%; max-width: 450px; margin: 40px auto 10px auto; position: relative; }
            .slider-track {
                width: 100%; height: 56px; background: rgba(0,0,0,0.04); border: 1px solid rgba(0,0,0,0.02);
                border-radius: 28px; position: relative; display: flex; align-items: center;
                justify-content: center; overflow: hidden; user-select: none;
            }
            .slider-text { font-size: 12px; font-weight: 600; color: #4b5563; letter-spacing: 0.5px; text-transform: uppercase; pointer-events: none; z-index: 1; }
            .slider-handle {
                width: 48px; height: 48px; background: #000; color: #fff;
                border-radius: 50%; position: absolute; left: 4px; top: 3px;
                display: flex; align-items: center; justify-content: center;
                cursor: grab; z-index: 2; transition: left 0.1s ease-out;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            }
            .slider-handle:active { cursor: grabbing; background: #0066cc; }
            .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}

        <div class="dynamic-bg">
            <div class="bg-blob blob-navy"></div>
            <div class="bg-blob blob-pink"></div>
        </div>

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
                    <label>Días Impactados por Clima</label>
                    <div class="value">{{ estadisticas.dias_lluvia }} días</div>
                </div>
                <div class="stat-card">
                    <label>Consultas sin Responder</label>
                    <div class="value" style="color: #dc2626;">{{ estadisticas.consultas_pendientes }}</div>
                </div>
                <div class="stat-card">
                    <label>Avance Físico Controlado</label>
                    <div class="value">{{ estadisticas.avance_porcentaje }}%</div>
                </div>
            </div>

            <div class="workspace-split">
                
                <div class="timeline-wrapper">
                    <div class="timeline-title">Historial de Folios</div>
                    {% for asiento in historial_asientos %}
                    <div class="timeline-item" onclick="verAsientoOld({{ asiento.numero }})">
                        <div class="timeline-header">
                            <span class="timeline-asiento">Asiento N° {{ asiento.numero }}</span>
                            <span class="timeline-fecha">{{ asiento.fecha }}</span>
                        </div>
                        <p>{{ asiento.resumen }}</p>
                    </div>
                    {% endfor %}
                </div>

                <div class="canvas-wrapper" id="mainCanvas">
                    
                    <div id="wrapperBotonWow">
                        <button class="btn-apertura-wow" onclick="activarLienzoRedaccion()">
                            <i class="bi bi-file-earmark-plus-fill" style="color: #0066cc;"></i><br>
                            Aperturar Asiento N° {{ estadisticas.total_asientos + 1 }}
                            <span>Residencia de Obra &bull; Folio Legal Correlativo</span>
                        </button>
                    </div>

                    <div class="form-lienzo" id="formularioAsiento">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h3 class="m-0" style="font-weight: 600; letter-spacing: -0.5px;">Asiento N° {{ estadisticas.total_asientos + 1 }}: Residencia de Obra</h3>
                            <span class="badge bg-dark py-2 px-3" style="font-size: 12px; border-radius: 8px;">MODO: BORRADOR LEGAL</span>
                        </div>

                        <form id="formLegalObra" onsubmit="event.preventDefault();">
                            <div class="form-section-title">1. Condiciones del Entorno</div>
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <label class="form-label">Estado Climático Dominante</label>
                                    <select class="form-select" required>
                                        <option value="soleado">Soleado / Despejado</option>
                                        <option value="nublado">Nublado / Nublado Parcial</option>
                                        <option value="lluvia_ligera">Lluvia Ligera (Sin paralización)</option>
                                        <option value="lluvia_intensa">Lluvia Intensa (Genera paralización parcial)</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Impacto Operativo</label>
                                    <select class="form-select" required>
                                        <option value="normal">Trabajo Normal (100% de frentes activos)</option>
                                        <option value="parcial">Restricción Parcial de Maquinaria</option>
                                        <option value="total">Paralización Total por Fuerza Mayor</option>
                                    </select>
                                </div>
                            </div>

                            <div class="form-section-title">2. Trabajos Ejecutados y Metrados</div>
                            <div class="mb-4">
                                <label class="form-label">Descripción Técnica Detallada (Frentes, Hitos y Progresivas)</label>
                                <textarea class="form-control" rows="5" placeholder="Escriba aquí los frentes activos, metrados controlados y actividades de ingeniería del día según el formato OSCE..." required></textarea>
                            </div>

                            <div class="form-section-title" style="color: #dc2626;">3. Cierre de Asiento e Inmutabilidad</div>
                            <p style="font-size: 12px; color: var(--apple-gray); margin: 0; text-align: center;">
                                Al firmar este asiento, los datos se registrarán en el servidor de forma definitiva. Conforme a la Directiva N° 009-2020-OSCE, **no podrá ser modificado ni eliminado** bajo ninguna circunstancia.
                            </p>

                            <div class="slider-container">
                                <div class="slider-track" id="sliderTrack">
                                    <div class="slider-progress" id="sliderProgress"></div>
                                    <div class="slider-text" id="sliderText">Deslizar para Firmar Asiento</div>
                                    <div class="slider-handle" id="sliderHandle">
                                        <i class="bi bi-chevron-right" style="font-size: 1.2rem;"></i>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>

                </div>
            </div>
        </div>

        <script>
            // Transición fluida del botón WOW al Lienzo de Redacción
            function activarLienzoRedaccion() {
                const btnWow = document.getElementById('wrapperBotonWow');
                const formLienzo = document.getElementById('formularioAsiento');
                const canvas = document.getElementById('mainCanvas');

                btnWow.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                btnWow.style.opacity = '0';
                btnWow.style.transform = 'scale(0.95)';

                setTimeout(() => {
                    btnWow.style.display = 'none';
                    canvas.style.justifyContent = 'flex-start';
                    canvas.style.alignItems = 'stretch';
                    formLienzo.style.display = 'block';
                    formLienzo.style.opacity = '0';
                    formLienzo.style.transition = 'opacity 0.4s ease';
                    requestAnimationFrame(() => formLienzo.style.opacity = '1');
                }, 300);
            }

            // Simulación básica de lectura de asientos antiguos
            function verAsientoOld(num) {
                alert("Abriendo Vista de Lectura Inmutable para el Asiento N° " + num);
            }

            // --- LÓGICA MOTOR DEL SLIDER IPHONE (FIRMA DIGITAL) ---
            const handle = document.getElementById('sliderHandle');
            const track = document.getElementById('sliderTrack');
            const progress = document.getElementById('sliderProgress');
            const text = document.getElementById('sliderText');
            
            let isDragging = false;
            let startX = 0;
            let maxSlide = 0;

            function calcularLimites() {
                maxSlide = track.clientWidth - handle.clientWidth - 8; // 8px por los paddings internos
            }

            window.addEventListener('resize', calcularLimites);
            setTimeout(calcularLimites, 500);

            handle.addEventListener('mousedown', (e) => {
                isDragging = true;
                startX = e.clientX - handle.offsetLeft;
                calcularLimites();
            });

            document.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                let left = e.clientX - startX;
                
                if (left < 4) left = 4;
                if (left > maxSlide) left = maxSlide;

                handle.style.left = left + 'px';
                progress.style.width = (left + 24) + 'px';

                // Si llega al final del tramo (98% o más) sella el cuaderno
                if (left >= maxSlide - 2) {
                    isDragging = false;
                    sellarAsientoLegal();
                }
            });

            document.addEventListener('mouseup', () => {
                if (!isDragging) return;
                isDragging = false;
                // Si no llegó al final, regresa suavemente al inicio (Efecto resorte)
                handle.style.transition = 'left 0.3s ease';
                progress.style.transition = 'width 0.3s ease';
                handle.style.left = '4px';
                progress.style.width = '0px';
                setTimeout(() => {
                    handle.style.transition = 'none';
                    progress.style.transition = 'none';
                }, 300);
            });

            function sellarAsientoLegal() {
                handle.style.left = maxSlide + 'px';
                progress.style.width = '100%';
                handle.style.background = '#00875a'; // Verde éxito
                handle.innerHTML = '<i class="bi bi-check-lg" style="color:#fff;"></i>';
                text.textContent = "ASIENTO FIRMADO Y CERRADO";
                text.style.color = "#00875a";
                
                setTimeout(() => {
                    alert("¡Éxito Legal! El Asiento ha sido firmado digitalmente por el Ingeniero Samuel Gutierrez y enviado de forma inmutable al servidor SAMU.");
                    window.location.reload();
                }, 600);
            }
        </script>
    </body>
    </html>
    """, estadisticas=estadisticas, historial_asientos=historial_asientos, menu_superior=menu_superior, es_admin=es_admin)
