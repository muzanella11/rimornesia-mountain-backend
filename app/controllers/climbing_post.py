from app.core.controllers import BaseControllers
from app.models.model_climbing_post import ModelClimbingPost
import re
import json

class ClimbingPost(BaseControllers):
    request = None

    TABLES = {}

    def __init__(self, request = None):
        super(ClimbingPost, self).__init__()

        self.request = request

    def run(self):
        data = {
            'code': 200,
            'message': 'Success',
            'data': []
        }

        return self.create_response(data)

    def get_list(self):
        data = {
            'code': 200,
            'message': 'Success',
            'data': [],
            'total_data': 0
        }

        data_model = {
            'type': 'list',
            'pagination': True,
            'filter': self.request.args
        }

        data_sql = getattr(ModelClimbingPost(data_model), 'get_list')()

        data['data'] = data_sql.get('data')
        data['total_data'] = data_sql.get('total_rows')

        return self.create_response(data)

    def get_detail(self, columns = None, value = None):
        if columns == "error":
            return self.create_response({
                'code': 400,
                'messages': 'Bad Request'
            })

        data = {
            'code': 200,
            'message': 'Success',
            'data': {},
            'total_data': 0
        }

        data_sql = getattr(ModelClimbingPost(), 'get_detail_by')(columns, value)

        data['data'] = data_sql.get('data')
        data['total_data'] = data_sql.get('total_rows')

        return self.create_response(data)

    def create_data(self):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        request_data = self.request.json

        mountain_id = request_data.get('mountain_id')
        name = request_data.get('name')
        description = request_data.get('description')
        location = request_data.get('location')
        cover = request_data.get('cover')
        avatar = request_data.get('avatar')
        status = request_data.get('status')
        is_open = request_data.get('is_open')
        rules = request_data.get('rules')
        price = request_data.get('price')
        discount = request_data.get('discount')
        quota = request_data.get('quota')
        is_refundable = request_data.get('is_refundable')

        if location:
            location = json.dumps(location)

        if discount == None:
            discount = 0
        
        data_model = {
            'mountain_id': mountain_id,
            'name': name,
            'description': description,
            'location': location,
            'cover': cover,
            'avatar': avatar,
            'status': status,
            'is_open': is_open,
            'rules': rules,
            'price': price,
            'discount': discount,
            'quota': quota,
            'is_refundable': is_refundable
        }

        getattr(ModelClimbingPost(), 'create_data')(data_model)

        return self.create_response(data)

    def update_data(self, climbing_post_id = None):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        request_data = self.request.json

        mountain_id = request_data.get('mountain_id')
        name = request_data.get('name')
        description = request_data.get('description')
        location = request_data.get('location')
        cover = request_data.get('cover')
        avatar = request_data.get('avatar')
        status = request_data.get('status')
        is_open = request_data.get('is_open')
        rules = request_data.get('rules')
        price = request_data.get('price')
        discount = request_data.get('discount')
        quota = request_data.get('quota')
        is_refundable = request_data.get('is_refundable')

        if location:
            location = json.dumps(location)

        if discount == None:
            discount = 0

        queries = "mountain_id='{}',\
            name='{}',\
            description='{}',\
            location='{}',\
            cover='{}',\
            avatar='{}',\
            status='{}',\
            is_open='{}',\
            rules='{}',\
            price='{}',\
            discount='{}',\
            quota='{}',\
            is_refundable='{}'".format(mountain_id, name, description, location, cover, avatar, status, is_open, rules, price, discount, quota, is_refundable)
        
        data_model = {
            'id': climbing_post_id,
            'data': queries
        }

        getattr(ModelClimbingPost(), 'update_data')(data_model)

        return self.create_response(data)

    def delete_data(self, climbing_post_id = None):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        data_sql = getattr(ModelClimbingPost(), 'delete_data')(climbing_post_id)

        return self.create_response(data)
        