from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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


if __name__ == '__main__':
    characterClass.run(debug=True)
