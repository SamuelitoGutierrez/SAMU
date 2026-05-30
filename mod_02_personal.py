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
    @media (max-width: 768px) { #step2 .personal-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
</style>

<div class="step-view" id="step2">
    <div class="step-title">2.- Personal de Obra</div>
    <div class="personal-head">
        <p class="text-muted small m-0">Ingrese la cantidad de personal presente en el frente de trabajo:</p>
        <div class="personal-actions">
            <span class="personal-total">Total: <span id="m2_total_personal">0</span></span>
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
<script>
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

    function m2_limpiar_personal() {
        m2_ids_personal().forEach(id => {
            const input = document.getElementById('v_' + id);
            if (input) input.value = '';
        });
        m2_totalizar_personal();
    }

    setTimeout(m2_totalizar_personal, 250);
</script>
"""
