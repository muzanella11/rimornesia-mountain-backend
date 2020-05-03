from app import app
from app.core.models import Models

class ModelIndonesiaAdministrative(Models):
    def __init__(self, params = None):
        super(ModelIndonesiaAdministrative, self).__init__(params)

    def get_province(self):
        self.table_name = 'provinces'

        sql_rows = self.execute("SELECT * from `{}`".format(self.table_name))

        return sql_rows

    def get_province_by_name(self, name):
        self.table_name = 'provinces'

        name = name.replace('-', ' ')

        sql_rows = self.execute("SELECT * from `{}` WHERE `name` = '{}'".format(self.table_name, name))

        return sql_rows

    def get_province_by_id(self, id):
        self.table_name = 'provinces'

        sql_rows = self.execute("SELECT * from `{}` WHERE `id` = '{}'".format(self.table_name, id))

        return sql_rows