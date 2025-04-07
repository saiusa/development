from django.urls import path
from .cart_views import AddToCartView, ViewCartView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add_to_cart'),  # Add product to cart
    path('view/', ViewCartView.as_view(), name='view_cart'),    # View cart items
]