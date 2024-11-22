from rest_framework import permissions, viewsets
from .models import Measurement, Device, Host, Unit, Location
from .serializers import MeasurementSerializer, MeasurementListSerializer, DeviceSerializer, HostSerializer, UnitSerializer, LocationSerializer

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.order_by("-recorded_at").all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return MeasurementListSerializer
        return MeasurementSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.AllowAny]

class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = [permissions.AllowAny]

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]





