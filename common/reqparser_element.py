import time

import datetime

import config


class DateTime(object):
    def __new__(cls, source):
        if isinstance(source, long):
            if len(str(source)) > 10:
                source = int(str(source)[:10])
            timestamp = time.localtime(source)
            format_print = time.strftime(config.DATETIME_FORMAT, timestamp)
            return datetime.datetime.strptime(format_print, config.DATETIME_FORMAT)
        elif isinstance(source, int):
            if len(str(source)) > 10:
                source = int(str(source)[:10])
            timestamp = time.localtime(source)
            format_print = time.strftime(config.DATETIME_FORMAT, timestamp)
            return datetime.datetime.strptime(format_print,
                                              config.DATETIME_FORMAT)
        elif isinstance(source, unicode):
            return datetime.datetime.strptime(source, config.DATETIME_FORMAT)
