from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from .models import Plant, Location, Reminder, Note
from .serializers import PlantSerializer, LocationSerializer, ReminderSerializer, NoteSerializer
from .permissions import IsOwner, IsLocationOwnerOrReadOnly, IsPlantOwnerOrReadOnly


class UserPlantsViewSet(ModelViewSet):
    serializer_class = PlantSerializer
    permission_classes = [
        IsOwner,
        IsAuthenticated,
        IsLocationOwnerOrReadOnly,
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
        IsPlantOwnerOrReadOnly,
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
        IsPlantOwnerOrReadOnly
    ]

    def get_queryset(self):
        queryset = Note.objects.filter(plant_fk__loc_fk__owner_fk=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset
