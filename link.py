from linkkit import linkkit
import time
import json
# 连接阿里云

ProductKey = "a1bw1zXB8k4"  # 你的产品key
DeviceName = "Mi98"  # 你的设备名称
DeviceSecret = "290b3479cc2604418db6011596b7e9c8"  # 你的设备密码


def on_connect(session_flag, rc, userdata):
    print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
    pass
    # 取消连接阿里云


def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)


def on_subscribe_topic(mid, granted_qos, userdata):  # 订阅topic
    print("on_subscribe_topic mid:%d, granted_qos:%s" %
          (mid, str(','.join('%s' % it for it in granted_qos))))
    pass
    # 接收云端的数据


def on_topic_message(topic, payload, qos, userdata):
    # 设备端的接收到的数据却是b:"123"用了一个切片去处理数据
    print("阿里云上传回的数值是:", str(payload))
    # 拿到接收来的数据
    data = str(payload)[2:-1]
    print("阿里云上传回的数值是:", data)
    dataDict = json.loads(data)
    print("阿里云上传回的数值是:", type(dataDict))  # 切片左闭右开 取头不取尾
    # print(dataDict["jiang"])
    # 多层解析
    # {"temp":{"value":62}}
    print(dataDict["temp"]["value"])  # 解析多层数据

    pass
# 终止订阅云端数据


def on_unsubscribe_topic(mid, userdata):
    print("on_unsubscribe_topic mid:%d" % mid)
    pass
# 发布消息的结果，判断是否成功调用发布函数


def on_publish_topic(mid, userdata):
    print("on_publish_topic mid:%d" % mid)


# 设置连接参数，方法为“一机一密”型
lk = linkkit.LinkKit(
    host_name="cn-shanghai",  # 填自己的host_name
    product_key=ProductKey,  # 填自己的product_key
    device_name=DeviceName,  # 填自己的device_name
    device_secret=DeviceSecret)  # 填自己的device_secret
# 注册接收到云端数据的方法
lk.on_connect = on_connect
# 注册取消接收到云端数据的方法
lk.on_disconnect = on_disconnect
# 注册云端订阅的方法
lk.on_subscribe_topic = on_subscribe_topic
# 注册当接受到云端发送的数据的时候的方法
lk.on_topic_message = on_topic_message
# 注册向云端发布数据的时候顺便所调用的方法
lk.on_publish_topic = on_publish_topic
# 注册取消云端订阅的方法
lk.on_unsubscribe_topic = on_unsubscribe_topic

# 连接阿里云的函数（异步调用）
lk.connect_async()
time.sleep(2)
# 订阅主题
rc, mid = lk.subscribe_topic(lk.to_full_topic("user/get"))
# 发布主题

while True:
    data = {
        "id": "203302322",
        "version": "1.0",
        "params": {"Distance": 5.21, "Distance1": 5.21, "Distance2": 5.21, 'amp': 1, "temp": 1, "electricity": 3.99},
        "method": "thing.event.property.post"
    }

    rc, mid = lk.publish_topic(
        "/sys/a1bw1zXB8k4/Mi98/thing/event/property/post", str(data))

    time.sleep(18)
    pass
