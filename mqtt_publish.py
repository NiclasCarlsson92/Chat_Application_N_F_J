import paho.mqtt.client as paho
import random
import time

CLIENT_ID = f'kyh-mqtt-{random.randint(0, 1000)}'
USERNAME = 'kyh_1'
PASSWORD = 'kyh1super2'
BROKER = '104.248.47.103'
PORT = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT Broker')
    else:
        print(f'Failed to connect to Broker. Error code {rc}')


def connect_mqtt():
    client = paho.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)

    return client


def publish(user_id, sender_email):
    client = connect_mqtt()
    client.loop_start()
    message = f'You have new messages from {sender_email}'
    client.publish(f'kyh/iChat/{user_id}', message)
    time.sleep(1)
    client.loop_stop()
