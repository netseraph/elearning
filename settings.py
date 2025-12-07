"""配置"""

import logging
import os


def init_logging(level: int = 2):
    """初始化logging"""
    logging.getLogger("test")

    _level_list = (
        logging.NOTSET,
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    )
    _filename = f"{os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]}.log"
    _format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    if 0 <= level < len(_level_list):
        _l = level
    elif level < 0:
        _l = 0
    else:
        _l = len(_level_list) - 1

    _level = _level_list[_l]

    logging.basicConfig(
        filename=_filename, format=_format, level=_level, encoding="UTF-8"
    )
    