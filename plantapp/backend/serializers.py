from rest_framework.serializers import ModelSerializer

from .models import Plant, Location


class PlantSerializer(ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
