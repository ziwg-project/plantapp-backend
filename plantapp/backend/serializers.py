from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Plant, Location, Reminder


class PlantSerializer(ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class LocationSerializer(ModelSerializer):
    owner_fk = PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Location
        fields = '__all__'


class ReminderSerializer(ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
