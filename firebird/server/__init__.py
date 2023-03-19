from flask import Flask
import os
import logging.config


INSTANCE_PATH = os.getenv('INSTANCE_PATH')


def create_app():
    app = Flask(__name__, template_folder='routes/templates', instance_path=INSTANCE_PATH, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    logging.config.fileConfig(os.path.join(app.instance_path, 'logging.conf'))
    app.logger.info(f'Default event count: {app.config.get("DEFAULT_EVENT_COUNT", 100)}')

    from .routes import graph
    app.register_blueprint(graph.bp)

    return app