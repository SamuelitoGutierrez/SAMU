# =========================================================
# vistas_navbar.py
# Diseño visual idéntico a Apple.com (Mega-menú blanco sólido + Overlay)
# =========================================================

HTML_NAVBAR = """
<style>
    :root {
        --apple-text: #1d1d1f;
        --apple-gray: #86868b;
        --nav-height: 48px;
    }

    /* --- NAVBAR PRINCIPAL --- */
    .apple-nav {
        position: fixed; top: 0; width: 100%; height: var(--nav-height);
        background: rgba(255, 255, 255, 0.95); 
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        z-index: 1000;
        display: flex; justify-content: center;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .nav-content { width: 100%; max-width: 1024px; display: flex; justify-content: space-between; align-items: center; height: 100%; padding: 0 20px; }
    .nav-brand { font-family: 'Bauhaus 93', sans-serif; font-size: 1.3rem; text-decoration: none; color: #000; letter-spacing: 1px;}
    .nav-links { display: flex; gap: 30px; height: 100%; align-items: center; }
    .nav-link-item { font-size: 12px; color: rgba(0,0,0,0.8); cursor: pointer; text-decoration: none; transition: opacity 0.2s; height: 100%; display: flex; align-items: center; font-weight: 400; }
    .nav-link-item:hover { color: #000; }

    /* --- MEGA MENU DESPLEGABLE (BLANCO SÓLIDO) --- */
    .mega-menu {
        position: fixed; top: var(--nav-height); left: 0; width: 100%;
        background: #ffffff; /* BLANCO PURO SÓLIDO COMO APPLE */
        box-shadow: none; 
        border-bottom: 1px solid rgba(0,0,0,0.05); 
        display: grid; grid-template-rows: 0fr; opacity: 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); z-index: 999;
    }

    .mega-menu.active { grid-template-rows: 1fr; opacity: 1; }
    .mega-content { overflow: hidden; max-width: 1024px; margin: 0 auto; width: 100%; padding: 0 20px; }
    .mega-grid { display: flex; gap: 100px; padding: 45px 0 50px 0; }
    
    .mega-col h5 { font-size: 12px; color: var(--apple-gray); font-weight: 400; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 0.5px;}
    .mega-col a { display: block; font-size: 24px; font-weight: 600; color: var(--apple-text); text-decoration: none; margin-bottom: 14px; transition: color 0.2s; }
    .mega-col a:hover { color: #0066cc; }
    
    .mega-sub-col a { font-size: 14px; font-weight: 500; margin-bottom: 12px; color: var(--apple-text); }
    .mega-sub-col a:hover { color: #0066cc; }

    /* --- CORTINA DE DEGRADADO GRIS TRANSPARENTE (OVERLAY) --- */
    .nav-fade-overlay {
        position: fixed;
        top: var(--nav-height);
        left: 0; right: 0; bottom: 0;
        background: linear-gradient(180deg, rgba(245, 245, 247, 0.85) 0%, rgba(245, 245, 247, 0) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        z-index: 998; 
        opacity: 0;
        visibility: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        pointer-events: none;
    }

    .nav-fade-overlay.active {
        opacity: 1;
        visibility: visible;
    }

    /* TOAST DE SEGURIDAD */
    #lockToast {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px);
        background: rgba(29, 29, 31, 0.9); backdrop-filter: blur(10px); color: #fff; padding: 12px 25px; border-radius: 50px;
        font-size: 13px; transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); opacity: 0; z-index: 2000;
    }
    #lockToast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
</style>

<nav class="apple-nav" id="appleNav">
    <div class="nav-content">
        <a href="/panel" class="nav-brand">SAMU</a>
        <div class="nav-links">
            <span class="nav-link-item" onmouseover="openMenu('cuaderno')">Cuaderno de Obra</span>
            <span class="nav-link-item" onmouseover="openMenu('personal')">Control del Personal</span>
            <span class="nav-link-item" onmouseover="openMenu('equipo')">Equipo Mecánico</span>
            <span class="nav-link-item" onmouseover="openMenu('almacen')">Almacén</span>
            <span class="nav-link-item" onmouseover="openMenu('avance')">Avance de Obra</span>
            <span class="nav-link-item" onmouseover="openMenu('sistema')">Sistema</span>
        </div>
        <div style="font-size: 12px; display: flex; align-items: center; font-weight: 500;">
            {HTML_USUARIO}
        </div>
    </div>
</nav>

<div class="nav-fade-overlay" id="navFadeOverlay"></div>

<div class="mega-menu" id="megaMenu">
    <div class="mega-content">
        <div class="mega-grid" id="menuGrid">
            </div>
    </div>
</div>

<div id="lockToast"><i class="bi bi-lock-fill me-2"></i> Acceso restringido.</div>

<script>
    const esAdmin = {ADMIN_JS};
    const menuData = {
        cuaderno: {
            title: "Módulos de Registro",
            main: ["Residencia", "Supervisión"],
            sub: ["Análisis de Residencia", "Análisis de Supervisión", "Exportar Partes Diarios"]
        },
        personal: {
            title: "Gestión Humana",
            main: ["Registro de Personal", "Personal en Obra", "Asistencias"],
            sub: ["Sistema de Papeletas", "Análisis de Asistencias", "Reporte de Tareos"]
        },
        equipo: {
            title: "Control de Flota",
            main: ["Maquinaria y Vehículos", "Operativos", "Horas Máquina"],
            sub: ["Combustible a Equipo", "Análisis Horas Máquina", "Rendimiento por KM"]
        },
        almacen: {
            title: "Inventario",
            main: ["Materiales Generales", "Combustible Principal"],
            sub: ["Análisis de Stock", "Ingresos y Salidas"]
        },
        avance: {
            title: "Ejecución Técnica",
            main: ["Partidas y Metrados", "Actividades Diarias", "Topografía"],
            sub: ["Análisis de Metrados", "Curva S del Proyecto"]
        },
        sistema: {
            title: "Administración",
            main: ["Gestión de Usuarios", "Roles y Permisos"],
            sub: ["Actividad del Sistema", "Configuración Global"]
        }
    };

    let timeoutMenu;
    const megaMenu = document.getElementById('megaMenu');
    const appleNav = document.getElementById('appleNav');
    const navFadeOverlay = document.getElementById('navFadeOverlay');

    function openMenu(cat) {
        clearTimeout(timeoutMenu);
        const data = menuData[cat];
        const grid = document.getElementById('menuGrid');
        grid.innerHTML = `
            <div class="mega-col" style="width: 320px;">
                <h5>${data.title}</h5>
                ${data.main.map(m => `<a href="#" onclick="checkAcceso(event)">${m}</a>`).join('')}
            </div>
            <div class="mega-col mega-sub-col">
                <h5>Más herramientas</h5>
                ${data.sub.map(s => `<a href="#" onclick="checkAcceso(event)">${s}</a>`).join('')}
            </div>
        `;
        megaMenu.classList.add('active');
        navFadeOverlay.classList.add('active');
    }

    function closeMenu() {
        timeoutMenu = setTimeout(() => {
            megaMenu.classList.remove('active');
            navFadeOverlay.classList.remove('active');
        }, 150);
    }

    function cancelClose() {
        clearTimeout(timeoutMenu);
    }

    // --- CORRECCIÓN CLAVE PARA EL MOUSE ---
    // Detectamos la salida y entrada tanto en la barra como en el menú.
    appleNav.addEventListener('mouseleave', closeMenu);
    appleNav.addEventListener('mouseenter', cancelClose);
    
    megaMenu.addEventListener('mouseleave', closeMenu);
    megaMenu.addEventListener('mouseenter', cancelClose);

    function checkAcceso(e) {
        e.preventDefault();
        if (!esAdmin) {
            const toast = document.getElementById('lockToast');
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        } else {
            alert("Redirigiendo al módulo de SAMU...");
        }
    }
</script>
"""
