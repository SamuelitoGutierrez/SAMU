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
    @media (max-width: 768px) { #step2 .personal-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
</style>

<div class="step-view" id="step2">
    <div class="step-title">2.- Personal de Obra</div>
    <p class="text-muted small mb-3">Ingrese la cantidad de personal presente en el frente de trabajo:</p>
    <div class="personal-grid">
        <div class="elegant-card" id="c_oper"><div class="p-icon"><i class="bi bi-person-badge-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Operarios</span><input type="number" class="req-step2" id="v_oper" placeholder="0" oninput="evaluarTarjeta('oper')"></div>
        <div class="elegant-card" id="c_ofic"><div class="p-icon"><i class="bi bi-person-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Oficiales</span><input type="number" class="req-step2" id="v_ofic" placeholder="0" oninput="evaluarTarjeta('ofic')"></div>
        <div class="elegant-card" id="c_peon"><div class="p-icon"><i class="bi bi-person-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Peones</span><input type="number" class="req-step2" id="v_peon" placeholder="0" oninput="evaluarTarjeta('peon')"></div>
        <div class="elegant-card" id="c_meca"><div class="p-icon"><i class="bi bi-tools"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Mecánicos</span><input type="number" class="req-step2" id="v_meca" placeholder="0" oninput="evaluarTarjeta('meca')"></div>
        <div class="elegant-card" id="c_ctrl"><div class="p-icon"><i class="bi bi-clipboard-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Controladores</span><input type="number" class="req-step2" id="v_ctrl" placeholder="0" oninput="evaluarTarjeta('ctrl')"></div>
        <div class="elegant-card" id="c_ope_maq"><div class="p-icon"><i class="bi bi-truck"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:800;">Operadores</span><input type="number" class="req-step2" id="v_ope_maq" placeholder="0" oninput="evaluarTarjeta('ope_maq')"></div>
    </div>
</div>
"""
