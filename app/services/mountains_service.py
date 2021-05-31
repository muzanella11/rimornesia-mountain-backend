from app import app
from app.libraries.random_string import RandomString
from app.models.model_mountains import ModelMountains
from app.models.model_indonesia_administrative import ModelIndonesiaAdministrative
from time import gmtime, strftime
import re
import requests

class MountainsService(object):
    config = {}
    base_result = {
        'data': None,
        'total_data': 0
    }
    
    def __init__(self, config = None):
        super(MountainsService, self).__init__()

        if config:
            self.config = config

    def generate_mountain_list(self, data_model = None):
        data_sql = getattr(ModelMountains(data_model), 'get_list')()

        raw_data = data_sql.get('data')

        if raw_data:
            for item_raw_data in raw_data:
                # Get province value
                data_province_id = item_raw_data.get('province_id')

                content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('provinces', 'id', data_province_id)
                content_data = content_data.get('data')
                
                item_raw_data['province'] = content_data

                # Get regency value
                data_regency_id = item_raw_data.get('regency_id')

                content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('regencies', 'id', data_regency_id)
                content_data = content_data.get('data')
                
                item_raw_data['regency'] = content_data

                # Get district value
                data_district_id = item_raw_data.get('district_id')

                content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('districts', 'id', data_district_id)
                content_data = content_data.get('data')
                
                item_raw_data['district'] = content_data

                # Get village value
                data_village_id = item_raw_data.get('village_id')

                content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('villages', 'id', data_village_id)
                content_data = content_data.get('data')
                
                item_raw_data['village'] = content_data                

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def generate_mountain_detail(self, columns = None, booking_code = None):
        data_sql = getattr(ModelMountains(), 'get_detail_by')(columns, booking_code)

        raw_data = data_sql.get('data')

        if raw_data:
            # Get province value
            data_province_id = raw_data.get('province_id')

            content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('provinces', 'id', data_province_id)
            content_data = content_data.get('data')

            raw_data['province'] = content_data

            # Get regency value
            data_regency_id = raw_data.get('regency_id')

            content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('regencies', 'id', data_regency_id)
            content_data = content_data.get('data')

            raw_data['regency'] = content_data

            # Get district value
            data_district_id = raw_data.get('district_id')

            content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('districts', 'id', data_district_id)
            content_data = content_data.get('data')

            raw_data['district'] = content_data

            # Get village value
            data_village_id = raw_data.get('village_id')

            content_data = getattr(ModelIndonesiaAdministrative(), 'get_detail_by')('villages', 'id', data_village_id)
            content_data = content_data.get('data')

            raw_data['village'] = content_data

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result
