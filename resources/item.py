from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
import sqlite3
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    def json(self):
        return {'name': self.name,'price':self.price}

    @jwt_required #jwt required to access the item
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'},404

    #@jwt_required() #jwt required to access the item
    def post(self,name):
        data = Item.parser.parse_args()
        #print(data)
        item = ItemModel(name,**data) #(name,**data)

        try:
            ItemModel.save_to_db(item)
        except:
            return {'message':'Error inserting the item'},500

        return item.json(),201

        if ItemModel.find_by_name(name):
            return {'message':'Item already exists'},400
        

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin permission required'},401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db
        return {'message':'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}