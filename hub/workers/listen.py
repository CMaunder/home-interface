import pika
import json
from pathlib import Path
from dotenv import load_dotenv
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



env_path = Path('.') / '.env.local'
load_dotenv(dotenv_path=env_path)

import os
import django

# Step 1: Set the environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "home_api.settings")

# Step 2: Initialize Django
django.setup()

# Step 3: Import your models
from monitoring.models import Location

# Example ORM operation
def list_objects():
    for obj in Location.objects.all():
        print(obj)

# if __name__ == "__main__":
print("listing objects")
list_objects()

QUEUE_NAME = 'measurements'

def listen():
    print('starting listener...')
    creds = pika.PlainCredentials(
            username=os.getenv("RABBITMQ_USER"), 
            password=os.getenv("RABBITMQ_PASSWORD")
        )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_SERVER"), credentials=creds))

    channel = connection.channel()
    q = channel.queue_declare(QUEUE_NAME, durable=True)

    def save_data(ch, method, properties, body):
        message = body.decode()
        print(message)
        data = json.loads(message)
        print(f"[x] message received:")
        print(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    print("In continuous mode, waiting for messages...")
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=save_data)
    channel.start_consuming()

listen()