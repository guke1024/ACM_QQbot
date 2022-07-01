import sys
import os
import time


class Logger(object):
    def __init__(self, filename="log.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding='utf-8')

    def write(self, message):
        if str(message).isspace() is False:
            self.terminal.write(str(message) + '\n')
            self.log.write(str(time.strftime('%Y-%m-%d %H:%M:%S\n', time.localtime())) + str(message) + '\n\n')
            self.log.flush()  # 缓冲区的内容及时更新到log文件中

    def flush(self):
        pass


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    sys.stdout = Logger()

    # 之后用print输出的就既在屏幕上，又在log文件里
    print(path)
