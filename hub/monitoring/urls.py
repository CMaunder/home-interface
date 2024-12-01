from rest_framework.routers import DefaultRouter

from .views import MeasurementViewSet, LocationViewSet, UnitViewSet, HostViewSet, DeviceViewSet, LightViewSet


router = DefaultRouter()
router.register(r'measurements', MeasurementViewSet, basename="measurement")
router.register(r'hosts', HostViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'units', UnitViewSet)
router.register(r'lights', LightViewSet)
urlpatterns = router.urls