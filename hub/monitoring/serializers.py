from rest_framework import serializers
from datetime import datetime, timedelta
from .models import Measurement, Host, Device, Location, Unit, Light
from .utils import round_seconds
import pytz

class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

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

class LightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Light
        fields = '__all__'


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    recorded_at = serializers.SerializerMethodField()
    inserted_at = serializers.SerializerMethodField()
    measure = serializers.SerializerMethodField()

    def get_recorded_at(self, obj):
        return round_seconds(obj.recorded_at)
    
    def get_inserted_at(self, obj):
        return round_seconds(obj.inserted_at)
    
    def get_measure(self, obj):
        return str(round(obj.measure, 1))

    class Meta:
        model = Measurement
        fields = '__all__'

    def validate_recorded_at(self, value):
        now_datetime = datetime.now() + timedelta(minutes=1)
        now_datetime = now_datetime.replace(tzinfo=pytz.utc)
        if value > now_datetime:
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
    
class MeasurementCreateUpdateSerializer(MeasurementSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

class MeasurementDetailSerializer(MeasurementSerializer):
    unit = UnitSerializer(read_only=True)
    host = HostSerializer(read_only=True)
    device = DeviceSerializer(read_only=True)
    
class MeasurementListSerializer(MeasurementSerializer):
    unit = serializers.SlugRelatedField(read_only=True, slug_field='name')
    device = serializers.SlugRelatedField(read_only=True, slug_field='name')
    host = serializers.SlugRelatedField(read_only=True, slug_field='ip_address')