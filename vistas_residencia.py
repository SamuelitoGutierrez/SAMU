# =========================================================
# vistas_residencia.py
# Módulo: Llenado Extenso del Cuaderno de Residencia
# 100% Responsivo y Estructurado Legalmente
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

@residencia_bp.route('/residencia')
def redactar_asiento():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Visitante')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    # Datos simulados de contexto de obra
    numero_asiento = 88
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    
    historial_asientos = [
        {"numero": 87, "fecha": "23/May/2026", "resumen": "Paralización Frente 02 por falla en Excavadora CAT 336."},
        {"numero": 86, "fecha": "22/May/2026", "resumen": "Colocación de subbase granular KM 12+400."}
    ]

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Asiento de Residencia</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
            :root { 
                --apple-text: #1d1d1f; 
                --apple-gray: #86868b; 
                --glass-bg: rgba(255, 255, 255, 0.7); 
                --glass-border: rgba(255, 255, 255, 0.9); 
            }
            body { margin: 0; font-family: 'Inter', sans-serif; background-color: #fbfbfd; color: var(--apple-text); min-height: 100vh; overflow-x: hidden; }
            
            /* Fondo Animado sutil */
            .dynamic-bg { position: fixed; inset: 0; z-index: -2; background: #fbfbfd; overflow: hidden; }
            .bg-blob { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; }
            .blob-navy { width: 60vw; height: 60vw; background: #0f172a; opacity: 0.12; top: -10%; left: -10%; animation: movAzul 22s infinite alternate; }
            .blob-pink { width: 60vw; height: 60vw; background: #f9a8d4; opacity: 0.12; bottom: -10%; right: -10%; animation: movRosa 26s infinite alternate; }
            @keyframes movAzul { 100% { transform: translate(10vw,10vh) scale(1.1); } }
            @keyframes movRosa { 100% { transform: translate(-10vw,-10vh) scale(1.1); } }

            /* Contenedor Principal */
            .workspace-container { max-width: 1300px; margin: 0 auto; padding: 100px 20px 40px; }
            
            .header-obra { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 25px; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 15px;}
            .btn-back { background: none; border: none; font-size: 14px; font-weight: 600; color: #0066cc; padding: 0; cursor: pointer; display: flex; align-items: center; gap: 6px; text-decoration: none;}
            .btn-back:hover { text-decoration: underline; }
            .header-title h1 { font-size: 26px; font-weight: 700; margin: 0; letter-spacing: -0.5px;}
            .header-title p { margin: 0; font-size: 13px; color: var(--apple-gray); font-weight: 500;}

            /* Split View */
            .workspace-split { display: grid; grid-template-columns: 280px 1fr; gap: 24px; align-items: start; }
            
            /* Lado Izquierdo: Historial */
            .timeline-wrapper { background: var(--glass-bg); border: 1px solid var(--glass-border); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border-radius: 20px; padding: 20px; max-height: calc(100vh - 150px); overflow-y: auto; position: sticky; top: 90px;}
            .timeline-title { font-size: 11px; font-weight: 700; color: var(--apple-gray); text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;}
            .timeline-item { background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.8); padding: 12px; border-radius: 12px; margin-bottom: 10px; cursor: pointer; transition: 0.2s; }
            .timeline-item:hover { background: #fff; border-color: #cbd5e1; }
            .timeline-item strong { color: #0066cc; display: block; font-size: 12px; margin-bottom: 4px; }
            .timeline-item p { font-size: 11px; color: #475569; margin: 0; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

            /* Lado Derecho: Formulario Legal Extenso */
            .canvas-wrapper { background: var(--glass-bg); border: 1px solid var(--glass-border); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border-radius: 20px; padding: 35px; box-shadow: 0 10px 40px rgba(0,0,0,0.03); }
            
            .form-section { margin-bottom: 35px; }
            .form-section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 2px solid rgba(0,102,204,0.1); }
            .section-number { background: #0066cc; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; }
            .section-title { font-size: 15px; font-weight: 700; color: #1d1d1f; margin: 0; }
            
            .form-label { font-size: 12px; font-weight: 600; color: #475569; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.3px;}
            .form-control, .form-select { border-radius: 12px; padding: 12px 15px; font-size: 14px; background: rgba(255,255,255,0.9); border: 1px solid #cbd5e1; transition: all 0.2s; color: #1d1d1f;}
            .form-control:focus, .form-select:focus { background: #ffffff; border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.1); outline: none; }
            
            /* Cajas de agrupación interna */
            .sub-box { background: rgba(248, 250, 252, 0.6); border: 1px solid #e2e8f0; border-radius: 14px; padding: 15px; margin-bottom: 15px; }

            /* Slider de Firma (Responsivo) */
            .slider-container { width: 100%; max-width: 450px; margin: 40px auto 10px auto; position: relative; }
            .slider-track { width: 100%; height: 60px; background: rgba(0,0,0,0.04); border-radius: 30px; border: 1px solid rgba(0,0,0,0.05); position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; user-select: none; touch-action: none; }
            .slider-text { font-size: 13px; font-weight: 600; color: #4b5563; text-transform: uppercase; pointer-events: none; z-index: 1; letter-spacing: 0.5px;}
            .slider-handle { width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; cursor: grab; z-index: 2; touch-action: none; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }

            /* ========================================================
               📱 ADAPTACIÓN PARA CELULARES Y TABLETS
               ======================================================== */
            @media (max-width: 991px) {
                .workspace-split { grid-template-columns: 1fr; }
                .timeline-wrapper { position: relative; top: 0; max-height: 250px; order: 2; } /* Historial pasa al final */
                .canvas-wrapper { order: 1; padding: 25px 20px; } /* Formulario arriba */
            }
            @media (max-width: 576px) {
                .workspace-container { padding: 80px 15px 30px; }
                .header-obra { flex-direction: column; align-items: flex-start; gap: 15px; }
                .header-title h1 { font-size: 22px; }
                .form-section-header { margin-bottom: 10px; }
                .slider-text { font-size: 10px; }
                .sub-box { padding: 12px; }
            }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}
        
        <div class="dynamic-bg">
            <div class="bg-blob blob-navy"></div>
            <div class="bg-blob blob-pink"></div>
        </div>

        <div class="workspace-container">
            <div class="header-obra">
                <div>
                    <a href="/cuaderno" class="btn-back"><i class="bi bi-arrow-left"></i> Volver al Lobby Central</a>
                    <div class="header-title mt-3">
                        <h1>Apertura de Asiento de Obra</h1>
                        <p>Documento de carácter legal y técnico &bull; PU N-110</p>
                    </div>
                </div>
                <div class="text-end d-none d-sm-block">
                    <span class="badge bg-primary py-2 px-3" style="font-size: 13px; border-radius: 10px;">Perfil: Residencia</span>
                </div>
            </div>

            <div class="workspace-split">
                <div class="timeline-wrapper">
                    <div class="timeline-title">Últimos Folios Registrados</div>
                    {% for asiento in historial_asientos %}
                    <div class="timeline-item">
                        <strong>N° {{ asiento.numero }} - {{ asiento.fecha }}</strong>
                        <p>{{ asiento.resumen }}</p>
                    </div>
                    {% endfor %}
                </div>

                <div class="canvas-wrapper">
                    <div class="d-flex justify-content-between align-items-center mb-4 pb-3" style="border-bottom: 1px dashed #cbd5e1;">
                        <h2 class="m-0" style="font-weight: 700; color: #0066cc;">Asiento N° {{ numero_asiento }}</h2>
                        <h5 class="m-0" style="color: var(--apple-gray); font-weight: 500;">Fecha: {{ fecha_hoy }}</h5>
                    </div>
                    
                    <form id="formResidencia" onsubmit="event.preventDefault();">
                        
                        <div class="form-section">
                            <div class="form-section-header">
                                <div class="section-number">1</div><h3 class="section-title">Condiciones Climáticas</h3>
                            </div>
                            <div class="sub-box row g-3">
                                <div class="col-md-4 col-sm-6">
                                    <label class="form-label">Mañana (07:00 - 12:00)</label>
                                    <select class="form-select"><option>Soleado</option><option>Nublado</option><option>Lluvia</option></select>
                                </div>
                                <div class="col-md-4 col-sm-6">
                                    <label class="form-label">Tarde (13:00 - 18:00)</label>
                                    <select class="form-select"><option>Soleado</option><option>Nublado</option><option>Lluvia</option></select>
                                </div>
                                <div class="col-md-4 col-sm-12">
                                    <label class="form-label">Impacto Operativo</label>
                                    <select class="form-select"><option>Trabajo Normal</option><option>Paralización Parcial</option><option>Paralización Total</option></select>
                                </div>
                            </div>
                        </div>

                        <div class="form-section">
                            <div class="form-section-header">
                                <div class="section-number">2</div><h3 class="section-title">Personal del Contratista</h3>
                            </div>
                            <div class="sub-box row g-3">
                                <div class="col-4"><label class="form-label">Técnicos</label><input type="number" class="form-control" placeholder="Cant."></div>
                                <div class="col-4"><label class="form-label">Oficiales</label><input type="number" class="form-control" placeholder="Cant."></div>
                                <div class="col-4"><label class="form-label">Peones</label><input type="number" class="form-control" placeholder="Cant."></div>
                                <div class="col-12">
                                    <label class="form-label">Personal Clave Presente</label>
                                    <input type="text" class="form-control" placeholder="Ej: Residente, Especialista en Suelos, Especialista de Seguridad...">
                                </div>
                            </div>
                        </div>

                        <div class="form-section">
                            <div class="form-section-header">
                                <div class="section-number">3</div><h3 class="section-title">Equipo Mecánico Mayor</h3>
                            </div>
                            <div class="sub-box">
                                <label class="form-label">Relación de Maquinaria Operativa / Inoperativa</label>
                                <textarea class="form-control" rows="3" placeholder="Ej: 02 Excavadoras (01 operativa, 01 en mantenimiento), 04 Volquetes operativos..."></textarea>
                            </div>
                        </div>

                        <div class="form-section">
                            <div class="form-section-header">
                                <div class="section-number">4</div><h3 class="section-title">Ejecución y Metrados</h3>
                            </div>
                            <div class="sub-box">
                                <label class="form-label">Descripción de Partidas Ejecutadas (Indicar Progresivas)</label>
                                <textarea class="form-control" rows="5" placeholder="Detalle las actividades realizadas en los distintos frentes de trabajo, metrados aproximados y progresivas de la vía PU N-110..."></textarea>
                            </div>
                        </div>

                        <div class="form-section" style="margin-bottom: 10px;">
                            <div class="form-section-header">
                                <div class="section-number" style="background:#dc2626;">5</div><h3 class="section-title text-danger">Ocurrencias y Requerimientos</h3>
                            </div>
                            <div class="sub-box" style="border-color: rgba(220, 38, 38, 0.2); background: rgba(254, 242, 242, 0.4);">
                                <label class="form-label" style="color: #dc2626;">Consultas, Atrasos, Solicitudes a Supervisión</label>
                                <textarea class="form-control" rows="6" placeholder="Redacte aquí cualquier ocurrencia relevante, problemas con el terreno, solicitudes de RFI, justificación de paralizaciones..."></textarea>
                            </div>
                        </div>

                        <div class="text-center mt-4">
                            <p style="font-size: 12px; color: var(--apple-gray); margin-bottom: 5px;">Al deslizar, el asiento se guardará con la firma digital de <b>{{ nombre_completo }}</b>.</p>
                            <p style="font-size: 11px; color: #dc2626; font-weight: 600;">Este documento es legal e inmodificable.</p>
                            
                            <div class="slider-container">
                                <div class="slider-track" id="sliderTrack">
                                    <div class="slider-progress" id="sliderProgress"></div>
                                    <div class="slider-text" id="sliderText">Deslizar para Cerrar Asiento</div>
                                    <div class="slider-handle" id="sliderHandle"><i class="bi bi-chevron-right" style="font-size: 1.2rem;"></i></div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script>
            // --- MOTOR DEL SLIDER (SOPORTE TÁCTIL Y MOUSE) ---
            const handle = document.getElementById('sliderHandle');
            const track = document.getElementById('sliderTrack');
            const progress = document.getElementById('sliderProgress');
            const text = document.getElementById('sliderText');
            
            let isDragging = false, startX = 0, maxSlide = 0;

            function calcularLimites() { maxSlide = track.clientWidth - handle.clientWidth - 8; }
            window.addEventListener('resize', calcularLimites);
            setTimeout(calcularLimites, 300); // Precálculo al cargar

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
                
                // Disparo al llegar al final
                if (left >= maxSlide - 2) { 
                    isDragging = false; 
                    sellarResidencia(); 
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

            // Mouse
            handle.addEventListener('mousedown', (e) => startDrag(e.clientX));
            document.addEventListener('mousemove', (e) => onDrag(e.clientX));
            document.addEventListener('mouseup', stopDrag);
            
            // Touch (Celulares)
            handle.addEventListener('touchstart', (e) => startDrag(e.touches[0].clientX), {passive: true});
            document.addEventListener('touchmove', (e) => { 
                if(isDragging) onDrag(e.touches[0].clientX); 
            }, {passive: false});
            document.addEventListener('touchend', stopDrag);

            function sellarResidencia() {
                handle.style.left = maxSlide + 'px'; 
                progress.style.width = '100%'; 
                handle.style.background = '#00875a';
                handle.innerHTML = '<i class="bi bi-check-lg" style="color:#fff;"></i>'; 
                text.textContent = "ASIENTO FIRMADO"; 
                text.style.color = "#00875a";
                
                setTimeout(() => {
                    alert("Asiento de Residencia firmado y guardado exitosamente."); 
                    window.location.href = '/cuaderno'; // Regresa al lobby
                }, 800);
            }
        </script>
    </body>
    </html>
    """, historial_asientos=historial_asientos, menu_superior=menu_superior, numero_asiento=numero_asiento, fecha_hoy=fecha_hoy, nombre_completo=nombre_completo)
