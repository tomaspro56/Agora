from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id                  = db.Column(db.Integer, primary_key=True)
    nombre              = db.Column(db.String(120), nullable=False)
    usuario             = db.Column(db.String(80),  unique=True, nullable=False)
    email               = db.Column(db.String(200), unique=True, nullable=False)
    password_hash       = db.Column(db.String(256), nullable=False)
    rol                 = db.Column(db.String(20), nullable=False)          # 'cliente' | 'proveedor'
    categoria_proveedor = db.Column(db.String(30), nullable=True)           # restaurante/tecnico/farmacia/paqueteria
    fecha_creacion      = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos_como_cliente   = db.relationship('Pedido', foreign_keys='Pedido.cliente_id',
                                              backref='cliente', lazy=True)
    pedidos_como_proveedor = db.relationship('Pedido', foreign_keys='Pedido.proveedor_id',
                                              backref='proveedor', lazy=True)
    productos              = db.relationship('Producto', backref='proveedor', lazy=True)

    def to_dict(self):
        return {
            'id':                  self.id,
            'nombre':              self.nombre,
            'usuario':             self.usuario,
            'email':               self.email,
            'rol':                 self.rol,
            'categoria_proveedor': self.categoria_proveedor,
            'fecha_creacion':      self.fecha_creacion.isoformat(),
        }


class Producto(db.Model):
    __tablename__ = 'productos'

    id           = db.Column(db.Integer, primary_key=True)
    nombre       = db.Column(db.String(200), nullable=False)
    descripcion  = db.Column(db.Text, nullable=True)
    precio       = db.Column(db.Float, nullable=False)
    stock        = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    categoria    = db.Column(db.String(30), nullable=False)  # restaurante/tecnico/farmacia/paqueteria
    proveedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    activo       = db.Column(db.Boolean, default=True)

    detalles = db.relationship('DetallePedido', backref='producto', lazy=True)

    def to_dict(self):
        return {
            'id':           self.id,
            'nombre':       self.nombre,
            'descripcion':  self.descripcion,
            'precio':       self.precio,
            'stock':        self.stock,
            'stock_minimo': self.stock_minimo,
            'categoria':    self.categoria,
            'proveedor_id': self.proveedor_id,
            'activo':       self.activo,
        }


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    ESTADOS = ['recibido', 'aceptado', 'preparando', 'en_camino', 'entregado', 'cancelado']

    id             = db.Column(db.Integer, primary_key=True)
    cliente_id     = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    proveedor_id   = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    estado         = db.Column(db.String(20), default='recibido')
    direccion      = db.Column(db.String(300), nullable=True)
    descripcion    = db.Column(db.Text, nullable=True)
    total          = db.Column(db.Float, default=0.0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    detalles = db.relationship('DetallePedido', backref='pedido',
                                lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id':             self.id,
            'cliente_id':     self.cliente_id,
            'proveedor_id':   self.proveedor_id,
            'estado':         self.estado,
            'direccion':      self.direccion,
            'descripcion':    self.descripcion,
            'total':          self.total,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'detalles':       [d.to_dict() for d in self.detalles],
        }


class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'

    id             = db.Column(db.Integer, primary_key=True)
    pedido_id      = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id    = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad       = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id':              self.id,
            'pedido_id':       self.pedido_id,
            'producto_id':     self.producto_id,
            'cantidad':        self.cantidad,
            'precio_unitario': self.precio_unitario,
        }
