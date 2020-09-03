from app import db
from models import User, Planet
from flask import Blueprint

planet_cli = Blueprint('planet_cli', __name__)


@planet_cli.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@planet_cli.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@planet_cli.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)
    venus = Planet(planet_name='Venus',
                     planet_type='Class K',
                     home_star='Sol',
                     mass=4.867e24,
                     radius=3760,
                     distance=67.24e6)
    earth = Planet(planet_name='Earth',
                   planet_type='Class M',
                   home_star='Sol',
                   mass=5.972e24,
                   radius=3959,
                   distance=92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William',
                     last_name='Herschel',
                     email='test@test.com',
                     password='P@ssw0rd')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')