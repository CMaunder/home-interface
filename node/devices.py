import pika
from time import sleep
import adafruit_dht
import board
import datetime
import json
from statistics import mean
from dotenv import load_dotenv
import os
import socket

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TEMPERATURE = "temperature"
HUMIDITY = "humidity"

class RabbitMQClient:
    def __init__(self, queue_name='measurements'):
        self.queue_name = queue_name
        creds = pika.PlainCredentials(username=os.getenv("RABBITMQ_USER"), password=os.getenv("RABBITMQ_PASSWORD"))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("RABBITMQ_SERVER"), credentials=creds))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def send(self, message):
        self.channel.basic_publish(exchange='',
                    routing_key=self.queue_name,
                    body=message,
                    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
                    )
        print(f"[x] message: {message} sent.")

class DHT11(RabbitMQClient):
    def __init__(self):
        self.device_name = "DHT11"
        self.hostname = socket.gethostname()
        super().__init__()


    def get_data_avg(self, readings=5):
        dht_device = adafruit_dht.DHT11(board.D4)
        temp_array = []
        humidity_array = []
        i = 0
        while i < readings:
            print(f"taking reading: {i+1}")
            try:
                temp_array.append(dht_device.temperature)
                humidity_array.append(dht_device.humidity)
            except RuntimeError as err:
                # TODO - add retry functionality here if err.args[0] == "Checksum did not validate. Try again.", or maybe retry for any RuntimeError, with limit
                print(err.args[0])
            i += 1
            if i < readings:
                sleep(3)
            else:
                dht_device.exit()
        if len(temp_array) == 0 or len(humidity_array) == 0:
            raise Exception(f"Temp or humidity failed to record after {readings} readings.")
        return {TEMPERATURE: mean(temp_array), 
                HUMIDITY: mean(humidity_array)}
    

    def _format_message(self, data, unit):
        assert unit is not None
        now = datetime.datetime.now()
        message = {"unit": unit, 
                "measure": data.get(unit),
                "recorded_at": str(now),
                "device": self.device_name,
                "hostname": self.hostname}
        return json.dumps(message)


    def capture(self):
        data = self.get_data_avg(readings=3)
        self.send(self._format_message(data, TEMPERATURE))
        self.send(self._format_message(data, HUMIDITY))
        self.close_connection()

if __name__ == '__main__':
    DHT11().capture()
