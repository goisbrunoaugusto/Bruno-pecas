from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CarModel
from parts.models import Part
from parts.serializers import PartSerializer
from .serializers import CarModelDetailSerializer, CarModelSerializer
from rest_framework import generics
from users.permissions import IsAdminRole

class CarModelListView(generics.ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated]

class CarModelDetailView(generics.RetrieveAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class CarModelCreateView(generics.CreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminRole]

class CarModelUpdateView(generics.UpdateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id'

class CarModelDeleteView(generics.DestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id'

class ListCarModelsForPart(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, part_id):
        try:
            part = Part.objects.get(id=part_id)
            car_models = part.car_models.all()
            serializer = CarModelSerializer(car_models, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Part.DoesNotExist:
            return Response({"error": "Part not found."}, status=status.HTTP_404_NOT_FOUND)
