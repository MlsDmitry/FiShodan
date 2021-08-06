from os.path import join
from flask import Flask
from celery import Celery
import joblib


def create_application():
    global app, celery
    app = Flask(
        'FiShodan',
        template_folder='./fish_shodan/templates',
        static_url_path='/static',
        static_folder='./fish_shodan/static'
        )
    app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)
    
    app.config['WTF_CSRF_SECRET_KEY'] = 'abc'
    
    from fish_shodan import routes
    app.register_blueprint(routes.main_page_bp)   

    return app