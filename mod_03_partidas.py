# =========================================================
# mod_03_partidas.py
# Módulo: 3.- Partidas Ejecutadas (Corregido: Live Preview + Auto-Foco)
# =========================================================

from flask import Blueprint

mod_03_bp = Blueprint('mod_03_partidas', __name__)

PARTIDAS_HTML = """
<style>
    /* Estilos del buscador predictivo */
    .dropdown-partidas { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 12px 12px; max-height: 200px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: none; }
    .dropdown-item-p { padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 10px; align-items: center; }
    .dropdown-item-p:hover, .dropdown-item-p.selected { background: #f0f9ff; color: #0263a0; font-weight: 600; }
    .badge-item { background: #1e293b; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; }
    .badge-unidad { background: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; margin-left: auto;}
    
    /* Estilos de la tabla tipo Excel */
    .excel-table th { background: #f8fafc; font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 800; letter-spacing: 0.5px; border-bottom: 2px solid #e2e8f0;}
    .excel-table td { font-size: 13px; vertical-align: middle; border-color: #f1f5f9;}
    .excel-paste-zone { border: 2px dashed #cbd5e1; border-radius: 12px; padding: 10px; background: #f8fafc; text-align: center; color: #64748b; font-size: 12px; font-weight: 600; cursor: pointer; transition: 0.3s; margin-bottom: 15px;}
    .excel-paste-zone:hover { border-color: #0263a0; color: #0263a0; background: #f0f9ff;}
</style>

<div class="step-view" id="step3">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">3.- Partidas Ejecutadas</div>
        <button type="button" class="btn btn-sm btn-outline-success rounded-pill fw-bold shadow-sm" onclick="abrirModalRegistrarPartidas()">
            <i class="bi bi-grid-3x3"></i> Registrar Partidas
        </button>
    </div>
    
    <p class="text-muted small mb-3">Busque la partida y presione <b>Enter</b>. Digite el metrado y presione <b>Enter</b> nuevamente <span class="text-primary fw-bold">(El metrado es opcional)</span>.</p>
    
    <div class="position-relative mb-4">
        <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" id="buscadorPartidas" placeholder="Ej: 07.01 o Transporte..." autocomplete="off" onkeyup="manejarTeclasBuscador(event)" onfocus="filtrarCatalogo()" oninput="filtrarCatalogo()">
        </div>
        <div class="dropdown-partidas" id="dropdownPartidas"></div>
    </div>
    
    <div id="listaPartidasAgregadas" class="d-flex flex-column gap-2 req-step3 mb-3"></div>
    <input type="hidden" id="v_partidas" class="req-step3" value="">
</div>

<div class="modal fade" id="modalRegistrarPartidas" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content" style="border-radius: 20px; overflow: hidden; border: none; box-shadow: 0 25px 50px rgba(0,0,0,0.2);">
            <div class="modal-header border-0 bg-light pb-3">
                <h5 class="modal-title fw-bold text-dark"><i class="bi bi-table text-success me-2"></i> Base de Partidas</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4 bg-white" id="zonaPegadoModal">
                
                <div class="excel-paste-zone" id="pasteHint">
                    <i class="bi bi-clipboard-check fs-4 d-block mb-1"></i>
                    Copie las 3 columnas desde su Excel y presione <b>Ctrl + V</b> en cualquier parte de esta ventana para cargarlas automáticamente.
                </div>

                <div class="table-responsive" style="max-height: 40vh; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 12px;">
                    <table class="table table-hover mb-0 excel-table">
                        <thead style="position: sticky; top: 0; z-index: 10;">
                            <tr>
                                <th width="15%">ITEM</th>
                                <th width="65%">PARTIDA</th>
                                <th width="15%">UND DE MEDIDA</th>
                                <th width="5%" class="text-center"><i class="bi bi-gear"></i></th>
                            </tr>
                        </thead>
                        <tbody id="tbodyCatalogo">
                        </tbody>
                        <tfoot>
                            <tr class="bg-light">
                                <td><input type="text" id="man_item" placeholder="Ej: 01.01" class="form-control form-control-sm border-0 shadow-none bg-white"></td>
                                <td><input type="text" id="man_desc" placeholder="Escriba el nombre de la partida..." class="form-control form-control-sm border-0 shadow-none bg-white"></td>
                                <td><input type="text" id="man_und" placeholder="M3" class="form-control form-control-sm border-0 shadow-none bg-white text-center"></td>
                                <td class="text-center"><button type="button" class="btn btn-sm btn-dark rounded-pill" onclick="agregarPartidaManual()"><i class="bi bi-plus-lg"></i></button></td>
                            </tr>
                        </tfoot>
                    </table>
                </div>

            </div>
            <div class="modal-footer border-0 pt-0 bg-white">
                <span class="text-muted small fw-semibold me-auto">Total partidas registradas: <span id="lbl_total_cat" class="text-primary">0</span></span>
                <button type="button" class="btn btn-primary rounded-pill px-4 fw-bold" data-bs-dismiss="modal">Listo, continuar</button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="modalMetrado" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content" style="border-radius: 20px; border: 2px solid #0263a0; box-shadow: 0 20px 40px rgba(2,99,160,0.15);">
            <div class="modal-body p-4 text-center">
                <div class="badge-item mb-2" id="lbl_m_item">00.00</div>
                <h6 class="fw-bold text-dark mb-3" id="lbl_m_desc" style="line-height: 1.3;">Descripción de la Partida</h6>
                
                <div class="input-group input-group-lg mb-2 shadow-sm">
                    <input type="number" step="0.01" class="form-control text-center fw-bold" id="inputMetrado" placeholder="0.00" onkeydown="if(event.key==='Enter'){event.preventDefault(); confirmarMetrado();}">
                    <span class="input-group-text bg-white fw-bold text-primary" id="lbl_m_und">UND</span>
                </div>
                <p class="small text-muted mb-0">Presione <b>Enter</b> para guardar.</p>
            </div>
        </div>
    </div>
</div>

<script>
    // ==========================================
    // INICIALIZACIÓN GLOBAL Y AUTO-FOCO
    // ==========================================
    // Usamos window.m3_lista para que vistas_residencia.py pueda leerlo e imprimirlo
    window.m3_lista = window.m3_lista || [];
    window.catalogoMaestro = window.catalogoMaestro || [];
    
    let partidaSeleccionadaTemporal = null;
    let indexSeleccionadoDropdown = -1;
    let miniModalInstance = null;

    // Enganche al DOM para mover los modales y forzar el Auto-Focus
    setTimeout(() => {
        const mReg = document.getElementById('modalRegistrarPartidas');
        const mMet = document.getElementById('modalMetrado');
        if(mReg && mReg.parentNode !== document.body) document.body.appendChild(mReg);
        if(mMet && mMet.parentNode !== document.body) {
            document.body.appendChild(mMet);
            
            // CORRECCIÓN: Evento oficial de Bootstrap para enfocar el cursor sin dar click
            mMet.addEventListener('shown.bs.modal', function () {
                document.getElementById('inputMetrado').focus();
            });
        }
    }, 500);

    // ==========================================
    // LÓGICA DE REGISTRO DE PARTIDAS (EXCEL + MANUAL)
    // ==========================================
    function abrirModalRegistrarPartidas() { 
        renderizarTablaCatalogo();
        new bootstrap.Modal(document.getElementById('modalRegistrarPartidas')).show(); 
    }

    document.addEventListener('paste', function(e) {
        const modalEl = document.getElementById('modalRegistrarPartidas');
        if (!modalEl || !modalEl.classList.contains('show')) return; 

        e.preventDefault();
        let pasteData = (e.clipboardData || window.clipboardData).getData('text');
        if(!pasteData.trim()) return;

        const rows = pasteData.split('\\n');
        let countAgregados = 0;

        rows.forEach(row => {
            if(!row.trim()) return;
            const cols = row.split('\\t'); 
            if(cols.length >= 3) {
                window.catalogoMaestro.push({ item: cols[0].trim(), descripcion: cols[1].trim(), unidad: cols[2].trim() });
                countAgregados++;
            } else if (cols.length === 2) {
                window.catalogoMaestro.push({ item: cols[0].trim(), descripcion: cols[1].trim(), unidad: 'GLB' });
                countAgregados++;
            }
        });

        if(countAgregados > 0) {
            renderizarTablaCatalogo();
            document.getElementById('pasteHint').innerHTML = `<i class="bi bi-check-circle-fill text-success fs-4 d-block mb-1"></i> ¡Excelente! Se cargaron ${countAgregados} partidas al catálogo.`;
            document.getElementById('pasteHint').style.borderColor = '#10b981';
            document.getElementById('pasteHint').style.backgroundColor = '#ecfdf5';
        }
    });

    function agregarPartidaManual() {
        const item = document.getElementById('man_item').value.trim();
        const desc = document.getElementById('man_desc').value.trim();
        const und = document.getElementById('man_und').value.trim() || 'GLB';

        if(!desc) { alert("La descripción es obligatoria."); return; }

        window.catalogoMaestro.push({ item: item || '-', descripcion: desc, unidad: und.toUpperCase() });
        
        document.getElementById('man_item').value = '';
        document.getElementById('man_desc').value = '';
        document.getElementById('man_und').value = '';
        document.getElementById('man_item').focus();
        
        renderizarTablaCatalogo();
    }

    function eliminarDelCatalogo(index) {
        window.catalogoMaestro.splice(index, 1);
        renderizarTablaCatalogo();
    }

    function renderizarTablaCatalogo() {
        const tbody = document.getElementById('tbodyCatalogo');
        tbody.innerHTML = window.catalogoMaestro.map((p, idx) => `
            <tr>
                <td class="fw-bold text-dark">${p.item}</td>
                <td class="fw-semibold text-secondary">${p.descripcion}</td>
                <td class="text-center"><span class="badge-unidad bg-light text-dark">${p.unidad}</span></td>
                <td class="text-center"><button type="button" class="btn btn-sm text-danger border-0 p-0" onclick="eliminarDelCatalogo(${idx})"><i class="bi bi-x-circle-fill"></i></button></td>
            </tr>
        `).join('');
        document.getElementById('lbl_total_cat').innerText = window.catalogoMaestro.length;
    }

    // ==========================================
    // BUSCADOR PREDICTIVO (DOBLE ENTER)
    // ==========================================
    function filtrarCatalogo() {
        const input = document.getElementById('buscadorPartidas').value.toLowerCase();
        const dropdown = document.getElementById('dropdownPartidas');
        
        if(input === '' || window.catalogoMaestro.length === 0) {
            dropdown.style.display = 'none';
            return;
        }

        const filtrados = window.catalogoMaestro.filter(p => p.item.toLowerCase().includes(input) || p.descripcion.toLowerCase().includes(input)).slice(0, 8);
        
        if(filtrados.length > 0) {
            dropdown.innerHTML = filtrados.map((p, idx) => `
                <div class="dropdown-item-p ${idx === 0 ? 'selected' : ''}" onclick="abrirMiniModal(${idx})" id="drop_item_${idx}">
                    <span class="badge-item">${p.item}</span>
                    <span class="text-truncate">${p.descripcion}</span>
                    <span class="badge-unidad">${p.unidad}</span>
                </div>
            `).join('');
            dropdown.style.display = 'block';
            indexSeleccionadoDropdown = 0;
            dropdown.dataset.filtrados = JSON.stringify(filtrados);
        } else {
            dropdown.style.display = 'none';
        }
    }

    function manejarTeclasBuscador(e) {
        const dropdown = document.getElementById('dropdownPartidas');
        if(dropdown.style.display === 'none') return;
        
        const items = dropdown.getElementsByClassName('dropdown-item-p');
        
        if (e.key === 'ArrowDown') {
            if (indexSeleccionadoDropdown < items.length - 1) indexSeleccionadoDropdown++;
            actualizarSeleccionDropdown(items);
        } else if (e.key === 'ArrowUp') {
            if (indexSeleccionadoDropdown > 0) indexSeleccionadoDropdown--;
            actualizarSeleccionDropdown(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            abrirMiniModal(indexSeleccionadoDropdown);
        }
    }

    function actualizarSeleccionDropdown(items) {
        for(let i=0; i<items.length; i++) { items[i].classList.remove('selected'); }
        if(items[indexSeleccionadoDropdown]) {
            items[indexSeleccionadoDropdown].classList.add('selected');
            items[indexSeleccionadoDropdown].scrollIntoView({block: 'nearest'});
        }
    }

    // ==========================================
    // MINI MODAL DE METRADO
    // ==========================================
    function abrirMiniModal(indexFiltrado) {
        const dropdown = document.getElementById('dropdownPartidas');
        const filtrados = JSON.parse(dropdown.dataset.filtrados);
        partidaSeleccionadaTemporal = filtrados[indexFiltrado];
        
        // Limpiamos buscador y cerramos menú
        document.getElementById('buscadorPartidas').value = '';
        dropdown.style.display = 'none';

        // Llenamos datos
        document.getElementById('lbl_m_item').innerText = partidaSeleccionadaTemporal.item;
        document.getElementById('lbl_m_desc').innerText = partidaSeleccionadaTemporal.descripcion;
        document.getElementById('lbl_m_und').innerText = partidaSeleccionadaTemporal.unidad;
        document.getElementById('inputMetrado').value = '';

        // Mostramos
        if(!miniModalInstance) miniModalInstance = new bootstrap.Modal(document.getElementById('modalMetrado'));
        miniModalInstance.show();
        
        // El auto-focus ahora es manejado por el evento 'shown.bs.modal' al inicio del script.
    }

    function confirmarMetrado() {
        const metradoVal = document.getElementById('inputMetrado').value;
        
        // Se inyecta en la variable global window.m3_lista para que vistas_residencia lo lea
        window.m3_lista.push({
            item: partidaSeleccionadaTemporal.item,
            descripcion: partidaSeleccionadaTemporal.descripcion,
            unidad: partidaSeleccionadaTemporal.unidad,
            metrado: metradoVal !== '' ? parseFloat(metradoVal).toFixed(2) : ''
        });

        miniModalInstance.hide();
        renderizarPartidasEjecutadas();
        document.getElementById('v_partidas').value = "lleno"; 
        
        // Escribe directamente en el Cuaderno Físico
        if (typeof sincronizarDatos === "function") sincronizarDatos();
        
        // Devuelve el cursor al buscador principal
        setTimeout(() => { document.getElementById('buscadorPartidas').focus(); }, 300);
    }

    function eliminarPartidaEjecutada(index) { 
        window.m3_lista.splice(index, 1); 
        if(window.m3_lista.length === 0) document.getElementById('v_partidas').value = ""; 
        renderizarPartidasEjecutadas(); 
        if (typeof sincronizarDatos === "function") sincronizarDatos(); 
    }

    function renderizarPartidasEjecutadas() {
        const container = document.getElementById('listaPartidasAgregadas');
        container.innerHTML = window.m3_lista.map((p, index) => `
            <div class="bg-white border rounded-3 p-2 d-flex justify-content-between align-items-center shadow-sm" style="border-left: 4px solid #0263a0 !important;">
                <div class="d-flex align-items-center gap-2 text-truncate" style="max-width: 350px;">
                    <span class="badge-item">${p.item}</span>
                    <span class="small fw-semibold text-truncate" title="${p.descripcion}">${p.descripcion}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="fw-bold text-dark fs-6">${p.metrado ? p.metrado : '-'} <small class="text-muted" style="font-size:10px;">${p.metrado ? p.unidad : ''}</small></span>
                    <button type="button" class="btn btn-sm text-danger border-0 ms-2" onclick="eliminarPartidaEjecutada(${index})"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
