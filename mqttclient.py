import random, time
from paho.mqtt import client as mqtt_client
import sqlite3

def create_database():
    con = sqlite3.connect("Msg_database.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, message TEXT)")
    con.close()

broker = 'broker.emqx.io'
port = 1883
topic = "charger/1/connector/1/session/1"
client_id = f'mqtt-test-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(3)
        msg = "Session_id:1, energy_delivered_in_kWh:30, duration:_in_seconds:45, session_cost_in_cents:70"
        result = client.publish(topic, msg)
        time.sleep(57)
        status = result[0]
        if status == 1:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 10:
            break


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received message: `{msg.payload.decode()}` from the topic: `{msg.topic}`")
        received_message = msg.payload.decode()
        con = sqlite3.connect("Msg_database.db", check_same_thread=False)
        cursor = con.cursor()
        cursor.execute("INSERT INTO messages VALUES (?, ?)", (None, received_message))
        con.commit()
        con.close()
    client.subscribe("charger/1/connector/1/session/1", qos=1)
    client.on_message = on_message


def run():
    create_database()
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
