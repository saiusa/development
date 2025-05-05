from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .store_views import ProductViewSet, CartItemViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]