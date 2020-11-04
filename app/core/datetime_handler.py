# from time import gmtime, strftime
from time import gmtime, strftime
from datetime import datetime

class DateTime(object):
    server_time_zone = '+00:00'
    date_time_now = None
    date_time_ago = None
    date_time_diff = None
    years = 0
    months = 0
    days = 0
    weeks = 0
    hours = 0
    minutes = 0
    seconds = 0

    def __init__(self):
        super(DateTime, self).__init__()

        self.set_date_time_now()

    def set_date_time_now(self):
        self.date_time_now = datetime.now()
        self.date_time_now = self.date_time_now.strftime("%Y-%m-%d %H:%M:%S")

    def get_date_time_now(self):
        return self.date_time_now

    def time_elapsed_string(self, time_ago):
        self.date_time_ago = time_ago
        
        self.set_time_diff()
        self.set_days()
        self.set_weeks()
        self.set_years()
        self.set_months()
        self.set_minutes()
        self.set_hours()

        return {
            'years': self.years,
            'months': self.months,
            'weeks': self.weeks,
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }

    def set_time_diff(self):
        now = datetime.strptime(self.date_time_now, "%Y-%m-%d %H:%M:%S")
        now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        ago = datetime.strptime(self.date_time_ago, "%Y-%m-%d %H:%M:%S")
        ago = datetime(ago.year, ago.month, ago.day, ago.hour, ago.minute, ago.second)

        self.date_time_diff = now - ago

        print('difff : ', self.date_time_diff)

    def set_years(self):
        self.years = self.days / 365

        print('years : ', self.years)

    def set_months(self):
        self.months = self.weeks / 4

        print('months : ', self.months)

    def set_days(self):
        self.days = self.date_time_diff.days

        print('days : ', self.days)

    def set_weeks(self):
        self.weeks = self.date_time_diff.days / 7

        print('weeks : ', self.weeks)

    def set_minutes(self):
        self.minutes = divmod(self.date_time_diff.seconds, 60)
        self.seconds = self.minutes[1]
        self.minutes = self.minutes[0]

        print('minutes : ', self.minutes)
        print('seconds : ', self.seconds)

    def set_hours(self):
        self.hours = self.minutes / 60

        print('hours : ', self.hours)

    def context_to_string(self, context, format = None):
        # Context is `datetime`
        if format != None:
            return context.strftime(format)

        return context.strftime("%Y-%m-%d %H:%M:%S")

    def timezone(self, formatted = True):
        timezone = strftime("%z", gmtime())
        # timezone = self.server_time_zone

        if formatted == True:
            timezone = [x for x in timezone]
            timezone = '{}{}{}:{}{}'.format(timezone[0], timezone[1], timezone[2], timezone[3], timezone[4])

        return timezone

    def get_server_time_zone(self):
        return self.server_time_zone