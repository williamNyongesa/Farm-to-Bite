from app import ma
from models import Fruit

class FruitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Fruit
        load_instance = True
