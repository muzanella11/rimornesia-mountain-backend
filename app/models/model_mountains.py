from app import app
from app.core.models import Models

class ModelMountains(Models):
    def __init__(self, params = None):
        super(ModelMountains, self).__init__(params)

    def get_list(self, table_name = None):
        self.table_name = table_name

        print('date now : ', self.get_date_time_now())

        # time_elapsed = self.time_elapsed_string('2019-05-09 18:32:00')

        # print('time elapsed : ', time_elapsed)

        sql_rows = self.execute("SELECT id, name, formatted_address, location, {}, {} from `{}`".format(self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name))

        return sql_rows

    def get_detail_by(self, table_name = None, columns = None, value = None):
        self.table_name = table_name

        if columns == "name":
            value = value.replace('-', ' ')

        sql_rows = self.execute("SELECT * from `{}` WHERE `{}` = '{}'".format(self.table_name, columns, value))

        return sql_rows