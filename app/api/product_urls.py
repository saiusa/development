from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .product_views import ProductViewSet, CartViewSet, CheckoutViewSet, CartItemUpdateDeleteView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'checkouts', CheckoutViewSet, basename='checkout')

urlpatterns = [
    path('', include(router.urls)),
    path('carts/<int:cart_id>/items/<int:product_id>/', CartItemUpdateDeleteView.as_view(), name='cart-item-update-delete'),
]