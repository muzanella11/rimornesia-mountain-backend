from app.core.database import Database
import os

DB_NAME = os.environ.get('DB_NAME')

app = dict()

db_connection = Database().connect(DB_NAME)

app['mysql_instance'] = db_connection['mysql_instance']
app['mysql_connection'] = db_connection['mysql_connection']
app['mysql_ctx'] = db_connection['mysql_ctx']

try:
    app['mysql_ctx'].execute("DROP DATABASE {}".format(DB_NAME))
except app['mysql_instance'].Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    print(err.msg)
else:
    print("Database {} has been droped.".format(DB_NAME))

app['mysql_ctx'].close()
app['mysql_connection'].close()
