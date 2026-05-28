MAQUINARIA_HTML = """
<style>
    #step8 { border-radius: 24px; padding: 18px; border: 1px solid #cbd5e1; background: linear-gradient(180deg, #f8fafc 0%, #ffffff 46%); }
    .m8-layout { display: grid; gap: 14px; }
    .m8-panel { border: 1px solid #e2e8f0; border-radius: 22px; background: rgba(255,255,255,0.9); padding: 14px; box-shadow: 0 16px 34px rgba(15,23,42,0.06); }
    .m8-register-toggle { width: 100%; border: none; border-radius: 24px; padding: 18px 20px; color: #fff; background: linear-gradient(135deg, #0f172a, #075985, #0ea5e9); box-shadow: 0 18px 38px rgba(15,23,42,0.18); display: flex; align-items: center; justify-content: space-between; gap: 14px; text-align: left; transition: 0.22s ease; }
    .m8-register-toggle:hover { transform: translateY(-1px); box-shadow: 0 22px 42px rgba(15,23,42,0.22); }
    .m8-register-toggle strong { display: block; font-size: 14px; font-weight: 900; }
    .m8-register-toggle small { display: block; margin-top: 3px; color: rgba(255,255,255,0.78); font-size: 11px; font-weight: 700; }
    .m8-register-toggle i { font-size: 24px; }
    .m8-collapsible { overflow: hidden; max-height: 0; opacity: 0; transform: translateY(-14px); padding-top: 0; padding-bottom: 0; border-width: 0; margin-top: -8px; transition: max-height 0.35s ease, opacity 0.25s ease, transform 0.25s ease, padding 0.25s ease, margin 0.25s ease; }
    .m8-collapsible.active { max-height: 1400px; opacity: 1; transform: translateY(0); padding-top: 14px; padding-bottom: 14px; border-width: 1px; margin-top: 0; }
    .m8-titlebar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
    .m8-titlebar h6 { margin: 0; font-size: 12px; font-weight: 900; color: #334155; text-transform: uppercase; letter-spacing: 0.45px; }
    .m8-actions { display: flex; gap: 9px; flex-wrap: wrap; }
    .m8-btn { border: none; border-radius: 14px; padding: 10px 13px; color: #fff; background: linear-gradient(135deg, #075985, #0ea5e9); font-size: 12px; font-weight: 900; white-space: nowrap; box-shadow: 0 12px 26px rgba(2,132,199,0.16); }
    .m8-btn.secondary { background: linear-gradient(135deg, #475569, #94a3b8); }
    .m8-btn.purple { background: linear-gradient(135deg, #6d28d9, #a78bfa); }
    .m8-category-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .m8-cat { border: 1px solid #cbd5e1; background: #fff; border-radius: 18px; padding: 12px 13px 12px 44px; min-height: 62px; position: relative; text-align: left; color: #475569; font-size: 12px; font-weight: 900; box-shadow: 0 10px 24px rgba(15,23,42,0.05); transition: 0.2s ease; }
    .m8-cat i { position: absolute; top: 14px; left: 13px; width: 24px; height: 24px; display: grid; place-items: center; border-radius: 12px; background: #f1f5f9; font-size: 14px; }
    .m8-cat small { display: block; margin-top: 2px; font-size: 10px; line-height: 1.2; font-weight: 700; opacity: 0.72; }
    .m8-cat.active { color: #fff; transform: translateY(-1px); box-shadow: 0 16px 32px rgba(15,23,42,0.16); }
    .m8-cat.active i { background: rgba(255,255,255,0.18); }
    .m8-cat.gov.active { background: linear-gradient(135deg, #075985, #0ea5e9); border-color: #0ea5e9; }
    .m8-cat.srv.active { background: linear-gradient(135deg, #7c3aed, #a78bfa); border-color: #a78bfa; }
    .m8-form-grid { display: grid; grid-template-columns: 1.25fr 1fr 1fr 1fr 0.65fr 0.95fr auto; gap: 9px; align-items: end; }
    .m8-base-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1.1fr auto; gap: 9px; align-items: end; }
    .m8-class-field { grid-column: 1 / -1; }
    .m8-entity-grid { display: none; grid-template-columns: 1fr; gap: 9px; margin-bottom: 12px; }
    .m8-entity-grid.active { display: grid; }
    .m8-service-field { display: none; }
    .m8-service-field.active { display: block; }
    .m8-contract-grid { display: none; grid-template-columns: 1fr; gap: 9px; margin-bottom: 12px; }
    .m8-contract-grid.active { display: grid; }
    .m8-field label { display: block; margin-bottom: 4px; font-size: 10px; font-weight: 900; color: #64748b; text-transform: uppercase; letter-spacing: 0.35px; }
    .m8-field input, .m8-field select { width: 100%; border: 1px solid #cbd5e1; border-radius: 13px; padding: 9px 10px; outline: none; font-size: 12px; font-weight: 700; background: #f8fafc; }
    .m8-field input:focus, .m8-field select:focus { border-color: #0284c7; background: #fff; box-shadow: 0 0 0 3px rgba(2,132,199,0.11); }
    .m8-paste { border: 2px dashed #cbd5e1; background: #f8fafc; border-radius: 18px; padding: 12px; text-align: center; color: #64748b; font-size: 12px; font-weight: 800; }
    .m8-paste textarea { width: 100%; height: 44px; margin-top: 4px; border: 0; background: transparent; outline: none; resize: none; text-align: center; font-size: 12px; }
    .m8-table-wrap { border: 1px solid #e2e8f0; border-radius: 18px; overflow: hidden; background: #fff; }
    .m8-table { width: 100%; border-collapse: collapse; font-size: 12px; }
    .m8-table th { background: #f1f5f9; color: #475569; padding: 9px 8px; font-size: 10px; font-weight: 900; text-transform: uppercase; border-bottom: 1px solid #cbd5e1; }
    .m8-table td { padding: 8px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
    .m8-table input { width: 100%; border: 1px solid #dbeafe; border-radius: 9px; padding: 6px 7px; font-size: 11px; font-weight: 700; outline: none; background: #fff; }
    .m8-empty { padding: 18px; color: #94a3b8; text-align: center; font-weight: 800; }
    .m8-preview { border-radius: 16px; min-height: 118px; resize: vertical; font-size: 12px; background: #f8fafc; }
    .m8-hidden { display: none; }
    .m8-preview-actions { display: flex; justify-content: flex-end; gap: 8px; padding: 10px; background: #f8fafc; }
    @media (max-width: 992px) { .m8-category-grid, .m8-form-grid, .m8-base-grid, .m8-contract-grid { grid-template-columns: 1fr; } }
</style>

<div class="step-view" id="step8">
    <div class="step-title">8.- Maquinarias, vehículos y equipos</div>
    <div class="m8-layout">
        <button type="button" class="m8-register-toggle" id="m8_registro_toggle" onclick="m8_toggle_registro_base()">
            <span>
                <strong><i class="bi bi-plus-square-fill me-2"></i>Registrar maquinarias, vehículos y equipos</strong>
                <small>Abra este panel para crear la base por clasificación, entidad y pegado masivo.</small>
            </span>
            <i class="bi bi-chevron-down" id="m8_registro_icono"></i>
        </button>

        <div class="m8-panel m8-collapsible" id="m8_registro_base_panel">
            <div class="m8-titlebar">
                <h6><i class="bi bi-bookmark-plus-fill me-1"></i> Base de maquinarias, vehículos y equipos</h6>
                <button type="button" class="m8-btn secondary" onclick="m8_limpiar_base_categoria()"><i class="bi bi-eraser me-1"></i> Limpiar base seleccionada</button>
            </div>
            <div class="m8-entity-grid" id="m8_entidad_registro_box">
                <div class="m8-field"><label>Datos de la entidad</label><input id="m8_nueva_entidad" list="m8_entidades_list" placeholder="Nombre de la entidad / empresa" oninput="m8_entidad_base_cambiada()" onkeydown="m8_enter(event, 'm8_base_nombre')"></div>
            </div>
            <div class="m8-base-grid">
                <div class="m8-field m8-class-field"><label>Clasificación</label><select id="m8_base_cat" onchange="m8_base_categoria_cambio()"><option value="maq_gore">Maquinarias del Gobierno Regional Puno</option><option value="maq_serv">Maquinarias por servicio y/o contrato</option><option value="mov_gore">Movilidades del Gobierno Regional Puno</option><option value="mov_serv">Movilidades por servicio y/o contrato</option><option value="eq_gore">Equipo liviano del Gobierno Regional Puno</option><option value="eq_serv">Equipo liviano por servicio y/o contrato</option></select></div>
                <div class="m8-field"><label>Maquinaria / vehículo / equipo</label><input id="m8_base_nombre" placeholder="Camión volquete" onkeydown="m8_enter(event, 'm8_base_marca')"></div>
                <div class="m8-field"><label>Marca</label><input id="m8_base_marca" placeholder="Volvo" onkeydown="m8_enter(event, 'm8_base_modelo')"></div>
                <div class="m8-field"><label>Modelo, placa o serie</label><input id="m8_base_modelo" placeholder="FMX 6X4 R / EGK-176" onkeydown="m8_enter_guardar_base(event)"></div>
                <button type="button" class="m8-btn purple" onclick="m8_agregar_base()"><i class="bi bi-plus-lg me-1"></i> Registrar maquinaria</button>
            </div>
            <div class="m8-paste mt-3">
                <div><i class="bi bi-clipboard-check me-1"></i> Pegado masivo para la base: maquinaria | marca | modelo, placa o serie. En servicio use primero la entidad seleccionada.</div>
                <textarea id="m8_base_paste" placeholder="Pegar aquí..." onpaste="m8_pegar_base(event)"></textarea>
            </div>
            <div class="m8-table-wrap m8-hidden mt-3" id="m8_base_preview_box">
                <table class="m8-table">
                    <thead><tr><th>Entidad</th><th>Maquinaria</th><th>Marca</th><th>Modelo, placa o serie</th><th></th></tr></thead>
                    <tbody id="m8_base_preview_tbody"></tbody>
                </table>
                <div class="m8-preview-actions">
                    <button type="button" class="m8-btn secondary" onclick="m8_cancelar_base_preview()">Cancelar</button>
                    <button type="button" class="m8-btn purple" onclick="m8_confirmar_base_preview()">Agregar a la base</button>
                </div>
            </div>
        </div>

        <div class="m8-panel">
            <div class="m8-titlebar">
                <h6><i class="bi bi-list-check me-1"></i> Seleccione la clasificación para el registro diario</h6>
                <button type="button" class="m8-btn secondary" onclick="m8_limpiar_categoria()"><i class="bi bi-eraser me-1"></i> Limpiar diario</button>
            </div>
            <div class="m8-category-grid">
                <button type="button" class="m8-cat gov active" id="m8_cat_maq_gore" onclick="m8_cambiar_categoria('maq_gore')"><i class="bi bi-truck"></i> Maquinarias<small>Gobierno Regional Puno</small></button>
                <button type="button" class="m8-cat srv" id="m8_cat_maq_serv" onclick="m8_cambiar_categoria('maq_serv')"><i class="bi bi-file-earmark-text"></i> Maquinarias<small>Servicio y/o contrato</small></button>
                <button type="button" class="m8-cat gov" id="m8_cat_mov_gore" onclick="m8_cambiar_categoria('mov_gore')"><i class="bi bi-car-front"></i> Movilidades<small>Gobierno Regional Puno</small></button>
                <button type="button" class="m8-cat srv" id="m8_cat_mov_serv" onclick="m8_cambiar_categoria('mov_serv')"><i class="bi bi-file-earmark-check"></i> Movilidades<small>Servicio y/o contrato</small></button>
                <button type="button" class="m8-cat gov" id="m8_cat_eq_gore" onclick="m8_cambiar_categoria('eq_gore')"><i class="bi bi-tools"></i> Equipo liviano<small>Gobierno Regional Puno</small></button>
                <button type="button" class="m8-cat srv" id="m8_cat_eq_serv" onclick="m8_cambiar_categoria('eq_serv')"><i class="bi bi-clipboard2-check"></i> Equipo liviano<small>Servicio y/o contrato</small></button>
            </div>
        </div>

        <div class="m8-panel">
            <div class="m8-titlebar"><h6><i class="bi bi-pencil-square me-1"></i> Registro diario de trabajo</h6></div>
            <div class="m8-contract-grid" id="m8_contrato_box">
                <div class="m8-field"><label>Entidad / contratista</label><select id="m8_entidad" onchange="m8_entidad_cambiada()"></select></div>
            </div>
            <datalist id="m8_entidades_list"></datalist>
            <div class="m8-form-grid">
                <div class="m8-field"><label>Seleccionar equipo registrado</label><select id="m8_equipo_select" onchange="m8_usar_equipo()"></select></div>
                <div class="m8-field"><label>Maquinaria</label><input id="m8_nombre" placeholder="Nombre" onkeydown="m8_enter(event, 'm8_marca')"></div>
                <div class="m8-field"><label>Marca</label><input id="m8_marca" placeholder="Marca" onkeydown="m8_enter(event, 'm8_modelo')"></div>
                <div class="m8-field"><label>Placa/serie</label><input id="m8_modelo" placeholder="Modelo / placa / serie" onkeydown="m8_enter(event, 'm8_hm')"></div>
                <div class="m8-field"><label id="m8_medida_label">HM</label><input id="m8_hm" placeholder="08:00 HM" onkeydown="m8_enter(event, 'm8_combustible')"></div>
                <div class="m8-field"><label>Combustible</label><input id="m8_combustible" placeholder="20 GLN Diesel" onkeydown="m8_enter_guardar(event)"></div>
                <button type="button" class="m8-btn" onclick="m8_agregar_actual()"><i class="bi bi-plus-lg me-1"></i> Agregar</button>
            </div>
            <div class="m8-paste mt-3">
                <div id="m8_paste_help"><i class="bi bi-clipboard-check me-1"></i> Pegado masivo diario: maquinaria | marca | placa/serie | HM | combustible</div>
                <textarea id="m8_paste" placeholder="Pegar aquí..." onpaste="m8_pegar_diario(event)"></textarea>
            </div>
            <div class="m8-table-wrap m8-hidden mt-3" id="m8_diario_preview_box">
                <table class="m8-table">
                    <thead><tr><th>Entidad</th><th>Maquinaria</th><th>Marca</th><th>Modelo, placa o serie</th><th id="m8_preview_medida">HM</th><th>Combustible</th><th></th></tr></thead>
                    <tbody id="m8_diario_preview_tbody"></tbody>
                </table>
                <div class="m8-preview-actions">
                    <button type="button" class="m8-btn secondary" onclick="m8_cancelar_diario_preview()">Cancelar</button>
                    <button type="button" class="m8-btn" onclick="m8_confirmar_diario_preview()">Agregar al día</button>
                </div>
            </div>
        </div>

        <div class="m8-table-wrap">
            <table class="m8-table">
                <thead>
                    <tr><th>Maquinaria</th><th>Marca</th><th>Modelo, placa o serie</th><th id="m8_th_medida">HM</th><th>Combustible</th><th></th></tr>
                </thead>
                <tbody id="m8_tbody"></tbody>
            </table>
        </div>

        <div class="m8-table-wrap">
            <table class="m8-table">
                <thead>
                    <tr><th colspan="5">Base registrada de la clasificación seleccionada</th></tr>
                    <tr><th>Entidad</th><th>Maquinaria</th><th>Marca</th><th>Modelo, placa o serie</th><th></th></tr>
                </thead>
                <tbody id="m8_base_tbody"></tbody>
            </table>
        </div>

        <label class="form-label small fw-bold text-muted">Texto que pasará al cuaderno</label>
        <textarea class="form-control req-step8 m8-preview" id="v_maquina" rows="7" readonly placeholder="Aquí se generará la maquinaria del día..."></textarea>
    </div>
</div>

<script>
    window.m8_base = window.m8_base || { maq_gore: [], maq_serv: [], mov_gore: [], mov_serv: [], eq_gore: [], eq_serv: [] };
    window.m8_registros = window.m8_registros || { maq_gore: [], maq_serv: [], mov_gore: [], mov_serv: [], eq_gore: [], eq_serv: [] };
    window.m8_entidad_actual = window.m8_entidad_actual || { maq_serv: '', mov_serv: '', eq_serv: '' };
    window.m8_entidades_registradas = window.m8_entidades_registradas || { maq_serv: [], mov_serv: [], eq_serv: [] };
    window.m8_base_pendientes = window.m8_base_pendientes || [];
    window.m8_diario_pendientes = window.m8_diario_pendientes || [];
    let m8_categoria_actual = 'maq_gore';

    const m8_titulos = {
        maq_gore: '* Maquinarias del Gobierno Regional Puno',
        maq_serv: '* Maquinarias por servicio y/o contrato',
        mov_gore: '* Movilidades del Gobierno Regional Puno',
        mov_serv: '* Movilidades por servicio y/o contrato',
        eq_gore: '* Equipo liviano del Gobierno Regional Puno',
        eq_serv: '* Equipo liviano por servicio y/o contrato'
    };

    function m8_es_servicio(cat = m8_categoria_actual) { return cat.endsWith('_serv'); }
    function m8_texto(valor) { return String(valor || '').replace(/\\s+/g, ' ').trim(); }
    function m8_escape(valor) {
        return m8_texto(valor).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    }
    function m8_item(data) {
        return {
            entidad: m8_texto(data.entidad),
            nombre: m8_texto(data.nombre),
            marca: m8_texto(data.marca),
            modelo: m8_texto(data.modelo),
            hm: m8_texto(data.hm),
            combustible: m8_texto(data.combustible)
        };
    }
    function m8_hm(texto) {
        const t = m8_texto(texto);
        if(!t) return '';
        return /\\bhm\\b/i.test(t) ? t : `${t} HM`;
    }
    function m8_es_movilidad(cat = m8_categoria_actual) {
        return cat.startsWith('mov_');
    }
    function m8_es_equipo_liviano(cat = m8_categoria_actual) {
        return cat.startsWith('eq_');
    }
    function m8_medida(texto, cat = m8_categoria_actual) {
        const t = m8_texto(texto);
        if(!t) return '';
        if(m8_es_movilidad(cat)) return /d[ií]a/i.test(t) ? t : `${t} Día`;
        return /\\bhm\\b/i.test(t) ? t : `${t} HM`;
    }
    function m8_combustible_defecto(cat = m8_categoria_actual) {
        if(cat === 'mov_gore' || m8_es_equipo_liviano(cat)) return 'Gasohol';
        return '';
    }
    function m8_actualizar_campos() {
        const esMovilidad = m8_es_movilidad();
        document.getElementById('m8_medida_label').innerText = esMovilidad ? 'Día' : 'HM';
        document.getElementById('m8_th_medida').innerText = esMovilidad ? 'Día' : 'HM';
        document.getElementById('m8_hm').placeholder = esMovilidad ? '1 Día' : '08:00 HM';
        document.getElementById('m8_paste_help').innerHTML = `<i class="bi bi-clipboard-check me-1"></i> Pegado masivo diario: maquinaria | marca | placa/serie | ${esMovilidad ? 'día' : 'HM'} | combustible`;
        const combustible = document.getElementById('m8_combustible');
        const defecto = m8_combustible_defecto();
        combustible.placeholder = defecto ? '20 GLN Gasohol' : '20 GLN Diesel';
        if(defecto && !m8_texto(combustible.value)) combustible.value = defecto;
    }
    function m8_combustible(texto, cat = m8_categoria_actual) {
        const t = m8_texto(texto);
        if(!t) return '';
        if(/\\b(gln|diesel|gasohol)\\b/i.test(t)) return t;
        if(m8_es_movilidad(cat) || m8_es_equipo_liviano(cat)) return `${t} GLN Gasohol`;
        if(cat.startsWith('maq_')) return `${t} GLN Diesel`;
        return t;
    }
    function m8_compacto(texto) {
        return m8_texto(texto).replace(/\\s+/g, '');
    }
    function m8_base_es_servicio() {
        return m8_es_servicio(document.getElementById('m8_base_cat').value);
    }
    function m8_entidades(cat = m8_categoria_actual) {
        return [...new Set([...(window.m8_entidades_registradas[cat] || []), ...(window.m8_base[cat] || []).map(x => m8_texto(x.entidad))].filter(Boolean))];
    }
    function m8_actualizar_datalist() {
        const entidades = m8_entidades(m8_categoria_actual);
        document.getElementById('m8_entidades_list').innerHTML = entidades.map(e => `<option value="${m8_escape(e)}"></option>`).join('');
        const select = document.getElementById('m8_entidad');
        if(select) {
            const actual = m8_texto(select.value || window.m8_entidad_actual[m8_categoria_actual]);
            select.innerHTML = '<option value="">Seleccione entidad...</option>' + entidades.map(e => `<option value="${m8_escape(e)}">${m8_escape(e)}</option>`).join('');
            if(actual && entidades.some(e => e.toLowerCase() === actual.toLowerCase())) select.value = entidades.find(e => e.toLowerCase() === actual.toLowerCase());
        }
    }
    function m8_base_categoria_cambio() {
        document.getElementById('m8_entidad_registro_box').classList.toggle('active', m8_base_es_servicio());
        if(!m8_base_es_servicio()) document.getElementById('m8_nueva_entidad').value = '';
        m8_render_base();
        m8_refrescar_select();
        m8_actualizar_datalist();
    }

    function m8_cambiar_categoria(cat) {
        m8_guardar_entidad();
        m8_categoria_actual = cat;
        document.getElementById('m8_base_cat').value = cat;
        Object.keys(m8_titulos).forEach(k => {
            const btn = document.getElementById(`m8_cat_${k}`);
            if(btn) btn.classList.toggle('active', k === cat);
        });
        document.getElementById('m8_contrato_box').classList.toggle('active', m8_es_servicio(cat));
        document.getElementById('m8_entidad_registro_box').classList.toggle('active', m8_es_servicio(cat));
        document.getElementById('m8_nueva_entidad').value = window.m8_entidad_actual[cat] || '';
        m8_actualizar_campos();
        m8_actualizar_datalist();
        if(m8_es_servicio(cat)) document.getElementById('m8_entidad').value = window.m8_entidad_actual[cat] || '';
        m8_refrescar_select();
        m8_render_base();
        m8_render();
    }

    function m8_toggle_registro_base() {
        const panel = document.getElementById('m8_registro_base_panel');
        const icono = document.getElementById('m8_registro_icono');
        const abierto = panel.classList.toggle('active');
        icono.className = abierto ? 'bi bi-chevron-up' : 'bi bi-chevron-down';
        if(abierto) {
            setTimeout(() => document.getElementById('m8_base_cat').focus(), 220);
        }
    }

    function m8_guardar_entidad() {
        if(!m8_es_servicio()) return;
        window.m8_entidad_actual[m8_categoria_actual] = m8_texto(document.getElementById('m8_entidad').value);
    }

    function m8_entidad_cambiada() {
        m8_guardar_entidad();
        document.getElementById('m8_nueva_entidad').value = document.getElementById('m8_entidad').value;
        m8_refrescar_select();
        m8_sincronizar();
    }

    function m8_entidad_base_cambiada() {
        const cat = document.getElementById('m8_base_cat').value;
        if(!m8_es_servicio(cat)) return;
        const entidad = m8_texto(document.getElementById('m8_nueva_entidad').value);
        window.m8_entidad_actual[cat] = entidad;
        if(cat === m8_categoria_actual) {
            m8_actualizar_datalist();
            document.getElementById('m8_entidad').value = entidad;
            m8_refrescar_select();
        }
    }

    function m8_agregar_entidad() {
        const cat = document.getElementById('m8_base_cat').value;
        if(!m8_es_servicio(cat)) return;
        const entidad = m8_texto(document.getElementById('m8_nueva_entidad').value);
        if(!entidad) return;
        window.m8_entidades_registradas[cat] = window.m8_entidades_registradas[cat] || [];
        if(!window.m8_entidades_registradas[cat].some(x => x.toLowerCase() === entidad.toLowerCase())) {
            window.m8_entidades_registradas[cat].push(entidad);
        }
        window.m8_entidad_actual[cat] = entidad;
        document.getElementById('m8_nueva_entidad').value = entidad;
        if(cat === m8_categoria_actual) document.getElementById('m8_entidad').value = entidad;
        document.getElementById('m8_nueva_entidad').value = '';
        m8_actualizar_datalist();
        m8_refrescar_select();
        document.getElementById('m8_base_nombre').focus();
    }

    function m8_agregar_base(data = null) {
        const cat = document.getElementById('m8_base_cat').value;
        const item = data ? m8_item(data) : m8_item({
            entidad: document.getElementById('m8_nueva_entidad').value,
            nombre: document.getElementById('m8_base_nombre').value,
            marca: document.getElementById('m8_base_marca').value,
            modelo: document.getElementById('m8_base_modelo').value
        });
        if(!item.nombre) return;
        if(m8_es_servicio(cat) && !item.entidad) return;
        window.m8_base[cat].push({ entidad: m8_es_servicio(cat) ? item.entidad : '', nombre: item.nombre, marca: item.marca, modelo: item.modelo });
        if(!data) {
            document.getElementById('m8_base_nombre').value = '';
            document.getElementById('m8_base_marca').value = '';
            document.getElementById('m8_base_modelo').value = '';
            document.getElementById('m8_base_nombre').focus();
        }
        if(m8_es_servicio(cat)) {
            window.m8_entidades_registradas[cat] = window.m8_entidades_registradas[cat] || [];
            if(!window.m8_entidades_registradas[cat].some(x => x.toLowerCase() === item.entidad.toLowerCase())) {
                window.m8_entidades_registradas[cat].push(item.entidad);
            }
            window.m8_entidad_actual[cat] = item.entidad;
            if(cat === m8_categoria_actual) document.getElementById('m8_entidad').value = item.entidad;
        }
        m8_actualizar_datalist();
        m8_refrescar_select();
        m8_render_base();
    }

    function m8_pegar_base(event) {
        event.preventDefault();
        const data = (event.clipboardData || window.clipboardData).getData('text');
        const cat = document.getElementById('m8_base_cat').value;
        window.m8_base_pendientes = [];
        data.split('\\n').forEach(row => {
            const cols = row.split('\\t').map(m8_texto);
            if(cols[0]) {
                if(m8_es_servicio(cat)) {
                    const entidadActual = m8_texto(document.getElementById('m8_nueva_entidad').value);
                    if(entidadActual) {
                        window.m8_base_pendientes.push(m8_item({ entidad: entidadActual, nombre: cols[0], marca: cols[1], modelo: cols[2] }));
                    } else {
                        window.m8_base_pendientes.push(m8_item({ entidad: cols[0], nombre: cols[1], marca: cols[2], modelo: cols[3] }));
                    }
                } else {
                    window.m8_base_pendientes.push(m8_item({ nombre: cols[0], marca: cols[1], modelo: cols[2] }));
                }
            }
        });
        const paste = document.getElementById('m8_base_paste');
        paste.value = window.m8_base_pendientes.length ? `Revise ${window.m8_base_pendientes.length} registros antes de agregar.` : '';
        m8_render_base_preview();
    }

    function m8_refrescar_select() {
        const select = document.getElementById('m8_equipo_select');
        const entidad = m8_texto(document.getElementById('m8_entidad').value);
        const lista = (window.m8_base[m8_categoria_actual] || []).filter(item => !m8_es_servicio() || m8_texto(item.entidad) === entidad);
        if(m8_es_servicio() && !entidad) {
            select.innerHTML = '<option value="">Primero escriba o seleccione una entidad...</option>';
            select.dataset.items = '[]';
            return;
        }
        select.innerHTML = '<option value="">Seleccione o escriba manualmente...</option>' + lista.map((item, idx) => `<option value="${idx}">${m8_escape(item.nombre)} | ${m8_escape(item.marca)} | ${m8_escape(item.modelo)}</option>`).join('');
        select.dataset.items = JSON.stringify(lista);
    }

    function m8_usar_equipo() {
        const idx = document.getElementById('m8_equipo_select').value;
        const items = JSON.parse(document.getElementById('m8_equipo_select').dataset.items || '[]');
        const item = items[idx];
        if(!item) return;
        document.getElementById('m8_nombre').value = item.nombre || '';
        document.getElementById('m8_marca').value = item.marca || '';
        document.getElementById('m8_modelo').value = item.modelo || '';
        const defecto = m8_combustible_defecto();
        if(defecto && !m8_texto(document.getElementById('m8_combustible').value)) document.getElementById('m8_combustible').value = defecto;
        document.getElementById('m8_hm').focus();
    }

    function m8_agregar_actual(data = null) {
        const item = data ? m8_item(data) : m8_item({
            entidad: document.getElementById('m8_entidad').value,
            nombre: document.getElementById('m8_nombre').value,
            marca: document.getElementById('m8_marca').value,
            modelo: document.getElementById('m8_modelo').value,
            hm: document.getElementById('m8_hm').value,
            combustible: document.getElementById('m8_combustible').value || m8_combustible_defecto()
        });
        if(!item.nombre) return;
        if(m8_es_servicio()) item.entidad = m8_texto(item.entidad || document.getElementById('m8_entidad').value);
        if(m8_es_servicio() && !item.entidad) return;
        window.m8_registros[m8_categoria_actual].push(item);
        if(!data) {
            ['m8_nombre', 'm8_marca', 'm8_modelo', 'm8_hm', 'm8_combustible'].forEach(id => document.getElementById(id).value = '');
            const defecto = m8_combustible_defecto();
            if(defecto) document.getElementById('m8_combustible').value = defecto;
            document.getElementById('m8_equipo_select').value = '';
            document.getElementById('m8_equipo_select').focus();
        }
        m8_render();
    }

    function m8_pegar_diario(event) {
        event.preventDefault();
        const data = (event.clipboardData || window.clipboardData).getData('text');
        window.m8_diario_pendientes = [];
        data.split('\\n').forEach(row => {
            const cols = row.split('\\t').map(m8_texto);
            if(cols[0]) {
                window.m8_diario_pendientes.push(m8_item({ entidad: document.getElementById('m8_entidad').value, nombre: cols[0], marca: cols[1], modelo: cols[2], hm: cols[3], combustible: cols[4] || m8_combustible_defecto() }));
            }
        });
        const paste = document.getElementById('m8_paste');
        paste.value = window.m8_diario_pendientes.length ? `Revise ${window.m8_diario_pendientes.length} registros antes de agregar.` : '';
        m8_render_diario_preview();
    }

    function m8_formatear(item, cat = m8_categoria_actual) {
        return [item.nombre, m8_compacto(item.marca), m8_compacto(item.modelo), m8_medida(item.hm, cat), m8_combustible(item.combustible || m8_combustible_defecto(cat), cat)].map(m8_texto).join('\\t');
    }

    function m8_sincronizar() {
        m8_guardar_entidad();
        const bloques = [];
        Object.keys(m8_titulos).forEach(cat => {
            const lista = window.m8_registros[cat] || [];
            if(lista.length === 0) return;
            const bloque = [m8_titulos[cat]];
            if(m8_es_servicio(cat)) {
                const grupos = {};
                lista.forEach(item => {
                    const entidad = m8_texto(item.entidad) || 'servicio y/o contrato';
                    if(!grupos[entidad]) grupos[entidad] = [];
                    grupos[entidad].push(item);
                });
                Object.keys(grupos).forEach(entidad => {
                    bloque.push(`- ${entidad}`);
                    grupos[entidad].forEach(item => bloque.push(`${m8_formatear(item, cat)}`));
                });
                bloques.push(bloque.join('\\n'));
                return;
            }
            lista.forEach(item => bloque.push(`${m8_formatear(item, cat)}`));
            bloques.push(bloque.join('\\n'));
        });
        document.getElementById('v_maquina').value = bloques.join('\\n');
        if(typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    function m8_render() {
        const lista = window.m8_registros[m8_categoria_actual] || [];
        const tbody = document.getElementById('m8_tbody');
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6"><div class="m8-empty">No hay registros diarios en esta clasificación.</div></td></tr>';
            m8_sincronizar();
            return;
        }
        tbody.innerHTML = lista.map((item, idx) => `
            <tr><td>${m8_escape(item.nombre)}</td><td>${m8_escape(item.marca)}</td><td>${m8_escape(item.modelo)}</td><td>${m8_escape(m8_medida(item.hm))}</td><td>${m8_escape(m8_combustible(item.combustible || m8_combustible_defecto()))}</td><td class="text-end"><button type="button" class="btn btn-sm text-danger border-0" onclick="m8_eliminar(${idx})"><i class="bi bi-trash"></i></button></td></tr>
        `).join('');
        m8_sincronizar();
    }

    function m8_render_base() {
        const cat = document.getElementById('m8_base_cat').value;
        const lista = window.m8_base[cat] || [];
        const tbody = document.getElementById('m8_base_tbody');
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5"><div class="m8-empty">No hay equipos en la base de esta clasificación.</div></td></tr>';
            return;
        }
        tbody.innerHTML = lista.map((item, idx) => `
            <tr><td>${m8_escape(item.entidad)}</td><td>${m8_escape(item.nombre)}</td><td>${m8_escape(item.marca)}</td><td>${m8_escape(item.modelo)}</td><td class="text-end"><button type="button" class="btn btn-sm text-danger border-0" onclick="m8_eliminar_base(${idx})"><i class="bi bi-trash"></i></button></td></tr>
        `).join('');
    }

    function m8_eliminar(idx) {
        window.m8_registros[m8_categoria_actual].splice(idx, 1);
        m8_render();
    }

    function m8_eliminar_base(idx) {
        const cat = document.getElementById('m8_base_cat').value;
        window.m8_base[cat].splice(idx, 1);
        m8_refrescar_select();
        m8_render_base();
    }

    function m8_limpiar_categoria() {
        window.m8_registros[m8_categoria_actual] = [];
        m8_render();
    }

    function m8_limpiar_base_categoria() {
        const cat = document.getElementById('m8_base_cat').value;
        window.m8_base[cat] = [];
        m8_refrescar_select();
        m8_render_base();
    }

    function m8_enter(event, nextId) {
        if(event.key !== 'Enter') return;
        event.preventDefault();
        document.getElementById(nextId).focus();
    }
    function m8_enter_guardar(event) {
        if(event.key !== 'Enter') return;
        event.preventDefault();
        m8_agregar_actual();
    }
    function m8_enter_guardar_base(event) {
        if(event.key !== 'Enter') return;
        event.preventDefault();
        m8_agregar_base();
    }
    function m8_enter_guardar_entidad(event) {
        if(event.key !== 'Enter') return;
        event.preventDefault();
        m8_agregar_entidad();
    }

    function m8_actualizar_pendiente(tipo, idx, campo, valor) {
        const lista = tipo === 'base' ? window.m8_base_pendientes : window.m8_diario_pendientes;
        if(!lista[idx]) return;
        lista[idx][campo] = m8_texto(valor);
    }

    function m8_eliminar_pendiente(tipo, idx) {
        if(tipo === 'base') {
            window.m8_base_pendientes.splice(idx, 1);
            m8_render_base_preview();
        } else {
            window.m8_diario_pendientes.splice(idx, 1);
            m8_render_diario_preview();
        }
    }

    function m8_render_base_preview() {
        const box = document.getElementById('m8_base_preview_box');
        const tbody = document.getElementById('m8_base_preview_tbody');
        const esServicio = m8_base_es_servicio();
        box.classList.toggle('m8-hidden', window.m8_base_pendientes.length === 0);
        tbody.innerHTML = window.m8_base_pendientes.map((item, idx) => `
            <tr>
                <td><input ${esServicio ? '' : 'disabled'} value="${m8_escape(item.entidad)}" oninput="m8_actualizar_pendiente('base', ${idx}, 'entidad', this.value)"></td>
                <td><input value="${m8_escape(item.nombre)}" oninput="m8_actualizar_pendiente('base', ${idx}, 'nombre', this.value)"></td>
                <td><input value="${m8_escape(item.marca)}" oninput="m8_actualizar_pendiente('base', ${idx}, 'marca', this.value)"></td>
                <td><input value="${m8_escape(item.modelo)}" oninput="m8_actualizar_pendiente('base', ${idx}, 'modelo', this.value)"></td>
                <td class="text-end"><button type="button" class="btn btn-sm text-danger border-0" onclick="m8_eliminar_pendiente('base', ${idx})"><i class="bi bi-trash"></i></button></td>
            </tr>
        `).join('');
    }

    function m8_confirmar_base_preview() {
        const pendientes = [...window.m8_base_pendientes];
        pendientes.forEach(item => m8_agregar_base(item));
        window.m8_base_pendientes = [];
        document.getElementById('m8_base_paste').value = '';
        document.getElementById('m8_nueva_entidad').value = '';
        ['m8_base_nombre', 'm8_base_marca', 'm8_base_modelo'].forEach(id => document.getElementById(id).value = '');
        m8_render_base_preview();
    }

    function m8_cancelar_base_preview() {
        window.m8_base_pendientes = [];
        document.getElementById('m8_base_paste').value = '';
        m8_render_base_preview();
    }

    function m8_render_diario_preview() {
        const box = document.getElementById('m8_diario_preview_box');
        const tbody = document.getElementById('m8_diario_preview_tbody');
        document.getElementById('m8_preview_medida').innerText = m8_es_movilidad() ? 'Día' : 'HM';
        box.classList.toggle('m8-hidden', window.m8_diario_pendientes.length === 0);
        tbody.innerHTML = window.m8_diario_pendientes.map((item, idx) => `
            <tr>
                <td><input ${m8_es_servicio() ? '' : 'disabled'} value="${m8_escape(item.entidad)}" oninput="m8_actualizar_pendiente('diario', ${idx}, 'entidad', this.value)"></td>
                <td><input value="${m8_escape(item.nombre)}" oninput="m8_actualizar_pendiente('diario', ${idx}, 'nombre', this.value)"></td>
                <td><input value="${m8_escape(item.marca)}" oninput="m8_actualizar_pendiente('diario', ${idx}, 'marca', this.value)"></td>
                <td><input value="${m8_escape(item.modelo)}" oninput="m8_actualizar_pendiente('diario', ${idx}, 'modelo', this.value)"></td>
                <td><input value="${m8_escape(item.hm)}" oninput="m8_actualizar_pendiente('diario', ${idx}, 'hm', this.value)"></td>
                <td><input value="${m8_escape(item.combustible)}" oninput="m8_actualizar_pendiente('diario', ${idx}, 'combustible', this.value)"></td>
                <td class="text-end"><button type="button" class="btn btn-sm text-danger border-0" onclick="m8_eliminar_pendiente('diario', ${idx})"><i class="bi bi-trash"></i></button></td>
            </tr>
        `).join('');
    }

    function m8_confirmar_diario_preview() {
        const pendientes = [...window.m8_diario_pendientes];
        pendientes.forEach(item => m8_agregar_actual(item));
        window.m8_diario_pendientes = [];
        document.getElementById('m8_paste').value = '';
        m8_render_diario_preview();
    }

    function m8_cancelar_diario_preview() {
        window.m8_diario_pendientes = [];
        document.getElementById('m8_paste').value = '';
        m8_render_diario_preview();
    }

    setTimeout(() => m8_cambiar_categoria('maq_gore'), 300);
</script>
"""
