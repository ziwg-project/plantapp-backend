from django.urls import path
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from .views import UserPlantsViewSet, UserLocationsViewSet, UserRemindersViewSet, UserNotesViewSet, UserLogsViewSet, identify_plant

router = DefaultRouter()
router.register('plant', UserPlantsViewSet, 'plant')
router.register('location', UserLocationsViewSet, 'location')
router.register('reminder', UserRemindersViewSet, 'reminder')
router.register('note', UserNotesViewSet, 'note')
router.register('log', UserLogsViewSet, 'log')
router.register('devices', FCMDeviceAuthorizedViewSet, 'device')

urlpatterns = [
    path('plant-id/', identify_plant),
]

urlpatterns += router.urls
