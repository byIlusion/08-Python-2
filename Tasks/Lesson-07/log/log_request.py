import logging
import inspect
from functools import wraps


def log(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        LOG_FORMATTER = "%(asctime)s | %(message)s"
        DATEFMT = "%Y.%m.%d %H:%M:%S"

        request_handler = logging.FileHandler('log/requests.log', encoding='utf-8')
        request_handler.setFormatter(logging.Formatter(LOG_FORMATTER, datefmt=DATEFMT))

        logger = logging.getLogger('requests')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(request_handler)

        # f_names = [func.__name__]
        # frame = inspect.currentframe()
        # current_f_name = frame.f_code.co_name
        # i = 0
        # while frame.f_code.co_name != '<module>' and i < 10:
        #     i += 1
        #     if frame.f_code.co_name != current_f_name:
        #         f_names.append(frame.f_code.co_name)
        #     frame = frame.f_back
        # f_names.reverse()
        # MSG = f'func: {" -> ".join(f_names)}, args: {args}, kwargs: {kwargs}'

        frames = inspect.stack()
        current_f_name = inspect.currentframe().f_code.co_name
        f_names = []
        for frame in frames:
            if frame.function != current_f_name and frame.function != '<module>':
                f_names.append(frame.function)

        called_function = f' вызвана из функции {f_names[0]}()' if len(f_names) > 0 else ''
        MSG = f'Функция: {func.__name__}(){called_function}, args: {args}, kwargs: {kwargs}'
        logger.log(logging.DEBUG, MSG)

        return func(*args, **kwargs)
    return wrap
