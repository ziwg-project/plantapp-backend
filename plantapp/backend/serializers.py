from django.utils import timezone

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, ValidationError

from .models import Plant, Location, Reminder, Note, Log


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
    notification_task = PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Reminder
        fields = '__all__'


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
    
    def create(self, validated_data):
        current_ts = timezone.now()
        if current_ts < validated_data['log_tmstp']:
            raise ValidationError("Log timestamp value cannot exceed the present timestamp!")
        return Log.objects.create(**validated_data)