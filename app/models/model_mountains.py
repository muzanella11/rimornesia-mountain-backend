from app import app
from app.core.models import Models

class ModelMountains(Models):
    def __init__(self, params = None):
        super(ModelMountains, self).__init__(params)

    def get_list(self, table_name = None):
        self.table_name = table_name

        # time_elapsed = self.time_elapsed_string('2019-05-09 18:32:00')

        # print('time elapsed : ', time_elapsed)

        sql_rows = self.execute("SELECT id, name, formatted_address, location, {}, {} from `{}`".format(self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name))

        convert_attribute_list = [
            'created_at',
            'updated_at'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list)

        return sql_rows

    def get_detail_by(self, table_name = None, columns = None, value = None):
        self.table_name = table_name

        if columns == "name":
            value = value.replace('-', ' ')

        sql_rows = self.execute("SELECT * from `{}` WHERE `{}` = '{}'".format(self.table_name, columns, value))

        convert_attribute_list = [
            'created_at',
            'updated_at'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list)

        return sql_rows