"""电建e学自动学习"""

import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import ORIGIN_URL, SESSION_PATH_LIST, LESSON_SKIP_LIST, MPS
from settings import init_logging
from mymodule import show_info, seconds_to_hms


def auto_elearning_simple(browser):
    """简化版自动学习"""
    browser.implicitly_wait(60)

    _completion_mark = False

    while not _completion_mark:
        _completion_mark = True
        browser.refresh()
        # 定位课程列表
        print("定位课程列表")
        _ele_list_lessonlist = browser.find_elements(
            by=By.CLASS_NAME, value="lesson-list"
        )
        _course_count = len(_ele_list_lessonlist)
        show_info(0, f"此培训班共{_course_count}个课程")
        for i in range(_course_count):
            # _ele_lesson in _ele_list_lessonlist[i]:

            # 课程名称
            _ele_lesson_title = _ele_list_lessonlist[i].find_element(
                by=By.CLASS_NAME, value="title.ellipsis-2.tr.font16.link"
            )
            # 课程进度
            _ele_lesson_progress = _ele_list_lessonlist[i].find_element(
                by=By.CLASS_NAME, value="el-progress__text"
            )

            show_info(
                1,
                (
                    f"课程{i}: [{_ele_lesson_title.text}] 已完成: {_ele_lesson_progress.text}"
                ),
            )

            if _ele_lesson_progress.text != "100%" and i not in LESSON_SKIP_LIST:
                _completion_mark = False
                # 点击课程标题,在新的标签页打开未完成的课程.
                _ele_lesson_title.click()

                # 焦点切换到课程标签页
                _handles = browser.window_handles

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
                _chapterduration = int(_ele_chapterduration.text)

                # 定位进度信息
                _ele_progress = browser.find_element(
                    by=By.CLASS_NAME, value="jindu.el-row.el-row--flex"
                )
                _ele_learnd = _ele_progress.find_element(
                    by=By.CLASS_NAME, value="orange.font18"
                )
                _learnd = int(_ele_learnd.text)

                show_info(
                    2, f"本课程总时长为{_chapterduration}分钟,已累计学习{_learnd}分钟."
                )

                # 定位开始学习按钮
                _ele_start_btn = browser.find_element(
                    by=By.CLASS_NAME, value="el-button.el-button--warning"
                )
                # 点击开始学习按钮
                show_info(3, "开始学习")
                _ele_start_btn.click()

                # 打开视频标签页
                _handles_video = browser.window_handles

                # 焦点切换至视频播放标签页
                browser.switch_to.window(_handles_video[-1])

                # 显式等待,直到相关元素出现,最多等标签页待300秒.
                _browser_wait = WebDriverWait(browser, 300)

                # 等待[播放键]元素出现
                _playbutton = "vjs-play-control.vjs-control.vjs-button.vjs-paused"
                _browser_wait.until(
                    EC.visibility_of_element_located((By.CLASS_NAME, _playbutton))
                )
                # 定位播放按钮
                _ele_play = browser.find_element(by=By.CLASS_NAME, value=_playbutton)

                # 点击播放按钮,开始播放视频

                _ele_play.click()
                # 强制等待,直到视频播放完毕
                # 将分钟转换为秒
                _duration = (_chapterduration - _learnd) * MPS

                # 视频加载完成，开始播放。预计播放时长为 9028 秒（2 小时 30 分 28 秒），请耐心观看。
                _h, _m, _s = seconds_to_hms(duration=_duration)
                _message = f"视频加载完成，开始播放。预计播放时长为 {_duration} 秒（{_h} 小时 {_m} 分 {_s} 秒），请耐心观看。"
                show_info(3, _message)

                sleep(_duration)

                show_info(3, "视频播放结束.")
                # 关闭视频标签页

                browser.close()

                # 焦点切换回课程标签页
                browser.switch_to.window(_handles[1])

                # 关闭程标签页
                show_info(2, "关闭课程标签页")
                browser.close()

                # 焦点切换回培训班标签页
                browser.switch_to.window(_handles[0])
    show_info(0, "本培训班全部课程学完.")


if __name__ == "__main__":
    init_logging()
    show_info(0, "电建e学培训班开始自动学习")
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
        # print("本地文件夹找到chromedriver.exe,尝试使用本地driver")
        service = Service(driverath)
        driver = webdriver.Chrome(options=options, service=service)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_window_position(0, 0)
    driver.set_window_size(width=1500, height=1200)
    driver.implicitly_wait(60)

    # 打开登录网页
    driver.get(ORIGIN_URL)
    # 等待扫码登录,最长等待60秒
    driver_wait = WebDriverWait(driver, 60)

    # 等待[用户]元素出现,如果出现,意味登录成功.
    driver_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "crumbs1")))

    for session_path in SESSION_PATH_LIST:
        URL = f"{ORIGIN_URL}{session_path}"
        # 打开培训班
        driver.get(URL)
        driver.refresh()
        auto_elearning_simple(driver)

    driver.quit()
