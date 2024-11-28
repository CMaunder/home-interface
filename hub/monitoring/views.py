from rest_framework import permissions, viewsets
from django.db.models import Count
from .models import Measurement, Device, Host, Unit, Location
from rest_framework.exceptions import ValidationError
from .serializers import MeasurementDetailSerializer, MeasurementListSerializer, DeviceSerializer, HostSerializer, UnitSerializer, LocationSerializer, MeasurementCreateUpdateSerializer
from fnmatch import fnmatch
from datetime import datetime, timedelta

class MeasurementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return MeasurementListSerializer
        elif self.action == 'update' or self.action == 'create':
            return MeasurementCreateUpdateSerializer
        return MeasurementDetailSerializer
    
    def get_queryset(self):
        queryset = Measurement.objects.order_by("-recorded_at")
        query_params = self.request.query_params
        unit = query_params.get('unit')
        if unit:
            if not Unit.objects.filter(name=unit).exists():
                raise ValidationError("No unit exists within the database.")
            queryset = queryset.filter(unit__name=unit)
        last_timeunits = [param for param in query_params if fnmatch(param, "last-*")]
        if len(last_timeunits) > 1:
            raise ValidationError("Specify only one last_ query param.")
        if len(last_timeunits) == 1:
            timeunit = last_timeunits[0].split("-")[1]
            last = float(query_params.get(last_timeunits[0]))
            try:
                date_then = datetime.now() - timedelta(**{timeunit: last})
                queryset = queryset.filter(recorded_at__gt=date_then)
            except TypeError as e:
                raise ValidationError(e)
        queryset = queryset.select_related("unit", "device", "host")
        return queryset

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





