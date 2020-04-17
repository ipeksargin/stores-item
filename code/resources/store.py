from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'store already exist'},404
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'error saving store'},500

        return store.json(),201

    def get(self,name):
        store= StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'store not found'}, 404

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message':'store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

