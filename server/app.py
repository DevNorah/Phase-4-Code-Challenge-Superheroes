#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# Routes for Hero
@app.route('/heroes', methods=['GET', 'POST'])
def heroes():
    if request.method == 'GET':
        heroes = Hero.query.all()
        return make_response(jsonify([hero.to_dict() for hero in heroes]), 200)
    elif request.method == 'POST':
        new_hero = Hero(
            name=request.json['name'], 
            super_name=request.json['super_name']
        )
        db.session.add(new_hero)
        db.session.commit()
        return make_response(new_hero.to_dict(), 201)
    
@app.route('/heroes/<int:hero_id>', methods=['GET', 'PUT', 'DELETE'])
def hero(hero_id):
    hero = Hero.query.get_or_404(hero_id)
    if request.method == 'GET':
        return make_response(hero.to_dict(), 200)
    elif request.method == 'PUT':
        hero.name = request.json.get('name', hero.name)
        hero.super_name = request.json.get('super_name', hero.super_name)
        db.session.commit()
        return make_response(hero.to_dict(), 200)
    elif request.method == 'DELETE':
        db.session.delete(hero)
        db.session.commit()
        return make_response({'message': 'Hero deleted'}, 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
