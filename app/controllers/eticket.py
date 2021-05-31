from app.core.controllers import BaseControllers
from app.services.ticket_service import TicketService
import re
import json

class ETicket(BaseControllers):
    request = None

    TABLES = {}

    def __init__(self, request = None):
        super(ETicket, self).__init__()

        self.request = request

    def get_detail(self, columns = None, value = None):
        if columns == "error":
            return self.create_response({
                'code': 400,
                'messages': 'Bad Request'
            })

        data_sql = TicketService().generate_ticket_detail(columns, value)
        raw_data = data_sql.get('data')

        eticket_type_raw = raw_data.get('type')
        eticket_type = eticket_type_raw
        eticket_type = eticket_type.split('_')
        eticket_type = ' '.join(eticket_type).title()

        data = {
            'title': 'E-Tiket {}'.format(eticket_type),
            'title_type': eticket_type
        }

        data['data'] = raw_data
        data['total_data'] = data_sql.get('total_rows')

        # Select eticket views
        template = '/views/eticket/eticket.html'

        if eticket_type_raw == 'climbing_post':
            template = '/views/eticket/climbing_post.html'

        return self.views(template, data)
        