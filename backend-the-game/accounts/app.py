from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime
import psycopg2
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://wfwbzwfgjbfqrz:06d8ed7b46af6d80d3ef18ffa8a3fb6921dd14c888d98d3a9f202501e1af4e33@ec2-44-198-236-169.compute-1.amazonaws.com:5432/df4ilmqt009tc0"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
bcrypt = Bcrypt(app)

class Users(db.Model):
    users_id = db.Column(db.Integer, primary_key=True)
    users_name = db.Column(db.String, unique=True, nullable=False)
    users_password = db.Column(db.String, nullable=False)
    users_email = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, users_name, users_password, users_email):
        self.users_name = users_name
        self.users_password = users_password
        self.users_email = users_email

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('users_id', 'users_name', 'users_password', 'users_email')

users_schema = UsersSchema()
multiple_users_schema = UsersSchema(many=True)

@app.route('/user/add', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be JSON')

    post_data = request.get_json()
    users_name = post_data.get('users_name')
    users_password = post_data.get('users_password')
    users_email = post_data.get('users_email')

    possible_duplicate_user = db.session.query(Users).filter(Users.users_name == users_name).first()
    possible_duplicate_email = db.session.query(Users).filter(Users.users_email == users_email).first()

    if possible_duplicate_user is not None:
        return jsonify('Error: That username has been taken')

    if possible_duplicate_email is not None:
        return jsonify('Error: That email has been taken')

    encrypt_users_password = bcrypt.generate_password_hash(users_password).decode("utf-8")
    new_user = Users(users_name, encrypt_users_password, users_email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify("User has been successfully added")

@app.route('/user/verify', methods=['POST'])
def verify_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be JSON')

    post_data = request.get_json()
    users_name = post_data.get('users_name')
    users_password = post_data.get('users_password')
    users_email = post_data.get('users_email')

    user = db.session.query(Users).filter(Users.users_name == users_name).first() or db.session.query(Users).filter(Users.users_email == users_email).first()

#TODO check back at SQLAlchmey if problems arise on loging in
    if user is None:
        return jsonify ('User not verified')

    if bcrypt.check_password_hash(user.users_password, users_password) == False:
        return jsonify ('User password not verified')

    return jsonify('User has been verified')

@app.route('/user/get', methods=['GET'])
def get_users():
    users = db.session.query(Users).all()
    return jsonify(multiple_users_schema.dump(users))

@app.route('/user/get/<id>', methods=['GET'])
def get_user(id):
    user = db.session.query(Users).filter(Users.users_id == id).first()
    return jsonify(users_schema.dump(user))

@app.route('/user/get/username/<users_name>', methods=['GET'])
def get_user_by_username(users_name):
    username = db.session.query(Users).filter(Users.users_name == users_name).first()
    return jsonify(users_schema.dump(username))

class Users_Info(db.Model):
    users_id = db.Column(db.Integer, primary_key=True)
    users_first_name = db.Column(db.String, unique=False, nullable=False)
    users_middle_name = db.Column(db.String, unique=False, nullable=False)
    users_last_name = db.Column(db.String, unique=False, nullable=False)
    users_birthday = db.Column(db.String, nullable=False)

    def __init__(self, users_first_name, users_middle_name, users_last_name, users_birthday):
        self.users_first_name = users_first_name
        self.users_middle_name = users_middle_name
        self.users_last_name = users_last_name
        self.users_birthday = users_birthday

class Users_InfoSchema(ma.Schema):
    class Meta:
        fields = ('users_id', 'users_first_name', 'users_middle_name', 'users_last_name', 'users_birthday')

users_info_schema = Users_InfoSchema()
multiple_users_info_schema = Users_InfoSchema(many=True)


@app.route('/users-info/add', methods=['POST'])
def add_user_info():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be JSON')

    post_data = request.get_json()
    users_first_name = post_data.get('users_first_name')
    users_middle_name = post_data.get('users_middle_name')
    users_last_name = post_data.get('users_last_name')
    users_birthday = post_data.get('users_birthday')

    new_user_info = Users_Info(users_first_name, users_middle_name, users_last_name, users_birthday)

    db.session.add(new_user_info)
    db.session.commit()

    return jsonify("User info has been successfully added")

@app.route('/users-info/get', methods=['GET'])
def get_users_info():
    users_info = db.session.query(Users_Info).all()
    return jsonify(multiple_users_info_schema.dump(users_info))

class Products(db.Model):
    products_id = db.Column(db.Integer, primary_key=True)
    products_title = db.Column(db.String, unique=False, nullable=False)
    products_image = db.Column(db.String, unique=False, nullable=False)
    products_description = db.Column(db.String, unique=False, nullable=False)
    products_price = db.Column(db.Integer, unique=False, nullable=False)
    products_category = db.Column(db.String, unique=False, nullable=False)


    def __init__(self, products_title, products_image, products_description, products_price, products_category ):
        self.products_title = products_title
        self.products_image = products_image
        self.products_description = products_description
        self.products_price = products_price
        self.products_category = products_category 


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ('products_id', 'products_title', 'products_image', 'products_description', 'products_price', 'products_category ')

products_schema = ProductsSchema()
multiple_products_schema = ProductsSchema(many=True)


@app.route('/products/add', methods=['POST'])
def add_products():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be JSON')

    post_data = request.get_json()
    products_title = post_data.get('products_title')
    products_image = post_data.get('products_image')
    products_description = post_data.get('products_description')
    products_price = post_data.get('products_price')
    products_category  = post_data.get('products_category')

    new_products = Products(products_title, products_image, products_description, products_price, products_category )

    db.session.add(new_products)
    db.session.commit()

    return jsonify("Product has been successfully added")

@app.route('/products/get', methods=['GET'])
def get_products():
    products = db.session.query(Products).all()
    return jsonify(multiple_products_schema.dump(products))

class Users_Products(db.Model):
    users_products_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, unique=False, nullable=False)
    products_id = db.Column(db.Integer, unique=False, nullable=False)
    products_title = db.Column(db.String, unique=False, nullable=False)
    products_image = db.Column(db.String, unique=False, nullable=False)
    products_description = db.Column(db.String, unique=False, nullable=False)
    products_price = db.Column(db.Integer, unique=False, nullable=False)
    products_category = db.Column(db.String, unique=False, nullable=False)


    def __init__(self, users_id, products_id, products_title, products_image, products_description, products_price, products_category):
        self.users_id = users_id
        self.products_title = products_title
        self.products_image = products_image
        self.products_description = products_description
        self.products_price = products_price
        self.products_category = products_category


class Users_ProductsSchema(ma.Schema):
    class Meta:
        fields = ('users_products_id', 'users_id', 'products_id', 'products_title', 'products_image', 'products_description', 'products_price, products_category')

users_products_schema = Users_ProductsSchema()
multiple_users_products_schema = Users_ProductsSchema(many=True)


@app.route('/users_products/add', methods=['POST'])
def add_users_products():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be JSON')

    post_data = request.get_json()
    users_id = post_data.get('users_id')
    products_title = post_data.get('products_title')
    products_image = post_data.get('products_image')
    products_description = post_data.get('products_description')
    products_price = post_data.get('products_price')
    products_category = post_data.get('products_category')

    new_users_products = Users_Products(users_id, products_title, products_image, products_description, products_price, products_category)

    db.session.add(new_users_products)
    db.session.commit()

    return jsonify("Users product has been successfully added")

@app.route('/users_products/get', methods=['GET'])
def get_users_products():
    users_products = db.session.query(Users_Products).all()
    return jsonify(multiple_users_products_schema.dump(users_products))


if __name__ == "__main__":
    app.run(debug=True)
