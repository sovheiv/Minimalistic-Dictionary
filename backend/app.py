from flask import Flask
from flask_cors import CORS


def create_app():

    app = Flask(import_name=__name__)
    CORS(app)
    from endpoints import admin

    app.register_blueprint(admin)
    return app
