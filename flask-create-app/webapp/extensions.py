from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
celery = Celery(__name__, broker='redis://localhost:6379/0')
login_manager = LoginManager()
mail = Mail()
