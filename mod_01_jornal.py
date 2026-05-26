# =========================================================
# mod_01_jornal.py
# Componente: 1.- Jornal de Trabajo
# =========================================================

from flask import Blueprint

mod_01_bp = Blueprint('mod_01_jornal', __name__)

# Exponemos el bloque HTML limpio para que el chasis lo ensamble
JORNAL_HTML = """
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
    <input type="hidden" id="v_jornal_m" class="req-step1" value="07:00 - 12:00">
    <input type="hidden" id="v_jornal_t" class="req-step1" value="13:00 - 17:00">
</div>
"""
