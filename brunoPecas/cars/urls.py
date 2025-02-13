from django.urls import path
from .views import (
    CarModelListView, 
    CarModelCreateView,
    CarModelDetailView,
    CarModelUpdateView,
    CarModelDeleteView,
    ListCarModelsForPart
)

urlpatterns = [
    path('list/', CarModelListView.as_view(), name='car-list'),
    path('create/', CarModelCreateView.as_view(), name='car-create'),
    path('<int:id>/', CarModelDetailView.as_view(), name='car-detail'),
    path('<int:id>/update/', CarModelUpdateView.as_view(), name='car-update'),
    path('<int:id>/delete/', CarModelDeleteView.as_view(), name='car-delete'),
    path('<int:part_id>/car-models/', ListCarModelsForPart.as_view(), name='list-car-models-for-part'),

]