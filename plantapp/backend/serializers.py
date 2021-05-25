from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Plant, Location, Reminder, Note


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


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
