# Generated by Django 4.2.16 on 2024-11-25 20:30

from django.db import migrations

def populate_initial_data(apps, schema_editor):
    Unit = apps.get_model('monitoring', 'Unit')
    Host = apps.get_model('monitoring', 'Host')
    Device = apps.get_model('monitoring', 'Device')
    Location = apps.get_model('monitoring', 'Location')

    charlie_office = Location.objects.create(name='charlie_office', description='Small')
    living_room = Location.objects.create(name='living_room', description='Large')
    Host.objects.create(hostname="raspberrypi", description="raspberry pi 5, 4gb" ,ip_address="192.168.1.70", location=charlie_office)
    pizero = Host.objects.create(hostname="pizero", description="raspberry pi zero 2w", ip_address="192.168.1.71", location=living_room)
    Device.objects.create(name="DHT11", 
                                  description="Temperature & Humidity Sensor features a temperature & humidity sensor complex with a calibrated digital signal output.")
    
    Unit.objects.create(name="temperature", dimension="Celcius")
    Unit.objects.create(name="humidity", dimension="percent")
    Unit.objects.create(name="soil_hydrated", dimension="boolean")

    

class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data)
    ]
