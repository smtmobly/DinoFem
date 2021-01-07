"""
继承的办法
因为，从封装1的那个py文件中可以看到，下面调用的函数都是继承的别的类，那么我们直接把那个类拿过来使用就可以了

"""

import logging


class LoggerHandler(logging.Logger):

    def __init__(self,
                 name = "root",
                 level = 'DEBUG',
                 file = "log.txt",
                 format = '%(levelname)s(%(lineno)s):%(message)s'
    ):

        # logger = logging.gerLogger(name)
        super().__init__(name)

        #logger = logging.getLogger(name)
        #设置级别
        self.setLevel(level)

        fmt = logging.Formatter(format)
        # 初始化处理器
        if file:
            file_handle = logging.FileHandler(file)
            file_handle.setLevel(level)

            self.addHandler(file_handle)
            file_handle.setFormatter(fmt)
        stream_handler = logging.StreamHandler()

        # 设置handle 的级别
        stream_handler.setLevel(level)

        self.addHandler(stream_handler)
        stream_handler.setFormatter(fmt)


logger = LoggerHandler()
if __name__ == '__main__':
    logger = LoggerHandler()
    logger.debug("hello world")
    logger.warning("错误")
