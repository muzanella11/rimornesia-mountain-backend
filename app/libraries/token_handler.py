from app.core.datetime_handler import DateTime

class TokenHandler(object):
    config = {}
    time_by = None
    time_by_value = None
    session_time = None

    def __init__(self, config = None):
        super(TokenHandler, self).__init__()

        if config:
            self.config = config

        if self.config.get('time_by'):
            self.time_by = self.config.get('time_by')

        if self.config.get('time_by_value'):
            self.time_by_value = int(self.config.get('time_by_value'))

        if self.config.get('session_time'):
            self.session_time = self.config.get('session_time')

    def create_expired_time(self):
        if not self.session_time: return
        if not self.time_by: return

        parse_date = DateTime({
            'is_utc_timezone': True
        }).context_to_datetime(self.session_time)
        parse_date = int(parse_date.strftime('%s')) * 1000 # to millisecond
        expired = parse_date

        if self.time_by == 'hours':
            hours = ((self.time_by_value * 60) * 60) * 1000 # to millisecond
            expired = expired + hours

            return expired

        if self.time_by == 'minute':
            minute = (self.time_by_value * 60) * 1000 # to millisecond
            expired = expired + minute

            return expired

        return expired

    def check_expired_time(self, expired_time = None):
        date_time_now = DateTime().get_date_time_now()
        expired_time = int(expired_time)

        date_time_now = DateTime({
            'is_utc_timezone': True
        }).context_to_datetime(date_time_now)
        date_time_now = int(date_time_now.strftime('%s')) * 1000 # to millisecond

        return date_time_now >= expired_time