from app import app
from app.libraries.random_string import RandomString
from app.models.model_ticket import ModelTicket
from app.models.model_ticket_type import ModelTicketType
from app.services.booking_service import BookingService
import requests
import pdfkit

class TicketService(object):
    config = {}
    base_result = {
        'data': None,
        'total_data': 0
    }
    TICKET_CODE_LENGTH = 11
    BILLING_HOST = app.environment.get('APP_BILLING_HOST')
    MOUNTAIN_HOST = app.environment.get('APP_MOUNTAIN_HOST')
    
    def __init__(self, config = None):
        super(TicketService, self).__init__()

        if config:
            self.config = config

    def generate_ticket_list(self, data_model = None):
        data_sql = getattr(ModelTicket(data_model), 'get_list')()

        raw_data = data_sql.get('data')

        if raw_data:
            for item_raw_data in raw_data:
                # Get booking type value
                data_type = item_raw_data.get('type')

                content_data = getattr(ModelTicketType(), 'get_detail_by')('id', data_type)
                content_data = content_data.get('data')
                
                item_raw_data['type'] = content_data.get('name')

                # Get booking data
                booking_code = item_raw_data.get('booking_code')

                if booking_code:
                    data_booking = getattr(BookingService(), 'generate_booking_detail')('code', booking_code)
                    data_booking = data_booking.get('data')

                    item_raw_data['booking'] = data_booking
                

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def generate_ticket_detail(self, columns = None, booking_code = None):
        data_sql = getattr(ModelTicket(), 'get_detail_by')(columns, booking_code)

        raw_data = data_sql.get('data')

        if raw_data:
            # Get booking type value
            data_type = raw_data.get('type')

            content_data = getattr(ModelTicketType(), 'get_detail_by')('id', data_type)
            content_data = content_data.get('data')
            
            raw_data['type'] = content_data.get('name')

            # Get booking data
            booking_code = raw_data.get('booking_code')

            if booking_code:
                data_booking = getattr(BookingService(), 'generate_booking_detail')('code', booking_code)
                data_booking = data_booking.get('data')

                rawbooking_code = raw_data['booking'] = data_booking

        self.base_result['data'] = raw_data
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def create_ticket(self, data_model = None):
        # To Do :: Create validation here
        getattr(ModelTicket(), 'create_data')(data_model)

    def update_ticket(self, data_model = None):
        # To Do :: Create validation here
        getattr(ModelTicket(), 'update_data')(data_model)

    def generate_ticket_code(self):
        result = RandomString({
            'key_length': self.TICKET_CODE_LENGTH
        }).run()

        result = '{}{}{}'.format('RMNSA', result.upper(), 'TIX')

        return result

    def check_availability_ticket_code(self, booking_code = None):
        availability_result = {
            'status': 0,
            'message': 'Available',
            'booking_code': booking_code
        }

        # Check availability booking code
        data_sql = getattr(ModelTicket(), 'get_detail_by')('code', booking_code)

        if data_sql.get('data'):
            availability_result['status'] = 1
            availability_result['message'] = 'Not Available'

        self.base_result['data'] = availability_result
        self.base_result['total_data'] = data_sql.get('total_rows')

        return self.base_result

    def get_payment_code(self):
        return 1

    def generate_eticket(self, ticket_code = None):
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        # pdfkit.from_url('http://google.com', 'out.pdf', configuration=config)
        pdfkit.from_url('{}/eticket/{}'.format(self.MOUNTAIN_HOST, ticket_code), 'out.pdf', configuration=config)

        return 'Success'