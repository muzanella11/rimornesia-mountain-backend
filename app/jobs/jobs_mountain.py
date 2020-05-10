from __future__ import print_function

from app.core.jobs import Jobs
from app.config.migrations import MigrationsConfig
import os
import requests
import json
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

DB_NAME = os.environ.get('DB_NAME')
MAPS_HOST = os.environ.get('MAPS_HOST')
MAPS_API_KEY = os.environ.get('MAPS_API_KEY')
MAPS_SESSION_TOKEN = os.environ.get('MAPS_SESSION_TOKEN')
MAPS_URL_GEOCODE_JSON = '/maps/api/place/textsearch/json'
MAPS_URL = '{}{}?key={}&sensor=false&language=ID'.format(MAPS_HOST, MAPS_URL_GEOCODE_JSON, MAPS_API_KEY)

LIMIT = 1

ACTION = MigrationsConfig().getAction()
TABLES = {}
JOBS_TYPE_GEOCODE = 'mountains_administrative'

print('here mountain')

jobs = Jobs()
reconnect = False

# Create or Use database
jobs.create_database(DB_NAME)

page = 1
counter_province_data = 0
total_mountain_data = 0

fa_raw_counter = []

while True:
    print('[RUNNING] Jobs Mountain {}'.format(JOBS_TYPE_GEOCODE))
    print('[PAGE] {}'.format(page))
    print('[LIMIT] {}'.format(LIMIT))

    if JOBS_TYPE_GEOCODE == 'mountains':
        # Mountain Data
        request_provinces = requests.get('http://localhost:5000/province?page={}&limit={}'.format(page, LIMIT))
        response_provinces = request_provinces.json()
        data_provinces = response_provinces.get('data')

        provinces_result = []

        if data_provinces == None:
            print('[END] Jobs Geocode {}'.format(JOBS_TYPE_GEOCODE))
            break

        for item in data_provinces:
            province_name = item.get('name').encode('utf-8')
            location = json.loads(item.get('location'))
            latitude = location.get('lat')
            longitude = location.get('lng')
            location = "{},{}".format(latitude, longitude)

            print('location : ', location)

            print('[PREPARE] Find Geocode {}'.format(province_name))

            province_name = province_name.lower()
            province_name = province_name.split(' ')

            data_temp = []

            for item_province in province_name:
                data_temp.append(item_province.capitalize())

            data_temp = '+'.join(data_temp)

            provinces_result.append({
                'location': location,
                'province': data_temp
            })

        for item_province_result in provinces_result:
            province_name = item_province_result.get('province').replace('+', ' ').upper()
            query = 'gunung+{}'.format(province_name.lower()).replace(' ', '+')
            location = item_province_result.get('location')
            next_page_token = ''

            counter_province_data = counter_province_data + 1

            print('query name : ', query)

            print('[COUNTER] DATA PROVINCES : {}'.format(counter_province_data))

            print('[FIND] Geocode Data {} '.format(province_name), end='')

            request_geocode = requests.get('{}&query={}&location={}&page_token={}'.format(MAPS_URL, query, location, next_page_token))
            request_response = request_geocode.json()
            result_response = request_response.get('results')
            next_page_token = request_response.get('next_page_token')

            if len(result_response) > 0:
                print('[OK]')
                
                mountain_raw_data = result_response

                for mountain_item in mountain_raw_data:
                    total_mountain_data = total_mountain_data + 1

                    print('[TOTAL] Mountain Data : ', total_mountain_data)

                    location = json.dumps(mountain_item.get('geometry').get('location'))
                    formatted_address = mountain_item.get('formatted_address')
                    raw_address = formatted_address.split(', ')
                    
                    print('raw address : ', raw_address)

                    name = mountain_item.get('name').decode('utf-8')
                    raw_location = json.dumps(mountain_item)
                    
                    # Insert to mountains
                    TABLES['mountains'] = {
                        'action': ACTION.get('insert'),
                        'command': (
                            "INSERT INTO `mountains` (`name`,`formatted_address`, `location`, `raw_location`, `created_at`) VALUES"
                            " ('{}','{}','{}','{}', {})".format(name.replace('Gn.', 'Gunung'), formatted_address, location, raw_location, 'NOW()')
                        )
                    }

                    if reconnect == True:
                        jobs = Jobs()
                        
                        # Create or Use database
                        jobs.create_database(DB_NAME)

                    # Execute Command
                    jobs.create_begin_process('Insert Table Provinces')
                    jobs.execute_command(
                        TABLES
                    )
                    jobs.create_end_process('Insert Table Provinces')

                    # Reconnect db because `cursor.execute` cannot run multiple queries
                    reconnect = True

                    # Close Connection
                    jobs.close_connection()

                    # print('hereee : ', TABLES)
            else:
                print('[FAILED]')
                
    if JOBS_TYPE_GEOCODE == 'mountains_administrative':
        # Mountain Data
        request_mountains = requests.get('http://localhost:5000/mountain?page={}&limit={}'.format(page, LIMIT))
        response_mountains = request_mountains.json()
        data_mountains = response_mountains.get('data')

        if data_mountains == None:
            print('[END] Jobs Geocode {}'.format(JOBS_TYPE_GEOCODE))
            break

        for item in data_mountains:
            mountain_name = item.get('name')
            formatted_address = item.get('formatted_address')
            fa_raw = formatted_address.split(', ')

            villages = None
            districts = None
            regencies = None
            provinces = None

            village_id = ''
            district_id = ''
            regency_id = ''
            province_id = ''

            if len(fa_raw) == 7:
                villages = fa_raw[2].lower()
                villages = villages.replace('tim.', 'timur').replace('bar.', 'barat')
                villages = villages.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')
                villages = villages.split('/')[0]
                districts = fa_raw[3].lower()
                districts = districts.replace('tim.', 'timur').replace('bar.', 'barat')
                districts = districts.replace('uta.', 'utara').replace('sel.', 'selatan')
                districts = districts.replace('kec. ', '').replace(' ', '-')
                districts = districts.split('/')[0]
                regencies = fa_raw[4].lower()
                regencies = regencies.replace('tim.', 'timur').replace('bar.', 'barat')
                regencies = regencies.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')
                regencies = regencies.split('/')[0]
                provinces = fa_raw[5].lower()
                provinces = provinces.replace('tim.', 'timur').replace('bar.', 'barat')
                provinces = provinces.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')

            if len(fa_raw) == 6:
                villages = fa_raw[1].lower()
                villages = villages.replace('tim.', 'timur').replace('bar.', 'barat')
                villages = villages.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')
                villages = villages.split('/')[0]
                districts = fa_raw[2].lower()
                districts = districts.replace('tim.', 'timur').replace('bar.', 'barat')
                districts = districts.replace('uta.', 'utara').replace('sel.', 'selatan')
                districts = districts.replace('kec. ', '').replace(' ', '-')
                districts = districts.split('/')[0]
                regencies = fa_raw[3].lower()
                regencies = regencies.replace('tim.', 'timur').replace('bar.', 'barat')
                regencies = regencies.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')
                regencies = regencies.split('/')[0]
                provinces = fa_raw[4].lower()
                provinces = provinces.replace('tim.', 'timur').replace('bar.', 'barat')
                provinces = provinces.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')
                provinces = provinces.split('/')[0]

            if len(fa_raw) == 5:
                districts = fa_raw[1].lower()
                districts = districts.replace('tim.', 'timur').replace('bar.', 'barat')
                districts = districts.replace('uta.', 'utara').replace('sel.', 'selatan')
                districts = districts.replace('kec. ', '').replace(' ', '-')
                districts = districts.split('/')[0]
                regencies = fa_raw[2].lower()
                regencies = regencies.replace('tim.', 'timur').replace('bar.', 'barat')
                regencies = regencies.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')
                regencies = regencies.split('/')[0]
                provinces = fa_raw[3].lower()
                provinces = provinces.replace('tim.', 'timur').replace('bar.', 'barat')
                provinces = provinces.replace('uta.', 'utara').replace('sel.', 'selatan').replace(' ', '-')
                provinces = provinces.split('/')[0]

            # Get Villages ID
            request_villages = requests.get('http://localhost:5000/village/{}'.format(villages))
            response_villages = request_villages.json()
            data_villages = response_villages.get('data')

            if data_villages != None:
                village_id = data_villages.get('id')

            # Get Districts ID
            request_districts = requests.get('http://localhost:5000/district/{}'.format(districts))
            response_districts = request_districts.json()
            data_districts = response_districts.get('data')
            
            if data_districts != None:
                district_id = data_districts.get('id')

            # Get Regencies ID
            request_regencies = requests.get('http://localhost:5000/regency/{}'.format(regencies))
            response_regencies = request_regencies.json()
            data_regencies = response_regencies.get('data')

            if data_regencies != None:
                regency_id = data_regencies.get('id')

            # Get Provinces ID
            request_provinces = requests.get('http://localhost:5000/province/{}'.format(provinces))
            response_provinces = request_provinces.json()
            data_provinces = response_provinces.get('data')
            
            if data_provinces != None:
                province_id = data_provinces.get('id')

            # Update data
            TABLES['mountains'] = {
                'action': ACTION.get('update'),
                'command': (
                    "UPDATE mountains"
                    " SET province_id='{}', district_id='{}', regency_id='{}', village_id='{}', updated_at=now() WHERE name='{}'".format(province_id, district_id, regency_id, village_id, mountain_name)
                )
            }

            print('province id : ', " SET province_id={}, district_id={}, regency_id={}, village_id={} WHERE name={}".format(province_id, district_id, regency_id, village_id, mountain_name))

            if reconnect == True:
                jobs = Jobs()
                
                # Create or Use database
                jobs.create_database(DB_NAME)

            # Execute Command
            jobs.create_begin_process('Insert Table Provinces')
            jobs.execute_command(
                TABLES
            )
            jobs.create_end_process('Insert Table Provinces')

            # Reconnect db because `cursor.execute` cannot run multiple queries
            reconnect = True

            # Close Connection
            jobs.close_connection()

            # print('formatted : ', len(fa_raw))
            # print('formatted : ', fa_raw)
            
            fa_raw_counter.append(TABLES)

        # print('data fa raw counter : ', fa_raw_counter)
        # print('data fa raw counter length : ', len(fa_raw_counter))

    page = page + 1

# Reconnect db because `cursor.execute` cannot run multiple queries
reconnect = False

# Close Connection
jobs.close_connection()

print('[SUCCESS] Running Jobs Geocode :)')