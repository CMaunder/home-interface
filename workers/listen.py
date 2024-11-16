import pika
import json
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path('.') / '.env.local'
load_dotenv(dotenv_path=env_path)


QUEUE_NAME = 'measurements'

def listen():
    print('starting listener')
    print(os.getenv("RABBITMQ_USER"))
    print(os.getenv("RABBITMQ_PASSWORD"))
    print(os.getenv("RABBITMQ_SERVER"))
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