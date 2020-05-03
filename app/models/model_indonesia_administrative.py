from app import app
from app.core.models import Models

class ModelIndonesiaAdministrative(Models):
    def __init__(self, params = None):
        super(ModelIndonesiaAdministrative, self).__init__(params)

    def get_list(self, table_name = None):
        self.table_name = table_name

        sql_rows = self.execute("SELECT * from `{}`".format(self.table_name))

        return sql_rows

    def get_detail_by(self, table_name = None, columns = None, value = None):
        self.table_name = table_name

        if columns == "name":
            value = value.replace('-', ' ')

        sql_rows = self.execute("SELECT * from `{}` WHERE `{}` = '{}'".format(self.table_name, columns, value))

        return sql_rows