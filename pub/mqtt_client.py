import paho.mqtt.client as mqtt
import json
from time import sleep


def on_publish(topic, payload, qos):
    print("topic is now published")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


class MQTTclient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_publish = on_publish
        self.client.on_disconnect = on_disconnect

    def connect(self, port=1883):
        """
        interval = keep the connection open for this time default 60sec
        """
        self.client.connect("localhost", port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, pub):
        self.client.publish(topic, json.dumps(pub))
        sleep(1) # sleep for 1 second, let message publish

