from flask import request, jsonify
from models import db, User, Product, Order, OrderItem
from schemas import UserSchema, ProductSchema, OrderSchema
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_routes(app):
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], email=data['email'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    @app.route('/api/products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        product_schema = ProductSchema(many=True)
        return product_schema.jsonify(products), 200

    @app.route('/api/order', methods=['POST'])
    def create_order():
        data = request.get_json()
        new_order = Order(user_id=data['user_id'], total_price=data['total_price'])
        db.session.add(new_order)
        db.session.commit()

        for item in data['items']:
            order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['quantity'])
            db.session.add(order_item)
        
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201
