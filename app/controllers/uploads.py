from app.core.controllers import BaseControllers
from app.models.model_stories import ModelStories
from app.core.upload_file import UploadFile
import re
import json

class Uploads(BaseControllers):
    request = None

    TABLES = {}

    def __init__(self, request = None):
        super(Uploads, self).__init__()

        self.request = request

    def run(self):
        return False

    def get_detail(self, path = None):
        return UploadFile().get_file_local(path)

    def create_data(self):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        request_data = self.request.json

        file = request_data.get('file')
        path = request_data.get('path')
        # file = file.split(',')[1]

        # print('file : ', file)

        upload = UploadFile().run(file, path)

        data['data'] = {
            'path': upload.get('path')
        }

        return self.create_response(data)

    def delete_data(self, path = None):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        upload = UploadFile().remove_file(path)

        data['code'] = upload.get('code')
        data['message'] = upload.get('message')

        return self.create_response(data)
        