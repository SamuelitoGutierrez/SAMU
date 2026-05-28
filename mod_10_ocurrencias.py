OCURRENCIAS_HTML = """
<style>
    #step10 { border-radius: 24px; padding: 22px; border: 1px solid #fecaca; background: linear-gradient(180deg, #fff1f2 0%, #ffffff 48%); }
    .m10-layout { display: grid; gap: 14px; }
    .m10-panel { border: 1px solid #fee2e2; border-radius: 22px; background: rgba(255,255,255,.92); padding: 16px; box-shadow: 0 16px 34px rgba(190,18,60,.08); }
    .m10-tabs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .m10-tab { border: 1px solid #fecaca; background: #fff; color: #9f1239; border-radius: 18px; padding: 14px 14px 14px 48px; min-height: 68px; position: relative; text-align: left; font-size: 12px; font-weight: 900; transition: .2s ease; box-shadow: 0 10px 24px rgba(15,23,42,.05); }
    .m10-tab i { position: absolute; left: 14px; top: 16px; width: 24px; height: 24px; border-radius: 12px; display: grid; place-items: center; background: #fff1f2; }
    .m10-tab small { display: block; margin-top: 3px; font-size: 10px; font-weight: 700; opacity: .72; }
    .m10-tab.active { color: #fff; transform: translateY(-1px); box-shadow: 0 16px 32px rgba(190,18,60,.18); }
    .m10-tab.ocurrencia.active { background: linear-gradient(135deg, #9f1239, #fb7185); border-color: #fb7185; }
    .m10-tab.conocimiento.active { background: linear-gradient(135deg, #075985, #38bdf8); border-color: #38bdf8; }
    .m10-editor { border: 1px solid #fecaca; border-radius: 18px; background: #fff; padding: 12px; }
    .m10-editor textarea { width: 100%; min-height: 170px; border: 0; outline: 0; resize: vertical; font-size: 13px; line-height: 1.55; color: #334155; }
    .m10-history { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .m10-card { border: 1px solid #e2e8f0; border-radius: 18px; background: #f8fafc; padding: 12px; min-height: 92px; }
    .m10-card h6 { margin: 0 0 6px; font-size: 11px; font-weight: 900; color: #475569; text-transform: uppercase; letter-spacing: .35px; }
    .m10-card p { margin: 0; font-size: 12px; color: #64748b; line-height: 1.45; white-space: pre-wrap; }
    .m10-preview { border-radius: 16px; min-height: 96px; resize: vertical; font-size: 12px; background: #f8fafc; }
    .m10-actions { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .m10-action-btn { border: none; border-radius: 18px; padding: 14px 16px; color: #fff; font-size: 12px; font-weight: 900; box-shadow: 0 14px 30px rgba(15,23,42,.12); transition: .2s ease; }
    .m10-action-btn:hover { transform: translateY(-2px); }
    .m10-action-btn.draft { background: linear-gradient(135deg, #b45309, #f59e0b); }
    .m10-action-btn.close-seat { background: linear-gradient(135deg, #166534, #22c55e); }
    @media (max-width: 768px) { .m10-tabs, .m10-history { grid-template-columns: 1fr; } }
</style>

<div class="step-view" id="step10">
    <div class="step-title text-danger">10.- Ocurrencias, conocimientos y otros</div>
    <div class="m10-layout">
        <div class="m10-panel">
            <div class="m10-tabs">
                <button type="button" class="m10-tab ocurrencia active" id="m10_tab_ocurrencia" onclick="m10_tipo('Ocurrencia')"><i class="bi bi-exclamation-triangle-fill"></i> Ocurrencia<small>Hechos relevantes del día</small></button>
                <button type="button" class="m10-tab conocimiento" id="m10_tab_conocimiento" onclick="m10_tipo('Conocimiento')"><i class="bi bi-info-circle-fill"></i> Conocimiento<small>Comunicaciones o constancias</small></button>
            </div>
        </div>

        <div class="m10-panel">
            <div class="m10-editor">
                <textarea id="m10_texto" placeholder="Escriba o pegue aquí la ocurrencia, conocimiento u otro registro..." oninput="m10_sincronizar()" onpaste="setTimeout(m10_sincronizar, 50)"></textarea>
            </div>
        </div>

        <div class="m10-panel">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="m-0 fw-bold text-muted text-uppercase" style="font-size:11px; letter-spacing:.35px;">Dos asentados anteriores</h6>
                <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill fw-bold" onclick="m10_render_historial()">Actualizar</button>
            </div>
            <div class="m10-history" id="m10_historial"></div>
        </div>

        <label class="form-label small fw-bold text-muted">Texto que pasará al cuaderno</label>
        <textarea class="form-control border-danger req-step10 m10-preview" id="v_ocurrencia" readonly placeholder="Aquí se generará la ocurrencia o conocimiento..."></textarea>

        <div class="m10-panel">
            <div class="m10-actions">
                <button type="button" class="m10-action-btn draft" onclick="if(typeof guardarBorradorAsiento === 'function') guardarBorradorAsiento();">
                    <i class="bi bi-save2 me-1"></i> Guardar como borrador
                </button>
                <button type="button" class="m10-action-btn close-seat" onclick="if(typeof cerrarAsiento === 'function') cerrarAsiento();">
                    <i class="bi bi-lock-fill me-1"></i> Cerrar asiento
                </button>
            </div>
        </div>
    </div>
</div>

<script>
    window.m10_tipo_actual = window.m10_tipo_actual || 'Ocurrencia';

    function m10_escape(texto) {
        return String(texto || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    }

    function m10_fecha_actual() {
        const fechaCuaderno = document.getElementById('lbl_hoja_fecha');
        const fechaModal = document.getElementById('initFecha');
        return (fechaCuaderno && fechaCuaderno.textContent && fechaCuaderno.textContent !== '--')
            ? fechaCuaderno.textContent.trim()
            : (fechaModal ? fechaModal.value : new Date().toISOString().slice(0, 10));
    }

    function m10_tipo(tipo) {
        window.m10_tipo_actual = tipo;
        document.getElementById('m10_tab_ocurrencia').classList.toggle('active', tipo === 'Ocurrencia');
        document.getElementById('m10_tab_conocimiento').classList.toggle('active', tipo === 'Conocimiento');
        m10_sincronizar();
    }

    function m10_historial_guardado() {
        try { return JSON.parse(localStorage.getItem('samu_m10_historial') || '[]'); }
        catch (e) { return []; }
    }

    function m10_guardar_historial(texto) {
        const limpio = String(texto || '').trim();
        if (!limpio) return;
        const fecha = m10_fecha_actual();
        let historial = m10_historial_guardado().filter(item => item.fecha !== fecha);
        historial.push({ fecha, tipo: window.m10_tipo_actual, texto: limpio });
        historial = historial.slice(-20);
        localStorage.setItem('samu_m10_historial', JSON.stringify(historial));
    }

    function m10_render_historial() {
        const fecha = m10_fecha_actual();
        const recientes = m10_historial_guardado().filter(item => item.fecha !== fecha).slice(-2).reverse();
        const cont = document.getElementById('m10_historial');
        if (recientes.length === 0) {
            cont.innerHTML = `<div class="m10-card"><h6>Sin registros previos</h6><p>Aquí aparecerán los dos asentados anteriores registrados en este equipo.</p></div>`;
            return;
        }
        cont.innerHTML = recientes.map(item => `
            <div class="m10-card">
                <h6>${m10_escape(item.fecha)} - ${m10_escape(item.tipo)}</h6>
                <p>${m10_escape(item.texto)}</p>
            </div>
        `).join('');
    }

    function m10_sincronizar() {
        const texto = String(document.getElementById('m10_texto').value || '').trim();
        const salida = texto ? `* ${window.m10_tipo_actual}:\\n${texto}` : '';
        document.getElementById('v_ocurrencia').value = salida;
        m10_guardar_historial(texto);
        m10_render_historial();
        if (typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    setTimeout(() => {
        m10_render_historial();
        m10_sincronizar();
    }, 300);
</script>
"""
