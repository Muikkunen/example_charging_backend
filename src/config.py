"""
This module provides configuration settings for the application.
"""

import os

# MQTT broker details
MQTT_BROKER_ADDRESS_DEFAULT = "127.0.0.1" # This is used to run script locally
PORT = 1883
TOPIC = "charger/1/connector/1/session/1"

# MongoDB configurations
USERNAME = "your_username"
PASSWORD = "your_password"
DATABASE_URL_DEFAULT = "mongodb://localhost:27017/" # This is used to run script locally
DATABASE_PORT_DEFAULT = "8000"
DATABASE_NAME = "mydatabase"
DATABASE_COLLECTION = "mycollection"

# Enable executing scripts without docker (after launching mqtt broker and database)
broker_address = os.getenv("MQTT_BROKER_ADDRESS", MQTT_BROKER_ADDRESS_DEFAULT)
mongo_database_url = os.getenv("DATABASE_URL", DATABASE_URL_DEFAULT)
mongo_port = os.getenv("DATABASE_PORT", DATABASE_PORT_DEFAULT)