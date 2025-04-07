from django.urls import path
from .checkout_views import CheckoutView

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),  # Process checkout
]