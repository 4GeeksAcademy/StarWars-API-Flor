"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorite
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = User.query.all()
    if response_body == []: 
        return jsonify({"msg": "No existen usuarios"}), 404
    serialized_user=[item.serialize() for item in response_body]

    return jsonify(serialized_user), 200


@app.route('/planet', methods=['GET'])
def get_planet():

    response_body = Planet.query.all()
    if response_body == []: 
        return jsonify({"msg": "No existen planetas"}), 404
    serialized_planet=[item.serialize() for item in response_body]

    return jsonify(serialized_planet), 200


@app.route('/people', methods=['GET'])
def get_people():

    response_body = People.query.all()
    if response_body == []: 
        return jsonify({"msg": "No existen personajes"}), 404
    serialized_people=[item.serialize() for item in response_body]

    return jsonify(serialized_people), 200


@app.route('/favorite', methods=['GET'])
def get_favorite():

    response_body = Favorite.query.all()
    if response_body == []: 
        return jsonify({"msg": "No existen favoritos"}), 404
    serialized_favorite=[item.serialize() for item in response_body]

    return jsonify(serialized_favorite), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    personaje=People.query.filter_by(id=people_id).first()
    if personaje is None: 
        return jsonify({"msg": "No existe el personaje"}), 404
    return jsonify(personaje.serialize()), 200


@app.route('/user/favorite/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    favorito=Favorite.query.filter_by(user_id=user_id).all()
    if favorito == []:
        return jsonify({"msg": "No existe el favorito"}), 404
    
    serialized_favorite=[item.serialize() for item in favorito]
    return jsonify(serialized_favorite), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planeta=Planet.query.filter_by(id=planet_id).first()
    if planeta is None: 
        return jsonify({"msg": "No existe el planeta"}), 404
    return jsonify(planeta.serialize()), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    planeta=Planet.query.filter_by(id=planet_id).first()
    if planeta is None: 
        return jsonify({"msg": "No existe el planeta"}), 404
    
    body=json.loads(request.data)
    user_id=body["user_id"]
    user=User.query.filter_by(id=user_id).first()
    if user is None: 
        return jsonify({"msg": "No existe el usuario"}), 404
    
    new_favorite=Favorite(
        planet_id=planet_id,
        user_id=user_id #body["user_id"]
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msj": "Planeta favorito agrgado"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    personaje=People.query.filter_by(id=people_id).first()
    if personaje is None: 
        return jsonify({"msg": "No existe el personaje"}), 404
    
    body=json.loads(request.data)
    user_id=body["user_id"]
    user=User.query.filter_by(id=user_id).first()
    if user is None: 
        return jsonify({"msg": "No existe el usuario"}), 404
    
    new_favorite=Favorite(
        people_id=people_id,
        user_id=user_id #body["user_id"]
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msj": "Personaje favorito agrgado"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    planeta=Favorite.query.filter_by(planet_id=planet_id).all()
    if planeta == []: 
        return jsonify({"msg": "No existe el planeta favorito"}), 404
    
    print(planeta)
    return jsonify({"msj": "Personaje favorito agrgado"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
