from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json(silent=True) or {}

    nombre              = (data.get('nombre') or '').strip()
    usuario             = (data.get('usuario') or '').strip().lower()
    email               = (data.get('email') or '').strip().lower()
    password            = data.get('password') or ''
    rol                 = data.get('rol', 'cliente')
    categoria_proveedor = data.get('categoria_proveedor') or None

    if not nombre or not usuario or not email or not password:
        return jsonify({'error': 'nombre, usuario, email y password son requeridos'}), 400

    if rol not in ('cliente', 'proveedor'):
        return jsonify({'error': 'rol debe ser cliente o proveedor'}), 400

    if rol == 'proveedor' and categoria_proveedor not in (
            'restaurante', 'tecnico', 'farmacia', 'paqueteria'):
        return jsonify({'error': 'categoria_proveedor inválida'}), 400

    if Usuario.query.filter_by(usuario=usuario).first():
        return jsonify({'error': 'El usuario ya está registrado'}), 409

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 409

    nuevo = Usuario(
        nombre=nombre,
        usuario=usuario,
        email=email,
        password_hash=generate_password_hash(password),
        rol=rol,
        categoria_proveedor=categoria_proveedor if rol == 'proveedor' else None,
    )
    db.session.add(nuevo)
    db.session.commit()

    return jsonify(nuevo.to_dict()), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}

    usuario  = (data.get('usuario') or '').strip().lower()
    password = data.get('password') or ''

    if not usuario or not password:
        return jsonify({'error': 'usuario y password son requeridos'}), 400

    u = Usuario.query.filter_by(usuario=usuario).first()

    if not u:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

    if not check_password_hash(u.password_hash, password):
        return jsonify({'error': 'Credenciales incorrectas'}), 401

    return jsonify(u.to_dict()), 200
