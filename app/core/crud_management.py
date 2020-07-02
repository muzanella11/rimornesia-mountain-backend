from app.libraries.pagination import Pagination
class CrudManagement(object):
    params = None
    action_type = None
    filter_data = None
    limit = 0
    offset = 0
    pagination = {}
    find = None

    def __init__(self, params = None):
        super(CrudManagement, self).__init__()

        if params == None:
            return 
        
        self.params = params

        self.action_type = self.params.get('type')

        self.filter_data = self.params.get('filter')
    
        self.pagination_shown = self.params.get('pagination')

        self.pagination = Pagination({
            'page': self.filter_data.get('page'),
            'limit': self.filter_data.get('limit')
        }).run()

        self.limit = self.pagination.get('limit')
        self.offset = self.pagination.get('offset')

        self.find = self.params.get('find')

