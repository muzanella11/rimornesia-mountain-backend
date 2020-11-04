from app import app
from app.core.database import Database
from app.core.crud_management import CrudManagement
from app.core.datetime_handler import DateTime
from app.config.database import action_type
from decimal import Decimal
import json

class Models(CrudManagement, DateTime):
    table_name = None
    action_type = action_type()
    
    def __init__(self, params = None):
        super(Models, self).__init__(params)
        
    def set_table_name(self, table_name):
        self.table_name = table_name

    def get_table_name(self):
        return self.table_name

    def get_limit_offset(self):
        return "LIMIT {} OFFSET {}".format(self.limit, self.offset)

    def convert_time_zone(self, column):
        return "CONVERT_TZ(`{}`, '{}', '{}') as {}".format(column, self.get_server_time_zone(), self.timezone(), column)

    def convert_to_normal_date(self, context, attribute_list = [], format = None):
        # context is `sql_rows`
        if len(attribute_list) == 0:
            return context

        if type(context['data']) == list and len(context['data']) > 0:
            for item in context['data']:
                for item_attribute in attribute_list:
                    if item.get(item_attribute) != None:
                        item[item_attribute] = self.context_to_string(item.get(item_attribute), format)
        
        if type(context['data']) == dict and len(context['data']) > 0:
            for item in context['data']:
                for item_attribute in attribute_list:
                    if item == item_attribute and context['data'][item] != None:
                        context['data'][item_attribute] = self.context_to_string(context['data'][item_attribute], format)

        return context

    def execute(self, command):
        if self.limit > 0:
            command = "{} {}".format(command, self.get_limit_offset())

        app.mysql.execute(command)

        # This will extract row headers
        row_headers = [x[0] for x in app.mysql.description]

        raw_result = app.mysql.fetchall()

        result = {}

        if self.action_type == "list":
            result = []

            # Result as array []
            for raw_result_item in raw_result:
                result.append(dict(zip(row_headers,raw_result_item)))
        
        else:
            # Result as object {}
            for raw_result_item in raw_result:
                result = dict(zip(row_headers,raw_result_item))

        # Get total mysql rows count
        total_rows = app.mysql.rowcount

        if len(result) == 0:
            result = None

        return {
            'data': result,
            'total_rows': total_rows
        }

    def execute_command(self, commands):
        # Execute Command
        for table_name in commands:
            action_raw = commands.get(table_name)
            action_name = action_raw.get('action')
            action_command = action_raw.get('command')

            app.db_instance.execute_command(app, table_name, action_name, action_command)

    def connect(self):
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
        app.db_instance = db_instance

    def close_connection(self):
        app.db_instance.close_connection(app.mysql_connection, app.mysql)
        print(app.db_instance)