CUADERNO_OBRA_CSS = """
            /* ==========================================
               CUADERNO FISICO / PREVISUALIZACION
               ========================================== */
            .papel-fisico { background: #fdfdfa; width: 100%; min-height: 980px; padding: 34px 46px 42px; box-shadow: 0 18px 45px rgba(15,23,42,0.10); border: 1px solid #e2e8f0; font-family: Arial, sans-serif; color: #000; position: relative;}
            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }
            .p-title-box { text-align: center; flex: 1; margin-left: 60px;}
            .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0;}
            .p-num { font-size: 24px; font-weight: bold; }
            .p-meta { margin-bottom: 6px; padding-bottom: 7px; border-bottom: 3px solid #000; }
            .p-row { display: flex; align-items: flex-end; margin-bottom: 4px; }
            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; }
            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }
            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: var(--celeste-obra); font-size: 17px; font-weight: 500; white-space: nowrap; }
            .p-body-lines { position: relative; margin-top: 3px; }
            .pagina-cuaderno { background-image: repeating-linear-gradient(transparent, transparent 25px, #cbd5e1 26px); line-height: 26px; min-height: 650px; padding-top: 0; position: relative; }
            .pagina-cuaderno + .pagina-cuaderno { margin-top: 42px; padding-top: 0; border-top: 2px dashed #94a3b8; }
            .lapicero { font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: var(--celeste-obra); font-size: 17px; line-height: 26px; padding-left: 2px; font-weight: 400; text-align: justify; word-wrap: break-word; }
            .encabezado-asiento { position: relative; margin: 0 0 3px; min-height: 26px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: var(--celeste-obra); font-size: 16px; line-height: 26px; font-weight: 700; }
            .encabezado-asiento .titulo-asiento { width: 100%; text-align: center; text-transform: uppercase; color: var(--celeste-obra); font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; font-size: 16px; letter-spacing: 0.1px; font-weight: 800; padding: 0 128px 0 8px; white-space: nowrap; }
            .encabezado-asiento.continuacion .titulo-asiento { text-transform: none; color: var(--celeste-obra); font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; font-size: 16px; font-weight: 800; }
            .encabezado-asiento .fecha-asiento { position: absolute; top: 0; right: 0; text-align: right; white-space: nowrap; color: var(--celeste-obra); }
            .modulo-redaccion { margin: 0 0 0; }
            .modulo-titulo { display: block; font-weight: 700; color: #075985; }
            .modulo-contenido { display: block; padding-left: 22px; text-indent: 0; white-space: pre-wrap; }
            .van-final { display: block; text-align: right; padding-right: 8px; font-weight: 800; color: #075985; }
            .p-footer { display: flex; justify-content: space-between; margin-top: 46px; font-size: 12px; font-weight: bold; color: #000;}
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

                    <div class="p-body-lines" id="contenedorLineasCuaderno"></div>
                    <div class="p-footer">
                        <div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div>
                    </div>
                </div>
"""


