# =========================================================
# mod_04_mayor_metrado.py
# Módulo: 4.- Partidas de Mayor Metrado
# =========================================================

from flask import Blueprint


mod_04_bp = Blueprint("mod_04_mayor_metrado", __name__)

MAYOR_METRADO_HTML = """
<style>
    .m4-dropdown { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 14px 14px; max-height: 220px; overflow-y: auto; z-index: 1000; box-shadow: 0 14px 32px rgba(15,23,42,0.12); display: none; }
    .m4-option { padding: 11px 14px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 10px; align-items: center; }
    .m4-option:hover, .m4-option.selected { background: #f0f9ff; color: #0263a0; font-weight: 700; }
    .m4-badge { background: #0f172a; color: #fff; padding: 4px 8px; border-radius: 7px; font-size: 11px; font-weight: 800; white-space: nowrap; }
    .m4-und { background: #e2e8f0; color: #475569; padding: 4px 8px; border-radius: 7px; font-size: 11px; font-weight: 800; white-space: nowrap; margin-left: auto; }
    .m4-card { background: #fff; border: 1px solid #e2e8f0; border-left: 4px solid #0ea5e9 !important; border-radius: 14px; padding: 10px 12px; box-shadow: 0 8px 22px rgba(15,23,42,0.05); }
    .m4-card-desc { font-size: 12px; line-height: 1.25; white-space: normal; }
</style>

<div class="step-view" id="step4">
    <div class="step-title">4.- Partidas de Mayor Metrado</div>
    <p class="text-muted small mb-3">Seleccione una partida del catálogo, escriba el mayor metrado y presione <b>Enter</b>. Registro individual, sin carga masiva.</p>

    <div class="position-relative mb-4">
        <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" id="m4_buscador" placeholder="Buscar partida de mayor metrado..." autocomplete="off" onkeyup="m4_teclas(event)" onfocus="m4_filtrar()" oninput="m4_filtrar()">
        </div>
        <div class="m4-dropdown" id="m4_dropdown"></div>
    </div>

    <div id="m4_lista_ui" class="d-flex flex-column gap-2 mb-3"></div>
    <input type="hidden" id="v_mayor_m_status" class="req-step4" value="">
</div>

<div class="modal fade" id="m4_modal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content" style="border-radius: 22px; border: 2px solid #0ea5e9; box-shadow: 0 22px 45px rgba(14,165,233,0.18);">
            <div class="modal-body p-4 text-center">
                <span class="m4-badge mb-2 d-inline-block" id="m4_lbl_item">00.00</span>
                <h6 class="fw-bold text-dark mb-3" id="m4_lbl_desc" style="line-height:1.25; font-size:13px;">Descripción</h6>
                <div class="input-group input-group-lg mb-2 shadow-sm">
                    <input type="number" step="0.01" class="form-control text-center fw-bold" id="m4_input" placeholder="Mayor metrado" onkeydown="if(event.key==='Enter'){event.preventDefault(); m4_guardar();}">
                    <span class="input-group-text bg-white fw-bold text-primary" id="m4_lbl_und">UND</span>
                </div>
                <p class="small text-muted mb-0">Presione <b>Enter</b> para guardar y continuar.</p>
            </div>
        </div>
    </div>
</div>

<script>
    setTimeout(() => {
        const modal = document.getElementById('m4_modal');
        if(modal && modal.parentNode !== document.body) {
            document.body.appendChild(modal);
            modal.addEventListener('shown.bs.modal', function () {
                document.getElementById('m4_input').focus();
            });
        }
    }, 500);

    window.m4_lista = window.m4_lista || [];
    let m4_temp = null;
    let m4_idx = -1;
    let m4_modal_inst = null;

    function m4_filtrar() {
        const val = document.getElementById('m4_buscador').value.toLowerCase();
        const drop = document.getElementById('m4_dropdown');

        if(val === '' || !window.catalogoMaestro || window.catalogoMaestro.length === 0) {
            drop.style.display = 'none';
            return;
        }

        const filtrados = window.catalogoMaestro.filter(p => p.item.toLowerCase().includes(val) || p.descripcion.toLowerCase().includes(val)).slice(0, 8);
        if(filtrados.length === 0) {
            drop.style.display = 'none';
            return;
        }

        drop.innerHTML = filtrados.map((p, i) => `
            <div class="m4-option ${i === 0 ? 'selected' : ''}" onclick="m4_abrir(${i})">
                <span class="m4-badge">${p.item}</span>
                <span class="text-truncate">${p.descripcion}</span>
                <span class="m4-und">${p.unidad}</span>
            </div>
        `).join('');
        drop.dataset.filt = JSON.stringify(filtrados);
        drop.style.display = 'block';
        m4_idx = 0;
    }

    function m4_teclas(e) {
        const drop = document.getElementById('m4_dropdown');
        const items = drop.getElementsByClassName('m4-option');
        if(e.key === 'Enter') {
            e.preventDefault();
            if(drop.style.display === 'block' && items.length > 0) m4_abrir(m4_idx);
        } else if(e.key === 'ArrowDown' && drop.style.display === 'block') {
            if(m4_idx < items.length - 1) m4_idx++;
            m4_select(items);
        } else if(e.key === 'ArrowUp' && drop.style.display === 'block') {
            if(m4_idx > 0) m4_idx--;
            m4_select(items);
        }
    }

    function m4_select(items) {
        for(let i = 0; i < items.length; i++) items[i].classList.remove('selected');
        if(items[m4_idx]) {
            items[m4_idx].classList.add('selected');
            items[m4_idx].scrollIntoView({block: 'nearest'});
        }
    }

    function m4_abrir(idx) {
        const filtrados = JSON.parse(document.getElementById('m4_dropdown').dataset.filt);
        m4_temp = filtrados[idx];
        document.getElementById('m4_buscador').value = '';
        document.getElementById('m4_dropdown').style.display = 'none';
        document.getElementById('m4_lbl_item').innerText = m4_temp.item;
        document.getElementById('m4_lbl_desc').innerText = m4_temp.descripcion;
        document.getElementById('m4_lbl_und').innerText = m4_temp.unidad;
        document.getElementById('m4_input').value = '';
        if(!m4_modal_inst) m4_modal_inst = new bootstrap.Modal(document.getElementById('m4_modal'));
        m4_modal_inst.show();
    }

    function m4_guardar() {
        const metrado = document.getElementById('m4_input').value;
        if(!m4_temp) return;

        window.m4_lista.push({
            item: m4_temp.item,
            descripcion: m4_temp.descripcion,
            unidad: m4_temp.unidad,
            metrado: metrado !== '' ? parseFloat(metrado).toFixed(2) : ''
        });

        m4_modal_inst.hide();
        m4_render();
        document.getElementById('v_mayor_m_status').value = 'lleno';
        if(typeof sincronizarDatos === 'function') sincronizarDatos();
        setTimeout(() => document.getElementById('m4_buscador').focus(), 250);
    }

    function m4_del(idx) {
        window.m4_lista.splice(idx, 1);
        if(window.m4_lista.length === 0) document.getElementById('v_mayor_m_status').value = '';
        m4_render();
        if(typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    function m4_render() {
        const container = document.getElementById('m4_lista_ui');
        container.innerHTML = window.m4_lista.map((p, index) => `
            <div class="m4-card d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center gap-2" style="max-width: 410px;">
                    <span class="m4-badge">${p.item}</span>
                    <span class="fw-semibold text-dark m4-card-desc" title="${p.descripcion}">${p.descripcion}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="fw-bold text-primary">${p.metrado || '-'} <small class="text-muted">${p.metrado ? p.unidad : ''}</small></span>
                    <button type="button" class="btn btn-sm text-danger border-0" onclick="m4_del(${index})"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
