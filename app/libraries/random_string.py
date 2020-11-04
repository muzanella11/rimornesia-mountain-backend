import string
import random

class RandomString(object):
    config = {}
    key_length = 0
    is_return_number = False

    def __init__(self, config = None):
        super(RandomString, self).__init__()

        self.key_length = random.randint(0, 11)

        if config:
            self.config = config

        if self.config.get('key_length'):
            self.key_length = self.config.get('key_length')

        if self.config.get('is_return_number'):
            self.is_return_number = self.config.get('is_return_number')

    def run(self):
        return self.generate()

    def base_str(self):
        if self.config.get('is_return_number'):
            return (string.digits)  

        return (string.letters+string.digits)   

    def generate(self):
        keylist = [random.choice(self.base_str()) for i in range(self.key_length)]
        return ("".join(keylist))