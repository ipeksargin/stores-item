from models.item import ItemModel
from models.store import StoreModel
from marshmallow import ma


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        include_fk=True
