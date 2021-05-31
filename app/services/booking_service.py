from app import app
from app.libraries.random_string import RandomString
from app.models.model_booking import ModelBooking
from app.models.model_booking_type import ModelBookingType
from app.models.model_climbing_post import ModelClimbingPost
from app.services.climbing_post_service import ClimbingPostService
import requests

class BookingService(object):
    config = {}
    base_result = {
        'data': None,
        'total_data': 0
    }
    BOOKING_CODE_LENGTH = 11
    BILLING_HOST = app.environment.get('APP_BILLING_HOST')
    
    def __init__(self, config = None):
        super(BookingService, self).__init__()

        if config:
            self.config = config

    def generate_booking_list(self, data_model = None):
        data_sql = getattr(ModelBooking(data_model), 'get_list')()

        raw_data = data_sql.get('data')

        if raw_data:
            for item_raw_data in raw_data:
                # Get booking type value
                data_type = item_raw_data.get('type')

                content_data = getattr(ModelBookingType(), 'get_detail_by')('id', data_type)
                content_data = content_data.get('data')
                
                item_raw_data['type'] = content_data.get('name')

                # Get booking item
                data_item = item_raw_data.get('item')

                if item_raw_data['type'] == 'climbing_post':
                    content_data = getattr(ClimbingPostService(), 'generate_climbing_post_detail')('id', data_item)
                    content_data = content_data.get('data')

                    item_raw_data['item'] = content_data

                # Get payment expired status
                payment_code = item_raw_data.get('payment_code')
                item_raw_data['payment_expired'] = None

                if payment_code:
                    res_payment_code = requests.get('{}/payment/{}'.format(self.BILLING_HOST, payment_code))
                    res_payment_code = res_payment_code.json()

                    payment_data = res_payment_code.get('data')

                    item_raw_data['payment_expired'] = payment_data['is_expired']
                    item_raw_data['unique_code'] = payment_data['unique_code']
                

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def generate_booking_detail(self, columns = None, booking_code = None):
        data_sql = getattr(ModelBooking(), 'get_detail_by')(columns, booking_code)

        raw_data = data_sql.get('data')

        if raw_data:
            # Get booking type value
            data_type = raw_data.get('type')

            content_data = getattr(ModelBookingType(), 'get_detail_by')('id', data_type)
            content_data = content_data.get('data')
            
            raw_data['type'] = content_data.get('name')

            # Get booking item
            data_item = raw_data.get('item')

            if raw_data['type'] == 'climbing_post':
                content_data = getattr(ClimbingPostService(), 'generate_climbing_post_detail')('id', data_item)
                content_data = content_data.get('data')

                raw_data['item'] = content_data

            # Get payment expired status
            payment_code = raw_data.get('payment_code')
            raw_data['payment_expired'] = None

            if payment_code:
                res_payment_code = requests.get('{}/payment/{}'.format(self.BILLING_HOST, payment_code))
                res_payment_code = res_payment_code.json()

                payment_data = res_payment_code.get('data')

                raw_data['payment_expired'] = payment_data['is_expired']
                raw_data['unique_code'] = payment_data['unique_code']

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def create_booking(self, data_model = None):
        # To Do :: Create validation here
        # Get payment code
        res_payment_code = requests.get('{}/payment/code'.format(self.BILLING_HOST))
        res_payment_code = res_payment_code.json()
        payment_data = res_payment_code.get('data')
        payment_code = payment_data.get('payment_code')

        data_model['payment_code'] = payment_code

        # Create payment
        payment_payload = {
            'type': data_model['payment_type'],
            'code': data_model['payment_code'],
            'user_id': data_model['user_id'],
            'price_total': data_model['price_total'],
            'unique_code': int(str(data_model['price_total'])[-3:]),
            'booking_code': data_model['code']
        }
        res_payment = requests.post('{}/payment'.format(self.BILLING_HOST), json = payment_payload)
        res_payment = res_payment.json()

        getattr(ModelBooking(), 'create_data')(data_model)

    def update_booking(self, data_model = None):
        # To Do :: Create validation here
        getattr(ModelBooking(), 'update_data')(data_model)

    def generate_booking_code(self):
        result = RandomString({
            'key_length': self.BOOKING_CODE_LENGTH
        }).run()

        result = '{}{}{}'.format('RMNSA', result.upper(), 'BO')

        return result

    def check_availability_booking_code(self, booking_code = None):
        availability_result = {
            'status': 0,
            'message': 'Available',
            'booking_code': booking_code
        }

        # Check availability booking code
        data_sql = getattr(ModelBooking(), 'get_detail_by')('code', booking_code)

        if data_sql.get('data'):
            availability_result['status'] = 1
            availability_result['message'] = 'Not Available'

        self.base_result['data'] = availability_result
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def get_payment_code(self):
        return 1

    def get_booking_type(self, value = None):
        return getattr(ModelBookingType(), 'get_detail_by')('name', value)