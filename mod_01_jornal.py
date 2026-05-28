# =========================================================
# mod_01_jornal.py
# Módulo: 1.- Jornal de Trabajo
# =========================================================

JORNAL_HTML = """
<style>
    .m1-clima-wrap { margin-top: 18px; }
    .m1-clima-title { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 10px; }
    .m1-clima-title h6 { margin: 0; font-size: 12px; font-weight: 900; color: #475569; text-transform: uppercase; letter-spacing: .4px; }
    .m1-clima-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
    .m1-clima { border: 1px solid #dbeafe; border-radius: 18px; background: #fff; min-height: 72px; padding: 12px 10px; display: flex; align-items: center; gap: 10px; cursor: pointer; transition: .22s ease; box-shadow: 0 10px 24px rgba(15,23,42,.05); }
    .m1-clima:hover { transform: translateY(-1px); box-shadow: 0 14px 28px rgba(15,23,42,.10); }
    .m1-clima.active { transform: scale(1.035); border-color: #0284c7; background: linear-gradient(135deg, #eff6ff, #ffffff); box-shadow: 0 16px 30px rgba(2,132,199,.16); }
    .m1-clima-icon { width: 38px; height: 38px; border-radius: 16px; display: grid; place-items: center; color: #fff; font-size: 20px; flex: 0 0 auto; }
    .m1-sol { background: linear-gradient(135deg, #f59e0b, #facc15); }
    .m1-nube { background: linear-gradient(135deg, #64748b, #cbd5e1); }
    .m1-mixto { background: linear-gradient(135deg, #0ea5e9, #facc15); }
    .m1-lluvia { background: linear-gradient(135deg, #0369a1, #38bdf8); }
    .m1-clima strong { display: block; font-size: 12px; color: #334155; }
    .m1-clima small { display: block; font-size: 10px; color: #64748b; font-weight: 700; }
    @media (max-width: 768px) { .m1-clima-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
</style>

<div class="step-view active" id="step1">
    <div class="step-title">1.- Jornal de Trabajo</div>
    <p class="text-muted small mb-3">Haga clic en los turnos laborados en la jornada para registrarlos:</p>
    <div class="row g-3">
        <div class="col-sm-6">
            <div class="time-card active" id="card_m" onclick="toggleTurno('m')">
                <div class="clock-icon"><i class="bi bi-sunrise-fill"></i></div>
                <div class="w-100">
                    <label class="form-label mb-1">Mañana</label>
                    <div class="fw-bold fs-6 text-dark" id="lbl_jornal_m">07:00 - 12:00</div>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="time-card active" id="card_t" onclick="toggleTurno('t')">
                <div class="clock-icon"><i class="bi bi-sunset-fill"></i></div>
                <div class="w-100">
                    <label class="form-label mb-1">Tarde</label>
                    <div class="fw-bold fs-6 text-dark" id="lbl_jornal_t">13:00 - 17:00</div>
                </div>
            </div>
        </div>
    </div>
    <div class="m1-clima-wrap">
        <div class="m1-clima-title">
            <h6><i class="bi bi-cloud-sun-fill me-1"></i> Factor climático del día</h6>
            <span class="text-muted small fw-bold">Seleccione cómo estuvo el clima</span>
        </div>
        <div class="m1-clima-grid">
            <div class="m1-clima active" id="m1_clima_soleado" onclick="m1_set_clima('Soleado')"><div class="m1-clima-icon m1-sol"><i class="bi bi-sun-fill"></i></div><div><strong>Soleado</strong><small>Cielo despejado</small></div></div>
            <div class="m1-clima" id="m1_clima_nublado" onclick="m1_set_clima('Nublado')"><div class="m1-clima-icon m1-nube"><i class="bi bi-cloud-fill"></i></div><div><strong>Nublado</strong><small>Cielo cubierto</small></div></div>
            <div class="m1-clima" id="m1_clima_mixto" onclick="m1_set_clima('Parcialmente nublado')"><div class="m1-clima-icon m1-mixto"><i class="bi bi-cloud-sun-fill"></i></div><div><strong>Nube y sol</strong><small>Clima variable</small></div></div>
            <div class="m1-clima" id="m1_clima_lluvia" onclick="m1_set_clima('Lluvioso')"><div class="m1-clima-icon m1-lluvia"><i class="bi bi-cloud-rain-fill"></i></div><div><strong>Lluvioso</strong><small>Precipitación</small></div></div>
        </div>
    </div>
    <input type="hidden" id="v_jornal_m" class="req-step1" value="07:00 - 12:00">
    <input type="hidden" id="v_jornal_t" class="req-step1" value="13:00 - 17:00">
    <input type="hidden" id="v_clima" value="Soleado">
</div>
<script>
    function m1_set_clima(clima) {
        document.getElementById('v_clima').value = clima;
        ['soleado', 'nublado', 'mixto', 'lluvia'].forEach(id => {
            const card = document.getElementById(`m1_clima_${id}`);
            if(card) card.classList.remove('active');
        });
        const mapa = {'Soleado': 'soleado', 'Nublado': 'nublado', 'Parcialmente nublado': 'mixto', 'Lluvioso': 'lluvia'};
        const activo = document.getElementById(`m1_clima_${mapa[clima]}`);
        if(activo) activo.classList.add('active');
        if (typeof sincronizarDatos === 'function') sincronizarDatos();
    }
</script>
"""
