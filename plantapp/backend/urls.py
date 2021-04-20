from rest_framework.routers import DefaultRouter

from .views import UserPlantsViewSet, UserLocationsViewSet

router = DefaultRouter()
router.register('plant', UserPlantsViewSet, 'plant')
router.register('location', UserLocationsViewSet, 'location')

urlpatterns = router.urls
