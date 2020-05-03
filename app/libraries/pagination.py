import math

class Pagination(object):
    limit = 5
    page = 0
    offset = 0
    total_page = 0
    total_data = 0
    config = {}

    def __init__(self, config = {}):
        super(Pagination, self).__init__()

        self.config = config
        
        if self.config.get('page') and self.config.get('page').isnumeric() :
            self.page = int(self.config.get('page'))
        
        if self.config.get('limit') and self.config.get('limit').isnumeric():
            self.limit = int(self.config.get('limit'))

        if self.config.get('total_data') and self.config.get('total_data').isnumeric():
            self.total_data = int(self.config.get('total_data'))

        self.set_offset()
        self.set_total_page()


    def run(self):
        return {
            'limit': self.limit,
            'page': self.page,
            'offset': self.offset,
            'total_page': self.total_page,
            'total_data': self.total_data
        }

    def set_offset(self):
        if self.page > 0:
            self.offset = self.limit * (self.page - 1)

    def set_total_page(self):
        if self.total_data > 0:
            self.total_page = math.ceil(self.total_data / self.limit)