import logging
import logging.handlers
import sys


class ServerLogger:
    _LOG_FORMATTER = "%(asctime)s %(levelname)s %(module)s -> %(message)s"
    _DATEFMT = "%Y.%m.%d %H:%M:%S"

    def __init__(self,
                 filename: str = 'server.log',
                 lvl: str = 'info',
                 consoled=False):
        self._FILENAME = filename
        self._LEVEL = self._getLevel(lvl)
        self.LOGGER = logging.getLogger('server')
        self.LOGGER.setLevel(self._LEVEL)

        file_logger = logging.handlers.TimedRotatingFileHandler(filename=filename,
                                                                interval=1,
                                                                when='D',
                                                                backupCount=5,
                                                                encoding='utf-8')
        file_logger.setLevel(self._LEVEL)
        file_logger.setFormatter(logging.Formatter(self._LOG_FORMATTER, datefmt=self._DATEFMT))
        self.LOGGER.addHandler(file_logger)

        # Логгер для консольного вывода
        if consoled:
            console_logger = logging.StreamHandler(sys.stderr)
            console_logger.setLevel(logging.DEBUG)
            self.LOGGER.addHandler(console_logger)

    def _getLevel(self, lvl: str):
        lvls = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        return lvls[lvl.lower()] if lvl.lower() in lvls else lvls['info']

    def setLevel(self, lvl: str = 'info') -> None:
        self.LOGGER.setLevel(self._getLevel(lvl))

    def log(self, msg: str = '', lvl: str = 'debug') -> None:
        self.LOGGER.log(self._getLevel(lvl), msg)
