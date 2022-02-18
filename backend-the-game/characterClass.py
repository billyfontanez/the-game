from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from flask_mysqldb import MySQL
import os

characterClass = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
characterClass.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'characterClass.sqlite')
db = SQLAlchemy(characterClass)
ma = Marshmallow(characterClass)

class CharacterClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    klass = db.Column(db.String(144), unique=False)
    clain = db.Column(db.String(144), unique=False)
    hp = db.Column(db.Integer, unique=False)
    mp = db.Column(db.Integer, unique=False)
    defence = db.Column(db.Integer, unique=False)
    abilities = db.Column(db.String(144), unique=False)
    attacks = db.Column(db.String(144), unique=False)


    def __init__(self, name, klass, clain, hp, mp, defense, abilities, attacks):
        self.name = name
        self.klass = klass
        self.clain = clain
        self.hp = hp
        self.mp = mp
        self.defense = defense
        self.abilities = abilities
        self.attacks = attacks


class CharacterClassSchema(ma.Schema):
    class Meta:
        fields = ('name', 'klass', 'clain', 'hp', 'mp', 'defense', 'abilities', 'attacks')


character_class_schema = CharacterClassSchema()
character_classes_schema = CharacterClassSchema(many=True)

# Endpoint to create a new character
@characterClass.route('/new-character', methods=["POST"])
def add_new_character():
    name = request.json['name']
    klass = request.json['klass']
    clain = request.json['clain']
    hp = request.json['hp']
    mp = request.json['mp']
    defense = request.json['defense']
    abilities = request.json['abilities']
    attacks = request.json['attacks']

    new_character = CharacterClass(name, klass, clain, hp, mp, defense, abilities, attacks)

    db.session.add(new_character)
    db.session.commit()

    character = CharacterClass.query.get(new_character.id)

    return character_class_schema.jsonify(character)


if __name__ == '__main__':
    characterClass.run(host="localhost", port=8000, debug=True)
