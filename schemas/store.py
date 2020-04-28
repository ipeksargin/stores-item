from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema
from marshmallow import ma


class StoreSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many=True) #relation
    class Meta:
        model = StoreModel
        dump_only = ("id",)
        include_fk=True
