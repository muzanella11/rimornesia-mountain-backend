from app.core.controllers import BaseControllers
from app.services.booking_service import BookingService
import re
import json

class Booking(BaseControllers):
    request = None

    TABLES = {}
    BOOKING_CODE_LENGTH = 8

    def __init__(self, request = None):
        super(Booking, self).__init__()

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

        data_sql = BookingService().generate_booking_list(data_model)

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
            'data': {},
            'total_data': 0
        }

        data_sql = BookingService().generate_booking_detail(columns, value)

        data['data'] = data_sql.get('data')
        data['total_data'] = data_sql.get('total_rows')

        return self.create_response(data)

    def get_booking_code(self):
        data = {
            'code': 200,
            'message': 'Success',
            'data': {}
        }

        data['data'] = {
            'booking_code': BookingService().generate_booking_code()
        }

        return self.create_response(data)

    def get_availability_code(self, value = None):
        if not value:
            return self.create_response({
                'code': 400,
                'messages': 'Bad Request'
            })

        data = {
            'code': 200,
            'message': 'Success',
            'data': {},
            'total_data': 0
        }
        
        # Check availability booking code
        availability = BookingService().check_availability_booking_code(value)

        data['data'] = availability['data']
        data['total_data'] = availability['total_data']

        return self.create_response(data)

    def create_data(self):
        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        request_data = self.request.json

        booking_type = request_data.get('type')
        booking_code = request_data.get('code')
        user_id = request_data.get('user_id')
        item = request_data.get('item')
        checkin_date = request_data.get('checkin_date')
        checkout_date = request_data.get('checkout_date')
        price = request_data.get('price')
        quantity = request_data.get('quantity')
        price_total = request_data.get('price_total')
        payment_type = request_data.get('payment_type')
        payment_code = request_data.get('payment_code')
        payment_status = request_data.get('payment_status')
        passenger_manifest = request_data.get('passenger_manifest')

        if passenger_manifest:
            passenger_manifest = json.dumps(passenger_manifest)
        
        data_model = {
            'type': booking_type,
            'code': booking_code,
            'user_id': user_id,
            'item': item,
            'checkin_date': checkin_date,
            'checkout_date': checkout_date,
            'price': price,
            'payment_type': payment_type,
            'payment_code': payment_code,
            'payment_status': payment_status,
            'quantity': quantity,
            'price_total': price_total,
            'passenger_manifest': passenger_manifest
        }

        BookingService().create_booking(data_model)

        return self.create_response(data)

    def update_data(self, booking_code = None):
        if not booking_code:
            return self.create_response({
                'code': 400,
                'messages': 'Bad Request'
            })

        data = {
            'code': 200,
            'message': 'Success',
            'total_data': 0
        }

        request_data = self.request.json

        payment_id = request_data.get('payment_id')
        payment_code = request_data.get('payment_code')
        payment_status = request_data.get('payment_status')

        queries = "payment_id='{}',\
            payment_code='{}',\
            payment_status='{}'".format(payment_id, payment_code, payment_status)
        
        data_model = {
            'code': booking_code,
            'data': queries
        }

        BookingService().update_booking(data_model)

        return self.create_response(data)
        