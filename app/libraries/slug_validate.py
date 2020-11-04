import re

class SlugValidate(object):
    config = {}

    def __init__(self, config = None):
        super(SlugValidate, self).__init__()

        if config:
            self.config = config

    def run(self, value = None):
        return re.search('[_!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/\s]', value)