from fabric.api import run
from robota.server import app


def init_db():
    from robota.db import init_db

    init_db(app.config['DATABASE'])


def serve():
    app.run()
