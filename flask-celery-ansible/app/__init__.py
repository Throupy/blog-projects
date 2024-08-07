from flask import Flask
from app.extensions import celery
from app.routes import main

def create_app():
    # create_app (factory) approach
    app = Flask(__name__)
    app.config.from_object("config.Config")

    celery.conf.update(app.config)

    app.register_blueprint(main)

    return app
