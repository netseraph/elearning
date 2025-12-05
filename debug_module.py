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


def show_handles(driver):
    """显示当前浏览器handle信息"""
    print(
        (
            f"当前窗口的句柄:{driver.current_window_handle},"
            f"所有窗口的句柄:{driver.window_handles}"
        )
    )
