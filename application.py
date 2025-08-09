import os

import click
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from models import db
from datetime import datetime
from sqlalchemy import func
from controllers import livro

@click.command("init-db")
def init_db_command():
    with current_app.app_context():
        db.create_all()
    click.echo("Inicializando a base de dados...")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///blog.sqlite'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(init_db_command)

    db.init_app(app)

    
    app.register_blueprint(livro.app)

    return app