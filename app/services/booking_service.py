from app.libraries.random_string import RandomString
from app.models.model_booking import ModelBooking
from app.models.model_booking_type import ModelBookingType

class BookingService(object):
    config = {}
    base_result = {
        'data': None,
        'total_data': 0
    }
    BOOKING_CODE_LENGTH = 8
    
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

        self.base_result['data'] = data_sql.get('data')
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

        self.base_result['data'] = data_sql.get('data')
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def create_booking(self, data_model = None):
        # To Do :: Create validation here
        getattr(ModelBooking(), 'create_data')(data_model)

    def update_booking(self, data_model = None):
        # To Do :: Create validation here
        getattr(ModelBooking(), 'update_data')(data_model)

    def generate_booking_code(self):
        result = RandomString({
            'key_length': self.BOOKING_CODE_LENGTH
        }).run()

        result = result.upper()

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