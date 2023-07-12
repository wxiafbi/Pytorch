'''
1、导入模块 threading 模块
2、创建线程类的对象
3、启动线程
'''
import threading
import time


def dance(name1):
    for i in range(5):
        print("%s在跳舞" % (name1), i)
        time.sleep(1)


def sing(name2):
    for i in range(8):
        print("%s在唱歌" % (name2), i)
        time.sleep(2)


Mytread1 = threading.Thread(target=dance, args=("小红",))
Mytread2 = threading.Thread(target=sing, args=("小明",))

Mytread1.start()
print('-------')
Mytread2.start()
