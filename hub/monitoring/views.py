from rest_framework import permissions, viewsets
from django.db.models import Count
from .models import Measurement, Device, Host, Unit, Location, Light
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import MeasurementDetailSerializer, MeasurementListSerializer, DeviceSerializer, HostSerializer, UnitSerializer, LocationSerializer, MeasurementCreateUpdateSerializer, LightSerializer
from fnmatch import fnmatch
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from time import sleep

class MeasurementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return MeasurementListSerializer
        elif self.action == 'update' or self.action == 'create':
            return MeasurementCreateUpdateSerializer
        return MeasurementDetailSerializer
    
    def get_queryset(self):
        queryset = Measurement.objects.order_by("recorded_at")
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

class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['POST'], url_path='power')
    def trigger_power(self, request: Request, pk=None):
        light = Light.objects.get(id=pk)
        if request.data.get("state") == True:
            light.power_on()
            return Response(f'{light} on')
        elif request.data.get("state") == False:
            light.power_off()
            return Response(f'{light} off')
        return Response("Ensure body is set with state: boolean", status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'], url_path='set-hsb')
    def set_hsb(self, request: Request, pk=None):
        """ body ranges:
        hue: [0 - 360]
        saturation:[0 - 100]
        brightness:[0 - 100]
        """
        light = Light.objects.get(id=pk)
        updated_color = light.set_hsb(request.data)
        return Response(f'{light} - hsb updated: {updated_color[:3]}')
