from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from models import db, User, Product, Order, OrderItem
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

# Enable CORS for cross-origin requests
CORS(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://william:TheNyongess!!11@localhost/fruits"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Setup login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User loader for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Index route
class Index(Resource):
    def get(self):
        return {"message": "Welcome to the Farm Shopping App!"}

# User resource
class UserResource(Resource):
    @login_required
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            return [{"username": user.username, "email": user.email} for user in users]
        else:
            user = User.query.get_or_404(user_id)
            return {"username": user.username, "email": user.email}

# Product resource
class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id is None:
            products = Product.query.all()
            return [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "image": product.image
                }
                for product in products
            ]
        else:
            product = Product.query.get_or_404(product_id)
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "image": product.image
            }

# Order resource
class OrderResource(Resource):
    @login_required
    def get(self, order_id=None):
        if order_id is None:
            orders = Order.query.filter_by(user_id=current_user.id).all()
            return [
                {
                    "id": order.id,
                    "total_price": order.total_price,
                    "status": order.status,
                    "created_at": order.created_at.isoformat()
                }
                for order in orders
            ]
        else:
            order = Order.query.get_or_404(order_id)
            return {
                "id": order.id,
                "total_price": order.total_price,
                "status": order.status,
                "created_at": order.created_at.isoformat()
            }

    def post(self):
        data = request.get_json()
        new_order = Order(user_id=current_user.id, total_price=data["total_price"])
        db.session.add(new_order)
        db.session.commit()

        for item in data["items"]:
            order_item = OrderItem(order_id=new_order.id, product_id=item["product_id"], quantity=item["quantity"])
            db.session.add(order_item)
        
        db.session.commit()
        return {"message": "Order created successfully"}, 201

# Register resource
class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
        # Create a new user instance
        new_user = User(username=data["username"], email=data["email"], password=hashed_password)
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201






# Login resource
class Login(Resource):
    def get(self):
        return {"message": "Please log in with your email and password."}, 200

    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and check_password_hash(user.password, data['password']):
            login_user(user)
            return {"message": "Logged in successfully", "user": {"id": user.id, "email": user.email}}, 200
        else:
            return {"message": "Invalid email or password"}, 400

# Logout resource
class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {"message": "Logged out successfully"}, 200

# Add resources to the API
api.add_resource(Index, "/")
api.add_resource(UserResource, "/users", "/user/<int:user_id>")
api.add_resource(ProductResource, "/products", "/product/<int:product_id>")
api.add_resource(OrderResource, "/orders", "/order/<int:order_id>")
api.add_resource(RegisterResource, "/register")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

# Run the application
if __name__ == "__main__":
    app.run(port=3001, debug=True)
