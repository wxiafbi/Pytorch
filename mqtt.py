import time
import paho.mqtt.client as mqtt

# 连接参数
aliyun_host = "a1bw1zXB8k4.iot-as-mqtt.cn-shanghai.aliyuncs.com"  # 阿里云物联网平台的主机名
aliyun_port = 1883  # MQTT协议的默认端口
aliyun_username = "Mi98"  # 阿里云物联网平台的用户名
aliyun_password = "290b3479cc2604418db6011596b7e9c8"  # 阿里云物联网平台的密码
topic = "your-topic"  # 发布消息的主题

# 连接回调函数
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Aliyun IoT Platform!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code: ", rc)

# 发布消息回调函数
def on_publish(client, userdata, mid):
    print("Message published")

# 创建MQTT客户端
client = mqtt.Client(client_id="your-client-id")  # 可以自定义客户端ID
client.username_pw_set(aliyun_username, aliyun_password)
client.on_connect = on_connect
client.on_publish = on_publish

# 连接到阿里云物联网平台
print(1)
client.connect(aliyun_host, aliyun_port, 60)

# 发送数据
message = "Hello, World!"  # 要发送的消息
client.publish(topic, message)

# 等待消息发送完成
time.sleep(1)

# 断开连接
client.disconnect()
