/* =============================================
   PICKING.JS — Ágora
   ============================================= */

function toggleCheck(el) {
  el.classList.toggle('checked');
  verificarCompletitud();
}

function verificarCompletitud() {
  const checks = document.querySelectorAll('.item-check');
  const completados = Array.from(checks).filter(c => c.classList.contains('checked')).length;
  const total = checks.length;
  const todosCompletos = completados === total;

  const btn = document.getElementById('btn-confirmar');
  const hint = document.getElementById('btn-hint');
  btn.disabled = !todosCompletos;
  if (hint) hint.style.display = todosCompletos ? 'none' : '';

  // Actualizar contador del panel header
  const metaEl = document.querySelector('.panel-card-meta');
  if (metaEl) metaEl.textContent = completados + ' de ' + total + ' completado' + (total !== 1 ? 's' : '');
}

function confirmarPicking() {
  window.location.href = 'packing.html';
}
