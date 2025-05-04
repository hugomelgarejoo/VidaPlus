from flask import Blueprint, request, jsonify
import jwt
import datetime
from werkzeug.security import check_password_hash
from database import get_db_connection
from auth import auth_bp
from functools import wraps
from flask import request

app.register_blueprint(auth_bp)


auth_bp = Blueprint('auth', __name__)
chave_secreta = 'Jun99'

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and check_password_hash(usuario['senha'], senha):
        token = jwt.encode({
            'usuario_id': usuario['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, chave_secreta, algorithm='HS256')

        return jsonify({'token': token})

    return jsonify({'erro': 'Credenciais inválidas'}), 401

def login_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'erro': 'Token JWT ausente'}), 401

        try:
            dados = jwt.decode(token, chave_secreta, algorithms=['HS256'])
            request.usuario_id = dados['usuario_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated
