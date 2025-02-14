from rest_framework import serializers
from .models import Part

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'part_number', 'name', 'details', 'price', 'quantity']

class PartDetailsSerializer(serializers.ModelSerializer):
    car_models = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    class Meta:
        model = Part
        fields = ['id', 'part_number', 'name', 'details', 'price', 'quantity', 'car_models']