# =========================================================
# vistas_navbar.py
# Plantilla Visual del Menú SAMU - Completo y Responsivo
# =========================================================

HTML_NAVBAR = """
<style>
    :root {
        --apple-text: #1d1d1f;
        --apple-gray: #86868b;
        --nav-height: 52px;
    }

    /* --- BARRA PRINCIPAL --- */
    .apple-nav {
        position: fixed; 
        top: 0; 
        width: 100%; 
        height: var(--nav-height);
        background: rgba(255, 255, 255, 0.90); 
        backdrop-filter: saturate(180%) blur(20px); 
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        z-index: 1000; 
        display: flex; 
        justify-content: center; 
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .nav-content { 
        width: 100%; 
        max-width: 1100px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        height: 100%; 
        padding: 0 20px; 
    }
    
    .nav-brand { 
        font-family: 'Bauhaus 93', sans-serif; 
        font-size: 1.4rem; 
        text-decoration: none; 
        color: #000; 
        letter-spacing: 1px;
    }
    
    /* --- ENLACES ESCRITORIO --- */
    .nav-links { 
        display: flex; 
        gap: 28px; 
        height: 100%; 
        align-items: center; 
    }
    
    .nav-link-item { 
        font-size: 12px; 
        color: rgba(0,0,0,0.8); 
        cursor: pointer; 
        text-decoration: none; 
        transition: color 0.2s; 
        height: 100%; 
        display: flex; 
        align-items: center; 
        font-weight: 500; 
    }
    
    .nav-link-item:hover { 
        color: #0066cc; 
    }

    /* --- MEGA MENÚ ESCRITORIO --- */
    .mega-menu { 
        position: fixed; 
        top: var(--nav-height); 
        left: 0; 
        width: 100%; 
        background: rgba(255, 255, 255, 0.98); 
        backdrop-filter: blur(25px); 
        border-bottom: 1px solid rgba(0,0,0,0.05); 
        display: grid; 
        grid-template-rows: 0fr; 
        opacity: 0; 
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
        z-index: 999; 
    }
    
    .mega-menu.active { 
        grid-template-rows: 1fr; 
        opacity: 1; 
    }
    
    .mega-content { 
        overflow: hidden; 
        max-width: 1100px; 
        margin: 0 auto; 
        width: 100%; 
        padding: 0 20px; 
    }
    
    .mega-grid { 
        display: flex; 
        gap: 80px; 
        padding: 40px 0 50px 0; 
    }
    
    .mega-col h5 { 
        font-size: 11px; 
        color: var(--apple-gray); 
        font-weight: 600; 
        margin-bottom: 20px; 
        text-transform: uppercase; 
    }
    
    .mega-col a { 
        display: block; 
        font-size: 22px; 
        font-weight: 600; 
        color: var(--apple-text); 
        text-decoration: none; 
        margin-bottom: 12px; 
        transition: color 0.2s; 
        letter-spacing: -0.5px; 
    }
    
    .mega-sub-col a { 
        font-size: 13px; 
        font-weight: 500; 
        margin-bottom: 10px; 
    }
    
    .mega-col a:hover, .mega-sub-col a:hover { 
        color: #0066cc; 
    }

    /* --- OVERLAY OSCURO --- */
    .nav-fade-overlay { 
        position: fixed; 
        top: var(--nav-height); 
        left: 0; 
        right: 0; 
        bottom: 0; 
        background: rgba(0, 0, 0, 0.2); 
        backdrop-filter: blur(5px); 
        z-index: 998; 
        opacity: 0; 
        visibility: hidden; 
        transition: all 0.4s ease; 
        pointer-events: none; 
    }
    
    .nav-fade-overlay.active { 
        opacity: 1; 
        visibility: visible; 
    }

    /* --- ELEMENTOS MÓVILES --- */
    .btn-mobile-menu { 
        display: none; 
        background: none; 
        border: none; 
        font-size: 28px; 
        color: #1d1d1f; 
        cursor: pointer; 
        padding: 0; 
        transition: transform 0.2s;
    }
    
    .user-info-desktop { 
        font-size: 13px; 
        display: flex; 
        align-items: center; 
        font-weight: 500; 
        color: #1d1d1f; 
    }
    
    /* Panel del Menú Móvil */
    .mobile-dropdown {
        position: fixed; 
        top: var(--nav-height); 
        left: 0; 
        width: 100%; 
        height: calc(100vh - var(--nav-height));
        background: rgba(255, 255, 255, 0.98); 
        backdrop-filter: blur(25px); 
        -webkit-backdrop-filter: blur(25px);
        z-index: 999; 
        transform: translateY(-100%); 
        opacity: 0; 
        visibility: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
        overflow-y: auto; 
        padding: 30px 20px 80px 20px;
    }
    
    .mobile-dropdown.open { 
        transform: translateY(0); 
        opacity: 1; 
        visibility: visible; 
    }
    
    /* Estilos de los links en móvil */
    .mobile-category { 
        margin-bottom: 25px; 
    }
    
    .mobile-main-link {
        display: block;
        font-size: 22px;
        font-weight: 700;
        color: #1d1d1f;
        text-decoration: none;
        border-bottom: 2px solid rgba(0,0,0,0.05);
        padding-bottom: 12px;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    
    .mobile-main-link:hover {
        color: #0066cc;
    }
    
    .mobile-sub-item {
        display: block;
        font-size: 16px;
        font-weight: 500;
        color: #4b5563;
        text-decoration: none;
        margin-bottom: 15px;
        padding-left: 15px;
        border-left: 2px solid transparent;
        transition: all 0.2s;
    }
    
    .mobile-sub-item:hover {
        color: #0066cc;
        border-left: 2px solid #0066cc;
    }

    /* --- ALERTAS DEL SISTEMA --- */
    #lockToast { 
        position: fixed; 
        bottom: 30px; 
        left: 50%; 
        transform: translateX(-50%) translateY(100px); 
        background: #1d1d1f; 
        color: #fff; 
        padding: 14px 28px; 
        border-radius: 50px; 
        font-size: 13px; 
        font-weight: 500; 
        transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
        opacity: 0; 
        z-index: 2000; 
        white-space: nowrap;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    #lockToast.show { 
        transform: translateX(-50%) translateY(0); 
        opacity: 1; 
    }

    /* --- MEDIA QUERIES (TABLET Y CELULAR) --- */
    @media (max-width: 991px) {
        .nav-links { display: none; } 
        .user-info-desktop { display: none; } 
        .btn-mobile-menu { display: block; } 
        .mega-menu { display: none !important; } 
    }
</style>

<nav class="apple-nav" id="appleNav">
    <div class="nav-content">
        <a href="/panel" class="nav-brand">SAMU</a>
        
        <div class="nav-links">
            <a href="/cuaderno" class="nav-link-item" onmouseover="openMenu('cuaderno')">Cuaderno de Obra</a>
            <a href="#" class="nav-link-item" onmouseover="openMenu('personal')">Control del Personal</a>
            <a href="#" class="nav-link-item" onmouseover="openMenu('equipo')">Equipo Mecánico</a>
            <a href="/almacen" class="nav-link-item" onmouseover="openMenu('almacen')">Almacén</a>
            <a href="#" class="nav-link-item" onmouseover="openMenu('avance')">Avance de Obra</a>
            <a href="#" class="nav-link-item" onmouseover="openMenu('sistema')">Sistema</a>
        </div>
        
        <div class="user-info-desktop">{HTML_USUARIO}</div>
        
        <button class="btn-mobile-menu" id="btnMobileToggle" onclick="toggleMobileMenu()">
            <i class="bi bi-list" id="mobileIcon"></i>
        </button>
    </div>
</nav>

<div class="nav-fade-overlay" id="navFadeOverlay"></div>
<div class="mega-menu" id="megaMenu">
    <div class="mega-content"><div class="mega-grid" id="menuGrid"></div></div>
</div>

<div class="mobile-dropdown" id="mobileDropdown">
    <div style="font-size: 14px; font-weight: 600; color: #0066cc; margin-bottom: 30px; text-align: center; background: rgba(0,102,204,0.05); padding: 15px; border-radius: 16px;">
        <i class="bi bi-person-circle me-1"></i> {HTML_USUARIO}
    </div>
    <div id="mobileContent"></div>
</div>

<div id="lockToast"><i class="bi bi-shield-lock-fill me-2" style="color: #f9a8d4;"></i> Notificación del Sistema</div>

<script>
    const esAdmin = {ADMIN_JS};
    const rolUsuario = {ROL_JS};
    
    // Matriz de Datos: Hemos agregado navLabel y navUrl para que el celular sepa cuáles son las opciones principales.
    const menuData = {
        cuaderno: { 
            navLabel: "Cuaderno de Obra", navUrl: "/cuaderno",
            title: "Módulos de Registro", 
            main: [{ label: "Residencia", url: "/residencia" }, { label: "Supervisión", url: "/supervision" }], 
            sub: [{ label: "Análisis General", url: "#" }] 
        },
        personal: { 
            navLabel: "Control del Personal", navUrl: "#",
            title: "Gestión Humana", 
            main: [{ label: "Personal en Obra", url: "#" }, { label: "Asistencias", url: "#" }], 
            sub: [] 
        },
        equipo: { 
            navLabel: "Equipo Mecánico", navUrl: "#",
            title: "Control de Flota", 
            main: [{ label: "Maquinaria Operativa", url: "#" }, { label: "Horas Máquina", url: "#" }], 
            sub: [] 
        },
        almacen: { 
            navLabel: "Almacén", navUrl: "/almacen",
            title: "Movimientos de Almacén", 
            main: [
                { label: "Panel de Movimientos", url: "/almacen" },
                { label: "Materiales de Construcción", url: "/almacen/materiales" },
                { label: "Combustible", url: "/almacen/combustible" }
            ], 
            sub: [] 
        },
        avance: { 
            navLabel: "Avance de Obra", navUrl: "#",
            title: "Ejecución Técnica", 
            main: [{ label: "Partidas y Metrados", url: "#" }], 
            sub: [] 
        },
        sistema: {
            navLabel: "Sistema", navUrl: "#",
            title: "Administración",
            main: [{ label: "Usuarios y Permisos", url: "#" }],
            sub: []
        }
    };

    // --- LÓGICA DE ESCRITORIO ---
    let timeoutMenu;
    const megaMenu = document.getElementById('megaMenu');
    const navFadeOverlay = document.getElementById('navFadeOverlay');

    function openMenu(cat) {
        if(window.innerWidth <= 991) return; 
        clearTimeout(timeoutMenu); 
        const data = menuData[cat]; 
        if(!data) return;
        
        document.getElementById('menuGrid').innerHTML = `
            <div class="mega-col" style="width: 280px;">
                <h5>${data.title}</h5>
                ${data.main.map(m => `<a href="${m.url}" onclick="checkAcceso(event, '${m.url}')">${m.label}</a>`).join('')}
            </div>
            <div class="mega-col mega-sub-col">
                <h5>Más herramientas</h5>
                ${data.sub.map(s => `<a href="${s.url}" onclick="checkAcceso(event, '${s.url}')">${s.label}</a>`).join('')}
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

    function cancelClose() { clearTimeout(timeoutMenu); }

    document.getElementById('appleNav').addEventListener('mouseleave', closeMenu);
    document.getElementById('appleNav').addEventListener('mouseenter', cancelClose);
    megaMenu.addEventListener('mouseleave', closeMenu); 
    megaMenu.addEventListener('mouseenter', cancelClose);

    // --- LÓGICA MÓVIL CORREGIDA ---
    const mobileDropdown = document.getElementById('mobileDropdown');
    const mobileIcon = document.getElementById('mobileIcon');
    let isMobileMenuOpen = false;

    // Generamos el HTML móvil asegurándonos de incluir el Título Principal
    const mobileContent = document.getElementById('mobileContent');
    let mobileHTML = '';
    Object.values(menuData).forEach(seccion => {
        // Título Principal Clicable
        mobileHTML += `
        <div class="mobile-category">
            <a href="${seccion.navUrl}" class="mobile-main-link" onclick="checkAcceso(event, '${seccion.navUrl}')">
                ${seccion.navLabel}
            </a>
            <div style="padding-left: 10px;">
                <h6 style="font-size: 10px; color: var(--apple-gray); text-transform: uppercase; margin: 15px 0 10px 5px; font-weight: 700;">
                    ${seccion.title}
                </h6>
        `;
        // Opciones Internas
        seccion.main.forEach(link => { 
            mobileHTML += `<a href="${link.url}" class="mobile-sub-item" onclick="checkAcceso(event, '${link.url}')">${link.label}</a>`; 
        });
        mobileHTML += `</div></div>`;
    });
    mobileContent.innerHTML = mobileHTML;

    function toggleMobileMenu() {
        isMobileMenuOpen = !isMobileMenuOpen;
        const btn = document.getElementById('btnMobileToggle');
        if(isMobileMenuOpen) {
            mobileDropdown.classList.add('open');
            mobileIcon.classList.replace('bi-list', 'bi-x-lg');
            btn.style.transform = "rotate(90deg)";
            document.body.style.overflow = 'hidden'; 
        } else {
            mobileDropdown.classList.remove('open');
            mobileIcon.classList.replace('bi-x-lg', 'bi-list');
            btn.style.transform = "rotate(0deg)";
            document.body.style.overflow = '';
        }
    }

    // --- SEGURIDAD ---
    function tieneAcceso(url) {
        if (esAdmin) return true;
        if (url === '#') return false;
        if (rolUsuario === 'Almacenero' && url.startsWith('/almacen')) return true;
        if (['Ingeniero', 'Residente', 'Supervisor'].includes(rolUsuario)) {
            return ['/cuaderno', '/residencia', '/supervision', '/panel'].some(ruta => url.startsWith(ruta));
        }
        return false;
    }

    function checkAcceso(e, url) {
        if (!tieneAcceso(url)) {
            e.preventDefault();
            const toast = document.getElementById('lockToast');
            toast.innerHTML = url === '#' ? '<i class="bi bi-tools me-2" style="color: #0ea5e9;"></i> En construcción.' : '<i class="bi bi-shield-lock-fill me-2" style="color: #f9a8d4;"></i> Sin acceso.';
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        } else if(window.innerWidth <= 991) {
            // Cierra el menú suavemente al navegar en celular
            toggleMobileMenu(); 
        }
    }
</script>
"""
