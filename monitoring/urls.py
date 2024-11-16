from rest_framework.routers import DefaultRouter

from .views import MeasurementViewSet, LocationViewSet, UnitViewSet, HostViewSet, DeviceViewSet


router = DefaultRouter()
router.register(r'measurements', MeasurementViewSet)
router.register(r'hosts', HostViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'units', UnitViewSet)
urlpatterns = router.urls