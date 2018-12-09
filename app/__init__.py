import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, current_app
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.converters import DateConverter
from config import Config
import os

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.url_map.converters['date'] = DateConverter
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Set up the settings for when server is in production
    if not app.debug and not app.testing:

        # Set up logs when in production
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/natureengine.log', maxBytes=10240,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Nature Engine startup')

    return app
