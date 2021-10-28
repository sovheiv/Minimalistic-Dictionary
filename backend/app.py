from flask import Flask


def create_app():
    app = Flask(import_name=__name__)
    from endpoints import admin

    app.register_blueprint(admin)
    return app
