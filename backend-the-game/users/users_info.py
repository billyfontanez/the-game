from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
#from datetime import datetime
#import psycopg2
import os

users_info = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
users_info.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'users_info.sqlite')
db = SQLAlchemy(users_info)
ma = Marshmallow(users_info)
CORS(users_info)
bcrypt = Bcrypt(users_info)

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


@users_info.route('/users-info/add', methods=['POST'])
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

@users_info.route('/users-info/get', methods=['GET'])
def get_users_info():
    users_info = db.session.query(Users_Info).all()
    return jsonify(multiple_users_info_schema.dump(users_info))

if __name__ == '__main__':
    users_info.run(host="localhost", port=8002, debug=True)
