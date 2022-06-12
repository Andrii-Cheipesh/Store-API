from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": f"No {name} store in system."}, 404

    def post(self, name):
        if StoreModel.find_item_by_name(name):
            return {"message": f'Already have {name} store in system.'}, 400
        else:
            store = StoreModel(name)
            store.save_to_db()
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted."}


class StoresAll(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
