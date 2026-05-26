# =========================================================
# mod_02_personal.py
# Módulo: 2.- Personal de Obra
# =========================================================

PERSONAL_HTML = """
<div class="step-view" id="step2">
    <div class="step-title">2.- Personal de Obra</div>
    <p class="text-muted small mb-3">Ingrese la cantidad de personal presente en el frente de trabajo:</p>
    <div class="row g-2">
        <div class="col-4"><div class="elegant-card" id="c_oper"><div class="p-icon"><i class="bi bi-person-badge-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Operarios</span><input type="number" class="req-step2" id="v_oper" placeholder="0" oninput="evaluarTarjeta('oper')"></div></div>
        <div class="col-4"><div class="elegant-card" id="c_ofic"><div class="p-icon"><i class="bi bi-person-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Oficiales</span><input type="number" class="req-step2" id="v_ofic" placeholder="0" oninput="evaluarTarjeta('ofic')"></div></div>
        <div class="col-4"><div class="elegant-card" id="c_peon"><div class="p-icon"><i class="bi bi-person-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Peones</span><input type="number" class="req-step2" id="v_peon" placeholder="0" oninput="evaluarTarjeta('peon')"></div></div>
        <div class="col-4"><div class="elegant-card" id="c_meca"><div class="p-icon"><i class="bi bi-tools"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Mecánicos</span><input type="number" class="req-step2" id="v_meca" placeholder="0" oninput="evaluarTarjeta('meca')"></div></div>
        <div class="col-4"><div class="elegant-card" id="c_ctrl"><div class="p-icon"><i class="bi bi-clipboard-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Controladores</span><input type="number" class="req-step2" id="v_ctrl" placeholder="0" oninput="evaluarTarjeta('ctrl')"></div></div>
        <div class="col-4"><div class="elegant-card" id="c_ope_maq"><div class="p-icon"><i class="bi bi-truck"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Operadores</span><input type="number" class="req-step2" id="v_ope_maq" placeholder="0" oninput="evaluarTarjeta('ope_maq')"></div></div>
    </div>
</div>
"""
