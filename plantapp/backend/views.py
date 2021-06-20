import json
import uuid

import requests
from django.http import Http404
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .constants import PLANT_ID_API_KEY
from .models import Plant, Location, Reminder, Note, Log
from .permissions import IsOwner, IsLocationOwner, IsPlantOwner
from .serializers import PlantSerializer, LocationSerializer, ReminderSerializer, NoteSerializer, LogSerializer
from .utils import NotificationContentProvider, ScheduleMapper


class UserPlantsViewSet(ModelViewSet):
    serializer_class = PlantSerializer
    permission_classes = [
        IsOwner,
        IsAuthenticated,
        IsLocationOwner,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'sci_name']

    def get_queryset(self):
        queryset = Plant.objects.filter(loc_fk__owner_fk=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset


class UserLocationsViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [
        IsOwner,
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = Location.objects.filter(owner_fk=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset

    def perform_create(self, serializer):
        return serializer.save(owner_fk=self.request.user)


class UserRemindersViewSet(ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [
        IsOwner,
        IsAuthenticated,
        IsPlantOwner,
    ]

    def get_queryset(self):
        queryset = Reminder.objects.filter(plant_fk__loc_fk__owner_fk=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset

    def perform_create(self, serializer):
        schedule = self.__create_schedule(serializer)
        notification = NotificationContentProvider(serializer.validated_data)
        notification_task = PeriodicTask.objects.create(
            interval=schedule,
            name=uuid.uuid4(),
            task='plantapp.celery.send_notification',
            start_time=serializer.validated_data['base_tmstp'],
            args=json.dumps([serializer.validated_data['plant_fk'].loc_fk.owner_fk.pk, notification.title, notification.body])
        )
        return serializer.save(notification_task=notification_task)

    def perform_update(self, serializer):
        schedule = self.__create_schedule(serializer)
        notification = NotificationContentProvider(serializer.validated_data)
        notification_task = self.get_object().notification_task
        notification_task.interval = schedule
        notification_task.start_time = serializer.validated_data['base_tmstp']
        notification_task.args = json.dumps(
            [serializer.validated_data['plant_fk'].loc_fk.owner_fk.pk, notification.title, notification.body])
        notification_task.save()
        return serializer.save()

    @staticmethod
    def __create_schedule(serializer):
        schedule_data = ScheduleMapper.to_celery_beat_schedule(
            intrvl_num=serializer.validated_data['intrvl_num'],
            intrvl_type=serializer.validated_data['intrvl_type']
        )
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=schedule_data.every,
            period=schedule_data.period
        )
        return schedule


class UserNotesViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [
        IsOwner,
        IsAuthenticated,
        IsPlantOwner
    ]

    def get_queryset(self):
        queryset = Note.objects.filter(plant_fk__loc_fk__owner_fk=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset


class UserLogsViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = LogSerializer
    permission_classes = [
        IsOwner,
        IsAuthenticated,
        IsPlantOwner
    ]

    def get_queryset(self):
        queryset = Log.objects.filter(reminder_fk__plant_fk__loc_fk__owner_fk=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def identify_plant(request):
    if len(request.data) == 2 and all(key in request.data for key in ('plant_details', 'images')):
        request.data['api_key'] = PLANT_ID_API_KEY
        plantid_data = json.dumps(request.data)
        response = requests.post('https://api.plant.id/v2/identify', data=plantid_data).json()
        return Response(response)
    else:
        return Response('Incorrect json data provided!', status=status.HTTP_400_BAD_REQUEST)
