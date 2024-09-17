from flask import Blueprint, jsonify, request, g
from app import db
from models import Fruit, FruitSchema
import jwt
from functools import wraps
from config import Config

fruits_bp = Blueprint('fruits', __name__, url_prefix='/fruits')

# Initialize schema
fruit_schema = FruitSchema()
fruits_schema = FruitSchema(many=True)

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            g.user_id = data['id']
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

@fruits_bp.route('/', methods=['GET'])
@token_required
def get_fruits():
    fruits = Fruit.query.all()
    return jsonify(fruits_schema.dump(fruits))

@fruits_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_fruit(id):
    fruit = Fruit.query.get_or_404(id)
    return jsonify(fruit_schema.dump(fruit))

@fruits_bp.route('/', methods=['POST'])
@token_required
def add_fruit():
    data = request.get_json()
    new_fruit = Fruit(
        name=data['name'],
        price=data['price'],
        available=data.get('available', True)
    )
    db.session.add(new_fruit)
    db.session.commit()
    return jsonify(fruit_schema.dump(new_fruit)), 201

@fruits_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_fruit(id):
    data = request.get_json()
    fruit = Fruit.query.get_or_404(id)
    fruit.name = data.get('name', fruit.name)
    fruit.price = data.get('price', fruit.price)
    fruit.available = data.get('available', fruit.available)
    db.session.commit()
    return jsonify(fruit_schema.dump(fruit))

@fruits_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_fruit(id):
    fruit = Fruit.query.get_or_404(id)
    db.session.delete(fruit)
    db.session.commit()
    return jsonify({'message': 'Fruit deleted'})
