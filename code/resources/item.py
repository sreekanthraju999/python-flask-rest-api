from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This filed cannot be left blank'
        )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every Item requires a Store Id.'
        )

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message':'Item Not Found'}, 404

    def post(self,name):

        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'Item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name,**data) #  item = {'name':name, 'price':data['price'],data['store_id']}
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured while inserting Data'}, 500
        return item.json(), 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)

        if item is None:
            return {"message":'No Item Found'}, 400

        item.delete_from_db()
        return {'message':'item deleted'}

    def put(self,name):
        data=Item.parser.parse_args()
        item = ItemModel.find_by_name(name)


        #updated_item=ItemModel(name,data['price'])

        #updated_item={'name':name,'price':data['price']}

        if item is None:
            item = ItemModel(name,**data)

        else:
            item.price = data['price']


        item.save_to_db()
        return item.json()


class ItemsList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
