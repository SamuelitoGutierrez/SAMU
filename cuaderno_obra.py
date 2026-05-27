CUADERNO_OBRA_CSS = """
            /* ==========================================
               CUADERNO FISICO / PREVISUALIZACION
               ========================================== */
            .papel-fisico { background: #fdfdfa; width: 100%; min-height: 980px; padding: 45px 50px; box-shadow: 0 15px 40px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; font-family: Arial, sans-serif; color: #000; position: relative;}
            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; }
            .p-title-box { text-align: center; flex: 1; margin-left: 60px;}
            .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0;}
            .p-num { font-size: 24px; font-weight: bold; }
            .p-meta { margin-bottom: 12px; padding-bottom: 14px; border-bottom: 3px solid #000; }
            .p-row { display: flex; align-items: flex-end; margin-bottom: 6px; }
            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; }
            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }
            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 22px; font-weight: 700; white-space: nowrap; }
            .p-body-lines { background-image: repeating-linear-gradient(transparent, transparent 27px, #cbd5e1 28px); line-height: 28px; min-height: 650px; padding-top: 2px; position: relative; margin-top: 15px;}
            .lapicero { font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 22px; line-height: 28px; padding-left: 2px; font-weight: 700; text-align: justify; word-wrap: break-word; }
            .p-break-page { border-top: 2px dashed #94a3b8; margin: 35px 0 20px 0; padding-top: 15px; position: relative; }
            .p-footer { display: flex; justify-content: space-between; margin-top: 50px; font-size: 12px; font-weight: bold; color: #000;}
            .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }
"""


def obtener_cuaderno_obra_html(numero_hoja):
    return f"""
                <div class="papel-fisico" id="papelOficial">
                    <div class="p-header-top">
                        <div style="width: 80px;"></div>
                        <div class="p-title-box"><h1>CUADERNO DE OBRA</h1></div>
                        <div style="text-align: right; width: 80px;"><div class="p-num">No <span style="font-size: 26px; margin-left:3px;">{numero_hoja}</span></div></div>
                    </div>
                    <div class="p-meta">
                        <div class="d-flex w-100 mb-1">
                            <div class="d-flex" style="flex: 0.5;"><span class="p-label">Fecha:</span><div class="p-line"><span class="lapicero-meta" id="lbl_hoja_fecha">--</span></div></div>
                            <div class="d-flex" style="flex: 0.5; margin-left: 15px;"><span class="p-label">Modalidad:</span><div class="p-line"><span class="lapicero-meta">Administracion Directa</span></div></div>
                        </div>
                        <div class="p-row"><span class="p-label">Obra:</span><div class="p-line"><span class="lapicero-meta">Mejoramiento de la Carretera Asiruni - Rosaspata</span></div></div>
                        <div class="p-row"><span class="p-label">Proyecto:</span><div class="p-line"><span class="lapicero-meta">Tramo I</span></div></div>
                        <div class="p-row"><span class="p-label">Programa:</span><div class="p-line"><span class="lapicero-meta">-</span></div></div>
                        <div class="p-row"><span class="p-label">Entidad Ejecutora:</span><div class="p-line"><span class="lapicero-meta">Gobierno Regional Puno</span></div></div>
                    </div>

                    <div class="p-body-lines" id="contenedorLineasCuaderno">
                        <div class="lapicero" id="out_general"></div>
                    </div>
                    <div class="p-footer">
                        <div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div>
                    </div>
                </div>
"""


