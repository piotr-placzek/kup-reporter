import calendar
import datetime


class Date(object):
    @staticmethod
    def get_month_range(month, year):
        month_last_day = calendar.monthrange(year, month)[1]
        first_month_day = "{}-{}-01".format(year, month)
        last_month_day = "{}-{}-{}".format(year, month, month_last_day)
        return first_month_day, last_month_day

    @staticmethod
    def parse_date(date_string, date_time_format='%Y-%m-%dT%H:%M:%S.%f%z'):
        return datetime.datetime.strptime(date_string, date_time_format)

    @staticmethod
    def format_date_with_leading_zeros(day, month, year):
        day = '0{}'.format(day) if day < 10 else day
        month = '0{}'.format(month) if int(month) < 10 else month
        return '{}.{}.{}'.format(day, month, year)
