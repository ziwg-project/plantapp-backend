from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Plant, Location, Reminder
from .serializers import PlantSerializer, LocationSerializer, ReminderSerializer
from .permissions import IsOwner


class UserPlantsViewSet(ModelViewSet):
    serializer_class = PlantSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = Plant.objects.filter(loc_fk__owner_fk=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify if requester is the owner of the location the plant will be added to
        location_id = request.data.get('loc_fk')
        location_owner = Location.objects.get(pk=location_id).owner_fk
        if self.request.user == location_owner:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)


class UserLocationsViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner
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
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = Reminder.objects.filter(plant_fk__loc_fk__owner_fk__exact=self.request.user)
        if not queryset.count():
            raise Http404
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.data)
        serializer.is_valid(raise_exception=True)

        plant_id = request.data.get('plant_fk')
        plant_owner = Plant.objects.get(pk=plant_id).loc_fk.owner_fk
        if self.request.user == plant_owner:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
