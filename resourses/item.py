from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    """ parser is like searcher, he select some data from request
    (maybe words, it's like lexical analysis) and give it to us in acceptable format"""
    parser = reqparse.RequestParser()
    # we add arguments which our parser is try to find and give us in kind of dict format
    # if you want to add new arg - use .add_argument again
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank."
    )

    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Every item needs a store_id."
    )

    @jwt_required()
    def get(self, name):
        # can be an error with Item, not a self
        item = ItemModel.find_item_by_name(name)

        if item:
            return item.json_with_store()
        return {"message": "Item not found."}, 404

    def post(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {"message": "item already exist"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data["price"], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted."}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemAll(Resource):
    # here we have just one endpoint - get
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
