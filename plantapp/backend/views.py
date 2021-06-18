import requests
import json
from .constants import PLANT_ID_API_KEY

from django.http import Http404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from .models import Plant, Location, Reminder, Note, Log
from .serializers import PlantSerializer, LocationSerializer, ReminderSerializer, NoteSerializer, LogSerializer
from .permissions import IsOwner, IsLocationOwner, IsPlantOwner


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