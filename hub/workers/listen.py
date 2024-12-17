import pika
import json
from pathlib import Path
from dotenv import load_dotenv
import os, sys, django, pytz
from datetime import datetime, timedelta, date
from rest_framework.exceptions import ValidationError
from pprint import pprint


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env_path = Path('.') / '.env.local'
load_dotenv(dotenv_path=env_path)

# Step 1: Set the environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "home_api.settings")

# Step 2: Initialize Django
django.setup()

# Step 3: Import your models
from monitoring.models import Location, Measurement, Unit, Device, Host, Light
from monitoring.serializers import MeasurementSerializer

QUEUE_NAME = 'measurements'

def add_mins_to_time(time, minutes):
   return (datetime.combine(date(1,1,1),time) + timedelta(minutes=minutes)).time()

def update_light(measurement):
    now = datetime.now()
    unit = Unit.objects.get(id=measurement["unit"].id)
    if unit and unit.name == "brightness":
        try:
            desk_light = Light.objects.get(id=1)

            if desk_light.auto_power_on_time and add_mins_to_time(desk_light.auto_power_on_time, 5) >= now.time() >= desk_light.auto_power_on_time:
                desk_light.power_on()
            if desk_light.auto_power_off_time and add_mins_to_time(desk_light.auto_power_off_time, 5) >= now.time() >= desk_light.auto_power_off_time:
                desk_light.power_off()

            brightness_recorded = float(measurement.get("measure"))
            if brightness_recorded < 50:
                desk_light.set_hsb({"saturation": 100-2*brightness_recorded})
            else:
                desk_light.set_hsb({"saturation": 1})
        except Exception as e:
            print("Something went wrong: ", e)

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
        try:
            message = body.decode()
            data = json.loads(message)
            pprint(f"[x] message received: {message}")
            unit = Unit.objects.get(name=data.get("unit"))
            host = Host.objects.get(ip_address=data.get("ip_address"))
            device = Device.objects.get(name=data.get("device"))
        except Exception as e:
            print(e)
            # ack bad message to remove it from the queue
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        try:
            recorded_at = datetime.strptime(data['recorded_at'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=pytz.utc)
            measurement = Measurement(measure=data.get("measure"), 
                                      recorded_at=recorded_at, 
                                      unit=unit, 
                                      device=device,
                                      host=host)
            serializer = MeasurementSerializer(measurement)
            serializer.validate_recorded_at(recorded_at)
            serializer.validate({"measure": measurement.measure, "unit":measurement.unit})
            update_light(measurement)
            measurement.save()
        except ValidationError as e:
            # ack invalid message to remove it from the queue
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(e)
            return
        print(f"[x] record saved: {measurement}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        

    print(f"In continuous mode, waiting for messages from {QUEUE_NAME}...")
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=save_data)
    channel.start_consuming()

listen()