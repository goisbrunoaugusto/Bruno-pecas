from django.urls import path
from .views import (
    AssociatePartsToCarModels,
    DisassociatePartFromCarModel,
    PartListView, 
    PartUpdateView, 
    PartCreateView, 
    PartDestroyView, 
    ListPartsForCarModel,
    PartDetailView,
    PartCSVImportView
    )

urlpatterns = [
    path('associate-parts/', AssociatePartsToCarModels.as_view(), name='associate-parts'),
    path('disassociate-part/', DisassociatePartFromCarModel.as_view(), name='disassociate-part'),
    path('<int:car_model_id>/parts/', ListPartsForCarModel.as_view(), name='list-parts-for-car-model'),
    path('create/', PartCreateView.as_view(), name='part-create'),
    path('list/', PartListView.as_view(), name='part-list'),
    path('<int:id>/update/', PartUpdateView.as_view(), name='part-update'),
    path('<int:id>/delete/', PartDestroyView.as_view(), name='part-delete'),
    path('<int:id>/details/', PartDetailView.as_view(), name='part-detail'),
    path('import-parts/', PartCSVImportView.as_view(), name='import-parts'),
]