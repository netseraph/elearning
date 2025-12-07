"""自定义模块"""

from typing import Tuple,Any
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

HMSType = Tuple[int, int, int]


def seconds_to_hms(duration: int) -> HMSType:
    """以秒为单位的时时长转换成时分秒"""
    hours, _remainder = divmod(duration, 3600)
    minutes, seconds = divmod(_remainder, 60)
    return (hours, minutes, seconds)


def show_handles(driver: Any, info: str = ""):
    """显示当前浏览器handle信息"""
    _handles = driver.window_handles
    print(f"现在共有{len(_handles)}个标签页,handles分别为:")
    for _h in _handles:
        print(f"    {_h}")
    print(f"当前标签页的句柄为:{driver.current_window_handle}")
    print(info)


def show_info(level: int, info: str):
    """格式化显示信息"""
    if level == 0:
        print(info)
    else:
        _space = "  " * level
        _message = f"{_space}└─── {info}"
        print(_message)
    logging.info(info)


def is_element_exist(previous: Any, element: str) -> bool:
    """判断元素是否存在"""
    try:
        previous.find_element(by=By.CLASS_NAME, value=element)
        return True
    except NoSuchElementException:
        return False
