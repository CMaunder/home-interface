from rest_framework import permissions, viewsets
from .models import Measurement, Device, Host, Unit, Location
from .serializers import MeasurementDetailSerializer, MeasurementListSerializer, DeviceSerializer, HostSerializer, UnitSerializer, LocationSerializer, MeasurementCreateUpdateSerializer

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.order_by("-recorded_at").all()
    queryset = queryset.select_related("unit", "device", "host")
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return MeasurementListSerializer
        elif self.action == 'update' or self.action == 'create':
            return MeasurementCreateUpdateSerializer
        return MeasurementDetailSerializer

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





