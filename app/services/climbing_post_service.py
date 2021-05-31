from app import app
from app.models.model_climbing_post import ModelClimbingPost
from app.models.model_mountains import ModelMountains
from app.services.mountains_service import MountainsService
import re
import json

class ClimbingPostService(object):
    config = {}
    base_result = {
        'data': None,
        'total_data': 0
    }
    
    def __init__(self, config = None):
        super(ClimbingPostService, self).__init__()

        if config:
            self.config = config

    def generate_climbing_post_list(self, data_model = None):
        data_sql = getattr(ModelClimbingPost(data_model), 'get_list')()

        raw_data = data_sql.get('data')

        if raw_data:
            for item_raw_data in raw_data:
                # Get mountain value
                data_mountain_id = item_raw_data.get('mountain_id')

                content_data = MountainsService().generate_mountain_detail('id', data_mountain_id)
                content_data = content_data.get('data')
                
                item_raw_data['mountain'] = content_data
                

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def generate_climbing_post_detail(self, columns = None, value = None):
        data_sql = getattr(ModelClimbingPost(), 'get_detail_by')(columns, value)

        raw_data = data_sql.get('data')

        if raw_data:
            # Get mountain value
            data_mountain_id = raw_data.get('mountain_id')

            content_data = MountainsService().generate_mountain_detail('id', data_mountain_id)
            content_data = content_data.get('data')

            raw_data['mountain'] = content_data

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def create_climbing_post(self, data_model = None):
        # To Do :: Create validation here
        getattr(ModelClimbingPost(), 'create_data')(data_model)

    def update_climbing_post(self, data_model = None):
        # To Do :: Create validation here
        getattr(ModelClimbingPost(), 'update_data')(data_model)

    def delete_climbing_post(self, climbing_post_id = None):
        # To Do :: Create validation here
        getattr(ModelClimbingPost(), 'delete_data')(climbing_post_id)
