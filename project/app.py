from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT, jwt_required
from db import db


#----- Adding Resource ---
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoreList
#--------------------------



app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
api=Api(app)
app.secret_key='sree'

# Creates All the Tables before the first request Happens if no database is present
@app.before_first_request
def create_tables():
    db.create_all()
#--------------------------------------------------------

jwt=JWT(app,authenticate,identity) #/auth

api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemsList,'/items')
api.add_resource(Item,'/item/<string:name>') #http://127.0.0.1/student/sree
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
