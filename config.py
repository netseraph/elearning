"""参数"""

# 网址
ORIGIN_URL = "https://elearning.powerchina.cn"

# 需要完成的培训班列表
SESSION_PATH_LIST = (
    "/tms/index.html#/classesDetail?trainclassId=4222126803291984",
    "/tms/index.html#/classesDetail?trainclassId=1688870266388618",
)
# 需暂时跳过的课程
LESSON_SKIP_LIST = (-1,)

MPS = 61  # 每分钟按61秒转换,适当增加延时,保证视频播放完成.
