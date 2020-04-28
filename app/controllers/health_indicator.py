from flask import jsonify

class HealthIndicator(object):
    def run(self):
        data = {
            'code': 200,
            'message': 'Success',
            'data': []
        }

        return (
            jsonify(**data),
            data['code']
        )