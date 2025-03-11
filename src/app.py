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
from models import db, User, Planets, Characters, Vehicles, Spaceships, FavoritePlanets, FavoriteCharacters, FavoriteVehicles, FavoriteSpaceships
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

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# GET ALL

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    data = db.session.scalars(select(User)).all()
    results = list(map(lambda item: item.serialize(), data))
    return jsonify({"msg": "Aquí tienes la lista de todos los usuarios", "results": results}), 200


@app.route('/planetas', methods=['GET'])
def obtener_planetas():
    data = db.session.scalars(select(Planets)).all()
    results = list(map(lambda item: item.serialize(), data))
    return jsonify({"msg": "Aquí tienes la lista de todos los planetas", "results": results}), 200


@app.route('/personajes', methods=['GET'])
def obtener_personajes():
    data = db.session.scalars(select(Characters)).all()
    results = list(map(lambda item: item.serialize(), data))
    return jsonify({"msg": "Aquí tienes la lista de todos los planetas", "results": results}), 200


@app.route('/vehiculos', methods=['GET'])
def obtener_vehiculos():
    data = db.session.scalars(select(Vehicles)).all()
    results = list(map(lambda item: item.serialize(), data))
    return jsonify({"msg": "Aquí tienes la lista de todos los vehículos", "results": results}), 200


@app.route('/naves', methods=['GET'])
def obtener_naves():
    data = db.session.scalars(select(Spaceships)).all()
    results = list(map(lambda item: item.serialize(), data))
    return jsonify({"msg": "Aquí tienes la lista de todas las naves espaciales", "results": results}), 200

# GET x ID

@app.route('/usuario/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = db.session.get(User, id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 400
    return jsonify({"msg": "Aquí tienes los datos del usuario", "result": usuario.serialize()}), 200


@app.route('/planeta/<int:id>', methods=['GET'])
def obtener_planeta(id):
    planeta = db.session.get(Planets, id)
    if not planeta:
        return jsonify({"msg": "Planeta no encontrado"}), 400
    return jsonify({"msg": "Aquí tienes los datos del planeta", "result": planeta.serialize()}), 200


@app.route('/personaje/<int:id>', methods=['GET'])
def obtener_personaje(id):
    personaje = db.session.get(Characters, id)
    if not personaje:
        return jsonify({"msg": "Personaje no encontrado"}), 400
    return jsonify({"msg": "Aquí tienes los datos del personaje", "result": personaje.serialize()}), 200


@app.route('/vehiculo/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = db.session.get(Vehicles, id)
    if not vehiculo:
        return jsonify({"msg": "Vehículo no encontrado"}), 400
    return jsonify({"msg": "Aquí tienes los datos del vehículo", "result": vehiculo.serialize()}), 200


@app.route('/nave/<int:id>', methods=['GET'])
def obtener_nave(id):
    nave = db.session.get(Spaceships, id)
    if not nave:
        return jsonify({"msg": "Nave no encontrada"}), 400
    return jsonify({"msg": "Aquí tienes los datos de la nave", "result": nave.serialize()}), 200

# POST

@app.route('/favoritos-planeta', methods=['POST'])
def agregar_favorito_planeta():
    request_data = request.json
    favorito = FavoritePlanets(user_id=CURRENT_USER_ID, planet_id=request_data["planet_id"])
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"msg": "El planeta fue añadido a favoritos", "result": request_data}), 200


@app.route('/favoritos-personaje', methods=['POST'])
def agregar_favorito_personaje():
    request_data = request.json
    favorito = FavoriteCharacters(user_id=CURRENT_USER_ID, character_id=request_data["character_id"])
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"msg": "El personaje fue añadido a favoritos", "result": request_data}), 200


@app.route('/favoritos-vehiculo', methods=['POST'])
def agregar_favorito_vehiculo():
    request_data = request.json
    favorito = FavoriteVehicles(user_id=CURRENT_USER_ID, vehicle_id=request_data["vehicle_id"])
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"msg": "El vehículo fue añadido a favoritos", "result": request_data}), 200


@app.route('/favoritos-nave', methods=['POST'])
def agregar_favorito_nave():
    request_data = request.json
    favorito = FavoriteSpaceships(user_id=CURRENT_USER_ID, spaceship_id=request_data["spaceship_id"])
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"msg": "La nave fe añadida a favoritos", "result": request_data}), 200

# DELETE

@app.route('/favoritos-planeta/<int:id>', methods=['DELETE'])
def eliminar_favorito_planeta(id):
    return delete_favorite(FavoritePlanets, "planet_id", id, "El planeta ha sido eliminado de favoritos")


@app.route('/favoritos-personaje/<int:id>', methods=['DELETE'])
def eliminar_favorito_personaje(id):
    return delete_favorite(FavoriteCharacters, "character_id", id, "El personaje ha sido eliminado de favoritos")


@app.route('/favoritos-vehiculo/<int:id>', methods=['DELETE'])
def eliminar_favorito_vehiculo(id):
    return delete_favorite(FavoriteVehicles, "vehicle_id", id, "El vehículo ha sido eliminado de favoritos")


@app.route('/favoritos-nave/<int:id>', methods=['DELETE'])
def eliminar_favorito_nave(id):
    return delete_favorite(FavoriteSpaceships, "spaceship_id", id, "La nave ha sido eliminada de favoritos")

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

