from flask import jsonify

class HealthIndicator(object):
    def run(self):
        data = {
            'code': 200,
            'message': 'Success'
        }

        return (
            jsonify(**data),
            data['code']
        )