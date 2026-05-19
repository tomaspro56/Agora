/* =============================================
   FACTURACION.JS — Ágora
   ============================================= */

function confirmarFactura() {
  const cajas = document.querySelectorAll('.caja-estado');

  cajas.forEach(el => {
    el.textContent = 'Despachado';
    el.className = 'caja-estado estado-despacho';
  });

  setTimeout(() => {
    document.getElementById('confirm-overlay').classList.add('show');
  }, 600);
}
