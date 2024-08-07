from flask import Flask
from webapp.extensions import db, migrate, celery, login_manager, mail
from webapp.config import Config
from webapp.main.routes import main
from webapp.users.routes import users

def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions defined in webapp/extensions.py
    db.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config)
    login_manager.init_app(app)
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
