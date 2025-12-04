"""电建e学自动学习"""

# 2025.11.29修改
import logging
import os
from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import settings as SET


def debuginfo(level, info):
    """格式化显示信息"""
    if level == 0:
        print(info)
    else:
        _space = "  " * level
        _message = f"{_space}└─── {info}"
        print(_message)
    logging.debug(info)


def is_element_exist(previous, element):
    """判断元素是否存在"""
    try:
        previous.find_element(by=By.CLASS_NAME, value=element)
        return True
    except NoSuchElementException:
        return False


def auto_elearning(browser):
    """自动学习"""

    # 定位课程列表
    print("# 定位课程列表")
    _ele_list_lessonlist = browser.find_elements(by=By.CLASS_NAME, value="lesson-list")

    for _ele_lesson in _ele_list_lessonlist:
        # 课程名称
        _ele_lesson_title = _ele_lesson.find_element(
            by=By.CLASS_NAME, value="title.ellipsis-2.tr.font16.link"
        )
        # 课程进度
        _ele_lesson_progress = _ele_lesson.find_element(
            by=By.CLASS_NAME, value="el-progress__text"
        )
        _message = (
            f"课程: [{_ele_lesson_title.text}] 已完成: {_ele_lesson_progress.text}"
        )
        debuginfo(0, _message)

        if _ele_lesson_progress.text != "100%":
            # 打开未完成的课程
            _ele_lesson_title.click()
            # 焦点切换到课程标签页
            _handles = browser.window_handles
            _message = f"当前窗口的句柄:{browser.current_window_handle},所有窗口的句柄:{_handles}"
            debuginfo(0, _message)
            browser.switch_to.window(_handles[1])

            # 定位视频列表
            ele_list_videolist = browser.find_elements(
                by=By.CLASS_NAME, value="list.el-row.is-align-middle.el-row--flex"
            )
            _message = f"本课程共有{len(ele_list_videolist)}个视频"
            debuginfo(1, _message)

            for ele_video in ele_list_videolist:
                _ele_video_title = ele_video.find_element(
                    by=By.CLASS_NAME, value="ellipsis.el-col.el-col-20"
                )
                ele_video_duration = ele_video.find_element(
                    by=By.CLASS_NAME, value="gray.el-col.el-col-3"
                )
                split = ele_video_duration.text.split(":")
                _duration = 0
                for item in split:
                    _duration = _duration * 60 + int(item)
                _message = f"视频: [{_ele_video_title.text}] 时长: {_duration}秒"
                debuginfo(2, _message)

                # 如果找到已完成标记,说明视频播放完整
                if is_element_exist(
                    ele_video, "iconfont.icon-yiwancheng1.orange.font20"
                ):
                    debuginfo(3, "此视频已完整播放")
                else:
                    debuginfo(3, "此视频未完成播放")

                    # 点击视频链接,打开视频播放标签页
                    _ele_video_title.click()
                    _handles_video = browser.window_handles
                    # 焦点切换至视频播放标签页
                    browser.switch_to.window(_handles_video[-1])

                    # 显式等待,直到相关元素出现,最多等待120秒.
                    browser_wait = WebDriverWait(browser, 120)
                    # 等待[播放键]元素出现
                    _playbutton = "vjs-play-control.vjs-control.vjs-button.vjs-paused"
                    browser_wait.until(
                        EC.visibility_of_element_located((By.CLASS_NAME, _playbutton))
                    )
                    # 定位播放按钮
                    _ele_play = browser.find_element(
                        by=By.CLASS_NAME, value=_playbutton
                    )
                    # 点击播放按钮,开始播放视频

                    debuginfo(3, "视频加载完毕开始播放.")
                    _ele_play.click()
                    # 强制等待,直到视频播放完毕
                    _message = f"延时{_duration+5}秒,以便完整播放视频."
                    debuginfo(3, _message)

                    sleep(_duration + 5)

                    _message = (
                        f"当前窗口的句柄:{browser.current_window_handle},"
                        "所有窗口的句柄:{_handles_video}"
                    )
                    debuginfo(3, _message)

                    # 关闭视频标签页
                    debuginfo(3, "关闭视频标签页")
                    browser.close()

                    # 焦点切换回课程标签页
                    browser.switch_to.window(_handles[1])

                    # browser.refresh()
                    # 关闭课程标签页
                    debuginfo(2, "关闭课程标签页")
                    browser.close()

                    # 焦点切换回培训班标签页
                    browser.switch_to.window(_handles[0])
                    # browser.refresh()

    sleep(3)
    browser.close()


