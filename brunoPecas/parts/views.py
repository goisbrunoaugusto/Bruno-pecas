from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsAdminRole
from .models import Part
from cars.models import CarModel
from .serializers import PartSerializer, PartDetailsSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

class AssociatePartsToCarModels(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request):
        part_ids = request.data.get('part_ids', [])
        car_model_ids = request.data.get('car_model_ids', [])

        parts = Part.objects.filter(id__in=part_ids)
        if len(parts) != len(part_ids):
            return Response(
                {"error": "One or more part IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        car_models = CarModel.objects.filter(id__in=car_model_ids)
        if len(car_models) != len(car_model_ids):
            return Response(
                {"error": "One or more car model IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            for car_model in car_models:
                car_model.parts.add(*parts)

            return Response({"message": "Parts associated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DisassociatePartFromCarModel(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request):
        part_id = request.data.get('part_id')
        car_model_id = request.data.get('car_model_id')

        try:
            part = Part.objects.get(id=part_id)
            car_model = CarModel.objects.get(id=car_model_id)
            car_model.parts.remove(part)

            return Response({"message": "Part disassociated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListPartsForCarModel(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, car_model_id):
        try:
            car_model = CarModel.objects.get(id=car_model_id)
            parts = car_model.parts.all()
            serializer = PartSerializer(parts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CarModel.DoesNotExist:
            return Response({"error": "CarModel not found."}, status=status.HTTP_404_NOT_FOUND)

class PartListView(generics.ListAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]

class PartDetailView(generics.RetrieveAPIView):
    queryset = Part.objects.all()
    serializer_class = PartDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class PartCreateView(generics.CreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdminRole]

class PartUpdateView(generics.UpdateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id'

class PartDestroyView(generics.DestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id'