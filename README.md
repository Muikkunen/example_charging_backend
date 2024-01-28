# example_charging_backend
Example application showing how a a backend of a charging station could be implemented using MQTT, FastAPI, MongoDB and Docker.

# Requirements
This application requires Docker Compose (and Docker). Installation instructions can be found from: [Overview of installing Docker Compose](https://docs.docker.com/compose/install/).

# How to run
Start application (docker containers):
```shell
docker compose up --build
```

Fetch data:
```
curl http://localhost:8000/measurements/all
```

Or view data in a browser:
http://localhost:8000/docs#/default/get_measurements_measurements_all_get

And then 
Click on "Get" -> "Try it out" -> "Execute"