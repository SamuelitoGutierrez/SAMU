# =========================================================
# vistas_residencia.py
# Módulo: Sistema de Llenado Técnico-Legal de Residencia
# Ecosistema: SAMU
# Proyecto: Carretera PU N-110: Asiruni — Rosaspata — Huayrapata
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for, request
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    # Seguridad de acceso
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    # Datos base del folio actual (Asiento Par para Residente)
    numero_asiento = 88
    # Configurar formato de fecha en español local: "Domingo, 24/05/2026"
    dias_semana = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    fecha_dt = datetime.now()
    nombre_dia = dias_semana[int(fecha_dt.strftime("%w"))]
    fecha_formateada = f"{nombre_dia}, {fecha_dt.strftime('%d/%m/%Y')}"

    # Catálogo base de partidas precargadas para el buscador inteligente (PU N-110)
    catalogo_partidas = [
        {"codigo": "02.01", "descripcion": "Excavación no clasificada para explanaciones (Roca Suelta)"},
        {"codigo": "02.02", "descripcion": "Excavación no clasificada para explanaciones (Roca Fija)"},
        {"codigo": "02.03", "descripcion": "Perfilado y compactación en zonas de corte"},
        {"codigo": "03.01", "descripcion": "Conformación de subbase granular (E=0.20 m)"},
        {"codigo": "03.02", "descripcion": "Conformación de base granular (E=0.20 m)"},
        {"codigo": "04.01", "descripcion": "Imprimación asfáltica con MC-30"},
        {"codigo": "05.01", "descripcion": "Concreto fc=175 kg/cm2 para cunetas revestidas"},
        {"codigo": "05.02", "descripcion": "Excavación estructural para alcantarillas TMC 36\""}
    ]

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Asiento de Residencia N° {{ numero_asiento }}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
            :root { 
                --apple-text: #1d1d1f; 
                --apple-gray: #86868b; 
                --glass-bg: rgba(255, 255, 255, 0.65); 
                --glass-border: rgba(255, 255, 255, 0.85); 
            }
            body { margin: 0; font-family: 'Inter', sans-serif; background-color: #fbfbfd; color: var(--apple-text); min-height: 100vh; overflow-x: hidden; }
            
            /* --- FONDO ANIMADO --- */
            .dynamic-bg { position: fixed; inset: 0; z-index: -2; background: #fbfbfd; overflow: hidden; }
            .bg-blob { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; }
            .blob-navy { width: 60vw; height: 60vw; background: #0f172a; opacity: 0.12; top: -10%; left: -10%; animation: movAzul 22s infinite alternate; }
            .blob-pink { width: 60vw; height: 60vw; background: #f9a8d4; opacity: 0.12; bottom: -10%; right: -10%; animation: movRosa 26s infinite alternate; }
            @keyframes movAzul { 100% { transform: translate(10vw,10vh) scale(1.1); } }
            @keyframes movRosa { 100% { transform: translate(-10vw,-10vh) scale(1.1); } }

            .main-container { max-width: 1100px; margin: 0 auto; padding: 100px 15px 60px; }
            
            /* --- ACORDEONES PREMIUM STYLE APPLE --- */
            .accordion-item-samu {
                background: var(--glass-bg);
                border: 1px solid var(--glass-border);
                backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
                border-radius: 18px; margin-bottom: 14px; overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.01); transition: all 0.3s ease;
            }
            .accordion-item-samu:hover { box-shadow: 0 8px 25px rgba(0,0,0,0.03); border-color: #cbd5e1; }
            
            .accordion-header-samu {
                padding: 18px 24px; display: flex; justify-content: space-between; align-items: center;
                cursor: pointer; user-select: none; background: rgba(255,255,255,0.2);
            }
            .accordion-header-samu h4 { font-size: 14px; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 10px; }
            .accordion-header-samu .icon-chevron { transition: transform 0.3s ease; font-size: 1.1rem; color: var(--apple-gray); }
            
            .accordion-body-samu {
                padding: 24px; border-top: 1px solid rgba(0,0,0,0.04); display: none; background: rgba(255,255,255,0.3);
            }
            .accordion-item-samu.active .accordion-body-samu { display: block; }
            .accordion-item-samu.active .icon-chevron { transform: rotate(180deg); color: #0066cc; }

            /* Elementos de Formulario */
            .form-label { font-size: 11px; font-weight: 700; color: #4b5563; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.3px; }
            .form-control, .form-select { border-radius: 12px; padding: 11px 14px; font-size: 14px; background: rgba(255,255,255,0.8); border: 1px solid #cbd5e1; color: #000; font-weight: 500;}
            .form-control:focus, .form-select:focus { background: #ffffff; border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.1); outline: none; }
            
            .sub-card { background: rgba(255,255,255,0.4); border: 1px solid rgba(0,0,0,0.06); border-radius: 14px; padding: 16px; margin-bottom: 12px; }
            
            /* Switches y Estados */
            .form-switch .form-check-input { width: 42px; height: 22px; cursor: pointer; }
            
            /* Barra de Control Fija Inferior */
            .control-bar-fixed {
                position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.85);
                backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                border-top: 1px solid rgba(0,0,0,0.08); z-index: 900; padding: 12px 20px;
                display: flex; justify-content: space-between; align-items: center;
            }

            /* Excel-Like Modal styling */
            .excel-table { width: 100%; border-collapse: collapse; margin-top: 10px; background: white; }
            .excel-table th { background: #f1f5f9; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 8px; border: 1px solid #cbd5e1; text-align: center;}
            .excel-table td { border: 1px solid #cbd5e1; padding: 4px; }
            .excel-input { width: 100%; border: none; padding: 6px; font-size: 13px; font-weight: 500;}
            .excel-input:focus { outline: 2px solid #0066cc; border-radius: 2px; }

            /* Slider de Firma */
            .slider-container { width: 100%; max-width: 380px; margin: 15px auto; position: relative; }
            .slider-track { width: 100%; height: 54px; background: rgba(0,0,0,0.05); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; user-select: none; touch-action: none; }
            .slider-text { font-size: 11px; font-weight: 700; color: #374151; text-transform: uppercase; pointer-events: none; z-index: 1; letter-spacing: 0.5px;}
            .slider-handle { width: 46px; height: 46px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; cursor: grab; z-index: 2; touch-action: none; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
            .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.12); width: 0; pointer-events: none; }

            /* Vista de Copiado a mano */
            #printViewArea { display: none; background: white; color: black; padding: 40px; font-family: 'Courier New', Courier, monospace; line-height: 1.6; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }

            @media (max-width: 768px) {
                .main-container { padding-top: 80px; padding-bottom: 100px; }
                .accordion-header-samu { padding: 14px 16px; }
                .accordion-body-samu { padding: 16px 12px; }
                .control-bar-fixed { flex-direction: column; gap: 10px; text-align: center; }
            }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}
        
        <div class="dynamic-bg"><div class="bg-blob blob-navy"></div><div class="bg-blob blob-pink"></div></div>

        <div class="main-container">
            
            <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
                <div>
                    <h2 class="m-0" style="font-weight: 700; letter-spacing: -0.5px;">Asiento N° {{ numero_asiento }}: Residente</h2>
                    <p class="m-0 text-muted" style="font-size:13px;"><i class="bi bi-calendar3 me-1"></i> {{ fecha_formateada }}</p>
                </div>
                
                <div class="d-flex align-items-center gap-2">
                    <div class="bg-white border rounded-pill px-3 py-2 d-flex align-items-center gap-2 shadow-sm">
                        <span class="form-label m-0" style="font-size:10px;">Estado Libro Físico:</span>
                        <div class="form-check form-switch m-0 d-flex align-items-center">
                            <input class="form-check-input" type="checkbox" id="switchTranscrito" onchange="actualizarSemaforoFisico()">
                            <span class="badge ms-2" id="badgeFisico" style="font-size:11px; border-radius:20px;">Pendiente</span>
                        </div>
                    </div>
                    
                    <div id="areaModoDios"></div>
                </div>
            </div>

            <div id="formInteractiveArea">
                <form id="megaFormResidencia" onsubmit="event.preventDefault();">
                    
                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-clock-history color-primary"></i> 1. Jornal de Trabajo</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <div class="row g-3">
                                <div class="col-sm-6">
                                    <label class="form-label">Turno Mañana</label>
                                    <input type="text" class="form-control" id="jornal_manana" value="07:00 - 12:00">
                                </div>
                                <div class="col-sm-6">
                                    <label class="form-label">Turno Tarde</label>
                                    <input type="text" class="form-control" id="jornal_tarde" value="13:00 - 17:00">
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-people-fill"></i> 2. Personal de Obra</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <h5 class="form-label text-primary border-bottom pb-1 mb-3">Personal de Gastos Generales</h5>
                            <div class="sub-card">
                                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                                    <span class="fw-semibold" style="font-size:13px;">Ing. Samuel Tanner Gutierrez Mamani (Residente de Obra)</span>
                                    <div class="form-check form-switch"><input class="form-check-input check-asistencia" type="checkbox" checked></div>
                                </div>
                                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                                    <span class="fw-semibold" style="font-size:13px;">Ing. Especialista en Mecánica de Suelos</span>
                                    <div class="form-check form-switch"><input class="form-check-input check-asistencia" type="checkbox" checked></div>
                                </div>
                                <div class="d-flex justify-content-between align-items-center py-2">
                                    <span class="fw-semibold" style="font-size:13px;">Topógrafo de Frente Central</span>
                                    <div class="form-check form-switch"><input class="form-check-input check-asistencia" type="checkbox" checked></div>
                                </div>
                            </div>
                            
                            <h5 class="form-label text-primary border-bottom pb-1 mt-4 mb-3">Personal de Costo Directo (Según Tareo)</h5>
                            <div class="row g-2">
                                <div class="col-6 col-md-4"><label class="form-label">Operarios</label><input type="number" class="form-control" id="cant_operarios" value="0"></div>
                                <div class="col-6 col-md-4"><label class="form-label">Oficiales</label><input type="number" class="form-control" id="cant_oficiales" value="0"></div>
                                <div class="col-6 col-md-4"><label class="form-label">Peones</label><input type="number" class="form-control" id="cant_peones" value="0"></div>
                                <div class="col-6 col-md-4"><label class="form-label">Mecánicos</label><input type="number" class="form-control" id="cant_mecanicos" value="0"></div>
                                <div class="col-6 col-md-4"><label class="form-label">Controladores</label><input type="number" class="form-control" id="cant_controladores" value="0"></div>
                                <div class="col-6 col-md-4"><label class="form-label">Operadores Maq.</label><input type="number" class="form-control" id="cant_operadores" value="0"></div>
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-hammer"></i> 3. Partidas Ejecutadas</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <p class="text-muted small mb-3">Busque y añada las partidas ejecutadas en la jornada de hoy de la vía PU N-110.</p>
                            <div class="d-flex gap-2 mb-3">
                                <input type="text" class="form-control" id="buscadorPartidas" placeholder="Escriba palabra clave (ej. Excavación, Subbase)..." oninput="filtrarCatalogo()">
                                <button type="button" class="btn btn-dark btn-sm rounded-3 px-3" onclick="agregarFilaPartida('tablaPartidas3')"><i class="bi bi-plus-lg"></i></button>
                            </div>
                            <div id="listaSugerencias" class="list-group shadow-sm position-absolute" style="z-index:100; max-width:500px; display:none;"></div>
                            
                            <table class="excel-table" id="tablaPartidas3">
                                <thead><tr><th style="width:100px;">Código</th><th>Descripción de Partida</th><th style="width:120px;">Metrado</th><th style="width:50px;">Acción</th></tr></thead>
                                <tbody></tbody>
                            </table>
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-graph-up-arrow"></i> 4. Partidas de Mayor Metrado</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <button type="button" class="btn btn-outline-secondary btn-sm mb-3" onclick="agregarFilaPartida('tablaPartidas4')"><i class="bi bi-plus-lg me-1"></i> Añadir Mayor Metrado</button>
                            <table class="excel-table" id="tablaPartidas4">
                                <thead><tr><th style="width:100px;">Código</th><th>Descripción</th><th style="width:120px;">Metrado Excedente</th><th style="width:50px;"></th></tr></thead>
                                <tbody></tbody>
                            </table>
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-diagram-3"></i> 5. Sub Partidas Ejecutadas</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu text-center text-muted py-4">
                            <i class="bi bi-info-circle me-1"></i> Rubro habilitado estructuralmente. Sin registros requeridos para el tramo actual.
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-calendar-check"></i> 6. Actividades Ejecutadas</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <label class="form-label">Diario de actividades por frentes operativos</label>
                            <textarea class="form-control" id="actividades_diarias" rows="4" placeholder="Describa el progreso físico detallado, frentes activos y contingencias controladas..."></textarea>
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-box-seam"></i> 7. Movimiento de Almacén</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <div class="row g-4">
                                <div class="col-12">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <h6 class="form-label m-0 text-primary">Materiales de Construcción</h6>
                                        <button type="button" class="btn btn-sm btn-dark" onclick="agregarFilaAlmacen()"><i class="bi bi-plus-lg me-1"></i> Fila Excel</button>
                                    </div>
                                    <div class="table-responsive">
                                        <table class="excel-table" id="tablaExcelAlmacen">
                                            <thead><tr><th>Descripción del Material</th><th style="width:120px;">Ingreso (Cant.)</th><th style="width:120px;">Salida (Cant.)</th><th style="width:150px;">Guía / Vale N°</th><th style="width:50px;"></th></tr></thead>
                                            <tbody></tbody>
                                        </table>
                                    </div>
                                </div>
                                <div class="col-12 border-top pt-3">
                                    <h6 class="form-label text-primary mb-3">Movimiento de Combustibles</h6>
                                    <div class="row g-2">
                                        <div class="col-6 col-sm-3"><label class="form-label">Diesel B5 Ingreso (Gln)</label><input type="number" class="form-control" id="diesel_ing" value="0"></div>
                                        <div class="col-6 col-sm-3"><label class="form-label">Diesel B5 Salida (Gln)</label><input type="number" class="form-control" id="diesel_sal" value="0"></div>
                                        <div class="col-6 col-sm-3"><label class="form-label">Gasohol Ingreso (Gln)</label><input type="number" class="form-control" id="gas_ing" value="0"></div>
                                        <div class="col-6 col-sm-3"><label class="form-label">Gasohol Salida (Gln)</label><input type="number" class="form-control" id="gas_sal" value="0"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-truck-flatbed"></i> 8. Maquinarias, Vehículos y Equipos</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            
                            <div class="mb-4">
                                <h6 class="form-label text-primary border-bottom pb-1 mb-2">Maquinarias del Gobierno Regional Puno</h6>
                                <div class="table-responsive">
                                    <table class="excel-table" id="tablaMaqGore">
                                        <thead><tr><th style="width:40px;">Uso</th><th>Equipo / Descripción</th><th style="width:120px;">Marca / Serie</th><th style="width:100px;">Horas Máq. (HM)</th><th style="width:100px;">Combustible (Gln)</th></tr></thead>
                                        <tbody>
                                            <tr><td><input type="checkbox" class="form-check-input ck-maq" onchange="toggleFilaMaq(this)"></td><td><input type="text" class="excel-input" value="Excavadora Oruga CAT 336" readonly></td><td><input type="text" class="excel-input" value="CATERPILLAR" readonly></td><td><input type="number" class="excel-input v-maq" value="0" disabled></td><td><input type="number" class="excel-input v-maq" value="0" disabled></td></tr>
                                            <tr><td><input type="checkbox" class="form-check-input ck-maq" onchange="toggleFilaMaq(this)"></td><td><input type="text" class="excel-input" value="Tractor de Oruga D8T" readonly></td><td><input type="text" class="excel-input" value="CATERPILLAR" readonly></td><td><input type="number" class="excel-input v-maq" value="0" disabled></td><td><input type="number" class="excel-input v-maq" value="0" disabled></td></tr>
                                            <tr><td><input type="checkbox" class="form-check-input ck-maq" onchange="toggleFilaMaq(this)"></td><td><input type="text" class="excel-input" value="Motoniveladora 160K" readonly></td><td><input type="text" class="excel-input" value="CATERPILLAR" readonly></td><td><input type="number" class="excel-input v-maq" value="0" disabled></td><td><input type="number" class="excel-input v-maq" value="0" disabled></td></tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div class="mb-4 border-top pt-3">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <h6 class="form-label m-0 text-primary">Maquinarias por Servicio y/o Contrato</h6>
                                    <button type="button" class="btn btn-xs btn-outline-dark" onclick="agregarFilaServicio('tablaMaqServicio')"><i class="bi bi-plus-lg"></i> Agregar</button>
                                </div>
                                <div class="table-responsive">
                                    <table class="excel-table" id="tablaMaqServicio">
                                        <thead><tr><th>RUC Proveedor / Contrato</th><th>Equipo / Marca</th><th style="width:100px;">HM Trab.</th><th style="width:100px;">Comb. Sumin.</th><th style="width:40px;"></th></tr></thead>
                                        <tbody></tbody>
                                    </table>
                                </div>
                            </div>

                            <div class="row g-3 border-top pt-3">
                                <div class="col-md-6">
                                    <label class="form-label text-primary">Movilidades GORE Puno / Contrato</label>
                                    <textarea class="form-control" id="txt_movilidades" rows="2" placeholder="Camionetas, Volquetes de apoyo (Indicar KM y control)..."></textarea>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label text-primary">Equipos de Obra (GORE / Servicio)</label>
                                    <textarea class="form-control" id="txt_equipos" rows="2" placeholder="Estación Total, Grupo Electrógeno, Vibrocompactadores..."></textarea>
                                </div>
                            </div>

                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" onclick="toggleAcordeon(this)">
                            <h4><i class="bi bi-tools"></i> 9. Herramientas Manuales</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
                                <span class="text-muted small">Herramientas asignadas por defecto al tramo PU N-110</span>
                                <div class="form-check"><input class="form-check-input" type="checkbox" id="masterHerramientas" checked onchange="toggleTodasHerramientas(this)"> <label class="form-check-label small fw-bold" for="masterHerramientas">Marcar Todo</label></div>
                            </div>
                            <div class="row g-2" id="boxHerramientas">
                                <div class="col-6 col-sm-4"><div class="border p-2 rounded-3 bg-white"><input type="checkbox" class="form-check-input item-herramienta" checked> <span class="ms-1 small fw-semibold">Palas de acero</span></div></div>
                                <div class="col-6 col-sm-4"><div class="border p-2 rounded-3 bg-white"><input type="checkbox" class="form-check-input item-herramienta" checked> <span class="ms-1 small fw-semibold">Picos de excavación</span></div></div>
                                <div class="col-6 col-sm-4"><div class="border p-2 rounded-3 bg-white"><input type="checkbox" class="form-check-input item-herramienta" checked> <span class="ms-1 small fw-semibold">Buguies / Carretillas</span></div></div>
                                <div class="col-6 col-sm-4"><div class="border p-2 rounded-3 bg-white"><input type="checkbox" class="form-check-input item-herramienta" checked> <span class="ms-1 small fw-semibold">Amoladoras de banco</span></div></div>
                                <div class="col-6 col-sm-4"><div class="border p-2 rounded-3 bg-white"><input type="checkbox" class="form-check-input item-herramienta" checked> <span class="ms-1 small fw-semibold">Sierra Circular</span></div></div>
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item-samu">
                        <div class="accordion-header-samu" style="border-left: 4px solid #dc2626;" onclick="toggleAcordeon(this)">
                            <h4 class="text-danger"><i class="bi bi-exclamation-triangle-fill"></i> 10. Ocurrencias y Notas Legales</h4>
                            <i class="bi bi-chevron-down icon-chevron"></i>
                        </div>
                        <div class="accordion-body-samu">
                            <label class="form-label text-danger">Redacción libre técnico-legal del asiento</label>
                            <textarea class="form-control border-danger" id="ocurrencias_asiento" rows="6" placeholder="Consigne aquí incidentes críticos, solicitudes de ampliación, ingresos documentarios retrasados, RFI o directivas impartidas en la vía..."></textarea>
                        </div>
                    </div>

                </form>
            </div>

            <div id="printViewArea">
                <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
                    <h4 class="m-0 fw-bold">LIENZO DE TRANSCRIPCIÓN FÍSICA</h4>
                    <button class="btn btn-sm btn-outline-dark font-sans" onclick="ocultarVistaCopiado()"><i class="bi bi-eye-slash me-1"></i> Cerrar Vista Copiado</button>
                </div>
                <div id="printContentBody"></div>
            </div>

        </div>

        <div class="control-bar-fixed shadow-lg">
            <div class="d-flex align-items-center gap-2">
                <span id="saveStatusBadge" class="badge bg-success-subtle text-success py-2 px-3 border border-success-subtle" style="font-size:12px; border-radius:30px;">
                    <i class="bi bi-cloud-check-fill me-1"></i> Autoguardado Activo Local
                </span>
            </div>
            
            <div class="d-flex gap-2">
                <button type="button" class="btn btn-outline-dark rounded-pill px-4 btn-sm" onclick="mostrarVistaCopiado()"><i class="bi bi-file-earmark-text me-1"></i> Vista para Copiado</button>
                
                <div id="btnFirmaContainer">
                    <div class="slider-container">
                        <div class="slider-track" id="masterSliderTrack">
                            <div class="slider-progress" id="masterSliderProgress"></div>
                            <div class="slider-text" id="masterSliderText">Deslizar para Firmar Folio</div>
                            <div class="slider-handle" id="masterSliderHandle"><i class="bi bi-chevron-right"></i></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade" id="modalBarreraFuego" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content border-0 shadow-lg" style="border-radius:24px;">
                    <div class="modal-body text-center p-4">
                        <i class="bi bi-shield-slash-fill text-danger" style="font-size:3.5rem;"></i>
                        <h4 class="fw-bold mt-3 text-danger">ALERTA DE DISCREPANCIA LEGAL</h4>
                        <p class="text-muted small">Este asiento ya ha sido consignado y foliado a mano en el cuaderno físico original. Modificar los datos digitales romperá la concordancia auditora ante el GORE Puno.</p>
                        <div class="bg-light p-3 rounded-3 border mb-3 text-start">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="chkEntiendoResponsabilidad">
                                <label class="form-check-label small fw-semibold text-dark" for="chkEntiendoResponsabilidad">
                                    Asumo la total responsabilidad legal de forzar la edición del borrador firmado.
                                </label>
                            </div>
                        </div>
                        <div class="d-flex gap-2 justify-content-center">
                            <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal" onclick="abortarEdicionDios()">Cancelar</button>
                            <button type="button" class="btn btn-danger rounded-pill px-4" onclick="ejecutarAperturaDios()">Forzar Apertura</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        
        <script>
            const esAdmin = {{"true" if es_admin else "false"}};
            const catalogoPartidas = {{ catalogo_partidas | tojson }};
            let estaFirmadoGlobal = false;

            // --- MOTOR DE ACORDEONES ---
            function toggleAcordeon(elemento) {
                elemento.parentElement.classList.toggle('active');
            }

            // --- DINÁMICA SECCIÓN 3 Y 4: BUSCADOR DE PARTIDAS ---
            let tablaDestinoActual = 'tablaPartidas3';
            function filtrarCatalogo() {
                const query = document.getElementById('buscadorPartidas').value.toLowerCase();
                const sugBox = document.getElementById('listaSugerencias');
                if(!query) { sugBox.style.display = 'none'; return; }
                
                const filtrados = catalogoPartidas.filter(p => p.descripcion.toLowerCase().includes(query) || p.codigo.includes(query));
                if(filtrados.length === 0) { sugBox.style.display = 'none'; return; }
                
                sugBox.innerHTML = filtrados.map(p => `
                    <button type="button" class="list-group-item list-group-item-action font-sans small py-2" onclick="seleccionarPartida('${p.codigo}', '${p.descripcion}')">
                        <b>${p.codigo}</b> - ${p.descripcion}
                    </button>
                `).join('');
                sugBox.style.display = 'block';
            }
            
            function seleccionarPartida(codigo, desc) {
                const tbody = document.getElementById('tablaPartidas3').querySelector('tbody');
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="text" class="excel-input fw-bold text-primary text-center" value="${codigo}" readonly></td>
                    <td><input type="text" class="excel-input" value="${desc}" readonly></td>
                    <td><input type="text" class="excel-input text-end" placeholder="0.00 m3/m2"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `;
                tbody.appendChild(row);
                document.getElementById('buscadorPartidas').value = '';
                document.getElementById('listaSugerencias').style.display = 'none';
                forzarAutoguardado();
            }

            function agregarFilaPartida(idTabla) {
                const tbody = document.getElementById(idTabla).querySelector('tbody');
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="text" class="excel-input text-center" placeholder="00.00"></td>
                    <td><input type="text" class="excel-input" placeholder="Escriba partida manual..."></td>
                    <td><input type="text" class="excel-input text-end" placeholder="0.00"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `;
                tbody.appendChild(row);
                forzarAutoguardado();
            }

            // --- DINÁMICA SECCIÓN 7: EXCEL ALMACÉN ---
            function agregarFilaAlmacen() {
                const tbody = document.getElementById('tablaExcelAlmacen').querySelector('tbody');
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="text" class="excel-input" placeholder="Nombre del material / Cemento, fierro..."></td>
                    <td><input type="number" class="excel-input text-center" placeholder="0"></td>
                    <td><input type="number" class="excel-input text-center" placeholder="0"></td>
                    <td><input type="text" class="excel-input" placeholder="N° Vale / Guía"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `;
                tbody.appendChild(row);
                forzarAutoguardado();
            }

            // --- DINÁMICA SECCIÓN 8: MAQUINARIAS CONDICIONALES ---
            function toggleFilaMaq(chk) {
                const inputs = chk.parentElement.parentElement.querySelectorAll('.v-maq');
                inputs.forEach(inp => {
                    inp.disabled = !chk.checked;
                    if(!chk.checked) inp.value = "0";
                });
                forzarAutoguardado();
            }

            function agregarFilaServicio(idTabla) {
                const tbody = document.getElementById(idTabla).querySelector('tbody');
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="text" class="excel-input" placeholder="RUC / N° Contrato"></td>
                    <td><input type="text" class="excel-input" placeholder="Excavadora CAT, Camión..."></td>
                    <td><input type="number" class="excel-input text-center" placeholder="0.0"></td>
                    <td><input type="number" class="excel-input text-center" placeholder="0"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `;
                tbody.appendChild(row);
                forzarAutoguardado();
            }

            // --- DINÁMICA SECCIÓN 9: HERRAMIENTAS MASTER ---
            function toggleTodasHerramientas(master) {
                const checks = document.querySelectorAll('.item-herramienta');
                checks.forEach(c => c.checked = master.checked);
                forzarAutoguardado();
            }

            // --- MÓDULO DIOS Y RESPONSABILIDAD DE ACCESOS ---
            function inyectarBotonDios() {
                const area = document.getElementById('areaModoDios');
                if(esAdmin) {
                    area.innerHTML = `
                        <button id="btnLlaveDios" class="btn btn-warning rounded-pill px-3 py-2 btn-sm shadow-sm d-flex align-items-center gap-1" onclick="intentarAperturaModoDios()">
                            <i class="bi bi-key-fill"></i> Forzar Edición (Admin)
                        </button>
                    `;
                }
            }

            function intentarAperturaModoDios() {
                const isTranscrito = document.getElementById('switchTranscrito').checked;
                if (isTranscrito) {
                    const modal = new bootstrap.Modal(document.getElementById('modalBarreraFuego'));
                    modal.show();
                } else {
                    ejecutarAperturaDios();
                }
            }

            function abortarEdicionDios() {
                document.getElementById('chkEntiendoResponsabilidad').checked = false;
            }

            function ejecutarAperturaDios() {
                if(document.getElementById('switchTranscrito').checked && !document.getElementById('chkEntiendoResponsabilidad').checked) {
                    alert("Debe marcar la casilla de responsabilidad legal.");
                    return;
                }
                
                // Desbloqueo del Modo Dios
                estaFirmadoGlobal = false;
                const modalEl = document.getElementById('modalBarreraFuego');
                const modalInstance = bootstrap.Modal.getInstance(modalEl);
                if(modalInstance) modalInstance.hide();
                
                // Habilitar campos
                document.getElementById('formInteractiveArea').style.pointerEvents = 'auto';
                document.getElementById('formInteractiveArea').style.opacity = '1';
                document.getElementById('btnFirmaContainer').style.display = 'block';
                
                document.getElementById('saveStatusBadge').className = "badge bg-warning-subtle text-warning py-2 px-3 border border-warning-subtle";
                document.getElementById('saveStatusBadge').innerHTML = "<i class='bi bi-unlock-fill me-1'></i> Modo Dios: Edición Forzada Desbloqueada";
            }

            function actualizarSemaforoFisico() {
                const chk = document.getElementById('switchTranscrito');
                const badge = document.getElementById('badgeFisico');
                if(chk.checked) {
                    badge.textContent = "Foliado en Físico";
                    badge.className = "badge ms-2 bg-success text-white";
                } else {
                    badge.textContent = "Pendiente";
                    badge.className = "badge ms-2 bg-warning text-dark";
                }
                forzarAutoguardado();
            }

            // --- MOTOR DE AUTOGUARDADO AVANZADO (localStorage) ---
            const formKey = "samu_asiento_88_draft";
            
            function forzarAutoguardado() {
                if(estaFirmadoGlobal) return;
                
                // Extraer filas dinámicas de tablas
                const recopilarFilas = (idTabla) => {
                    const filas = [];
                    document.getElementById(idTabla).querySelectorAll('tbody tr').forEach(tr => {
                        const inputs = tr.querySelectorAll('input');
                        if(inputs.length >= 2) {
                            filas.push(Array.from(inputs).map(i => i.value || i.checked));
                        }
                    });
                    return filas;
                };

                const dataDraft = {
                    jornal_m: document.getElementById('jornal_manana').value,
                    jornal_t: document.getElementById('jornal_tarde').value,
                    cant_operarios: document.getElementById('cant_operarios').value,
                    cant_oficiales: document.getElementById('cant_oficiales').value,
                    cant_peones: document.getElementById('cant_peones').value,
                    cant_mecanicos: document.getElementById('cant_mecanicos').value,
                    cant_controladores: document.getElementById('cant_controladores').value,
                    cant_operadores: document.getElementById('cant_operadores').value,
                    txt_actividades: document.getElementById('actividades_diarias').value,
                    txt_movilidades: document.getElementById('txt_movilidades').value,
                    txt_equipos: document.getElementById('txt_equipos').value,
                    txt_ocurrencias: document.getElementById('ocurrencias_asiento').value,
                    semaforo_fisico: document.getElementById('switchTranscrito').checked,
                    // Tablas
                    partidas3: recopilarFilas('tablaPartidas3'),
                    partidas4: recopilarFilas('tablaPartidas4'),
                    almacenExcel: recopilarFilas('tablaExcelAlmacen'),
                    maquinariasGore: recopilarFilas('tablaMaqGore'),
                    maquinariasServicio: recopilarFilas('tablaMaqServicio')
                };

                localStorage.setItem(formKey, JSON.stringify(dataDraft));
                const status = document.getElementById('saveStatusBadge');
                status.innerHTML = `<i class="bi bi-cloud-check-fill me-1"></i> Borrador Guardado (${new Date().toLocaleTimeString()})`;
            }

            function cargarBorradorLocal() {
                const raw = localStorage.getItem(formKey);
                if(!raw) return;
                const draft = JSON.parse(raw);

                document.getElementById('jornal_manana').value = draft.jornal_m || '07:00 - 12:00';
                document.getElementById('jornal_tarde').value = draft.jornal_t || '13:00 - 17:00';
                document.getElementById('cant_operarios').value = draft.cant_operarios || 0;
                document.getElementById('cant_oficiales').value = draft.cant_oficiales || 0;
                document.getElementById('cant_peones').value = draft.cant_peones || 0;
                document.getElementById('cant_mecanicos').value = draft.cant_mecanicos || 0;
                document.getElementById('cant_controladores').value = draft.cant_controladores || 0;
                document.getElementById('cant_operadores').value = draft.cant_operadores || 0;
                document.getElementById('actividades_diarias').value = draft.txt_actividades || '';
                document.getElementById('txt_movilidades').value = draft.txt_movilidades || '';
                document.getElementById('txt_equipos').value = draft.txt_equipos || '';
                document.getElementById('ocurrencias_asiento').value = draft.txt_ocurrencias || '';
                
                document.getElementById('switchTranscrito').checked = draft.semaforo_fisico || false;
                actualizarSemaforoFisico();

                // Re-inyectar tablas
                const rellenarTabla = (idTabla, filas, htmlFn) => {
                    const tbody = document.getElementById(idTabla).querySelector('tbody');
                    tbody.innerHTML = '';
                    if(filas) {
                        filas.forEach(f => {
                            const row = document.createElement('tr');
                            row.innerHTML = htmlFn(f);
                            tbody.appendChild(row);
                        });
                    }
                };

                rellenarTabla('tablaPartidas3', draft.partidas3, f => `
                    <td><input type="text" class="excel-input fw-bold text-primary text-center" value="${f[0]}" readonly></td>
                    <td><input type="text" class="excel-input" value="${f[1]}" readonly></td>
                    <td><input type="text" class="excel-input text-end" value="${f[2]}"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `);

                rellenarTabla('tablaPartidas4', draft.partidas4, f => `
                    <td><input type="text" class="excel-input text-center" value="${f[0]}"></td>
                    <td><input type="text" class="excel-input" value="${f[1]}"></td>
                    <td><input type="text" class="excel-input text-end" value="${f[2]}"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `);

                rellenarTabla('tablaExcelAlmacen', draft.almacenExcel, f => `
                    <td><input type="text" class="excel-input" value="${f[0]}"></td>
                    <td><input type="number" class="excel-input text-center" value="${f[1]}"></td>
                    <td><input type="number" class="excel-input text-center" value="${f[2]}"></td>
                    <td><input type="text" class="excel-input" value="${f[3]}"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `);

                if(draft.maquinariasGore) {
                    const filasGore = document.getElementById('tablaMaqGore').querySelectorAll('tbody tr');
                    draft.maquinariasGore.forEach((f, idx) => {
                        if(filasGore[idx]) {
                            filasGore[idx].querySelectorAll('input')[0].checked = f[0];
                            filasGore[idx].querySelectorAll('input')[3].value = f[3];
                            filasGore[idx].querySelectorAll('input')[4].value = f[4];
                            filasGore[idx].querySelectorAll('input')[3].disabled = !f[0];
                            filasGore[idx].querySelectorAll('input')[4].disabled = !f[0];
                        }
                    });
                }

                rellenarTabla('tablaMaqServicio', draft.maquinariasServicio, f => `
                    <td><input type="text" class="excel-input" value="${f[0]}"></td>
                    <td><input type="text" class="excel-input" value="${f[1]}"></td>
                    <td><input type="number" class="excel-input text-center" value="${f[2]}"></td>
                    <td><input type="number" class="excel-input text-center" value="${f[3]}"></td>
                    <td class="text-center"><button class="btn p-1 text-danger" onclick="this.parentElement.parentElement.remove(); forzarAutoguardado();"><i class="bi bi-trash"></i></button></td>
                `);
            }

            // Escuchar cambios globales para el motor anti-pérdida
            document.getElementById('megaFormResidencia').addEventListener('input', forzarAutoguardado);
            document.getElementById('megaFormResidencia').addEventListener('change', forzarAutoguardado);

            // --- VISTA PARA COPIADO EN FÍSICO ---
            function mostrarVistaCopiado() {
                const body = document.getElementById('printContentBody');
                
                // Compilar un texto legible idéntico a las páginas del libro
                let html = `
                    <p><b>ASIENTO N° 88 DEL RESIDENTE DE OBRA - FECHA: ${document.getElementById('badgeFisico').parentElement.parentElement.parentElement.querySelector('p').textContent.replace(' ','')}</b></p>
                    <p><b>1. JORNAL DE TRABAJO:</b> MAÑANA: ${document.getElementById('jornal_manana').value} | TARDE: ${document.getElementById('jornal_tarde').value}</p>
                    <p><b>2. PERSONAL DE OBRA:</b><br>
                    - GASTOS GENERALES: Residente de Obra, Especialista en Suelos, Topógrafo (Presentes)<br>
                    - COSTO DIRECTO: Operarios (${document.getElementById('cant_operarios').value}), Oficiales (${document.getElementById('cant_oficiales').value}), Peones (${document.getElementById('cant_peones').value}), Mecánicos (${document.getElementById('cant_mecanicos').value}), Controladores (${document.getElementById('cant_controladores').value}), Operadores de Maquinaria (${document.getElementById('cant_operadores').value}).</p>
                    <p><b>3. PARTIDAS EJECUTADAS:</b><br>
                `;
                
                document.getElementById('tablaPartidas3').querySelectorAll('tbody tr').forEach(tr => {
                    const inp = tr.querySelectorAll('input');
                    html += `&nbsp;&nbsp;&bull; Partida ${inp[0].value}: ${inp[1].value} - Metrado: ${inp[2].value}<br>`;
                });

                html += `</p><p><b>4. PARTIDAS DE MAYOR METRADO:</b><br>`;
                document.getElementById('tablaPartidas4').querySelectorAll('tbody tr').forEach(tr => {
                    const inp = tr.querySelectorAll('input');
                    html += `&nbsp;&nbsp;&bull; ${inp[0].value} - ${inp[1].value} - Excedente: ${inp[2].value}<br>`;
                });

                html += `</p><p><b>5. SUB PARTIDAS EJECUTADAS:</b> Sin novedades en la jornada.</p>`;
                html += `<p><b>6. ACTIVIDADES EJECUTADAS:</b><br>${document.getElementById('actividades_diarias').value.replace(/\\n/g, '<br>')}</p>`;
                
                html += `<p><b>7. MOVIMIENTO DE ALMACÉN:</b><br>`;
                document.getElementById('tablaExcelAlmacen').querySelectorAll('tbody tr').forEach(tr => {
                    const inp = tr.querySelectorAll('input');
                    html += `&nbsp;&nbsp;&bull; Material: ${inp[0].value} | Ingreso: ${inp[1].value} | Salida: ${inp[2].value} | Doc: ${inp[3].value}<br>`;
                });
                
                html += `<b>8. MAQUINARIA Y FLOTA:</b><br>`;
                document.getElementById('tablaMaqGore').querySelectorAll('tbody tr').forEach(tr => {
                    const inp = tr.querySelectorAll('input');
                    if(inp[0].checked) {
                        html += `&nbsp;&nbsp;&bull; GORE PUNO: ${inp[1].value} (${inp[2].value}) - HM: ${inp[3].value} | Comb: ${inp[4].value} Gln<br>`;
                    }
                });

                html += `<p><b>9. HERRAMIENTAS MANUALES:</b> Se reporta el uso del 100% del kit estándar (Palas, picos, buguies, amoladoras y sierra circular) operativo en frentes.</p>`;
                html += `<p><b>10. OCURRENCIAS Y NOTAS LEGALES:</b><br>${document.getElementById('ocurrencias_asiento').value.replace(/\\n/g, '<br>')}</p>`;

                body.innerHTML = html;
                document.getElementById('formInteractiveArea').style.display = 'none';
                document.getElementById('printViewArea').style.display = 'block';
                window.scrollTo(0,0);
            }

            function ocultarVistaCopiado() {
                document.getElementById('printViewArea').style.display = 'none';
                document.getElementById('formInteractiveArea').style.display = 'block';
            }

            // --- MOTOR DEL SLIDER DE FIRMA FINAL ---
            const mHandle = document.getElementById('masterSliderHandle');
            const mTrack = document.getElementById('masterSliderTrack');
            const mProgress = document.getElementById('masterSliderProgress');
            const mText = document.getElementById('masterSliderText');
            let mIsDragging = false, mStartX = 0, mMaxSlide = 0;

            function calcLimitesMaster() { mMaxSlide = mTrack.clientWidth - mHandle.clientWidth - 8; }
            window.addEventListener('resize', calcLimitesMaster);
            setTimeout(calcLimitesMaster, 500);

            function startMasterDrag(clientX) {
                if(estaFirmadoGlobal) return;
                mIsDragging = true; mStartX = clientX - mHandle.offsetLeft; calcLimitesMaster();
            }
            function onMasterDrag(clientX) {
                if (!mIsDragging) return;
                let left = clientX - mStartX;
                if (left < 4) left = 4; if (left > mMaxSlide) left = mMaxSlide;
                mHandle.style.left = left + 'px'; mProgress.style.width = (left + 23) + 'px';
                if (left >= mMaxSlide - 2) { mIsDragging = false; firmarAsientoDefinitivo(); }
            }
            function stopMasterDrag() {
                if (!mIsDragging) return; mIsDragging = false;
                mHandle.style.transition = 'left 0.3s ease'; mProgress.style.transition = 'width 0.3s ease';
                mHandle.style.left = '4px'; mProgress.style.width = '0px';
                setTimeout(() => { mHandle.style.transition = 'none'; mProgress.style.transition = 'none'; }, 300);
            }

            mHandle.addEventListener('mousedown', (e) => startMasterDrag(e.clientX));
            document.addEventListener('mousemove', (e) => onMasterDrag(e.clientX));
            document.addEventListener('mouseup', stopMasterDrag);
            mHandle.addEventListener('touchstart', (e) => startMasterDrag(e.touches[0].clientX), {passive: true});
            document.addEventListener('touchmove', (e) => { if(mIsDragging) onMasterDrag(e.touches[0].clientX); }, {passive: false});
            document.addEventListener('touchend', stopMasterDrag);

            function firmarAsientoDefinitivo() {
                estaFirmadoGlobal = true;
                mHandle.style.left = mMaxSlide + 'px'; mProgress.style.width = '100%'; mHandle.style.background = '#00875a';
                mHandle.innerHTML = '<i class="bi bi-check-lg"></i>'; mText.textContent = "FOLIO DIGITAL FIRMADO"; mText.style.color = "#00875a";
                
                // Bloqueo total de inputs
                document.getElementById('formInteractiveArea').style.pointerEvents = 'none';
                document.getElementById('formInteractiveArea').style.opacity = '0.75';
                document.getElementById('btnFirmaContainer').style.display = 'none';
                
                document.getElementById('saveStatusBadge').className = "badge bg-dark-subtle text-dark py-2 px-3 border border-dark-subtle";
                document.getElementById('saveStatusBadge').innerHTML = "<i class='bi bi-lock-fill me-1'></i> Bloqueado: Folio Cerrado Legalmente";
                
                alert("Asiento N° 88 firmado digitalmente. Solo cuentas de administración podrán forzar correcciones bajo auditoría.");
            }

            // Al cargar la ventana por primera vez
            window.onload = () => {
                inyectarBotonDios();
                cargarBorradorLocal();
            };
        </script>
    </body>
    </html>
    """, numero_asiento=numero_asiento, fecha_formateada=fecha_formateada, catalogo_partidas=catalogo_partidas, es_admin=es_admin, nombre_completo=nombre_completo)
