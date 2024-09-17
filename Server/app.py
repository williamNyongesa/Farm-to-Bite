from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import Config
from routes import fruits_bp
from auth import auth_bp

# Initialize app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize CORS, database, and marshmallow for serialization
CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

def create_app():
    from routes import fruits_bp
    app.register_blueprint(fruits_bp)
    return app

# Main entry point
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
