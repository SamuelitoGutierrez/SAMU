# =========================================================
# mod_02_personal.py
# Módulo: 2.- Personal de Obra
# =========================================================

PERSONAL_HTML = """
<style>
    #step2 .personal-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
    #step2 .elegant-card { min-height: 118px; border-radius: 22px; border: 1px solid #e2e8f0; background: linear-gradient(180deg, #ffffff, #f8fafc); box-shadow: 0 12px 28px rgba(15,23,42,.06); cursor: pointer; position: relative; overflow: hidden; }
    #step2 .elegant-card::after { content: ""; position: absolute; inset: auto -30px -38px auto; width: 88px; height: 88px; border-radius: 50%; background: rgba(2,99,160,.08); transition: .25s ease; }
    #step2 .elegant-card.active { transform: translateY(-2px) scale(1.02); border-color: #0284c7; background: linear-gradient(135deg, #eff6ff, #ffffff); box-shadow: 0 18px 34px rgba(2,99,160,.14); }
    #step2 .elegant-card.active::after { transform: scale(1.35); background: rgba(2,99,160,.14); }
    #step2 .elegant-card .p-icon { width: 42px; height: 42px; border-radius: 18px; display: grid; place-items: center; background: #f1f5f9; color: #64748b; font-size: 22px; margin-bottom: 8px; transition: .25s ease; }
    #step2 .elegant-card.active .p-icon { background: linear-gradient(135deg, #075985, #0ea5e9); color: #fff; transform: scale(1.08); }
    #step2 .elegant-card input { position: relative; z-index: 2; }
    #step2 .personal-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
    #step2 .personal-total { border: 1px solid #bae6fd; border-radius: 999px; padding: 9px 13px; background: #f0f9ff; color: #075985; font-size: 12px; font-weight: 900; box-shadow: 0 10px 22px rgba(2,132,199,.10); }
    #step2 .personal-actions { display: flex; gap: 8px; flex-wrap: wrap; }
    #step2 .personal-mini-btn { border: 0; border-radius: 999px; padding: 8px 11px; font-size: 11px; font-weight: 900; color: #0f172a; background: #e2e8f0; }
    #step2 .qty-controls { position: relative; z-index: 3; display: flex; gap: 6px; justify-content: center; margin-top: 8px; }
    #step2 .qty-btn { width: 28px; height: 28px; border: 0; border-radius: 999px; display: grid; place-items: center; font-weight: 900; color: #075985; background: #e0f2fe; transition: .18s ease; }
    #step2 .qty-btn:hover { transform: translateY(-1px) scale(1.05); background: #bae6fd; }
    #step2 .gg-card { margin-top: 18px; border: 1px solid #dbeafe; border-radius: 24px; background: linear-gradient(135deg, #f8fafc, #eef6ff); padding: 16px; box-shadow: 0 14px 30px rgba(15,23,42,.06); }
    #step2 .m2-collapse { border: 1px solid #dbeafe; border-radius: 24px; background: #fff; margin-bottom: 14px; overflow: hidden; box-shadow: 0 14px 30px rgba(15,23,42,.06); }
    #step2 .m2-collapse-head { width: 100%; border: 0; background: linear-gradient(135deg, #eff6ff, #ffffff); padding: 14px 16px; display: flex; justify-content: space-between; align-items: center; font-weight: 950; color: #075985; }
    #step2 .m2-collapse-head i { transition: transform .2s ease; }
    #step2 .m2-collapse.closed .m2-collapse-head i { transform: rotate(-90deg); }
    #step2 .m2-collapse-body { padding: 16px; }
    #step2 .m2-collapse.closed .m2-collapse-body { display: none; }
    #step2 .gg-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 9px; }
    #step2 .gg-item { display: flex; align-items: center; gap: 9px; border: 1px solid #e2e8f0; border-radius: 16px; background: #fff; padding: 10px 11px; font-size: 12px; font-weight: 850; color: #334155; cursor: pointer; transition: .18s ease; }
    #step2 .gg-item:has(input:checked) { border-color: #2563eb; color: #1d4ed8; background: #eff6ff; box-shadow: 0 10px 22px rgba(37,99,235,.10); }
    #step2 .gg-add-row { display: flex; gap: 8px; margin-top: 12px; }
    #step2 .gg-add-row input { flex: 1; border: 1px solid #cbd5e1; border-radius: 999px; padding: 10px 14px; font-weight: 800; outline: none; }
    #step2 .gg-add-row input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,.12); }
    #step2 .gg-plus { width: 42px; height: 42px; border: 0; border-radius: 999px; color: #fff; background: linear-gradient(135deg, #2563eb, #0f766e); display: grid; place-items: center; font-size: 20px; box-shadow: 0 12px 24px rgba(37,99,235,.2); }
    @media (max-width: 768px) { #step2 .personal-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media (max-width: 768px) { #step2 .gg-grid { grid-template-columns: 1fr; } }
</style>

<div class="step-view" id="step2">
    <div class="step-title">2.- Personal de Obra</div>
    <div class="m2-collapse" id="m2_panel_gastos">
        <button type="button" class="m2-collapse-head" onclick="m2_toggle_panel('m2_panel_gastos')">
            <span><i class="bi bi-chevron-down me-2"></i>Personal de Gastos Generales</span>
            <span class="personal-total">Seleccionados: <span id="m2_total_gg">0</span></span>
        </button>
        <div class="m2-collapse-body">
            <p class="text-muted small fw-bold">Se arrastra automáticamente desde el asiento anterior y puede ajustarse para hoy.</p>
            <div class="gg-grid" id="m2_gastos_grid"></div>
            <div class="gg-add-row">
                <input type="text" id="m2_nuevo_gasto" placeholder="Agregar nuevo personal de gastos generales" onkeydown="if(event.key==='Enter'){event.preventDefault();m2_agregar_gasto();}">
                <button type="button" class="gg-plus" onclick="m2_agregar_gasto()" title="Agregar"><i class="bi bi-plus-lg"></i></button>
            </div>
        </div>
    </div>
    <div class="m2-collapse" id="m2_panel_directo">
        <button type="button" class="m2-collapse-head" onclick="m2_toggle_panel('m2_panel_directo')">
            <span><i class="bi bi-chevron-down me-2"></i>Personal de Costo Directo</span>
            <span class="personal-total">Total: <span id="m2_total_personal">0</span></span>
        </button>
        <div class="m2-collapse-body">
            <div class="personal-head">
                <p class="text-muted small m-0">Ingrese la cantidad de personal presente en el frente de trabajo:</p>
                <div class="personal-actions">
                    <button type="button" class="personal-mini-btn" onclick="m2_limpiar_personal()">Limpiar</button>
                </div>
            </div>
            <div class="personal-grid">
                <div class="elegant-card" id="c_oper"><div class="p-icon"><i class="bi bi-person-badge-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Operarios</span><input type="number" min="0" class="req-step2" id="v_oper" placeholder="0" oninput="m2_actualizar_personal('oper')"><div class="qty-controls"><button type="button" class="qty-btn" onclick="m2_sumar('oper', -1)">−</button><button type="button" class="qty-btn" onclick="m2_sumar('oper', 1)">+</button></div></div>
                <div class="elegant-card" id="c_ofic"><div class="p-icon"><i class="bi bi-person-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Oficiales</span><input type="number" min="0" class="req-step2" id="v_ofic" placeholder="0" oninput="m2_actualizar_personal('ofic')"><div class="qty-controls"><button type="button" class="qty-btn" onclick="m2_sumar('ofic', -1)">−</button><button type="button" class="qty-btn" onclick="m2_sumar('ofic', 1)">+</button></div></div>
                <div class="elegant-card" id="c_peon"><div class="p-icon"><i class="bi bi-person-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Peones</span><input type="number" min="0" class="req-step2" id="v_peon" placeholder="0" oninput="m2_actualizar_personal('peon')"><div class="qty-controls"><button type="button" class="qty-btn" onclick="m2_sumar('peon', -1)">−</button><button type="button" class="qty-btn" onclick="m2_sumar('peon', 1)">+</button></div></div>
                <div class="elegant-card" id="c_meca"><div class="p-icon"><i class="bi bi-tools"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Mecánicos</span><input type="number" min="0" class="req-step2" id="v_meca" placeholder="0" oninput="m2_actualizar_personal('meca')"><div class="qty-controls"><button type="button" class="qty-btn" onclick="m2_sumar('meca', -1)">−</button><button type="button" class="qty-btn" onclick="m2_sumar('meca', 1)">+</button></div></div>
                <div class="elegant-card" id="c_ctrl"><div class="p-icon"><i class="bi bi-clipboard-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Controladores</span><input type="number" min="0" class="req-step2" id="v_ctrl" placeholder="0" oninput="m2_actualizar_personal('ctrl')"><div class="qty-controls"><button type="button" class="qty-btn" onclick="m2_sumar('ctrl', -1)">−</button><button type="button" class="qty-btn" onclick="m2_sumar('ctrl', 1)">+</button></div></div>
                <div class="elegant-card" id="c_ope_maq"><div class="p-icon"><i class="bi bi-truck"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Operadores</span><input type="number" min="0" class="req-step2" id="v_ope_maq" placeholder="0" oninput="m2_actualizar_personal('ope_maq')"><div class="qty-controls"><button type="button" class="qty-btn" onclick="m2_sumar('ope_maq', -1)">−</button><button type="button" class="qty-btn" onclick="m2_sumar('ope_maq', 1)">+</button></div></div>
            </div>
        </div>
    </div>
</div>
<script>
    function m2_toggle_panel(id) {
        document.getElementById(id)?.classList.toggle('closed');
    }

    function m2_ids_personal() {
        return ['oper', 'ofic', 'peon', 'meca', 'ctrl', 'ope_maq'];
    }

    function m2_actualizar_personal(id) {
        const input = document.getElementById('v_' + id);
        if (input) input.value = Math.max(0, parseInt(input.value || 0) || 0) || '';
        if (typeof evaluarTarjeta === 'function') evaluarTarjeta(id);
        m2_totalizar_personal();
    }

    function m2_sumar(id, delta) {
        const input = document.getElementById('v_' + id);
        if (!input) return;
        const actual = parseInt(input.value || 0) || 0;
        input.value = Math.max(0, actual + delta) || '';
        m2_actualizar_personal(id);
    }

    function m2_totalizar_personal() {
        const total = m2_ids_personal().reduce((sum, id) => {
            const val = parseInt(document.getElementById('v_' + id)?.value || 0) || 0;
            document.getElementById('c_' + id)?.classList.toggle('active', val > 0);
            return sum + val;
        }, 0);
        const lbl = document.getElementById('m2_total_personal');
        if (lbl) lbl.innerText = total;
        if (typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    window.m2_gastos_base = window.m2_gastos_base || [
        "Residente de obra",
        "Ing Asistente",
        "Especialista III Suelos y Pavimentos",
        "Especialista Topografía y Explanaciones",
        "Especialista Impacto Ambiental y Seguridad",
        "Almacenero",
        "Administrador de Obra",
        "Técnico Administrativo",
        "Maestro de Obra",
        "Guardián",
        "Cocinero",
        "Chofer",
        "Asistente del Comunicador Social"
    ];
    window.m2_gastos_generales = window.m2_gastos_generales || [];

    function m2_render_gastos() {
        const grid = document.getElementById('m2_gastos_grid');
        if (!grid) return;
        const unicos = Array.from(new Set([...(window.m2_gastos_base || []), ...(window.m2_gastos_generales || [])]));
        window.m2_gastos_base = unicos;
        grid.innerHTML = unicos.map((nombre, idx) => {
            const checked = (window.m2_gastos_generales || []).includes(nombre) ? 'checked' : '';
            return `<label class="gg-item"><input type="checkbox" class="m2-gg-check" value="${nombre.replace(/"/g, '&quot;')}" ${checked} onchange="m2_toggle_gasto(this)"> <span>${nombre}</span></label>`;
        }).join('');
        m2_totalizar_gastos();
    }

    function m2_toggle_gasto(check) {
        const nombre = check.value;
        const set = new Set(window.m2_gastos_generales || []);
        if (check.checked) set.add(nombre); else set.delete(nombre);
        window.m2_gastos_generales = Array.from(set);
        m2_totalizar_gastos();
    }

    function m2_agregar_gasto() {
        const input = document.getElementById('m2_nuevo_gasto');
        const nombre = String(input?.value || '').trim();
        if (!nombre) return;
        if (!(window.m2_gastos_base || []).includes(nombre)) window.m2_gastos_base.push(nombre);
        if (!(window.m2_gastos_generales || []).includes(nombre)) window.m2_gastos_generales.push(nombre);
        if (input) input.value = '';
        m2_render_gastos();
    }

    function m2_totalizar_gastos() {
        const lbl = document.getElementById('m2_total_gg');
        if (lbl) lbl.innerText = (window.m2_gastos_generales || []).length;
        if (typeof sincronizarDatos === 'function') sincronizarDatos();
        if (typeof guardarEstadoLocal === 'function') guardarEstadoLocal();
    }

    function m2_limpiar_personal() {
        m2_ids_personal().forEach(id => {
            const input = document.getElementById('v_' + id);
            if (input) input.value = '';
        });
        m2_totalizar_personal();
    }

    window.m2_render = function() { m2_totalizar_personal(); m2_render_gastos(); };
    setTimeout(window.m2_render, 250);
</script>
"""
