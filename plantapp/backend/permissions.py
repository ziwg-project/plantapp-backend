from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Plant, Location, Note, Reminder


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Location):
            return obj.owner_fk == request.user
        elif isinstance(obj, Plant):
            return obj.loc_fk.owner_fk == request.user
        elif isinstance(obj, Reminder) or isinstance(obj, Note):
            return obj.plant_fk.loc_fk.owner_fk == request.user
        else:
            return False


class IsLocationOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            serializer = view.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_locations_pks = request.user.location_set.all().values_list('id', flat=True)
            if serializer.data.get('loc_fk') in user_locations_pks:
                return True
            return False


class IsPlantOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            serializer = view.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_plants_pks = Plant.objects.filter(loc_fk__owner_fk=request.user).values_list('id', flat=True)
            if serializer.data.get('plant_fk') in user_plants_pks:
                return True
            return False
