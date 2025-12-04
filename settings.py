"""常用参数"""

import logging
import os

__FILENAME = f"{os.path.split(os.getcwd())[-1]}.log"
__FORMAT = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
__LEVEL = logging.DEBUG
logging.basicConfig(
    filename=__FILENAME, format=__FORMAT, level=__LEVEL, encoding="UTF-8"
)

# 网址
ORIGIN_URL = "https://elearning.powerchina.cn"

# 需要完成的培训班列表
SESSION_PATH_LIST = (
    "/tms/index.html#/classesDetail?trainclassId=4222126803291984",
    "/tms/index.html#/classesDetail?trainclassId=1688870266388618",
)
