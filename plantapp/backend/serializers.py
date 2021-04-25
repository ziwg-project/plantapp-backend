from rest_framework.serializers import ModelSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

from .models import Plant, Location, Reminder


class PlantSerializer(ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class LocationSerializer(ModelSerializer):
    owner_fk = UserDetailsSerializer(required=False)

    class Meta:
        model = Location
        fields = '__all__'


class ReminderSerializer(ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
