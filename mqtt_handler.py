import paho.mqtt.client as mqtt

import json
import time

from config import BROKER_ADDRESS, PORT, TOPIC


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

# TODO: Add on_error!

# Create an MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER_ADDRESS, PORT, keepalive=60)

# Start the MQTT loop to handle communication in the background
client.loop_start()

# Simulate publishing a message every 2 seconds
try:
    time.sleep(0.1)
    while True:
        message = {
            "session_id": 1, "energy_delivered_in_kWh":30,
            "duration_in_seconds":45, "session_cost_in_cents": 70
        }
        
        # Publish the message to the specified topic
        client.publish(TOPIC, json.dumps(message))
        print(f"Published message to {TOPIC}")
        time.sleep(2)
except KeyboardInterrupt:
    # Disconnect on keyboard interrupt
    client.disconnect()
    print("Disconnected from the broker")
