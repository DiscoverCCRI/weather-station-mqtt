import paho.mqtt.client as mqtt
import json
from time import sleep


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("data/receive")  # 订阅消息


def on_message(client, userdata, msg):
    print("Topic:" + msg.topic + " Message:" + str(msg.payload.decode('utf-8')))


def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)


def on_publish(topic, payload, qos):
    print("topic is now published")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


class MQTTclient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_subscribe = on_subscribe
        self.client.on_publish = on_publish
        self.client.on_disconnect = on_disconnect
        self.client.connect("localhost", 1883, 60)

    def publish(self, topic, pub):
        self.client.loop_start()
        self.client.publish(topic, json.dumps(pub))
        sleep(1)
        self.client.loop_stop()

    def subscribe(self, topic):
        self.client.loop_start()
        self.client.subscribe(topic)
        sleep(1)
        self.client.loop_stop()

# if __name__ == "__main__":
#     client = MQTTclient()
#     while True:
#         client.subsribe("test/message")
