from app import app
from app.core.models import Models
import json

class ModelBooking(Models):
    def __init__(self, params = None):
        super(ModelBooking, self).__init__(params)

        self.table_name = 'booking'

    def get_list(self):
        sql_rows = self.execute("SELECT \
        id, \
        type, \
        code, \
        user_id, \
        item, \
        {}, \
        {}, \
        price, \
        quantity, \
        price_total, \
        payment_code, \
        payment_status, \
        passenger_manifest, \
        {}, {} from `{}`".format(self.convert_time_zone('checkin_date'), self.convert_time_zone('checkout_date'), self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name))

        if sql_rows['data']:
            result = []

            for item in sql_rows['data']:
                item['passenger_manifest'] = json.loads(item.get('passenger_manifest'))

                result.append(item)

            sql_rows['data'] = result

        convert_attribute_list = [
            'created_at',
            'updated_at'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list)

        # Convert date with format
        convert_attribute_list = [
            'checkin_date',
            'checkout_date'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list, '%Y-%m-%d')

        return sql_rows

    def get_detail_by(self, columns = None, value = None):
        if columns == "name":
            value = value.replace('-', ' ')

        sql_rows = self.execute("SELECT \
        id, \
        type, \
        code, \
        user_id, \
        item, \
        checkin_date, \
        checkout_date, \
        price, \
        quantity, \
        price_total, \
        payment_code, \
        payment_status, \
        passenger_manifest, \
        {}, {} from `{}` WHERE `{}` = '{}'".format(self.convert_time_zone('created_at'), self.convert_time_zone('updated_at'), self.table_name, columns, value))

        if sql_rows['data']:
            sql_rows['data']['passenger_manifest'] = json.loads(sql_rows['data'].get('passenger_manifest'))

        convert_attribute_list = [
            'created_at',
            'updated_at'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list)

        # Convert date with format
        convert_attribute_list = [
            'checkin_date',
            'checkout_date'
        ]

        sql_rows = self.convert_to_normal_date(sql_rows, convert_attribute_list, '%Y-%m-%d')

        return sql_rows

    def create_data(self, value = None):
        action = {}

        action['{}'.format(self.table_name)] = {
            'action': self.action_type.get('insert'),
            'command': (
                "INSERT INTO `{}` (\
                `type`, \
                `code`, \
                `user_id`, \
                `item`, \
                `checkin_date`, \
                `checkout_date`, \
                `price`, \
                `quantity`, \
                `price_total`, \
                `payment_code`, \
                `payment_status`, \
                `passenger_manifest`, \
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
                NOW())".format(
                    value.get('type'), 
                    value.get('code'),
                    value.get('user_id'),
                    value.get('item'),
                    value.get('checkin_date'), 
                    value.get('checkout_date'), 
                    value.get('price'),
                    value.get('quantity'),
                    value.get('price_total'),
                    value.get('payment_code'), 
                    value.get('payment_status'),
                    value.get('passenger_manifest')
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
                "UPDATE `{}` SET {}, updated_at=NOW() WHERE code={}".format(self.table_name, value.get('data'), value.get('code'))
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