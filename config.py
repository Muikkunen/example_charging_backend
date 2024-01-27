# MQTT broker details
#BROKER_ADDRESS = "mqtt.eclipse.org" # Seems that this might now work on Linux
BROKER_ADDRESS = "172.100.10.10" # Use this for docker
#BROKER_ADDRESS = "127.0.0.1" # Use this to run script locally
PORT = 1883
TOPIC = "charger/1/connector/1/session/1"

# TODO: Move these elsewhere
# MongoDB configurations
USERNAME = "your_username"
PASSWORD = "your_password"
DATABASE_URL = "mongodb://172.100.10.12:27017/"
#DATABASE_URL = "mongodb://localhost:27017/"
