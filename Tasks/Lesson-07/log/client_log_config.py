import logging
import sys


class ClientLogger:
    _LOG_FORMATTER = "%(asctime)s %(levelname)s %(module)s -> %(message)s"
    _DATEFMT = "%Y.%m.%d %H:%M:%S"

    def __init__(self,
                 filename: str = 'client.log',
                 lvl: str = 'info'):
        self._FILENAME = filename
        self._LEVEL = self._getLevel(lvl)
        self.LOGGER = logging.getLogger('client')
        self.LOGGER.setLevel(self._LEVEL)

        file_handler = logging.FileHandler(self._FILENAME)
        file_handler.setFormatter(logging.Formatter(self._LOG_FORMATTER, datefmt=self._DATEFMT))
        file_handler.setLevel(self._LEVEL)
        self.LOGGER.addHandler(file_handler)

        # Логгер для консольного вывода
        if lvl == 'debug':
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
