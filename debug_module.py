"""调试模块"""

import logging


def debuginfo(level, info):
    """格式化显示信息"""
    if level == 0:
        print(info)
    else:
        _space = "  " * level
        _message = f"{_space}└─── {info}"
        print(_message)
    logging.debug(info)


def show_handles(info, driver):
    """显示当前浏览器handle信息"""
    print(info)
    _handles = driver.window_handles
    print(f"现在共有{len(_handles)}个标签页,handles分别为:")
    for _h in _handles:
        print(f"    {_h}")
    print(f"当前标签页的句柄为:{driver.current_window_handle}")
