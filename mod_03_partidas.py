# =========================================================
# mod_03_partidas.py
# Módulo: 3.- Partidas Ejecutadas (Pegado Mágico Excel + UI Premium)
# =========================================================

from flask import Blueprint

mod_03_bp = Blueprint('mod_03_partidas', __name__)

PARTIDAS_HTML = """
<style>
    /* Buscador Predictivo */
    .dropdown-partidas { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 12px 12px; max-height: 250px; overflow-y: auto; z-index: 1000; box-shadow: 0 15px 30px rgba(0,0,0,0.15); display: none; }
    .dropdown-item-p { padding: 12px 18px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 12px; align-items: center; transition: 0.2s; }
    .dropdown-item-p:hover, .dropdown-item-p.selected { background: linear-gradient(90deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 4px solid #0263a0; color: #0f172a; font-weight: 700; }
    .badge-item { background: #1e293b; color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    .badge-unidad { background: #e2e8f0; color: #475569; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; white-space: nowrap; margin-left: auto;}
    
    /* Degradados y Estilos Premium */
    .modal-header-gradient { background: linear-gradient(135deg, #0263a0 0%, #0284c7 100%); color: white !important; border-radius: 20px 20px 0 0; border: none; padding: 1.2rem 1.5rem;}
    .modal-header-gradient .btn-close { filter: brightness(0) invert(1); opacity: 0.8; }
    .modal-header-gradient .btn-close:hover { opacity: 1; }
    
    .modal-dark-gradient { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; border-radius: 24px; border: 1px solid #334155; box-shadow: 0 25px 50px rgba(0,0,0,0.4); }
    
    /* Zona de Pegado Inteligente Excel */
    .paste-zone { border: 2px dashed #0ea5e9; border-radius: 16px; background: rgba(14, 165, 233, 0.04); transition: all 0.3s ease; position: relative; overflow: hidden; }
    .paste-zone:focus-within { border-color: #0263a0; background: rgba(2, 99, 160, 0.08); box-shadow: 0 0 0 4px rgba(2,99,160,0.1); }
    .paste-zone-input { width: 100%; height: 80px; background: transparent; border: none; outline: none; resize: none; color: transparent; text-shadow: 0 0 0 #0263a0; text-align: center; font-weight: 600; position: relative; z-index: 2;}
    .paste-zone-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; pointer-events: none; color: #0284c7; z-index: 1;}
    
    /* Tabla Estilo Excel */
    .excel-table { border-collapse: separate; border-spacing: 0; width: 100%; }
    .excel-table th { background: #f1f5f9; color: #475569; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; padding: 10px; border-bottom: 2px solid #cbd5e1; position: sticky; top: 0; z-index: 10;}
    .excel-table td { font-size: 13px; font-weight: 500; vertical-align: middle; padding: 8px 10px; border-bottom: 1px solid #e2e8f0; color: #1e293b;}
    .excel-table tr:hover td { background: #f8fafc; }
</style>

<div class="step-view" id="step3">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">3.- Partidas Ejecutadas</div>
        <button type="button" class="btn btn-sm text-white rounded-pill fw-bold shadow-sm" style="background: linear-gradient(135deg, #10b981, #059669); border: none;" onclick="abrirModalCatalogoGlobal()">
            <i class="bi bi-file-earmark-excel me-1"></i> Catálogo Base (Excel)
        </button>
    </div>
    
    <p class="text-muted small mb-3">Busque la partida ejecutada en el día y presione <b>Enter</b>. Digite el metrado y presione <b>Enter</b> nuevamente.</p>
    
    <div class="position-relative mb-4">
        <div class="input-group input-group-lg shadow-sm" style="border-radius: 12px; overflow: hidden; border: 1px solid #cbd5e1;">
            <span class="input-group-text bg-white border-0"><i class="bi bi-search text-primary"></i></span>
            <input type="text" class="form-control border-0 fw-semibold" id="m3_buscador" placeholder="Ej: 07.01 o Transporte..." autocomplete="off" onkeyup="m3_teclas(event)" onfocus="m3_filtrar()" oninput="m3_filtrar()" style="box-shadow: none;">
        </div>
        <div class="dropdown-partidas" id="m3_dropdown"></div>
    </div>
    
    <div id="m3_lista_ui" class="d-flex flex-column gap-2 req-step3 mb-3"></div>
    <input type="hidden" id="v_partidas" class="req-step3" value="">
</div>

<div class="modal fade" id="modalCatalogoGlobal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content" style="border-radius: 20px; overflow: hidden; border: none; box-shadow: 0 25px 50px rgba(0,0,0,0.3);">
            
            <div class="modal-header-gradient d-flex justify-content-between align-items-center">
                <h5 class="modal-title fw-bold m-0"><i class="bi bi-database-fill-add me-2"></i> Memoria Global de Partidas</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            
            <div class="modal-body p-4 bg-white">
                <div class="paste-zone mb-4 shadow-sm">
                    <div class="paste-zone-overlay">
                        <i class="bi bi-clipboard2-check-fill fs-2 mb-1"></i>
                        <span class="fw-bold">Haga clic aquí y presione Ctrl + V para pegar desde Excel</span>
                        <span class="small fw-normal text-secondary opacity-75">El sistema detectará las columnas automáticamente (Item, Partida, Unidad)</span>
                    </div>
                    <textarea class="paste-zone-input" onpaste="handlePegadoMagico(event)"></textarea>
                </div>

                <div class="table-responsive" style="max-height: 40vh; overflow-y: auto; border: 1px solid #cbd5e1; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);">
                    <table class="excel-table">
                        <thead>
                            <tr>
                                <th width="15%" class="text-center">Ítem</th>
                                <th width="65%">Descripción de la Partida</th>
                                <th width="10%" class="text-center">Unidad</th>
                                <th width="10%" class="text-center"><i class="bi bi-gear-fill"></i></th>
                            </tr>
                        </thead>
                        <tbody id="tbodyCatalogoGlobal">
                            </tbody>
                    </table>
                </div>
            </div>
            
            <div class="modal-footer border-top-0 bg-light d-flex justify-content-between py-3">
                <span class="text-muted small fw-semibold">Partidas cargadas: <span id="lbl_total_cat" class="badge bg-primary rounded-pill ms-1 fs-6">0</span></span>
                <div>
                    <button type="button" class="btn btn-outline-danger rounded-pill px-4 fw-bold me-2" onclick="limpiarCatalogo()">Vaciar</button>
                    <button type="button" class="btn btn-primary rounded-pill px-5 fw-bold shadow-sm" data-bs-dismiss="modal">Guardar y Cerrar</button>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="m3_modal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content modal-dark-gradient">
            <div class="modal-body p-4 text-center">
                
                <div class="mb-3">
                    <span class="badge" style="background: rgba(255,255,255,0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 13px;" id="m3_lbl_item">00.00</span>
                </div>
                
                <h5 class="fw-bold mb-4" id="m3_lbl_desc" style="line-height: 1.4; color: #f8fafc; font-size: 16px;">Descripción de la Partida</h5>
                
                <div class="input-group input-group-lg mb-3 shadow-lg" style="border-radius: 12px; overflow: hidden; border: 2px solid #38bdf8;">
                    <input type="number" step="0.01" class="form-control text-center fw-bold bg-white text-dark" id="m3_input" placeholder="Avance" onkeydown="if(event.key==='Enter'){event.preventDefault(); m3_guardar();}">
                    <span class="input-group-text fw-bold text-white" style="background: #0284c7; border: none;" id="m3_lbl_und">UND</span>
                </div>
                
                <p class="small mb-0" style="color: #94a3b8;"><i class="bi bi-keyboard me-1"></i> Presione <b>Enter</b> para continuar</p>
            </div>
        </div>
    </div>
</div>

<script>
    // ==========================================
    // INICIALIZACIÓN GLOBAL Y AUTO-FOCO
    // ==========================================
    window.m3_lista = window.m3_lista || [];
    window.catalogoMaestro = window.catalogoMaestro || [];
    
    let m3_temp = null;
    let m3_idx = -1;
    let m3_modal_inst = null;

    // Colocar modales en el Body y Auto-Foco instantáneo
    setTimeout(() => {
        const mCat = document.getElementById('modalCatalogoGlobal');
        const mMet = document.getElementById('m3_modal');
        if(mCat && mCat.parentNode !== document.body) document.body.appendChild(mCat);
        if(mMet && mMet.parentNode !== document.body) {
            document.body.appendChild(mMet);
            // Auto Focus sin necesidad de hacer clic
            mMet.addEventListener('shown.bs.modal', function () { document.getElementById('m3_input').focus(); });
        }
    }, 500);

    // ==========================================
    // LÓGICA DE PEGADO MÁGICO (EXCEL)
    // ==========================================
    function abrirModalCatalogoGlobal() { 
        renderizarTablaCatalogoGlobal();
        new bootstrap.Modal(document.getElementById('modalCatalogoGlobal')).show(); 
    }

    function handlePegadoMagico(e) {
        e.preventDefault();
        let pasteData = (e.clipboardData || window.clipboardData).getData('text');
        if(!pasteData.trim()) return;

        const rows = pasteData.split('\\n');
        let agregados = 0;

        rows.forEach(row => {
            if(!row.trim()) return;
            const cols = row.split('\\t'); 
            
            let item = '-';
            let desc = '';
            let und = 'GLB';

            // Inteligencia de columnas: Detecta si pegaste 1, 2 o 3 columnas
            if(cols.length >= 3) {
                item = cols[0].trim();
                desc = cols[1].trim();
                und = cols[2].trim().toUpperCase();
            } else if (cols.length === 2) {
                // Si son 2 columnas, puede ser (Item, Desc) o (Desc, Unidad)
                // Si la columna 1 es muy larga, asumimos que es (Desc, Unidad)
                if(cols[0].length > 15) {
                    desc = cols[0].trim();
                    und = cols[1].trim().toUpperCase();
                } else {
                    item = cols[0].trim();
                    desc = cols[1].trim();
                }
            } else if (cols.length === 1) {
                desc = cols[0].trim();
            }

            if(desc !== '') {
                window.catalogoMaestro.push({ item: item, descripcion: desc, unidad: und });
                agregados++;
            }
        });

        if(agregados > 0) {
            renderizarTablaCatalogoGlobal();
            if (typeof mostrarAlerta === "function") {
                mostrarAlerta(`¡Éxito! Se cargaron ${agregados} partidas en memoria.`, "success");
            }
        }
        
        // Limpia el textarea para el siguiente pegado
        e.target.value = '';
    }

    function eliminarCatalogo(index) {
        window.catalogoMaestro.splice(index, 1);
        renderizarTablaCatalogoGlobal();
    }

    function limpiarCatalogo() {
        if(confirm("¿Seguro que desea vaciar el catálogo completo?")) {
            window.catalogoMaestro = [];
            renderizarTablaCatalogoGlobal();
        }
    }

    function renderizarTablaCatalogoGlobal() {
        const tbody = document.getElementById('tbodyCatalogoGlobal');
        tbody.innerHTML = window.catalogoMaestro.map((p, idx) => `
            <tr>
                <td class="fw-bold text-center" style="color:#0263a0;">${p.item}</td>
                <td class="fw-semibold">${p.descripcion}</td>
                <td class="text-center"><span class="badge-unidad border border-secondary">${p.unidad}</span></td>
                <td class="text-center"><button type="button" class="btn btn-sm btn-outline-danger border-0 p-1" onclick="eliminarCatalogo(${idx})"><i class="bi bi-trash-fill"></i></button></td>
            </tr>
        `).join('');
        document.getElementById('lbl_total_cat').innerText = window.catalogoMaestro.length;
    }

    // ==========================================
    // BUSCADOR PREDICTIVO Y DOBLE ENTER
    // ==========================================
    function m3_filtrar() {
        const val = document.getElementById('m3_buscador').value.toLowerCase();
        const drop = document.getElementById('m3_dropdown');
        
        if(val === '' || window.catalogoMaestro.length === 0) {
            drop.style.display = 'none'; return;
        }

        const filtrados = window.catalogoMaestro.filter(p => p.item.toLowerCase().includes(val) || p.descripcion.toLowerCase().includes(val)).slice(0, 8);
        
        if(filtrados.length > 0) {
            drop.innerHTML = filtrados.map((p, idx) => `
                <div class="dropdown-item-p ${idx === 0 ? 'selected' : ''}" onclick="m3_abrir(${idx})" id="drop_item_${idx}">
                    <span class="badge-item">${p.item}</span>
                    <span class="text-truncate flex-grow-1">${p.descripcion}</span>
                    <span class="badge-unidad">${p.unidad}</span>
                </div>
            `).join('');
            drop.style.display = 'block';
            m3_idx = 0;
            drop.dataset.filt = JSON.stringify(filtrados);
        } else {
            drop.style.display = 'none';
        }
    }

    function m3_teclas(e) {
        const drop = document.getElementById('m3_dropdown');
        if(drop.style.display === 'none') return;
        
        const items = drop.getElementsByClassName('dropdown-item-p');
        
        if (e.key === 'ArrowDown') {
            if (m3_idx < items.length - 1) m3_idx++;
            m3_select(items);
        } else if (e.key === 'ArrowUp') {
            if (m3_idx > 0) m3_idx--;
            m3_select(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            m3_abrir(m3_idx);
        }
    }

    function m3_select(items) {
        for(let i=0; i<items.length; i++) { items[i].classList.remove('selected'); }
        if(items[m3_idx]) {
            items[m3_idx].classList.add('selected');
            items[m3_idx].scrollIntoView({block: 'nearest'});
        }
    }

    function m3_abrir(idx) {
        const f = JSON.parse(document.getElementById('m3_dropdown').dataset.filt);
        m3_temp = f[idx];
        
        document.getElementById('m3_buscador').value = '';
        document.getElementById('m3_dropdown').style.display = 'none';

        document.getElementById('m3_lbl_item').innerText = m3_temp.item;
        document.getElementById('m3_lbl_desc').innerText = m3_temp.descripcion;
        document.getElementById('m3_lbl_und').innerText = m3_temp.unidad;
        
        const inputMet = document.getElementById('m3_input');
        inputMet.value = '';

        if(!m3_modal_inst) m3_modal_inst = new bootstrap.Modal(document.getElementById('m3_modal'));
        m3_modal_inst.show();
    }

    function m3_guardar() {
        const metradoVal = document.getElementById('m3_input').value;
        
        window.m3_lista.push({
            item: m3_temp.item,
            descripcion: m3_temp.descripcion,
            unidad: m3_temp.unidad,
            metrado: metradoVal !== '' ? parseFloat(metradoVal).toFixed(2) : ''
        });

        m3_modal_inst.hide();
        m3_render();
        document.getElementById('v_partidas').value = "lleno"; 
        
        if (typeof sincronizarDatos === "function") sincronizarDatos();
        
        // Retorno del Foco inmediato al buscador
        setTimeout(() => { document.getElementById('m3_buscador').focus(); }, 300);
    }

    function m3_del(index) { 
        window.m3_lista.splice(index, 1); 
        if(window.m3_lista.length === 0) document.getElementById('v_partidas').value = ""; 
        m3_render(); 
        if (typeof sincronizarDatos === "function") sincronizarDatos(); 
    }

    function m3_render() {
        const container = document.getElementById('m3_lista_ui');
        container.innerHTML = window.m3_lista.map((p, index) => `
            <div class="bg-white border rounded-3 p-3 d-flex justify-content-between align-items-center shadow-sm" style="border-left: 4px solid #0263a0 !important;">
                <div class="d-flex align-items-center gap-3 text-truncate" style="max-width: 400px;">
                    <span class="badge-item">${p.item}</span>
                    <span class="fw-semibold text-dark text-truncate" title="${p.descripcion}">${p.descripcion}</span>
                </div>
                <div class="d-flex align-items-center gap-3">
                    <span class="fw-bold text-primary fs-5">${p.metrado ? p.metrado : '-'} <small class="text-muted fw-bold" style="font-size:11px;">${p.unidad}</small></span>
                    <button type="button" class="btn btn-sm btn-light text-danger border rounded-circle shadow-sm" onclick="m3_del(${index})"><i class="bi bi-trash-fill"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
