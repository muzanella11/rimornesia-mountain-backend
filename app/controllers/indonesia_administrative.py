from app.core.controllers import BaseControllers
from app.models.model_indonesia_administrative import ModelIndonesiaAdministrative
import re

class IndonesiaAdministrative(BaseControllers):
    request = None

    def __init__(self, request = None):
        super(IndonesiaAdministrative, self).__init__()

        self.request = request

    def run(self):
        data = {
            'code': 200,
            'message': 'Success',
            'data': []
        }

        return self.create_response(data)

    def province(self):
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

        data_provinces = ModelIndonesiaAdministrative(data_model).get_province()

        data['data'] = data_provinces.get('data')
        data['total_data'] = data_provinces.get('total_rows')

        return self.create_response(data)

    def province_by_name(self, name):
        if re.search('[_!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/\s]', name):
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

        data_provinces = ModelIndonesiaAdministrative().get_province_by_name(name)

        data['data'] = data_provinces.get('data')
        data['total_data'] = data_provinces.get('total_rows')

        return self.create_response(data)

    def province_by_id(self, id):
        data = {
            'code': 200,
            'message': 'Success',
            'data': [],
            'total_data': 0
        }

        data_provinces = ModelIndonesiaAdministrative().get_province_by_id(id)

        data['data'] = data_provinces.get('data')
        data['total_data'] = data_provinces.get('total_rows')

        return self.create_response(data)