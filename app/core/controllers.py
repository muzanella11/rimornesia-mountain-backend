from flask import jsonify, render_template, redirect, url_for
import json

class BaseControllers(object):
    def __init__(self):
        super(BaseControllers, self).__init__()

    def views(self, template = None, data = {}):
        return render_template(template, data=data)

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