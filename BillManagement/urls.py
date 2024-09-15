from django.urls import path
from BillManagement.views import (  # Ensure you import views correctly
    BillCreateView,
    BillDetailView,
    BillUpdateView,
    BillDeleteView,
    BillSplitView,
    BillSettlementView
)

urlpatterns = [
    path('bill/create/', BillCreateView.as_view(), name='bill-create'),
    path('bill/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('bill/<int:pk>/update/', BillUpdateView.as_view(), name='bill-update'),
    path('bill/<int:pk>/delete/', BillDeleteView.as_view(), name='bill-delete'),
    path('bill/<int:bill_id>/split/', BillSplitView.as_view(), name='bill-split'),
    path('bill/split/<int:split_id>/settle/', BillSettlementView.as_view(), name='bill-settle'),
]