CUADERNO_OBRA_JS = """
            // =====================================================================
            // MOTOR DEL CUADERNO DE OBRA POR MODULOS
            // =====================================================================
            function normalizarOracion(texto) {
                return String(texto || '')
                    .replace(/\\s+/g, ' ')
                    .trim();
            }

            function escaparHtml(texto) {
                return String(texto || '')
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#039;');
            }

            function escaparHtmlConSaltos(texto) {
                return escaparHtml(texto).replace(/\\n/g, '<br>');
            }

            function valor(id) {
                const el = document.getElementById(id);
                return el ? normalizarOracion(el.value) : '';
            }

            function formatoItem(p) {
                const item = p.item && p.item !== '-' ? `${p.item} ` : '';
                const progresiva = p.prog ? ` - ${p.prog}` : '';
                const metrado = p.metrado ? ` = ${p.metrado} ${p.unidad || ''}` : '';
                return normalizarOracion(`${item}${p.descripcion || ''}${progresiva}${metrado}`);
            }

            function agregarModulo(modulos, titulo, contenido) {
                const texto = String(contenido || '')
                    .split('\\n')
                    .map(linea => normalizarOracion(linea))
                    .filter(Boolean)
                    .join('\\n');
                modulos.push({ titulo, contenido: texto || '-' });
            }

            function cantidadPersonal(cantidad, nombre) {
                return `(${cantidad.toString().padStart(2, '0')}) ${nombre}`;
            }

            function redactarModulosCuaderno() {
                const modulos = [];

                const vJ1 = valor('v_jornal_m');
                const vJ2 = valor('v_jornal_t');
                if (vJ1 || vJ2) {
                    let partes = [];
                    if (vJ1) partes.push(`Mañana: ${vJ1}`);
                    if (vJ2) partes.push(`Tarde: ${vJ2}`);
                    agregarModulo(modulos, '1. Jornal de trabajo', partes.join(', '));
                } else {
                    agregarModulo(modulos, '1. Jornal de trabajo', '');
                }

                const personal = [
                    {k: 'Operario', v: parseInt(valor('v_oper') || 0)},
                    {k: 'Oficiales', v: parseInt(valor('v_ofic') || 0)},
                    {k: 'Peones', v: parseInt(valor('v_peon') || 0)},
                    {k: 'Mecánicos', v: parseInt(valor('v_meca') || 0)},
                    {k: 'Controladores de maquinaria', v: parseInt(valor('v_ctrl') || 0)},
                    {k: 'Operadores de maquinaria', v: parseInt(valor('v_ope_maq') || 0)}
                ].filter(x => x.v > 0);

                if (personal.length > 0) {
                    const primeraLinea = personal.slice(0, 4).map(x => cantidadPersonal(x.v, x.k)).join('    ');
                    const segundaLinea = personal.slice(4).map(x => cantidadPersonal(x.v, x.k)).join('    ');
                    agregarModulo(modulos, '2. Personal de obra', [primeraLinea, segundaLinea].filter(Boolean).join('\\n'));
                } else {
                    agregarModulo(modulos, '2. Personal de obra', '');
                }

                if (Array.isArray(window.m3_lista) && window.m3_lista.length > 0) {
                    agregarModulo(modulos, '3. Partidas ejecutadas', window.m3_lista.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '3. Partidas ejecutadas', '');
                }

                if (Array.isArray(window.m4_lista) && window.m4_lista.length > 0) {
                    agregarModulo(modulos, '4. Partidas de mayor metrado', window.m4_lista.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '4. Partidas de mayor metrado', valor('v_mayor_m'));
                }

                if (Array.isArray(window.m5_lista) && window.m5_lista.length > 0) {
                    agregarModulo(modulos, '5. Sub partidas ejecutadas', window.m5_lista.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '5. Sub partidas ejecutadas', valor('v_sub_p'));
                }

                if (Array.isArray(window.m6_lista) && window.m6_lista.length > 0) {
                    agregarModulo(modulos, '6. Actividades ejecutadas', window.m6_lista.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '6. Actividades ejecutadas', valor('v_activ'));
                }

                agregarModulo(modulos, '7. Movimiento de almacén', valor('v_almacen'));
                agregarModulo(modulos, '8. Maquinarias y equipos', valor('v_maquina'));
                agregarModulo(modulos, '9. Herramientas manuales', valor('v_herram'));
                agregarModulo(modulos, '10. Ocurrencias y otros', valor('v_ocurrencia'));

                return modulos;
            }

            function encabezadoPagina(asiento, fecha, continuacion=false) {
                const titulo = continuacion
                    ? `... viene del ASIENTO N° ${asiento} DEL RESIDENTE DE OBRA`
                    : `ASIENTO N° ${asiento} DEL RESIDENTE DE OBRA`;
                return `
                    <div class="encabezado-asiento ${continuacion ? 'continuacion' : ''}">
                        <div class="titulo-asiento">${escaparHtml(titulo)}</div>
                        <div class="fecha-asiento">${escaparHtml(fecha)}</div>
                    </div>
                `;
            }

            function htmlModulo(modulo) {
                return `
                    <div class="modulo-redaccion">
                        <span class="modulo-titulo">${escaparHtml(modulo.titulo)}</span>
                        <span class="modulo-contenido">${escaparHtmlConSaltos(modulo.contenido)}</span>
                    </div>
                `;
            }

            function paginaHtml(asiento, fecha, modulos, continuacion=false, van=false) {
                return `
                    <div class="pagina-cuaderno">
                        <div class="lapicero">
                            ${encabezadoPagina(asiento, fecha, continuacion)}
                            ${modulos.map(htmlModulo).join('')}
                            ${van ? '<span class="van-final">Van ...</span>' : ''}
                        </div>
                    </div>
                `;
            }

            function medirPagina(asiento, fecha, modulos, continuacion=false, van=false) {
                const contenedor = document.getElementById('contenedorLineasCuaderno');
                contenedor.innerHTML = paginaHtml(asiento, fecha, modulos, continuacion, van);
                const pagina = contenedor.querySelector('.pagina-cuaderno');
                return pagina ? pagina.scrollHeight : 0;
            }

            function dividirModulo(asiento, fecha, modulo, continuacion, maxHeight) {
                const palabras = modulo.contenido.split(' ');
                let low = 0;
                let high = palabras.length;
                let best = 0;

                while (low <= high) {
                    const mid = Math.floor((low + high) / 2);
                    const parte = { titulo: modulo.titulo, contenido: palabras.slice(0, mid).join(' ') };
                    if (medirPagina(asiento, fecha, [parte], continuacion, true) <= maxHeight) {
                        best = mid;
                        low = mid + 1;
                    } else {
                        high = mid - 1;
                    }
                }

                if (best <= 0) best = Math.min(1, palabras.length);

                return [
                    { titulo: modulo.titulo, contenido: palabras.slice(0, best).join(' ') },
                    { titulo: modulo.titulo, contenido: palabras.slice(best).join(' ') }
                ];
            }

            function construirPaginas(asiento, fecha, modulos) {
                const maxHeight = 650;
                const paginas = [];
                let actual = [];
                let continuacion = false;

                modulos.forEach((moduloOriginal) => {
                    let pendiente = { ...moduloOriginal };

                    while (pendiente && pendiente.contenido) {
                        const prueba = [...actual, pendiente];
                        if (medirPagina(asiento, fecha, prueba, continuacion, false) <= maxHeight) {
                            actual.push(pendiente);
                            pendiente = null;
                            continue;
                        }

                        if (actual.length > 0) {
                            paginas.push({ modulos: actual, continuacion, van: true });
                            actual = [];
                            continuacion = true;
                            continue;
                        }

                        const partes = dividirModulo(asiento, fecha, pendiente, continuacion, maxHeight);
                        paginas.push({ modulos: [partes[0]], continuacion, van: true });
                        pendiente = partes[1].contenido ? partes[1] : null;
                        continuacion = true;
                    }
                });

                paginas.push({ modulos: actual, continuacion, van: false });
                return paginas;
            }

            function sincronizarDatos() {
                if (!g_numAsiento) return;

                const asiento = g_numAsiento.padStart(4, '0');
                const modulos = redactarModulosCuaderno();
                const contenedor = document.getElementById('contenedorLineasCuaderno');

                if (modulos.length === 0) {
                    contenedor.innerHTML = paginaHtml(asiento, g_fechaAsiento, [], false, false);
                    return;
                }

                const paginas = construirPaginas(asiento, g_fechaAsiento, modulos);
                contenedor.innerHTML = paginas
                    .map(p => paginaHtml(asiento, g_fechaAsiento, p.modulos, p.continuacion, p.van))
                    .join('');
            }
"""
