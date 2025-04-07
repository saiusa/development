from django.urls import path
from .product_views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),  # List and create products
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Retrieve, update, delete a product
]
