from app.core.controllers import BaseControllers
from app.services.ticket_service import TicketService
import re
import json

class Ticket(BaseControllers):
    request = None

    TABLES = {}
    TICKET_CODE_LENGTH = 11

    def __init__(self, request = None):
        super(Ticket, self).__init__()

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

        data_sql = TicketService().generate_ticket_list(data_model)

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

        data_sql = TicketService().generate_ticket_detail(columns, value)

        data['data'] = data_sql.get('data')
        data['total_data'] = data_sql.get('total_rows')

        return self.create_response(data)

    def get_ticket_code(self):
        data = {
            'code': 200,
            'message': 'Success',
            'data': {}
        }

        data['data'] = {
            'ticket_code': TicketService().generate_ticket_code()
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
        
        # Check availability ticket code
        availability = TicketService().check_availability_ticket_code(value)

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

        ticket_type = request_data.get('type')
        ticket_code = request_data.get('code')
        booking_code = request_data.get('booking_code')
        
        data_model = {
            'type': ticket_type,
            'code': ticket_code,
            'booking_code': booking_code
        }

        TicketService().create_ticket(data_model)

        return self.create_response(data)

    def claim_ticket(self, ticket_code = None):
        if not ticket_code:
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

        is_claimed = request_data.get('is_claimed')
        approved_claim_by = request_data.get('approved_claim_by')

        queries = "is_claimed='{}', \
            approved_claim_by='{}'".format(is_claimed, approved_claim_by)
        
        data_model = {
            'code': ticket_code,
            'data': queries
        }

        TicketService().update_ticket(data_model)

        return self.create_response(data)

    def refund_ticket(self, ticket_code = None):
        if not ticket_code:
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

        is_refunded = request_data.get('is_refunded')
        notes_refund = request_data.get('notes_refund')

        queries = "is_refunded='{}', \
            notes_refund='{}'".format(is_refunded, notes_refund)
        
        data_model = {
            'code': ticket_code,
            'data': queries
        }

        TicketService().update_ticket(data_model)

        return self.create_response(data)

    def generate_eticket(self, ticket_code = None):
        return TicketService().generate_eticket(ticket_code)
        