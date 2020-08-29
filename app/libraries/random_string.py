import string
import random

class RandomString(object):
    config = {}
    key_length = 0

    def __init__(self, config = None):
        super(RandomString, self).__init__()

        self.key_length = random.randint(0, 11)

        if config:
            self.config = config

        if hasattr(self.config, 'key_length'):
            self.key_length = self.config.key_length

    def run(self):
        return self.generate()

    def base_str(self):
        return (string.letters+string.digits)   

    def generate(self):
        keylist = [random.choice(self.base_str()) for i in range(self.key_length)]
        return ("".join(keylist))