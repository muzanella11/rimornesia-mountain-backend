from app.core.controllers import BaseControllers
from app.services.mountains_service import MountainsService

class Mountains(BaseControllers):
    request = None

    def __init__(self, request = None):
        super(Mountains, self).__init__()

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

        data_sql = MountainsService().generate_mountain_list(data_model)

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
            'data': [],
            'total_data': 0
        }

        data_sql = MountainsService().generate_mountain_detail(columns, value)

        data['data'] = data_sql.get('data')
        data['total_data'] = data_sql.get('total_rows')

        return self.create_response(data)
        