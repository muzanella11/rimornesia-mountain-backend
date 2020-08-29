from flask import send_from_directory
from app.libraries.cdn77 import Cdn77
from app.libraries.random_string import RandomString
import base64
import os

class UploadFile(object):
    upload_directory = 'uploads'
    path_target = 'app/uploads'
    config = {}

    def __init__(self, config = None):
        super(UploadFile, self).__init__()

        if config:
            self.config = config

    def run(self, value, path):
        # Cdn77().run()
        return self.base64_to_file(value, path)

    def generate_file_name(self, value):
        file_type = self.get_file_type(value[0])
        file_name = RandomString().run()

        value = '{}.{}'.format(file_name, file_type)

        return value

    def get_file_type(self, value):
        value = value.split(';')[0].split('/')[1]

        return value

    def get_file_local(self, path):
        return send_from_directory(self.upload_directory, path)

    def base64_to_file(self, value, path):
        value = value.split(',')
        raw_path = path

        if path:
            self.path_target = self.path_target + path

        file_name = self.generate_file_name(value)
        file_result = value[1]
        path = '{}/{}'.format(self.path_target, file_name)

        # Check file exists and create new file name
        if self.check_file_exists(path):
            file_name = self.generate_file_name(value)
            path = '{}/{}'.format(self.path_target, file_name)

        path_result = '{}{}/{}'.format(self.upload_directory, raw_path if raw_path else '', file_name)

        self.upload({
            'path': path,
            'file': file_result
        })

        return {
            'path': path_result
        }

    def upload(self, value):
        path = value.get('path')
        file = value.get('file')

        self.check_directory(self.path_target)

        image_result = open(path, 'wb') # create a writable image and write the decoding result
        image_result.write(base64.decodestring(file))

    def check_directory(self, value):
        if not os.path.exists(value):
            os.mkdir(value)

    def check_file_exists(self, value):
        return os.path.isfile(value)

    def remove_file(self, path = None):
        raw_path = path

        if not raw_path:
            return {
                'code': 400,
                'message': 'Something wrong when remove file'
            }

        path = '{}/{}'.format(self.path_target, path)

        if not self.check_file_exists(path):
            return {
                'code': 404,
                'message': 'File not found'
            }

        os.remove(path)

        return {
            'code': 200,
            'message': 'Success removing file {}'.format(raw_path)
        }