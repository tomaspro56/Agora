/* =============================================
   TEMA.JS — Ágora
   Gestión de tema claro/oscuro persistente.
   Incluir en <head> de todas las páginas.
   ============================================= */

(function () {
  var LOGO = {
    light: '/imagenes/logo/agoraN.png',
    dark:  '/imagenes/logo/agoraO.png'
  };
  var ICONO = { light: '☾', dark: '☀' };

  function aplicarTema(tema) {
    document.documentElement.setAttribute('data-theme', tema);
    localStorage.setItem('tema', tema);

    var logo = document.getElementById('logo-img');
    if (logo) logo.src = LOGO[tema];

    var btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.textContent = ICONO[tema];
      btn.setAttribute('aria-label', tema === 'dark' ? 'Activar modo claro' : 'Activar modo oscuro');
    }
  }

  // Aplica data-theme inmediatamente (evita flash)
  var temaGuardado = localStorage.getItem('tema') || 'light';
  document.documentElement.setAttribute('data-theme', temaGuardado);

  // Actualiza logo y botón cuando el DOM esté listo
  document.addEventListener('DOMContentLoaded', function () {
    aplicarTema(temaGuardado);
  });

  // Expuesto globalmente para el botón de toggle en todas las páginas
  window.toggleTema = function () {
    var actual = document.documentElement.getAttribute('data-theme') || 'light';
    aplicarTema(actual === 'dark' ? 'light' : 'dark');
  };

  // Toggle de sidebar para mobile
  window.toggleSidebar = function () {
    document.body.classList.toggle('sidebar-open');
  };

  // Cerrar sidebar con ESC
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') document.body.classList.remove('sidebar-open');
  });
})();