def auto_elearning_simple(browser):
    """简化版自动学习"""

    # 定位课程列表
    print("# 定位课程列表")
    sleep(10)
    _ele_list_lessonlist = browser.find_elements(by=By.CLASS_NAME, value="lesson-list")

    for _ele_lesson in _ele_list_lessonlist:
        # 课程名称
        _ele_lesson_title = _ele_lesson.find_element(
            by=By.CLASS_NAME, value="title.ellipsis-2.tr.font16.link"
        )
        # 课程进度
        _ele_lesson_progress = _ele_lesson.find_element(
            by=By.CLASS_NAME, value="el-progress__text"
        )
        _message = (
            f"课程: [{_ele_lesson_title.text}] 已完成: {_ele_lesson_progress.text}"
        )
        debuginfo(0, _message)

        if _ele_lesson_progress.text != "100%":
            # 点击课程标题,在新的标签页打开未完成的课程.
            _ele_lesson_title.click()

            # 焦点切换到课程标签页
            _handles = browser.window_handles
            # _message = f"当前窗口的句柄:{browser.current_window_handle},所有窗口的句柄:{_handles}"
            # debuginfo(0, _message)
            browser.switch_to.window(_handles[1])

            sleep(10)  # 强制延时,等待网页加载.

            # 定位课程信息
            _ele_statistical = browser.find_element(
                by=By.CLASS_NAME, value="list-unstyled.statistical"
            )
            _ele_li = _ele_statistical.find_elements(by=By.TAG_NAME, value="li")
            # print(f"定位到的课程信息元素{len(_ele_li)}个子元素")

            # 定位课程时长
            _ele_chapterduration = _ele_li[0].find_element(
                by=By.CLASS_NAME, value="num"
            )
            # print(_ele_chapterduration)
            _chapterduration = _ele_chapterduration.text

            # 定位进度信息
            _ele_progress = browser.find_element(
                by=By.CLASS_NAME, value="jindu.el-row.el-row--flex"
            )
            _ele_learnd = _ele_progress.find_element(
                by=By.CLASS_NAME, value="orange.font18"
            )
            _learnd = _ele_learnd.text

            _message = f"本课程总时长为{_chapterduration}分钟,已累计学习{_learnd}分钟."
            debuginfo(1, _message)

            # 定位开始学习按钮
            _ele_start_btn = browser.find_element(
                by=By.CLASS_NAME, value="el-button.el-button--warning"
            )
            # 点击开始学习按钮
            _ele_start_btn.click()

            _handles_video = browser.window_handles
            # _message = f"当前窗口的句柄:{browser.current_window_handle},所有窗口的句柄:{_handles_video}."
            # debuginfo(1, _message)
            # 焦点切换至视频播放标签页
            browser.switch_to.window(_handles_video[-1])

            # 显式等待,直到相关元素出现,最多等待120秒.
            _browser_wait = WebDriverWait(browser, 120)
            # 等待[播放键]元素出现
            _playbutton = "vjs-play-control.vjs-control.vjs-button.vjs-paused"
            _browser_wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, _playbutton))
            )
            # 定位播放按钮
            _ele_play = browser.find_element(by=By.CLASS_NAME, value=_playbutton)
            # 点击播放按钮,开始播放视频
            debuginfo(2, "视频加载完毕开始播放.")
            _ele_play.click()
            # 强制等待,直到视频播放完毕
            _duration = (
                int(_chapterduration) - int(_learnd)
            ) * 61  # 每分钟按61秒计算,适当增加冗余
            _message = f"延时{_duration}秒({datetime.timedelta(seconds=_duration)}),以便完整播放视频."
            debuginfo(2, _message)
            sleep(_duration)

            _message = (
                f"当前窗口的句柄:{browser.current_window_handle},"
                "所有窗口的句柄:{_handles_video}"
            )
            debuginfo(3, _message)

            # 关闭视频标签页
            debuginfo(3, "关闭视频标签页")
            browser.close()

            # 焦点切换回课程标签页
            browser.switch_to.window(_handles[1])
            # 关闭课程标签页
            browser.close()

            # 焦点切换回培训班标签页
            browser.switch_to.window(_handles[0])
            browser.refresh()


if __name__ == "__main__":
    # 使用Chrome浏览器
    options = webdriver.ChromeOptions()
    # 实现了规避监测,禁止打印日志
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    # 静音
    options.add_argument("--mute-audio")

    driverath = f"{os.getcwd()}/chromedriver.exe"
    print(driverath)
    if os.path.exists(driverath):
        print("本地文件夹找到chromedriver.exe,尝试使用本地driver")
        service = Service(driverath)
        driver = webdriver.Chrome(options=options, service=service)
    else:
        driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.implicitly_wait(60)

    # 打开登录网页
    driver.get(SET.ORIGIN_URL)
    # 等待扫码登录,最长等待60秒
    driver_wait = WebDriverWait(driver, 300)

    # 等待[用户]元素出现,如果出现,意味登录成功.
    driver_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "crumbs1")))

    for session_path in SET.SESSION_PATH_LIST:
        URL = f"{SET.ORIGIN_URL}{session_path}"
        # 打开培训班
        driver.get(URL)
        auto_elearning_simple(driver)

    driver.quit()
