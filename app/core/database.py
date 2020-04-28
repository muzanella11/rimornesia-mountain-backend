from __future__ import print_function

from app.config.database import db_config
from mysql.connector import errorcode
import mysql.connector
# from mysql.connector import errorcode

class Database(object):
    db_connection = None
    mysql_instance = None
    mysql_connection = None
    mysql_ctx = None
    config = dict({
        'host': '',
        'port': '',
        'user': '',
        'password': '',
        'database': ''
    })

    def __init__(self):
        super(Database, self).__init__()
        self.config = db_config()

    def create_connection(self):
        instance = mysql.connector
        connection = instance.connect(**self.config)

        result = dict()

        result['instance'] = instance
        result['connection'] = connection

        return result

    def connect(self, db_name):
        if db_name:
            self.config['database'] = db_name  

        # connecting to database
        self.db_connection = self.create_connection()

        # setup instance and mysql context
        self.mysql_instance = self.db_connection.get('instance')
        self.mysql_connection = self.db_connection.get('connection')
        self.mysql_ctx = self.mysql_connection.cursor()

        # self.mysql_ctx.execute("show databases")

        result = dict()

        result['mysql_instance'] = self.mysql_instance
        result['mysql_connection'] = self.mysql_connection
        result['mysql_ctx'] = self.mysql_ctx

        return result

    def create_database(self, context):
        # Create Database
        try:
            context.mysql_ctx.execute("USE {}".format(context.DB_NAME))
        except context.mysql_instance.Error as err:
            print("Database {} does not exists.".format(context.DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                
                try:
                    context.mysql_ctx.execute(
                        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(context.DB_NAME))
                except context.mysql_instance.Error as err:
                    print("Failed creating database: {}".format(err))
                    exit(1)

                print("Database {} created successfully.".format(context.DB_NAME))
                context.mysql_connection.database = context.DB_NAME
            else:
                print(err)
                exit(1)

    def drop_database(self, context):
        # Drop Database
        try:
            context.mysql_ctx.execute(
                "DROP DATABASE [IF EXISTS] {}".format(context.DB_NAME)
            )
        except context.mysql_instance.Error as err:
            print("Database {} does not exists.".format(context.DB_NAME))
            print(err.msg)
        else:
            print("Database {} has been droped.".format(context.DB_NAME))

    def execute_command(self, context, table_name, action_name, action_command):
        # Execute Command
        try:
            print("[{}] table {}: ".format(action_name, table_name), end='')
            context.mysql_ctx.execute(action_command)
        except context.mysql_instance.Error as err:
            print("[FAILED]")
            print("Something wrong when {} table {} :(".format(action_name, table_name))
            print(err.msg)
            print("\n")
        else:
            print("[OK]")

    def rename_table(self, context, before_name, after_name):
        # Rename Table
        try:
            context.mysql_ctx.execute(
                "ALTER TABLE {} RENAME TO {}".format(before_name, after_name)
            )
        except context.mysql_instance.Error as err:
            print("Table {} does not exist.".format(before_name))
            print(err.msg)
        else:
            print("Rename table {} to {}".format(before_name, after_name))

    def close_connection(self, mysql_connection, mysql_context):
        if not mysql_connection and mysql_context:
            return

        mysql_context.close()
        mysql_connection.close()