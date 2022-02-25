from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
#import psycopg2
import os

users_login = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
users_login.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'users_login.sqlite')
db = SQLAlchemy(users_login)
ma = Marshmallow(users_login)
CORS(users_login)
bcrypt = Bcrypt(users_login)

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

@users_login.route('/user/add', methods=['POST'])
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

@users_login.route('/user/verify', methods=['POST'])
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

@users_login.route('/user/get', methods=['GET'])
def get_users():
    users = db.session.query(Users).all()
    return jsonify(multiple_users_schema.dump(users))

@users_login.route('/user/get/<id>', methods=['GET'])
def get_user(id):
    user = db.session.query(Users).filter(Users.users_id == id).first()
    return jsonify(users_schema.dump(user))

@users_login.route('/user/get/username/<users_name>', methods=['GET'])
def get_user_by_username(users_name):
    username = db.session.query(Users).filter(Users.users_name == users_name).first()
    return jsonify(users_schema.dump(username))

if __name__ == "__main__":
    users_login.run(host="localhost", port=8001, debug=True)
