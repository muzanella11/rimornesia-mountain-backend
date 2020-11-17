from dotenv import load_dotenv
import os
from flask import Flask
from app.core.database import Database
from app.config.database import db_config

load_dotenv()

DB_NAME = os.environ.get('DB_NAME')
IS_MIGRATE = os.environ.get('PYTHON_MIGRATE')

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    if IS_MIGRATE == "FALSE":
        # db instance
        db_instance = Database()

        # create connection
        db = db_instance.connect()

        # get mysql instance and connection and context
        mysql_instance = db.get('mysql_instance')
        mysql_connection = db.get('mysql_connection')
        mysql_ctx = db.get('mysql_ctx')

        app.mysql_instance = mysql_instance
        app.mysql_connection = mysql_connection
        app.mysql = mysql_ctx
        app.mysql_ctx = mysql_ctx
        app.mysql_lastrowid = None
        app.db_instance = db_instance
        app.environment = os.environ
        # app.mysql_close_connection = db_instance.close_connection(app.mysql_connection, app.mysql)

        # app.mysql.execute("show databases")

        # for i in app.mysql:
        #     print(i)

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

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    return app

app = create_app()

from app.config import routes
