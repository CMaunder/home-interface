#!/home/charlie/scripts/venv/bin/python
from devices import DHT11, SoilProbe, LightSensor
from gpiozero import LED
import RPi.GPIO as GPIO
from time import sleep

led = LED(27)

led.on()
SoilProbe().capture()
DHT11().capture()
led.off()
sleep(0.1)
LightSensor().capture()
GPIO.cleanup()

