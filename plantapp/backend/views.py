from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Plant, Location
from .serializers import PlantSerializer, LocationSerializer
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
        location_id = request.data.get('loc_fk', default=None)
        if Location.objects.filter(pk=location_id).first().owner_fk == self.request.user:
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
