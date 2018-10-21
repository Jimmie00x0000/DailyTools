import sys
import os
import time
import datetime
from pathlib import Path


class Logger(object):

    INFO = 1
    DEBUG = 2
    WARNING = 3
    ERROR = 4
    LEVEL_TEXT = ['?', 'INFO', 'DEBUG', 'WARNING', 'ERROR', '?']

    def __init__(self, log_dir):
        dt = datetime.datetime.now()
        log_file_name = '%4d-%02d-%02d-%02d-%02d-%2d.log' % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        if not log_dir.exists():
            log_dir.mkdir()
        self.log_file_path = os.path.join(log_dir, log_file_name)
        pass

    def log(self, level, msg):
        text = '%s [%s]: %s' % (time.asctime(), Logger.LEVEL_TEXT[level], msg)
        if getattr(sys, 'frozen', False):
            # info 级别的 log 被忽略
            if level >= Logger.DEBUG:
                file_handler = open(self.log_file_path, 'a+')
                file_handler.write(text + '\n')
                file_handler.close()
                pass
            pass
        else:
            print(text)
            pass

    def info(self, msg):
        Logger.log(self, Logger.INFO, msg)
        pass

    def warn(self, msg):
        Logger.log(self, Logger.WARNING, msg)
        pass

    def debug(self, msg):
        Logger.log(self, Logger.DEBUG, msg)
        pass

    def error(self, msg):
        Logger.log(self, Logger.ERROR, msg)
        pass


if __name__ == '__main__':
    _logger = Logger(Path.home())
    _logger.debug('测试一下。')
    pass