CUADERNO_OBRA_JS = """
            // =====================================================================
            // MOTOR DEL CUADERNO DE OBRA POR MODULOS
            // =====================================================================
            function paginateText(texto, contenedorId, maxHeight) {
                const container = document.getElementById(contenedorId);
                container.innerHTML = texto;
                if (container.offsetHeight <= maxHeight) return [texto, ""];

                let words = texto.split(' ');
                let low = 0, high = words.length;
                let best = 0;
                while (low <= high) {
                    let mid = Math.floor((low + high) / 2);
                    container.innerHTML = words.slice(0, mid).join(' ') + ' ... Van';
                    if (container.offsetHeight <= maxHeight) {
                        best = mid;
                        low = mid + 1;
                    } else {
                        high = mid - 1;
                    }
                }
                return [words.slice(0, best).join(' '), words.slice(best).join(' ')];
            }

            function sincronizarDatos() {
                if (!g_numAsiento) return;
                let as_str = g_numAsiento.padStart(4, '0');

                let cabecera = `<div style="display:flex; justify-content:space-between; width:100%; margin-bottom: 5px; font-family: Arial, sans-serif;"><div style="padding-left:40px; font-weight:bold; font-size:17px; color:#000;">ASIENTO No ${as_str} DEL RESIDENTE DE OBRA</div><div style="padding-right:10px; font-weight:bold; font-size:17px; color:#000;">${g_fechaAsiento}</div></div>`;
                let parrafo = "";

                const vJm = document.getElementById('v_jornal_m');
                const vJt = document.getElementById('v_jornal_t');
                const vJ1 = vJm ? vJm.value : '';
                const vJ2 = vJt ? vJt.value : '';
                if (vJ1 || vJ2) {
                    parrafo += "1.- Jornal de trabajo: ";
                    if (vJ1) parrafo += `Manana: ${vJ1}`;
                    if (vJ1 && vJ2) parrafo += ", ";
                    if (vJ2) parrafo += `Tarde: ${vJ2}`;
                    parrafo += ". ";
                }

                let p_data = [
                    {k: 'operarios', v: parseInt(document.getElementById('v_oper')?.value || 0)},
                    {k: 'oficiales', v: parseInt(document.getElementById('v_ofic')?.value || 0)},
                    {k: 'peones', v: parseInt(document.getElementById('v_peon')?.value || 0)},
                    {k: 'mecanicos', v: parseInt(document.getElementById('v_meca')?.value || 0)},
                    {k: 'controladores', v: parseInt(document.getElementById('v_ctrl')?.value || 0)},
                    {k: 'operadores', v: parseInt(document.getElementById('v_ope_maq')?.value || 0)}
                ];
                let p_filtrado = p_data.filter(x => x.v > 0);
                if (p_filtrado.length > 0) {
                    parrafo += "2.- Personal de obra: ";
                    parrafo += p_filtrado.map(x => `${x.v.toString().padStart(2, '0')} ${x.k}`).join(', ') + ". ";
                }

                if (typeof window.m3_lista !== 'undefined' && window.m3_lista.length > 0) {
                    parrafo += "3.- Partidas ejecutadas: ";
                    parrafo += window.m3_lista.map(p => p.metrado ? `${p.item} ${p.descripcion} = ${p.metrado} ${p.unidad}` : `${p.item} ${p.descripcion}`).join('; ') + ". ";
                }

                const cRestantes = [
                    {id: 'v_mayor_m', t: '4.- Partidas de mayor metrado'},
                    {id: 'v_sub_p', t: '5.- Sub partidas ejecutadas'},
                    {id: 'v_activ', t: '6.- Actividades ejecutadas'},
                    {id: 'v_almacen', t: '7.- Movimiento de almacen'},
                    {id: 'v_maquina', t: '8.- Maquinarias y equipos'},
                    {id: 'v_herram', t: '9.- Herramientas manuales'},
                    {id: 'v_ocurrencia', t: '10.- Ocurrencias y otros'}
                ];
                cRestantes.forEach(c => {
                    const el = document.getElementById(c.id);
                    if (el && el.value) parrafo += `${c.t}: ${el.value.replace(/\\n/g, ' ')} `;
                });

                const outContainer = document.getElementById('out_general');
                const [pagina1, pagina2] = paginateText(parrafo, 'out_general', 560);

                if (pagina2 === "") {
                    outContainer.innerHTML = cabecera + pagina1;
                } else {
                    let htmlFinal = cabecera + pagina1 + ' <span class="p-van-line d-inline" style="padding-left:15px;">... Van</span>';
                    htmlFinal += `<div class="p-break-page"></div>`;
                    htmlFinal += `<div style="display:flex; justify-content:space-between; width:100%; margin-bottom:10px; font-family:'Caveat', cursive; color:var(--celeste-obra); font-weight:bold; font-size:22px;">
                        <div style="padding-left:10px;">... VIENE DEL ASIENTO No ${as_str} DEL RESIDENTE DE OBRA</div>
                        <div style="padding-right:10px;">${g_fechaAsiento}</div>
                    </div>`;
                    htmlFinal += pagina2;
                    outContainer.innerHTML = htmlFinal;
                }
            }
"""
