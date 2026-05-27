# =========================================================
# mod_05_sub_partidas.py
# Módulo: 5.- Sub Partidas (Doble Enter + Metrado Opcional)
# =========================================================

from flask import Blueprint

mod_05_bp = Blueprint('mod_05_sub_partidas', __name__)

SUB_PARTIDAS_HTML = """
<style>
    /* Estilos aislados para el buscador predictivo del Módulo 5 */
    .dropdown-partidas { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 12px 12px; max-height: 200px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: none; }
    .dropdown-item-p { padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 10px; align-items: center; }
    .dropdown-item-p:hover, .dropdown-item-p.selected { background: #f0f9ff; color: #0263a0; font-weight: 600; }
    .badge-item { background: #1e293b; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; }
    .badge-unidad { background: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; margin-left: auto;}
</style>

<div class="step-view" id="step5">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">5.- Sub Partidas Ejecutadas</div>
        <button type="button" class="btn btn-sm btn-outline-success rounded-pill fw-bold shadow-sm" onclick="abrirCatalogoGlobal()">
            <i class="bi bi-journal-text"></i> Base Global de Partidas
        </button>
    </div>
    
    <p class="text-muted small mb-3">Busque la sub partida ejecutada y presione <b>Enter</b>. Digite el metrado y presione <b>Enter</b> nuevamente. <span class="text-primary fw-bold">(El metrado es opcional).</span></p>
    
    <div class="position-relative mb-4">
        <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" id="m5_buscador" placeholder="Ej: 07.01 o Perfilado..." autocomplete="off" onkeyup="m5_teclas(event)" onfocus="m5_filtrar()" oninput="m5_filtrar()">
        </div>
        <div class="dropdown-partidas" id="m5_dropdown"></div>
    </div>
    
    <div id="m5_lista_ui" class="d-flex flex-column gap-2 mb-3"></div>
    <input type="hidden" id="v_sub_p_status" class="req-step5" value="">
</div>

<div class="modal fade" id="m5_modal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content" style="border-radius: 20px; border: 2px solid #0263a0; box-shadow: 0 20px 40px rgba(2,99,160,0.15);">
            <div class="modal-body p-4 text-center">
                <div class="badge-item mb-2" id="m5_lbl_item">00.00</div>
                <h6 class="fw-bold text-dark mb-3" id="m5_lbl_desc" style="line-height: 1.3;">Descripción de la Sub Partida</h6>
                
                <div class="input-group input-group-lg mb-2 shadow-sm">
                    <input type="number" step="0.01" class="form-control text-center fw-bold" id="m5_input" placeholder="Opcional" onkeydown="if(event.key==='Enter'){event.preventDefault(); m5_guardar();}">
                    <span class="input-group-text bg-white fw-bold text-primary" id="m5_lbl_und">UND</span>
                </div>
                <p class="small text-muted mb-0">Presione <b>Enter</b> para guardar.</p>
            </div>
        </div>
    </div>
</div>

<script>
    // Enganche al DOM para mover el modal y forzar Auto-Focus
    setTimeout(() => {
        const mMet5 = document.getElementById('m5_modal');
        if(mMet5 && mMet5.parentNode !== document.body) {
            document.body.appendChild(mMet5);
            
            // Evento oficial de Bootstrap para enfocar el cursor sin dar click
            mMet5.addEventListener('shown.bs.modal', function () {
                document.getElementById('m5_input').focus();
            });
        }
    }, 500);

    // Variables aisladas para el Módulo 5
    window.m5_lista = window.m5_lista || [];
    let m5_temp = null;
    let m5_idx = -1;
    let m5_modal_inst = null;

    // Buscador y Filtro M5
    function m5_filtrar() {
        const val = document.getElementById('m5_buscador').value.toLowerCase();
        const drop = document.getElementById('m5_dropdown');
        
        if(val === '' || !window.catalogoMaestro || window.catalogoMaestro.length === 0) {
            drop.style.display = 'none';
            return;
        }

        const filt = window.catalogoMaestro.filter(p => p.item.toLowerCase().includes(val) || p.descripcion.toLowerCase().includes(val)).slice(0, 8);
        
        if(filt.length > 0) {
            drop.innerHTML = filt.map((p, i) => `
                <div class="dropdown-item-p ${i === 0 ? 'selected' : ''}" onclick="m5_abrir(${i})">
                    <span class="badge-item">${p.item}</span>
                    <span class="text-truncate">${p.descripcion}</span>
                    <span class="badge-unidad">${p.unidad}</span>
                </div>
            `).join('');
            drop.style.display = 'block';
            m5_idx = 0;
            drop.dataset.filt = JSON.stringify(filt);
        } else {
            drop.style.display = 'none';
        }
    }

    // Navegación por teclado (Flechas y Enter) M5
    function m5_teclas(e) {
        const drop = document.getElementById('m5_dropdown');
        if(drop.style.display === 'none') return;
        
        const items = drop.getElementsByClassName('dropdown-item-p');
        
        if (e.key === 'ArrowDown') {
            if (m5_idx < items.length - 1) m5_idx++;
            m5_select(items);
        } else if (e.key === 'ArrowUp') {
            if (m5_idx > 0) m5_idx--;
            m5_select(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            m5_abrir(m5_idx);
        }
    }

    function m5_select(items) {
        for(let i=0; i<items.length; i++) { items[i].classList.remove('selected'); }
        if(items[m5_idx]) {
            items[m5_idx].classList.add('selected');
            items[m5_idx].scrollIntoView({block: 'nearest'});
        }
    }

    // Abrir Modal de Metrado M5
    function m5_abrir(idx) {
        const f = JSON.parse(document.getElementById('m5_dropdown').dataset.filt);
        m5_temp = f[idx];
        
        document.getElementById('m5_buscador').value = '';
        document.getElementById('m5_dropdown').style.display = 'none';

        document.getElementById('m5_lbl_item').innerText = m5_temp.item;
        document.getElementById('m5_lbl_desc').innerText = m5_temp.descripcion;
        document.getElementById('m5_lbl_und').innerText = m5_temp.unidad;
        document.getElementById('m5_input').value = '';

        if(!m5_modal_inst) m5_modal_inst = new bootstrap.Modal(document.getElementById('m5_modal'));
        m5_modal_inst.show();
    }

    // Guardar (Soporta metrado vacío) M5
    function m5_guardar() {
        const val = document.getElementById('m5_input').value;
        
        if (!window.m5_lista) window.m5_lista = [];
        
        window.m5_lista.push({
            item: m5_temp.item,
            descripcion: m5_temp.descripcion,
            unidad: m5_temp.unidad,
            metrado: val !== '' ? parseFloat(val).toFixed(2) : ''
        });

        m5_modal_inst.hide();
        m5_render();
        document.getElementById('v_sub_p_status').value = "lleno"; 
        
        // Sincronizar con Cuaderno Físico
        if (typeof sincronizarDatos === "function") sincronizarDatos();
        
        // Retornar foco al buscador
        setTimeout(() => { document.getElementById('m5_buscador').focus(); }, 300);
    }

    function m5_del(idx) { 
        window.m5_lista.splice(idx, 1); 
        if(window.m5_lista.length === 0) document.getElementById('v_sub_p_status').value = "";
        m5_render(); 
        if (typeof sincronizarDatos === "function") sincronizarDatos(); 
    }

    // Dibujar tarjetas en pantalla M5
    function m5_render() {
        const container = document.getElementById('m5_lista_ui');
        container.innerHTML = window.m5_lista.map((p, index) => `
            <div class="bg-white border rounded-3 p-2 d-flex justify-content-between align-items-center shadow-sm" style="border-left: 4px solid #0263a0 !important;">
                <div class="d-flex align-items-center gap-2 text-truncate" style="max-width: 350px;">
                    <span class="badge-item">${p.item}</span>
                    <span class="small fw-semibold text-truncate" title="${p.descripcion}">${p.descripcion}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="fw-bold text-dark fs-6">${p.metrado ? p.metrado : '-'} <small class="text-muted" style="font-size:10px;">${p.metrado ? p.unidad : ''}</small></span>
                    <button type="button" class="btn btn-sm text-danger border-0 ms-2" onclick="m5_del(${index})"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
