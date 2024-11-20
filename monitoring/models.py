from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, null=True)
	dimension = models.CharField(max_length=200)

	def __str__(self):
		return f"{self.name} - {self.dimension}"

class Location(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, null=True)

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
	host = models.ForeignKey(Host, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.name} - {self.host}"

class Measurement(models.Model):
	measure = models.DecimalField(decimal_places=4, max_digits=15)
	inserted_at = models.DateTimeField(auto_now_add=True)
	recorded_at = models.DateTimeField()
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	device = models.ForeignKey(Device, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.unit} - {self.measure} {self.unit.dimension}"







  