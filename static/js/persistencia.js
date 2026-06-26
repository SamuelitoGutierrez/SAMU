/**
 * Guardado persistente: servidor (PostgreSQL) + respaldo local.
 * Al recargar (F5) o reiniciar el servidor, los datos se recuperan de la BD.
 */
(function () {
  const CLAVE_STORAGE = "samu_respaldo_panel";
  const CLAVE_API = "panel";

  const estado = document.getElementById("estadoGuardado");
  const area = document.getElementById("areaTrabajo");
  if (!area) return;

  let timer = null;

  function mostrar(texto, tipo) {
    if (!estado) return;
    estado.textContent = texto;
    estado.className = "estado-guardado" + (tipo ? " " + tipo : "");
  }

  function respaldoLocal(datos) {
    try {
      localStorage.setItem(CLAVE_STORAGE, JSON.stringify(datos));
    } catch (_) {}
  }

  function leerRespaldoLocal() {
    try {
      const raw = localStorage.getItem(CLAVE_STORAGE);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  async function cargar() {
    mostrar("Cargando…", "");
    try {
      const resp = await fetch("/api/datos?clave=" + encodeURIComponent(CLAVE_API));
      const data = await resp.json().catch(() => ({}));
      if (resp.ok && data.ok && data.datos && data.datos.texto !== undefined) {
        area.value = data.datos.texto;
        respaldoLocal(data.datos);
        mostrar("Datos recuperados", "ok");
        return;
      }
      const local = leerRespaldoLocal();
      if (local && local.texto !== undefined) {
        area.value = local.texto;
        mostrar("Respaldo local cargado", "");
        await guardar(true);
        return;
      }
      mostrar("", "");
    } catch (e) {
      const local = leerRespaldoLocal();
      if (local && local.texto !== undefined) {
        area.value = local.texto;
      }
      mostrar("Sin conexión — usando respaldo local", "err");
    }
  }

  async function guardar(silencioso) {
    const payload = { clave: CLAVE_API, datos: { texto: area.value } };
    respaldoLocal(payload.datos);
    if (!silencioso) mostrar("Guardando…", "");

    try {
      const resp = await fetch("/api/datos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await resp.json().catch(() => ({}));
      if (!resp.ok || !data.ok) {
        throw new Error(data.message || "Error " + resp.status);
      }
      if (!silencioso) mostrar("Guardado en servidor", "ok");
    } catch (e) {
      if (!silencioso) {
        mostrar(
          e.message === "Failed to fetch"
            ? "Sin conexión — guardado solo en este dispositivo"
            : e.message,
          "err"
        );
      }
    }
  }

  function programarGuardado() {
    respaldoLocal({ texto: area.value });
    clearTimeout(timer);
    timer = setTimeout(() => guardar(false), 600);
  }

  area.addEventListener("input", programarGuardado);
  window.addEventListener("beforeunload", () => {
    respaldoLocal({ texto: area.value });
    navigator.sendBeacon(
      "/api/datos",
      new Blob([JSON.stringify({ clave: CLAVE_API, datos: { texto: area.value } })], {
        type: "application/json",
      })
    );
  });

  cargar();
})();
