from app import app
# ///
#     Import local package
# from project.config.Database import connection as con, cursor as cur
# from project.config.DatetimeEncoder import DatetimeEncoder
# from project.config.Hash import Hash
# ///

class Hello:

    def __init__(self):
        pass

    def insert_data():
        mysql = app.mysql

        try:
            with mysql.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            mysql.commit()

            with mysql.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            mysql.close()

        # # create table
        # mysql.execute('CREATE TABLE "EX1" ('
        #             'id INTEGER NOT NULL,'
        #             'name VARCHAR, '
        #             'PRIMARY KEY (id));')

        # # insert a raw
        # mysql.execute('INSERT INTO "EX1" '
        #             '(id, name) '
        #             'VALUES (1,"raw1")')