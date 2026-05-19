from flask import Blueprint, request, jsonify
from models import db, Producto

inventario_bp = Blueprint('inventario', __name__)

CATEGORIAS = ('restaurante', 'tecnico', 'farmacia', 'paqueteria')


@inventario_bp.route('', methods=['GET'])
def listar_productos():
    categoria    = request.args.get('categoria', '').strip().lower()
    proveedor_id = request.args.get('proveedor_id', type=int)

    query = Producto.query.filter_by(activo=True)

    if categoria in CATEGORIAS:
        query = query.filter_by(categoria=categoria)

    if proveedor_id:
        query = query.filter_by(proveedor_id=proveedor_id)

    return jsonify([p.to_dict() for p in query.all()]), 200


@inventario_bp.route('', methods=['POST'])
def crear_producto():
    data = request.get_json(silent=True) or {}

    nombre       = (data.get('nombre') or '').strip()
    descripcion  = (data.get('descripcion') or '').strip()
    precio       = data.get('precio')
    stock        = int(data.get('stock', 0))
    stock_minimo = int(data.get('stock_minimo', 5))
    categoria    = (data.get('categoria') or '').strip().lower()
    proveedor_id = data.get('proveedor_id')

    if not nombre or precio is None or not categoria or not proveedor_id:
        return jsonify({'error': 'nombre, precio, categoria y proveedor_id son requeridos'}), 400

    if categoria not in CATEGORIAS:
        return jsonify({'error': f'categoria debe ser una de: {CATEGORIAS}'}), 400

    producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=float(precio),
        stock=stock,
        stock_minimo=stock_minimo,
        categoria=categoria,
        proveedor_id=proveedor_id,
        activo=True,
    )
    db.session.add(producto)
    db.session.commit()

    return jsonify(producto.to_dict()), 201


@inventario_bp.route('/<int:producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    data     = request.get_json(silent=True) or {}

    if 'nombre' in data:
        producto.nombre = data['nombre'].strip()
    if 'descripcion' in data:
        producto.descripcion = data['descripcion'].strip()
    if 'precio' in data:
        producto.precio = float(data['precio'])
    if 'stock' in data:
        producto.stock = int(data['stock'])
    if 'stock_minimo' in data:
        producto.stock_minimo = int(data['stock_minimo'])
    if 'activo' in data:
        producto.activo = bool(data['activo'])

    db.session.commit()
    return jsonify(producto.to_dict()), 200
