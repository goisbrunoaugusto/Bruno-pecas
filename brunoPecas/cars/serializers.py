from rest_framework import serializers
from .models import CarModel
from parts.serializers import PartSerializer

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'manufacturer', 'year', 'details']

class CarModelDetailSerializer(serializers.ModelSerializer):
    parts = PartSerializer(many=True, read_only=True)  # Assuming you have a PartSerializer
    
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'manufacturer', 'year', 'details', 'parts']
