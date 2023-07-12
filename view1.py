import json
import logging
import sys
import threading
import time

from linkkit import linkkit

logger = logging.getLogger('django')

# 来自一机一密的设备
options = {"ProductKey": "a1bw1zXB8k4",
           "DeviceName": "Mi98",
           "DeviceSecret": "290b3479cc2604418db6011596b7e9c8"
           }
options1 = {"ProductKey": "a1bw1zXB8k4",
            "DeviceName": "Mi90",
            "DeviceSecret": "fcb727b358187a7ad8ba2e227561cca4"
            }
options2 = {"ProductKey": "a1bw1zXB8k4",
            "DeviceName": "Mi175",
            "DeviceSecret": "93546702e8522310c861000afc965779"
            }
options3 = {"ProductKey": "a1bw1zXB8k4",
            "DeviceName": "Mi96",
            "DeviceSecret": "fd8cecfb378836304cc48c26f7bb677a"
            }

# 示例代码配置设备的设备证书以及连接的公共示例的RegionID
lk = linkkit.LinkKit(
    host_name="cn-shanghai",  # 华东2（上海），根据自己的RegionID
    product_key=options["ProductKey"],
    device_name=options["DeviceName"],
    device_secret=options["DeviceSecret"])


def sanyuanzu(p_k: str, d_n: str, d_s: str):
    PASS_WORD = linkkit.LinkKit(
        host_name="cn-shanghai",  # 华东2（上海），根据自己的RegionID
        product_key=options["ProductKey"],
        device_name=options["DeviceName"],
        device_secret=options["DeviceSecret"])
    return PASS_WORD





def on_connect(session_flag, rc, userdata):
    """
    callback after connect_async
    :param session_flag: type:int description:is previous connect session,0 new session; 1 previous session
    :param rc: type:int rc的值决定了连接成功或者不成功:
    :param userdata: type:  description:same as LinkKit input parameter user_data
    """
    print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
    if rc == 0:
        # 连接成功
        print("Connection successful")
    elif rc == 1:
        # 协议版本错误
        print("Protocol version error")
    elif rc == 2:
        # 无效的客户端标识
        print("Invalid client identity")
    elif rc == 3:
        # 服务器无法使用
        print("server unavailable")
    elif rc == 4:
        # 错误的用户名或密码
        print("Wrong user name or password")
    elif rc == 5:
        # 未经授权
        print("unaccredited")
    print("Connect with the result code " + str(rc))


def on_disconnect(rc, userdata):
    """
    callback after connection disconnect
    :param rc: type:int description:0 success call for disconnect,1 network error
    :param userdata: type: description:same as LinkKit input parameter user_data
    """
    print("on_disconnect:rc:%d,userdata:" % rc)
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


def on_topic_message(topic, payload, qos, userdata):
    """
    callback after subscribe_topic call
    :param topic: 订阅的主题
    :param payload: 内容
    :param qos: 质量服务等级
    :param userdata:
    """
    print("on_topic_message:" + topic + " payload:" +
          str(payload) + " qos:" + str(qos))
    json_msg = json.loads(payload.decode('utf-8'))  # 一般为json数据
    try:
        # 接收到消息后的业务逻辑,同时处理多任务亦可以采用异步、线程池等
        pass
    except Exception as e:
        print('No this moType', e)


def on_subscribe_topic(mid, granted_qos, userdata):
    """
    callback after subscribe_topic call
    :param mid: type: int description:publish message id
    :param granted_qos: type:list(int) description: corresponding to subscribe_topic parameter topic,0 represent qos=0,1 represent qos=1,128 represent subscribe error
    :param userdata: type: description:same as LinkKit input parameter user_data
    """
    print("on_subscribe_topic mid:%d, granted_qos:%s" %
          (mid, str(','.join('%s' % it for it in granted_qos))))
    print(granted_qos)
    if granted_qos == 128:
        print("订阅失败")


def on_unsubscribe_topic(mid, userdata):
    """
    callback after unsubscribe topic
    :param mid: type: int description:publish message id
    :param userdata: type: description:same as LinkKit input parameter user_data
    """
    print("on_unsubscribe_topic mid:%d" % mid)
    pass


def on_publish_topic(mid, userdata):
    """
    callback after publish_topic call
    :param mid: type: int description:publish message id
    :param userdata: type: description:same as LinkKit input parameter user_data
    """
    print("on_publish_topic mid:%d" % mid)


# mqtt发布启动函数
def mqtt_publish(sensor_data, topic='defult', qos=0):
    try:
        rc, mid = lk.publish_topic(
            lk.to_full_topic("user/update"), sensor_data)
        print("mqtt_publish:已启动...", "user/update", sensor_data)
        return
    except KeyboardInterrupt:
        print("EXIT")
        # 这是网络循环的阻塞形式，直到客户端调用disconnect（）时才会返回。它会自动处理重新连接。
        lk.on_disconnect()
        sys.exit(0)


# 启动函数
def mqtt_run(lk):
    a = 0
    topic='/sys/'+options["ProductKey"]+'/'+options["DeviceName"]+'/thing/event/property/post'
    # 账号密码验证放到最前面
    # client.username_pw_set('user', 'user')
    # client = mqtt.Client()
    # 建立mqtt连接
    # 注册接收到云端数据的方法
    lk.on_connect = on_connect
    # 注册取消接收到云端数据的方法
    lk.on_disconnect = on_disconnect
    # 如果产品生产时错误地将一个三元组烧写到了多个设备，多个设备将会被物联网平台认为是同一个设备，
    # 从而出现一个设备上线将另外一个设备的连接断开的情况。用户可以将自己的接口信息上传到云端，那么云端可以通过接口的信息来进行问题定位。
    lk.config_device_info("Eth|03ACDEFF0032|Eth|03ACDEFF0031")
    # 企业实例域名配置的更改
    lk.config_mqtt(secure="", endpoint="iot-060a085o.mqtt.iothub.aliyuncs.com")
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
    # 因为他是他是异步调用需要时间所以如果没有这个延时函数的话，他就会出现not in connected state的错误
    time.sleep(2)
    # 订阅这个topic，不需要写prodect_key和device_name
    rc, mid = lk.subscribe_topic(lk.to_full_topic("user/get"))
    while a < 5:
        data = {
            "id": "203302322",
            "version": "1.0",
            "params": {"Distance": 50.21, "Distance1": 50.21, "Distance2": 50.21, 'amp': 1, "temp": 1, "electricity": 3.99, 'L': 50, 'valu': 121.19},
            "method": "thing.event.property.post"
        }

        # rc, mid = lk.publish_topic(
        #     "/sys/a1bw1zXB8k4/Mi175/thing/event/property/post", str(data))
        rc, mid = lk.publish_topic(topic, str(data))

        time.sleep(10)
        a = a+1


mqtt_run(sanyuanzu(options["ProductKey"],options["DeviceName"],options["DeviceSecret"]))
