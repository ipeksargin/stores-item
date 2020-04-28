from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema


store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

class Store(Resource):
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'store already exist'},404
        
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {'message':'error saving store'},500

        return store_schema.dump(store),201

    def get(self,name):
        store= StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {'message':'store not found'}, 404

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message':'store deleted'},200

    @classmethod
    def find_all(cls):
        return cls.query.all()

class StoreList(Resource):
    def get(self):
        return {'stores': store_list_schema.dump(StoreModel.find_all())},200