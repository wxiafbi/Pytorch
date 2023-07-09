import threading
from apps.mqtt import views

# 启用多线程 运行脱机主控模块
thread_mqtt_run = threading.Thread(target=views.mqtt_run)
thread_mqtt_run.start()
