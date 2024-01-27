import json
import time

import paho.mqtt.client as mqtt
from pymongo import MongoClient

from config import BROKER_ADDRESS, PORT, TOPIC, USERNAME, PASSWORD, DATABASE_URL

# Connect to MongoDB
database_client = MongoClient(
    DATABASE_URL,
    username=USERNAME,
    password=PASSWORD,
)

# Create or switch to a specific database
db = database_client["mydatabase"]

# Create or switch to a specific collection within the database
collection = db["mycollection"]


# Callbacks for various MQTT events
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        # Subscribe to the topic upon connection
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code: {rc}")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    # Insert the data into the collection
    data = json.loads(msg.payload.decode())
    data["timestamp"] = msg.timestamp # Add timestamp to the data
    collection.insert_one(data)
    print("Added to database:", data)


def on_error(client, userdata, error):
    print("An error occurred:", error)


def publish_message(client, message: str) -> None:
    # Publish the message to the specified topic
    client.publish(TOPIC, json.dumps(message))
    print(f"Published message to {TOPIC}")

# Create an MQTT client instance
mqtt_client = mqtt.Client()

# Set callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    # Connect to the broker
    mqtt_client.connect(BROKER_ADDRESS, PORT, keepalive=60)

    # Start the MQTT loop to handle communication in the background
    mqtt_client.loop_start()

    # Simulate publishing a message every 2 seconds
    try:
        time.sleep(0.1) # Ensure that connection has been established
        message = {
            "session_id": 1, "energy_delivered_in_kWh":30,
            "duration_in_seconds":45, "session_cost_in_cents": 70
        }
        while True:
            publish_message(mqtt_client, message)
            time.sleep(2)
    except KeyboardInterrupt:
        # Disconnect on keyboard interrupt
        mqtt_client.disconnect()
        print("Disconnected from the broker")

        # Close the MongoDB connection
        database_client.close()
        print("Closed MongoDB connection")

except ConnectionRefusedError as error:
    print(f"{error}")
