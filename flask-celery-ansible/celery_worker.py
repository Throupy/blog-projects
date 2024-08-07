from app import create_app
from app.extensions import celery

app = create_app()

if __name__ == '__main__':
    app.app_context().push()
    celery.start()
