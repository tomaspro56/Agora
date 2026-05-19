from flask import Blueprint, request, jsonify
from models import db, Pedido, DetallePedido

pedidos_bp = Blueprint('pedidos', __name__)


@pedidos_bp.route('', methods=['POST'])
def crear_pedido():
    data = request.get_json(silent=True) or {}

    cliente_id  = data.get('cliente_id')
    proveedor_id = data.get('proveedor_id')
    direccion   = (data.get('direccion') or '').strip()
    descripcion = (data.get('descripcion') or '').strip()
    total       = data.get('total', 0.0)
    detalles    = data.get('detalles', [])

    if not cliente_id:
        return jsonify({'error': 'cliente_id es requerido'}), 400

    pedido = Pedido(
        cliente_id=cliente_id,
        proveedor_id=proveedor_id,
        estado='recibido',
        direccion=direccion,
        descripcion=descripcion,
        total=float(total),
    )
    db.session.add(pedido)
    db.session.flush()  # obtener el id antes del commit

    for item in detalles:
        detalle = DetallePedido(
            pedido_id=pedido.id,
            producto_id=item.get('producto_id'),
            cantidad=int(item.get('cantidad', 1)),
            precio_unitario=float(item.get('precio_unitario', 0)),
        )
        db.session.add(detalle)

    db.session.commit()
    return jsonify(pedido.to_dict()), 201


@pedidos_bp.route('', methods=['GET'])
def listar_pedidos():
    cliente_id   = request.args.get('cliente_id', type=int)
    proveedor_id = request.args.get('proveedor_id', type=int)

    query = Pedido.query

    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    elif proveedor_id:
        query = query.filter_by(proveedor_id=proveedor_id)
    else:
        return jsonify({'error': 'Proporciona cliente_id o proveedor_id'}), 400

    pedidos = query.order_by(Pedido.fecha_creacion.desc()).all()
    return jsonify([p.to_dict() for p in pedidos]), 200


@pedidos_bp.route('/<int:pedido_id>/estado', methods=['PUT'])
def cambiar_estado(pedido_id):
    data        = request.get_json(silent=True) or {}
    nuevo_estado = data.get('estado', '').strip()

    if nuevo_estado not in Pedido.ESTADOS:
        return jsonify({'error': f'Estado inválido. Opciones: {Pedido.ESTADOS}'}), 400

    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = nuevo_estado
    db.session.commit()

    return jsonify(pedido.to_dict()), 200
