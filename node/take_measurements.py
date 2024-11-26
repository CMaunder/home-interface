#!/home/charlie/scripts/venv/bin/python
from devices import DHT11, SoilProbe
from gpiozero import LED

led = LED(27)

led.on()
SoilProbe().capture()
DHT11().capture()
led.off()