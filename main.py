from flask import Flask, render_template,request,redirect,url_for,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)




#Models

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    items=db.relationship('Item',backref='user')


    def toDict(self):
        return{
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)



class Item(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    name=db.Column(db.String,nullable=False)
    image=db.Column(db.String,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    cart_items=db.relationship('Item',backref='item')


    def toDict(self):
        return{
            'id': self.id,
            'name': self.name,
            'image':self.image,
            'quantity': self.quantity,
            'price':self.price
        }

class Cart(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    item_id=db.Column(db.Integer,db.ForeignKey('item.id'))



@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/test',methods=['GET'])
def testroute():
    return "<p1>TEST<p1>"


@app.route('/signup',methods=['POST'])
def signup():
    return jsonify(message="User Created"),200

@app.route('/login',methods=['POST'])
def login():
    return jsonify(message="Login Successful"),200

@app.route('/get_all_users',methods=['GET'])
def get_all_users():

    users=[{
        "id":1,
        "email": "marc123@mail.com",
        "username":"Marc"
    },
    {
        "id":2,
        "email": "matthew234@mail.com",
        "username":"Matthew"   
    },
    {
        "id":3,
        "email":"michael567@mail.com",
        "username":"Michael"
    }]
    return jsonify(users)

@app.route('/get_user_items',methods=['GET'])
def get_user_items():
    user_item= {
    "user_id": 2,
    "email": "matthew234@mail.com",
    "username": "Matthew",
    "items": [
        {
            "item_id": 1,
            "name": "pumpkin",
            "price": "6$ per pound",
            "image": "pumpkin.png",
            "quantity": "40lbs"
        },
        {
            "item_id": 2,
            "name": "mango",
            "price": "$3 per",
            "image": "mango.png",
            "quantity": 20
        }
    ]
}
    return user_item

@app.route('/list_items',methods=['POST'])
def list_items():
    
    return jsonify(message='Item created'),200

@app.route('/rate_user',methods=['POST'])
def rate_user():
    rated={
        "user_id":2,
        "rating":3
    }
    return jsonify(message='User rated'),rated

@app.route('/get_rating',methods=['GET'])
def get_rating():
    user_rating={
    "rating":3
    }
    return user_rating

@app.route('/get_all_items',methods=['GET'])
def get_all_items():
    all_items={"items":[
    {
    "user_id":2,
    "name":"pumpkin",
    "price":"6$ per pound",
    "image":"pumpkin.png",
    "quantity":"40lbs"
    },
    {
    "user_id":2,
    "name":"mango",
    "price":"$3 per",
    "image":"mango.png",
    "quantity":20
    },
    {
    "user_id":2,
    "item_id":3,
    "name":"Pommecythere",
    "price":"$2 per",
    "image":"pommecythere.png",
    "quantity":100
    }
    ]}
    return all_items


@app.route('/bulk_purchase',methods=['GET'])
def bulk_purchase():
    items={
    "user": [
    {
    "user_id": 2,
    "email": "matthew234@mail.com",
    "username": "Matthew",
    "items":[
    {
    "name":"Pommecythere",
    "price":"$2 per",
    "image":"pommecythere.png",
    "quantity":50
    }
        ]
    }
         ]
    }
    return items



@app.route('/search',methods=['GET'])
def search():
    results={
            "items": [
        {
        "name":"mango",
        "price":"$3 per",
        "image":"pumpkin.png",
        "quantity":20
        }
                ]

        }
    return results

@app.route('/sort_by_price',methods=['GET'])
def sort_by_price():
    sorted={
            "items":[
            {
            "item_id":3,
            "name":"Pommecythere",
            "price":"$2 per",
            "image":"pommecythere.png",
            "quantity":100
            },
            {
            "item_id":2,
            "name":"mango",
            "price":"$3 per",
            "image":"pumpkin.png",
            "quantity":20
            },
            {
            "item_id":1,
            "name":"pumpkin",
            "price":"6$ per pound",
            "image":"pumpkin.png",
            "quantity":"40lbs"
            }
                 ]
    }
    return sorted


@app.route('/sort_by_name',methods=['GET'])
def sort_by_name():
    results={
    "items": [
        {
            "item_id": 1,
            "name": "mango",
            "price": "$3 per",
            "image": "pumpkin.png",
            "quantity": 20
        },
        {
            "item_id": 3,
            "name": "Pommecythere",
            "price": "$2 per",
            "image": "pommecythere.png",
            "quantity": 100
        },
        {
            "item_id": 1,
            "name": "pumpkin",
            "price": "6$ per pound",
            "image": "pumpkin.png",
            "quantity": "40lbs"
        }
            ]
    }
    return results


@app.route('/get_item_detail',methods=['GET'])
def get_item_detail():
    item_details={
    "item_id": 1,
    "name": "mango",
    "price": "$3 per",
    "image": "pumpkin.png",
    "quantity": 20,
    "user": {
        "username": "Matthew"
        }
    }
    return item_details


if __name__=="__main__":
    app.run(debug=True)