"""
This module provides functionality for handling MQTT messages and interacting with a MongoDB database.
"""

import json
import sys
import time

from datetime import datetime
import paho.mqtt.client as mqtt
from pymongo import MongoClient

from config import PORT, TOPIC, USERNAME, PASSWORD, DATABASE_NAME, DATABASE_COLLECTION, broker_address, mongo_database_url

# Interval in seconds for publishing MQTT messages
MESSAGE_INTERVAL = 60

# Connect to MongoDB
database_client = MongoClient(
    mongo_database_url,
    username=USERNAME,
    password=PASSWORD,
)

# Create or switch to a specific database
db = database_client[DATABASE_NAME]

# Create or switch to a specific collection within the database
collection = db[DATABASE_COLLECTION]


def on_connect(client, userdata, flags, rc):
    """
    Handles the on_connect event of the MQTT client.

    Connects to the broker and subscribes to the specified topic upon successful connection.
    """
    if rc == 0:
        print("Connected to the broker")
        # Subscribe to the topic upon connection
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg):
    """
    Handles the on_message event of the MQTT client.

    Inserts the received message and into the MongoDB collection.
    """
    global collection
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    # Insert the data into the collection
    data = json.loads(msg.payload.decode())
    collection.insert_one(data)
    print("Added to database:", data)


def on_error(client, userdata, error):
    """
    Handles the on_error event of the MQTT client.

    Prints the error message when an error occurs during the MQTT operation.
    """
    print("An error occurred:", error)


def publish_message(client, msg: str) -> None:
    """
    Adds a timestamp to the specified message and publises it using provided MQTT client.
    """
    # Add timestamp to the data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg["timestamp"] = timestamp
    client.publish(TOPIC, json.dumps(msg))
    print(f"Published message to {TOPIC}")

# Create an MQTT client instance
mqtt_client = mqtt.Client()

# Set callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    # Connect to the broker
    mqtt_client.connect(broker_address, PORT, keepalive=60)
except ConnectionRefusedError as error:
    print(f"Cannot connect to the MQTT client. {error}")
    sys.exit(-1)

# Start the MQTT loop to handle communication in the background
mqtt_client.loop_start()

# Simulate publishing a message every 1 minute
try:
    time.sleep(0.1) # Ensure that connection has been established
    message = {
        "session_id": 1, "energy_delivered_in_kWh":30,
        "duration_in_seconds":45, "session_cost_in_cents": 70
    }
    while True:
        publish_message(mqtt_client, message)
        time.sleep(MESSAGE_INTERVAL)
except KeyboardInterrupt:
    # Disconnect on keyboard interrupt
    mqtt_client.disconnect()
    print("Disconnected from the broker")

    # Close the MongoDB connection
    database_client.close()
    print("Closed MongoDB connection")

