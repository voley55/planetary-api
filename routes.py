from app import db, mail
from models import Planet, User, user_schema, \
    users_schema, planet_schema, planets_schema
from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from flask_mail import Message


planet_api = Blueprint('planet_api', __name__)


@planet_api.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201


@planet_api.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@planet_api.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email:str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("your planetary API password is " + user.password,
                      sender="admin@planetary-api.com", recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist"), 401


@planet_api.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


@planet_api.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message="That planet doesn't exist"), 404


@planet_api.route('/add_planet', methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.json['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify("There is already planet by that name."), 409
    else:
        planet_type = request.json['planet_type']
        home_star = request.json['home_star']
        mass = float(request.json['mass'])
        radius = float(request.json['radius'])
        distance = float(request.json['distance'])

        new_planet = Planet(planet_name=planet_name,
                            planet_type=planet_type,
                            home_star=home_star,
                            mass=mass,
                            radius=radius,
                            distance=distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="You added a planet"), 201


@planet_api.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    planet_id = int(request.json['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.json['planet_name']
        planet.planet_type = request.json['planet_type']
        planet.home_star = request.json['home_star']
        planet.mass = float(request.json['mass'])
        planet.radius = float(request.json['radius'])
        planet.distance = float(request.json['distance'])
        db.session.commit()
        return jsonify(message="You updated a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404


@planet_api.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required
def remove_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted a planet"), 202
    else:
        return jsonify(message="That planet doesn't exist"), 404
