# =========================================================
# mod_03_partidas.py
# Módulo: 3.- Partidas Ejecutadas (Con Motor Masivo Excel)
# =========================================================

PARTIDAS_HTML = """
<div class="step-view" id="step3">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">3.- Partidas Ejecutadas</div>
        <button type="button" class="btn btn-sm btn-outline-success rounded-pill fw-bold shadow-sm" onclick="abrirModalMasivo()">
            <i class="bi bi-file-earmark-excel"></i> Pegado Masivo
        </button>
    </div>
    
    <p class="text-muted small mb-3">Escribe la descripción de la partida y presiona <b>Enter</b> para agregarla rápido, o usa el botón verde para importar masivamente desde Excel.</p>
    
    <div class="input-group mb-3 shadow-sm">
        <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
        <input type="text" class="form-control border-start-0 ps-0" id="buscadorPartidas" placeholder="Ej: Conformación de base granular..." onkeydown="if(event.key==='Enter'){event.preventDefault(); agregarPartidaRapida();}">
        <button class="btn btn-primary px-3" type="button" onclick="agregarPartidaRapida()"><i class="bi bi-plus-lg"></i></button>
    </div>
    
    <div id="listaPartidasAgregadas" class="d-flex flex-column gap-2 req-step3 mb-3"></div>
    
    <input type="hidden" id="v_partidas" class="req-step3" value="">
</div>

<div class="modal fade" id="modalExcel" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="border-radius: 20px;">
            <div class="modal-header border-0 pb-0">
                <h5 class="modal-title fw-bold text-success"><i class="bi bi-file-earmark-spreadsheet"></i> Pegado Masivo (Excel)</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p class="small text-muted mb-2">Copia las filas desde tu Excel (<b>Descripción | Metrado</b>) y presiona <code>Ctrl + V</code> aquí abajo:</p>
                <textarea id="textoExcelMasivo" class="form-control" rows="8" placeholder="Pegue aquí los datos tabulados..."></textarea>
            </div>
            <div class="modal-footer border-0 pt-0">
                <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-success rounded-pill px-4 fw-bold" onclick="procesarExcelMasivo()">Procesar Datos</button>
            </div>
        </div>
    </div>
</div>
"""
