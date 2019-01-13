import os
from logging.config import fileConfig

from flask import Flask


def create_app():
    """
    flask application initialization skeleton

    :return Flask:
    """
    app_dir_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.abspath(os.path.join(app_dir_path, os.pardir))
    app = Flask(__name__, instance_relative_config=True, root_path=root_path)

    app.config.from_object(os.getenv('APP_SETTINGS', 'app.config.LocalConfig'))

    if os.path.exists(os.path.join(app.instance_path, 'log_config.conf')):
        fileConfig(
            os.path.join(app.instance_path, 'log_config.conf'),
            defaults={
                'logfilename': os.path.join(app.root_path, app.config.get('LOGFILE_PATH'))},
            disable_existing_loggers=False
        )

    with app.app_context():
        from app.api import api
        from app.db import db
        from app.routes import configure_routes

        configure_routes(api)
        api.init_app(app)
        db.init_app(app)

    return app
