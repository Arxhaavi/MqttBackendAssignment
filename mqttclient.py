import random, time
from paho.mqtt import client as mqtt_client
import sqlite3

# Here we define the creation and connection of the database. If the database already exists it just connects
# to it and and closes the connection
def create_database():
    con = sqlite3.connect("Msg_database.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, message TEXT)")
    con.close()

# Information for the mqtt-client to connect to the broker and the topic we will later subscribe to
broker = 'broker.emqx.io'
port = 1883
topic = "charger/1/connector/1/session/1"
client_id = f'mqtt-test-{random.randint(0, 1000)}'

# Here we connect to the broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            # If the connection is successful you'll see this message
            print("Connected to MQTT Broker!")
        else:
            # If the connection does not succeed you will get this message with the error code
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID which we have randomized earlier
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# We define the publishing loop here. The first message is published 3 seconds after the application is run,
# and the next one and all the consequent ones one minute apart
def publish(client):
    msg_count = 1
    while True:
        time.sleep(3)
        msg = "Session_id:1, energy_delivered_in_kWh:30, duration:_in_seconds:45, session_cost_in_cents:70"
        result = client.publish(topic, msg)
        time.sleep(57)
        status = result[0]
        # If the message is not succesfully published, you get notified of it
        if status == 1:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        # I set a limit so that the application only sends up to 10 messages. 
        if msg_count > 10:
            break

# Here we define the topic the client subscribes to, and what happens when messages are received through the topic
def subscribe(client: mqtt_client):
    # When a message is received, the application prints the message that was received, then opens a connection
    # to the database that was created earlier and pushes the message payload to the database.
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
