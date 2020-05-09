from flask import jsonify
import json

class BaseControllers(object):
    def __init__(self):
        super(BaseControllers, self).__init__()

    def create_response(self, data = {}):
        base_response = {
            'code': 500,
            'messages': 'Internal Server Error'
        }

        if not data.get('code'):
            data = base_response

        return (
            jsonify(**data),
            data['code']
        )