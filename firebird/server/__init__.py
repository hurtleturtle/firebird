from flask import Flask
import os


INSTANCE_PATH = os.getenv('INSTANCE_PATH')


def create_app():
    app = Flask(__name__, template_folder='routes/templates', instance_path=INSTANCE_PATH, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    from .routes import graph
    app.register_blueprint(graph.bp)

    return app