import logging
import sys


class ClientLogger:
    _LOG_FORMATTER = "%(asctime)s %(levelname)s %(module)s -> %(message)s"
    _DATEFMT = "%Y.%m.%d %H:%M:%S"

    def __init__(self,
                 filename: str = 'client.log',
                 lvl: str = 'info',
                 conslog: bool = True):
        self._FILENAME = filename
        self._LEVEL = self._getLevel(lvl)
        logging.basicConfig(
            filename=self._FILENAME,
            format=self._LOG_FORMATTER,
            level=self._LEVEL,
            datefmt=self._DATEFMT
        )
        self.LOGGER = logging.getLogger('server')
        if conslog:
            CONSOLE_LOGGER = logging.StreamHandler(sys.stderr)
            CONSOLE_LOGGER.setLevel(logging.ERROR)
            self.LOGGER.addHandler(CONSOLE_LOGGER)

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
