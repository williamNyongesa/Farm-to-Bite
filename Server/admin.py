from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import User, Fruit

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Create admin interface
admin = Admin(app, name='Farm-to-Bite Admin', template_mode='bootstrap3')

# Add views for models
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Fruit, db.session))

@app.route('/admin/')
def admin_index():
    return admin.index()

# Register blueprint
app.register_blueprint(admin_bp)
