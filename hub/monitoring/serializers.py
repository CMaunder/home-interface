from rest_framework import serializers
from django.utils import timezone
from .models import Measurement, Host, Device, Location, Unit

class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ['url', 'name', 'dimension']

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

    def validate_recorded_at(self, value):
        if value > timezone.now():
            raise serializers.ValidationError('Value cannot be in the future.')
        return value
    
    def validate(self, data):
        unit = data['unit']
        if unit.dimension.lower() == 'percent':
            if not 0 <= data['measure'] <= 100:
                raise serializers.ValidationError(f'Percentage dimension {unit} must be between 0 and 100.')
        elif unit.dimension.lower() == 'celcius':
            if data['measure'] < -273.15:
                raise serializers.ValidationError(f'Temperature cannot be below absolute zero.')
        return data
    
class MeasurementListSerializer(MeasurementSerializer):
    unit = UnitSerializer(read_only=True)
    device = DeviceSerializer(read_only=True)