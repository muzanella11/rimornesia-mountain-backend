from __future__ import print_function

from app.core.jobs import Jobs
from app.config.migrations import MigrationsConfig
import os
import requests
import json

DB_NAME = os.environ.get('DB_NAME')
MAPS_HOST = os.environ.get('MAPS_HOST')
MAPS_API_KEY = os.environ.get('MAPS_API_KEY')
MAPS_SESSION_TOKEN = os.environ.get('MAPS_SESSION_TOKEN')
MAPS_URL_GEOCODE_JSON = '/maps/api/geocode/json'
MAPS_URL = '{}{}?key={}&components=country:ID&language=id'.format(MAPS_HOST, MAPS_URL_GEOCODE_JSON, MAPS_API_KEY)

LIMIT = 1000

ACTION = MigrationsConfig().getAction()
TABLES = {}
JOBS_TYPE_GEOCODE = 'districts'

print('here geocode')

jobs = Jobs()
reconnect = False

# Create or Use database
jobs.create_database(DB_NAME)

page = 1
counter_data = 0

while True:
    print('[RUNNING] Jobs Geocode {}'.format(JOBS_TYPE_GEOCODE))
    print('[PAGE] {}'.format(page))
    print('[LIMIT] {}'.format(LIMIT))

    if JOBS_TYPE_GEOCODE == 'provinces':
        # Provinces Data
        request_provinces = requests.get('http://localhost:5000/province?page={}&limit={}'.format(page, LIMIT))
        response_provinces = request_provinces.json()
        data_provinces = response_provinces.get('data')

        provinces_result = []

        if data_provinces == None:
            print('[END] Jobs Geocode {}'.format(JOBS_TYPE_GEOCODE))
            break

        for item in data_provinces:
            province_name = item.get('name').encode('utf-8')

            print('[PREPARE] Find Geocode {}'.format(province_name))

            province_name = province_name.lower()
            province_name = province_name.split(' ')

            data_temp = []

            for item_province in province_name:
                data_temp.append(item_province.capitalize())

            data_temp = '+'.join(data_temp)

            provinces_result.append(data_temp)

        for item_province_result in provinces_result:
            province_name = item_province_result.replace('+', ' ').upper()

            counter_data = counter_data + 1

            print('[COUNTER] DATA : {}'.format(counter_data))

            print('[FIND] Geocode Data {} '.format(province_name), end='')

            request_geocode = requests.get('{}&address={}'.format(MAPS_URL, item_province_result))
            request_response = request_geocode.json()
            result_response = request_response.get('results')

            if len(result_response) > 0:
                print('[OK]')
                location = json.dumps(result_response[0].get('geometry').get('location'))
                result = json.dumps(result_response)

                TABLES['provinces'] = {
                    'action': ACTION.get('update'),
                    'command': (
                        "UPDATE `provinces`"
                        " SET location='{}', raw_geocode='{}'"
                        " WHERE name='{}'".format(location, result, province_name)
                    )
                }

                if reconnect == True:
                    jobs = Jobs()
                    
                    # Create or Use database
                    jobs.create_database(DB_NAME)

                # Execute Command
                jobs.create_begin_process('Update Table Provinces')
                jobs.execute_command(
                    TABLES
                )
                jobs.create_end_process('Update Table Provinces')

                # Reconnect db because `cursor.execute` cannot run multiple queries
                reconnect = True

                # Close Connection
                jobs.close_connection()

                # print('hereee : ', TABLES)
            else:
                print('[FAILED]')

    if JOBS_TYPE_GEOCODE == 'regencies':
        # Regencies Data
        request_regencies = requests.get('http://localhost:5000/regency?page={}&limit={}'.format(page, LIMIT))
        response_regencies = request_regencies.json()
        data_regencies = response_regencies.get('data')

        regencies_result = []

        if data_regencies == None:
            print('[END] Jobs Geocode {}'.format(JOBS_TYPE_GEOCODE))
            break

        for item in data_regencies:
            regency_name = item.get('name').encode('utf-8')

            print('[PREPARE] Find Geocode {}'.format(regency_name))

            regency_name = regency_name.lower()
            regency_name = regency_name.split(' ')

            data_temp = []

            for item_regency in regency_name:
                data_temp.append(item_regency.capitalize())

            data_temp = '+'.join(data_temp)

            regencies_result.append(data_temp)

        for item_regency_result in regencies_result:
            regency_name = item_regency_result.replace('+', ' ').upper()

            counter_data = counter_data + 1

            print('[COUNTER] DATA : {}'.format(counter_data))

            print('[FIND] Geocode Data {} '.format(regency_name), end='')

            request_geocode = requests.get('{}&address={}'.format(MAPS_URL, item_regency_result))
            request_response = request_geocode.json()
            result_response = request_response.get('results')

            if len(result_response) > 0:
                print('[OK]')
                location = json.dumps(result_response[0].get('geometry').get('location'))
                result = json.dumps(result_response)

                TABLES['regencies'] = {
                    'action': ACTION.get('update'),
                    'command': (
                        "UPDATE `regencies`"
                        " SET location='{}', raw_geocode='{}'"
                        " WHERE name='{}'".format(location, result, regency_name)
                    )
                }

                if reconnect == True:
                    jobs = Jobs()
                    
                    # Create or Use database
                    jobs.create_database(DB_NAME)

                # Execute Command
                jobs.create_begin_process('Update Table Regencies')
                jobs.execute_command(
                    TABLES
                )
                jobs.create_end_process('Update Table Regencies')

                # Reconnect db because `cursor.execute` cannot run multiple queries
                reconnect = True

                # Close Connection
                jobs.close_connection()

                # print('hereee : ', TABLES)
            else:
                print('[FAILED]')

    if JOBS_TYPE_GEOCODE == 'districts':
        # Districts Data
        request_districts = requests.get('http://localhost:5000/district?page={}&limit={}'.format(page, LIMIT))
        response_districts = request_districts.json()
        data_districts = response_districts.get('data')

        districts_result = []

        if data_districts == None:
            print('[END] Jobs Geocode {}'.format(JOBS_TYPE_GEOCODE))
            break

        for item in data_districts:
            district_name = item.get('name').encode('utf-8')

            print('[PREPARE] Find Geocode {}'.format(district_name))

            district_name = district_name.lower()
            district_name = district_name.split(' ')

            data_temp = []

            for item_district in district_name:
                data_temp.append(item_district.capitalize())

            data_temp = '+'.join(data_temp)

            districts_result.append(data_temp)

        for item_district_result in districts_result:
            district_name = item_district_result.replace('+', ' ').upper()

            counter_data = counter_data + 1

            print('[COUNTER] DATA : {}'.format(counter_data))

            print('[FIND] Geocode Data {} '.format(district_name), end='')

            request_geocode = requests.get('{}&address={}'.format(MAPS_URL, item_district_result))
            request_response = request_geocode.json()
            result_response = request_response.get('results')

            if len(result_response) > 0:
                print('[OK]')
                location = json.dumps(result_response[0].get('geometry').get('location'))
                result = json.dumps(result_response)

                TABLES['districts'] = {
                    'action': ACTION.get('update'),
                    'command': (
                        "UPDATE `districts`"
                        " SET location='{}', raw_geocode='{}'"
                        " WHERE name='{}'".format(location, result, district_name)
                    )
                }

                if reconnect == True:
                    jobs = Jobs()
                    
                    # Create or Use database
                    jobs.create_database(DB_NAME)

                # Execute Command
                jobs.create_begin_process('Update Table Districts')
                jobs.execute_command(
                    TABLES
                )
                jobs.create_end_process('Update Table Districts')

                # Reconnect db because `cursor.execute` cannot run multiple queries
                reconnect = True

                # Close Connection
                jobs.close_connection()

                # print('hereee : ', TABLES)
            else:
                print('[FAILED]')

    if JOBS_TYPE_GEOCODE == 'villages':
        # Villages Data
        request_villages = requests.get('http://localhost:5000/village?page={}&limit={}'.format(page, LIMIT))
        response_villages = request_villages.json()
        data_villages = response_villages.get('data')

        villages_result = []

        if data_villages == None:
            print('[END] Jobs Geocode {}'.format(JOBS_TYPE_GEOCODE))
            break

        for item in data_villages:
            village_name = item.get('name').encode('utf-8')

            print('[PREPARE] Find Geocode {}'.format(village_name))

            village_name = village_name.lower()
            village_name = village_name.split(' ')

            data_temp = []

            for item_village in village_name:
                data_temp.append(item_village.capitalize())

            data_temp = '+'.join(data_temp)

            villages_result.append(data_temp)

        for item_village_result in villages_result:
            village_name = item_village_result.replace('+', ' ').upper()

            counter_data = counter_data + 1

            print('[COUNTER] DATA : {}'.format(counter_data))

            print('[FIND] Geocode Data {} '.format(village_name), end='')

            request_geocode = requests.get('{}&address={}'.format(MAPS_URL, item_village_result))
            request_response = request_geocode.json()
            result_response = request_response.get('results')

            if len(result_response) > 0:
                print('[OK]')
                location = json.dumps(result_response[0].get('geometry').get('location'))
                result = json.dumps(result_response)

                TABLES['villages'] = {
                    'action': ACTION.get('update'),
                    'command': (
                        "UPDATE `villages`"
                        " SET location='{}', raw_geocode='{}'"
                        " WHERE name='{}'".format(location, result, village_name)
                    )
                }

                if reconnect == True:
                    jobs = Jobs()
                    
                    # Create or Use database
                    jobs.create_database(DB_NAME)

                # Execute Command
                jobs.create_begin_process('Update Table Villages')
                jobs.execute_command(
                    TABLES
                )
                jobs.create_end_process('Update Table Villages')

                # Reconnect db because `cursor.execute` cannot run multiple queries
                reconnect = True

                # Close Connection
                jobs.close_connection()

                # print('hereee : ', TABLES)
            else:
                print('[FAILED]')

    page = page + 1

# Reconnect db because `cursor.execute` cannot run multiple queries
reconnect = False

# Close Connection
jobs.close_connection()

print('[SUCCESS] Running Jobs Geocode :)')