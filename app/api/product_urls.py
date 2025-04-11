from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .product_views import ProductViewSet, CartViewSet, CheckoutViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)
router.register(r'checkout', CheckoutViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
