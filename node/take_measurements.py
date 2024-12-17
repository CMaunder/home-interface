#!/home/charlie/scripts/venv/bin/python
from devices import DHT11, SoilProbe, LightSensor
from gpiozero import LED
import RPi.GPIO as GPIO

led = LED(27)

led.on()
SoilProbe().capture()
DHT11().capture()
LightSensor().capture()
GPIO.cleanup()
led.off()
