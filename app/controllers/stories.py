from app.core.controllers import BaseControllers
from app.models.model_stories import ModelStories
import re
import json

class Stories(BaseControllers):
    request = None

    TABLES = {}

    def __init__(self, request = None):
        super(Stories, self).__init__()

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

        data_sql = getattr(ModelStories(data_model), 'get_list')()

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

        data_sql = getattr(ModelStories(), 'get_detail_by')(columns, value)

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

        user_id = request_data.get('user_id')
        climbing_post_id = request_data.get('climbing_post_id')
        content = request_data.get('content')
        is_published = request_data.get('is_published')

        if len(content) > 0:
            content = [str(x) for x in content]
            content = ','.join(content)
        
        data_model = {
            'user_id': user_id,
            'climbing_post_id': climbing_post_id,
            'content': content,
            'is_published': is_published
        }

        getattr(ModelStories(), 'create_data')(data_model)

        return self.create_response(data)

    def update_data(self, stories_id = None):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        request_data = self.request.json

        user_id = request_data.get('user_id')
        climbing_post_id = request_data.get('climbing_post_id')
        content = request_data.get('content')
        is_published = request_data.get('is_published')

        if len(content) > 0:
            content = [str(x) for x in content]
            content = ','.join(content)
        
        queries = "user_id='{}',\
            climbing_post_id='{}',\
            content='{}',\
            is_published='{}'".format(user_id, climbing_post_id, content, is_published)
        
        data_model = {
            'id': stories_id,
            'data': queries
        }

        getattr(ModelStories(), 'update_data')(data_model)

        return self.create_response(data)

    def delete_data(self, stories_id = None):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        data_sql = getattr(ModelStories(), 'delete_data')(stories_id)

        return self.create_response(data)
        