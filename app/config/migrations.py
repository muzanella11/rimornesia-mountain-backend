class MigrationsConfig(object):
    ACTION = {
        'alter': 'ALTER',
        'create': 'CREATE',
        'drop': 'DROP',
        'insert': 'INSERT'
    }

    def __init__(self):
        super(MigrationsConfig, self).__init__()

    def getAction(self):
        return self.ACTION
    