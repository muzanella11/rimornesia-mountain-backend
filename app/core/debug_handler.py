class DebugHandler(object):
    base_config = {
        'title': 'Debug',
        'messages': 'Test Debug Handler'
    }
    config = {}

    def __init__(self, config = {}):
        super(DebugHandler, self).__init__()
        self.config = config

        self.run()

    def run(self):
        print('debug \n')
        
        self.template()

    def getTitle(self):
        if not self.config.get('title'):
            return self.base_config.get('title')

        return self.config.get('title')

    def getMessages(self):
        if not self.config.get('messages'):
            return self.base_config.get('messages')

        return self.config.get('messages')

    def template(self):
        print("/**************** :: BEGIN {} :: ****************/".format(self.getTitle()))
        print("{}".format(self.getMessages()))
        print("/**************** :: END {} :: ****************/".format(self.getTitle()))