from app import app
from app.core.models import Models
import json

class ModelStories(Models):
    def __init__(self, params = None):
        super(ModelStories, self).__init__(params)

        self.table_name = 'stories'

    def get_list(self):
        sql_rows = self.execute("SELECT \
        id, \
        user_id, \
        climbing_post_id, \
        content, \
        is_published, \
        {}, {} from `{}`".format(self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name))

        if sql_rows['data']:
            result = []

            for item in sql_rows['data']:
                item['content'] = [int(x) for x in item.get('content').split(',')]

                result.append(item)

            sql_rows['data'] = result

        convert_attribute_list = [
            'created_at',
            'updated_at'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list)

        return sql_rows

    def get_detail_by(self, columns = None, value = None):
        if columns == "name":
            value = value.replace('-', ' ')

        sql_rows = self.execute("SELECT \
        id, \
        user_id, \
        climbing_post_id, \
        content, \
        is_published, \
        {}, {} from `{}` WHERE `{}` = '{}'".format(self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name, columns, value))

        if sql_rows['data']:
            sql_rows['data']['content'] = [int(x) for x in sql_rows['data'].get('content').split(',')]

        convert_attribute_list = [
            'created_at',
            'updated_at'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list)

        return sql_rows

    def create_data(self, value = None):
        action = {}

        action['{}'.format(self.table_name)] = {
            'action': self.action_type.get('insert'),
            'command': (
                "INSERT INTO `{}` (\
                `user_id`, \
                `climbing_post_id`, \
                `content`, \
                `is_published`, \
                `created_at` \
                ) VALUES".format(self.table_name) +
                " (\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                NOW())".format(
                    value.get('user_id'), 
                    value.get('climbing_post_id'), 
                    value.get('content'),
                    value.get('is_published')
                )
            )
        }

        self.execute_command(
            action
        )

    def update_data(self, value):
        action = {}

        action['{}'.format(self.table_name)] = {
            'action': self.action_type.get('update'),
            'command': (
                "UPDATE `{}` SET {}, updated_at=NOW() WHERE id={}".format(self.table_name, value.get('data'), value.get('id'))
            )
        }

        self.execute_command(
            action
        )

    def delete_data(self, value):
        action = {}

        action['{}'.format(self.table_name)] = {
            'action': self.action_type.get('delete'),
            'command': (
                "DELETE FROM `{}` WHERE id={}".format(self.table_name, value)
            )
        }

        self.execute_command(
            action
        )