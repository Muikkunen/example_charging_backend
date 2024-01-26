FROM python:3.12.1

ADD mqtt_handler.py .
ADD config.py .

COPY requirements.txt .
RUN pip install -r requirements.txt

# Define environment variable
ENV MQTT_BROKER_ADDRESS="127.0.0.1"

CMD ["python", "./mqtt_handler.py"]