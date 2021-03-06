from flask import Flask
from flask_caching import Cache
from .models import db, Reviews
from . import config
from app.import_csv import import_test_data
from flasgger import Swagger


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['CACHE_TYPE'] = 'SimpleCache'
    Swagger(flask_app)
    cache = Cache(flask_app)
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    if not db.session.query(Reviews).first():
        import_test_data(db)
    return flask_app, cache
