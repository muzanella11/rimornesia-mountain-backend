from app.core.controllers import BaseControllers
from app.models.model_stories_content import ModelStoriesContent
import re
import json

class StoriesContent(BaseControllers):
    request = None

    TABLES = {}

    def __init__(self, request = None):
        super(StoriesContent, self).__init__()

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

        data_sql = getattr(ModelStoriesContent(data_model), 'get_list')()

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

        data_sql = getattr(ModelStoriesContent(), 'get_detail_by')(columns, value)

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

        types = request_data.get('types')
        text = request_data.get('text')
        attachment_id = request_data.get('attachment_id')
        attachment_layout = request_data.get('attachment_layout')
        markup = request_data.get('markup')

        if markup:
            markup = json.dumps(markup)

        data_model = {
            'types': types,
            'text': text,
            'attachment_id': attachment_id,
            'attachment_layout': attachment_layout,
            'markup': markup
        }

        getattr(ModelStoriesContent(), 'create_data')(data_model)

        return self.create_response(data)

    def update_data(self, stories_content_id = None):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        request_data = self.request.json

        types = request_data.get('types')
        text = request_data.get('text')
        attachment_id = request_data.get('attachment_id')
        attachment_layout = request_data.get('attachment_layout')
        markup = request_data.get('markup')

        if markup:
            markup = json.dumps(markup)

        queries = "types='{}',\
            text='{}',\
            attachment_id='{}',\
            attachment_layout='{}',\
            markup='{}'".format(types, text, attachment_id, attachment_layout, markup)
        
        data_model = {
            'id': stories_content_id,
            'data': queries
        }

        getattr(ModelStoriesContent(), 'update_data')(data_model)

        return self.create_response(data)

    def delete_data(self, stories_content_id = None):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        data_sql = getattr(ModelStoriesContent(), 'delete_data')(stories_content_id)

        return self.create_response(data)
        