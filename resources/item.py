from flask_restful import Resource
from flask import request
from schemas.item import ItemSchema
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional,get_jwt_identity
import sqlite3
from models.item import ItemModel
from marshmallow import ValidationError

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)
class Item(Resource):
    @jwt_required #jwt required to access the item
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item),200
        return {'message':'item not found'},404

    #@jwt_required() #jwt required to access the item
    def post(self,name):
        item_json = request.get_json() #price,id
        item_json["name"] = name

        try:
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages,400

        try:
            ItemModel.save_to_db(item)
        except:
            return {'message':'Error inserting the item'},500

        return item_schema.dump(item),201

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

    def put(self, name): #put and post 
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json['price']
        else:
            item_json["name"] = name
    
            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages,400
        item.save_to_db()
        return item_json.dump(item),200

class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity() #the id stored in jwt
        items = [item_list_schema.dump(ItemModel.find_all())]
        if user_id:
            return {'items': items},200
        return {'items':[item['name'] for item in items],
                'message':'More data avaliable if you login.'},200