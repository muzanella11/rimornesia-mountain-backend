from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

def db_config():
    # db configuration
    config = {
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT', 3306),
        'user': os.environ.get('DB_USERNAME'),
        'password': os.environ.get('DB_PASSWORD'),
        'database': os.environ.get('DB_NAME')
    }

    return config

def create_connection():
    # db configuration
    config = {
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT', 3306),
        'user': os.environ.get('DB_USERNAME'),
        'password': os.environ.get('DB_PASSWORD'),
        'database': os.environ.get('DB_NAME')
    }

    connection = mysql.connector.connect(**config)
    instance = mysql.connector

    result = dict()

    result['instance'] = instance
    result['connection'] = connection

    return result