from django.urls import path, include
from .views import Students 

from .views import ContactListView
from .views import ContactUpdateDetailView 


urlpatterns = [
    path('students/', Students.as_view(), name='list_students'),
    path('contact/', ContactListView.as_view(),name = 'contact_new'),
    path('contact/<int:contact_id>/', ContactListView.as_view(), name='contact_detail'),
    path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'),
    
    path('products/', include('api.product_urls')),  # Product-related URLs
    path('cart/', include('api.cart_urls')),        # Cart-related URLs
    path('checkout/', include('api.checkout_urls')), # Checkout-related URLs
]