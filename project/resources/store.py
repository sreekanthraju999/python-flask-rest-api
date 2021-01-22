from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'No Store Found'}, 404

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            print(store.json())
            return {'message': 'Store Already exists'}, 400
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An Error while creating the Store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
            return {'message': 'Store Deleted Successfully'}
        return {'message': 'No Store Found'}, 404

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
