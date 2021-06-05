from rest_framework.routers import DefaultRouter

from django.urls import path

from .views import UserPlantsViewSet, UserLocationsViewSet, UserRemindersViewSet, UserNotesViewSet, identify_plant

router = DefaultRouter()
router.register('plant', UserPlantsViewSet, 'plant')
router.register('location', UserLocationsViewSet, 'location')
router.register('reminder', UserRemindersViewSet, 'reminder')
router.register('note', UserNotesViewSet, 'note')

urlpatterns = [
    path('plant-id/', identify_plant),
]

urlpatterns += router.urls
