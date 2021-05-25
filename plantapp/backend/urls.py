from rest_framework.routers import DefaultRouter

from .views import UserPlantsViewSet, UserLocationsViewSet, UserRemindersViewSet, UserNotesViewSet

router = DefaultRouter()
router.register('plant', UserPlantsViewSet, 'plant')
router.register('location', UserLocationsViewSet, 'location')
router.register('reminder', UserRemindersViewSet, 'reminder')
router.register('note', UserNotesViewSet, 'note')

urlpatterns = router.urls
