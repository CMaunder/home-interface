from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.exceptions import ValidationError
from lifxlan import Light as LifxLight
from lifxlan.errors import WorkflowException

class Unit(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, null=True)
	dimension = models.CharField(max_length=200)

	def __str__(self):
		return f"{self.name} - {self.dimension}"

class Location(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, null=True)

	def __str__(self):
		return self.name

class Host(models.Model):
	hostname = models.CharField(max_length=200)
	ip_address = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=2000, null=True)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.hostname} - {self.ip_address}"

class Device(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, null=True)

	def __str__(self):
		return f"{self.name}"

class Measurement(models.Model):
	measure = models.DecimalField(decimal_places=4, max_digits=15)
	inserted_at = models.DateTimeField(auto_now_add=True)
	recorded_at = models.DateTimeField()
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	device = models.ForeignKey(Device, on_delete=models.CASCADE)
	host = models.ForeignKey(Host, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.measure} {self.unit.dimension} - {self.device.name} : {datetime.strftime(self.recorded_at, '%Y-%m-%d %H:%M:%S')}"

class Light(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=2000, null=True)
	ip_address = models.CharField(max_length=200, unique=True)
	mac_address = models.CharField(max_length=200, unique=True)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	transition_time = models.IntegerField(null=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.light = LifxLight(self.mac_address, self.ip_address)
		if not self.transition_time:
			self.transition_time = 1000

	def __str__(self):
		return f"{self.name}"
	
	def power_on(self):
		self.light.set_power("on", duration=self.transition_time)

	def power_off(self):
		self.light.set_power('off', duration=self.transition_time)

	def set_hsb(self, hsb_request):
		prev_hue, prev_sat, prev_brightness, prev_temp =self.light.get_color()
		hsb_request["hue"] = self._to_16_bit(hsb_request["hue"], 360) if hsb_request.get("hue") else prev_hue
		hsb_request["saturation"] = self._to_16_bit(hsb_request["saturation"], 100) if hsb_request.get("saturation") else prev_sat
		hsb_request["brightness"] = self._to_16_bit(hsb_request["brightness"], 100) if hsb_request.get("brightness") else prev_brightness
		color_to_send = [
			hsb_request["hue"],
			hsb_request["saturation"],
			hsb_request["brightness"],
			prev_temp
		]
		self.light.set_color(color_to_send, duration=self.transition_time)
		return color_to_send

	def _to_16_bit(self, value, max):
		if not 0 <= value <= max:
			raise ValidationError(f"Value ({value}) outside of allowed range 0 - {max}")
		return int(value * (65535/max))

