/* =============================================
   LOGIN.JS — Ágora
   ============================================= */

var API_BASE = 'http://localhost:5000/api';

// Si ya hay sesión activa, redirigir sin pasar por login
if (localStorage.getItem('agora_sesion_prov')) {
  window.location.replace('proveedor.html');
} else if (localStorage.getItem('agora_sesion')) {
  window.location.replace('cliente.html');
}

var rolElegido = null;

function elegirRol(rol) {
  rolElegido = rol;
  document.getElementById('step-rol').style.display = 'none';

  if (rol === 'proveedor') {
    document.getElementById('step-prov-login').style.display = 'block';
    setTimeout(function () { document.getElementById('prov-user').focus(); }, 50);
  } else {
    document.getElementById('step-form').style.display = 'block';
    cambiarTab('login');
    setTimeout(function () { document.getElementById('login-user').focus(); }, 50);
  }
}

function cambiarTab(tab) {
  var isLogin = tab === 'login';
  document.getElementById('tab-login').classList.toggle('activo', isLogin);
  document.getElementById('tab-registro').classList.toggle('activo', !isLogin);
  document.getElementById('form-login').style.display    = isLogin ? 'block' : 'none';
  document.getElementById('form-registro').style.display = isLogin ? 'none'  : 'block';
  document.getElementById('error-login').style.display    = 'none';
  document.getElementById('error-registro').style.display = 'none';
}

/* ── Login cliente ── */
function handleLogin(e) {
  e.preventDefault();
  var usuario = document.getElementById('login-user').value.trim();
  var pass    = document.getElementById('login-pass').value;
  var errEl   = document.getElementById('error-login');

  if (!usuario || !pass) {
    errEl.textContent = 'Completa usuario y contraseña para continuar.';
    errEl.style.display = 'block';
    return;
  }
  errEl.style.display = 'none';

  fetch(API_BASE + '/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: usuario, password: pass }),
  })
  .then(function(res) { return res.json().then(function(d) { return { ok: res.ok, data: d }; }); })
  .then(function(r) {
    if (!r.ok) {
      errEl.textContent = r.data.error || 'Credenciales incorrectas.';
      errEl.style.display = 'block';
      return;
    }
    _guardarSesionCliente(r.data);
  })
  .catch(function() {
    // Backend no disponible: guardar sesión localmente igual
    var perfilExistente = JSON.parse(localStorage.getItem('agora_perfil') || '{}');
    _guardarSesionCliente(Object.assign({}, perfilExistente, { nombre: usuario }));
  });
}

function _guardarSesionCliente(u) {
  localStorage.removeItem('proveedorActivo');
  localStorage.setItem('agora_perfil', JSON.stringify({
    id:      u.id      || null,
    nombre:  u.nombre  || u.usuario || 'Usuario',
    usuario: u.usuario || '',
    email:   u.email   || '',
    rol:     u.rol     || 'cliente',
  }));
  localStorage.setItem('agora_sesion', 'true');
  redirigirCliente();
}

/* ── Registro cliente ── */
function handleRegistro(e) {
  e.preventDefault();
  var nombre   = document.getElementById('reg-nombre').value.trim();
  var usuario  = document.getElementById('reg-usuario').value.trim().toLowerCase();
  var correo   = document.getElementById('reg-correo').value.trim();
  var pass     = document.getElementById('reg-pass').value;
  var errEl    = document.getElementById('error-registro');

  if (!nombre || !usuario || !correo || !pass) {
    errEl.textContent = 'Completa todos los campos para continuar.';
    errEl.style.display = 'block';
    return;
  }
  errEl.style.display = 'none';

  fetch(API_BASE + '/auth/registro', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: nombre, usuario: usuario, email: correo, password: pass, rol: 'cliente' }),
  })
  .then(function(res) { return res.json().then(function(d) { return { ok: res.ok, data: d }; }); })
  .then(function(r) {
    if (!r.ok) {
      errEl.textContent = r.data.error || 'Error al crear la cuenta.';
      errEl.style.display = 'block';
      return;
    }
    _guardarSesionCliente(r.data);
  })
  .catch(function() {
    // Backend no disponible: guardar localmente
    localStorage.setItem('agora_perfil', JSON.stringify({ nombre: nombre, usuario: usuario, email: correo }));
    localStorage.removeItem('proveedorActivo');
    localStorage.setItem('agora_sesion', 'true');
    redirigirCliente();
  });
}

function redirigirCliente() {
  localStorage.removeItem('pendingCat');
  window.location.href = 'cliente.html';
}

/* ── Login proveedor ── */
function handleProvLogin(e) {
  e.preventDefault();
  var email = document.getElementById('prov-user').value.trim();
  var pass  = document.getElementById('prov-pass').value;
  var errEl = document.getElementById('error-prov-login');

  if (!email || !pass) {
    errEl.textContent = 'Completa usuario y contraseña para continuar.';
    errEl.style.display = 'block';
    return;
  }
  errEl.style.display = 'none';

  fetch(API_BASE + '/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: email, password: pass }),
  })
  .then(function(res) { return res.json().then(function(d) { return { ok: res.ok, data: d }; }); })
  .then(function(r) {
    if (!r.ok) {
      errEl.textContent = r.data.error || 'Credenciales incorrectas.';
      errEl.style.display = 'block';
      return;
    }
    if (r.data.rol !== 'proveedor') {
      errEl.textContent = 'Esta cuenta no es de proveedor.';
      errEl.style.display = 'block';
      return;
    }
    _guardarSesionProv(r.data);
  })
  .catch(function() {
    // Backend no disponible: guardar localmente
    _guardarSesionProv({ usuario: email, nombre: email });
  });
}

function _guardarSesionProv(usuario) {
  localStorage.setItem('agora_perfil_prov', JSON.stringify({
    id:       usuario.id       || null,
    usuario:  usuario.email    || usuario.usuario || 'Proveedor',
    nombre:   usuario.nombre   || '',
    categoria: usuario.categoria_proveedor || null,
  }));
  localStorage.setItem('agora_sesion_prov', 'true');

  // Mostrar el selector de tipo de servicio
  document.getElementById('step-prov-login').style.display = 'none';
  document.getElementById('step-prov').style.display = 'block';
}

/* ── Selector de servicio proveedor ── */
function accederProveedor(tipo) {
  localStorage.setItem('proveedorActivo', tipo);
  window.location.href = 'proveedor.html';
}

/* ── Volver al selector de rol ── */
function volverAlRol() {
  document.getElementById('step-form').style.display       = 'none';
  document.getElementById('step-prov').style.display       = 'none';
  document.getElementById('step-prov-login').style.display = 'none';
  document.getElementById('step-rol').style.display        = 'block';
  rolElegido = null;
}

/* ── Mostrar / ocultar contraseña ── */
function togglePass(inputId, btn) {
  var input = document.getElementById(inputId);
  var svg   = btn.querySelector('svg');
  var mostrar = input.type === 'password';
  input.type = mostrar ? 'text' : 'password';
  // Ojo abierto vs ojo tachado
  svg.innerHTML = mostrar
    ? '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/>'
    : '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
}
