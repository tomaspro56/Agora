from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes.auth import auth_bp
from routes.pedidos import pedidos_bp
from routes.inventario import inventario_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///agora.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']                     = 'agora-lab-2025'

CORS(app)

db.init_app(app)

app.register_blueprint(auth_bp,      url_prefix='/api/auth')
app.register_blueprint(pedidos_bp,   url_prefix='/api/pedidos')
app.register_blueprint(inventario_bp, url_prefix='/api/productos')


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'}), 200


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
