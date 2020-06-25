from app import app
from app.core.models import Models
import json

class ModelClimbingPost(Models):
    def __init__(self, params = None):
        super(ModelClimbingPost, self).__init__(params)

        self.table_name = 'climbing_post'

    def get_list(self):
        sql_rows = self.execute("SELECT \
        id, \
        mountain_id, \
        name, \
        description, \
        location, \
        cover, \
        avatar, \
        status, \
        is_open, \
        rules, \
        price, \
        discount, \
        quota, \
        is_refundable, \
        {}, {} from `{}`".format(self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name))

        result = []

        for item in sql_rows['data']:
            item['location'] = json.loads(item.get('location'))

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
        mountain_id, \
        name, \
        description, \
        location, \
        cover, \
        avatar, \
        status, \
        is_open, \
        rules, \
        price, \
        discount, \
        quota, \
        is_refundable, \
        {}, {} from `{}` WHERE `{}` = '{}'".format(self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name, columns, value))

        if sql_rows['data']:
            sql_rows['data']['location'] = json.loads(sql_rows['data'].get('location'))
        
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
                `mountain_id`, \
                `name`, \
                `description`, \
                `location`, \
                `cover`, \
                `avatar`, \
                `status`, \
                `is_open`, \
                `rules`, \
                `price`, \
                `discount`, \
                `quota`, \
                `is_refundable`, \
                `created_at` \
                ) VALUES".format(self.table_name) +
                " (\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                '{}',\
                NOW())".format(
                    value.get('mountain_id'), 
                    value.get('name'), 
                    value.get('description'), 
                    value.get('location'), 
                    value.get('cover'), 
                    value.get('avatar'), 
                    value.get('status'), 
                    value.get('is_open'), 
                    value.get('rules'), 
                    value.get('price'), 
                    value.get('discount'), 
                    value.get('quota'), 
                    value.get('is_refundable')
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

        print('action : ', action)

        self.execute_command(
            action
        )