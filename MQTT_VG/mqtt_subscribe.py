import paho.mqtt.client as paho
import random

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


def on_message(client, userdata, msg):
    if not msg.retain:
        payload = msg.payload.decode()
        print(f'{payload}')


def subscribe(client):
    username = int(input(f'User ID: '))
    client.subscribe(f'kyh/iChat/{username}')
    client.on_message = on_message


def main():
    client = connect_mqtt()
    subscribe(client)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()


if __name__ == '__main__':
    main()
