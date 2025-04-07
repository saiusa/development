from django.shortcuts import render, get_object_or_404

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .checkout_models import Checkout, CheckoutItem
from .cart_models import Cart

# Checkout Views
class CheckoutListView(APIView):
    def get(self, request, *args, **kwargs):
        checkouts = Checkout.objects.all()
        checkout_data = [
            {
                'id': checkout.id,
                'customer_name': checkout.customer_name,
                'customer_email': checkout.customer_email,
                'customer_address': checkout.customer_address,
                'payment_method': checkout.payment_method,  # Include payment method
                'total_price': checkout.total_price,
                'created_at': checkout.created_at,
            }
            for checkout in checkouts
        ]
        return Response({'checkouts': checkout_data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        checkout = Checkout.objects.create(
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            customer_address=data.get('customer_address'),
            payment_method=data.get('payment_method'),  # Save payment method
            total_price=data.get('total_price'),
        )
        for item in data.get('items', []):
            product = next((p for p in PREDEFINED_PRODUCTS if p["id"] == item['product_id']), None)
            if not product:
                return Response({'error': f"Product with ID {item['product_id']} not found"}, status=status.HTTP_404_NOT_FOUND)

            CheckoutItem.objects.create(
                checkout=checkout,
                product_id=product["id"],
                quantity=item['quantity'],
                price=product["price"],
            )
        return Response({'message': 'Checkout created successfully!', 'id': checkout.id}, status=status.HTTP_201_CREATED)


class CheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        """Process checkout."""
        data = request.data
        cart, _ = Cart.objects.get_or_create()

        # Create a checkout instance
        checkout = Checkout.objects.create(
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            customer_address=data.get('customer_address'),
            payment_method=data.get('payment_method'),
            total_price=cart.total_price(),
        )

        # Move cart items to checkout items
        for cart_item in cart.items.all():
            CheckoutItem.objects.create(
                checkout=checkout,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear the cart
        cart.items.all().delete()

        return Response({'message': 'Checkout completed successfully!', 'checkout_id': checkout.id}, status=status.HTTP_201_CREATED)


class CheckoutDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        checkout = get_object_or_404(Checkout, pk=pk)
        items = checkout.items.all()
        checkout_data = {
            'id': checkout.id,
            'customer_name': checkout.customer_name,
            'customer_email': checkout.customer_email,
            'customer_address': checkout.customer_address,
            'payment_method': checkout.payment_method,  # Include payment method
            'total_price': checkout.total_price,
            'created_at': checkout.created_at,
            'items': [
                {
                    'product': next((p for p in PREDEFINED_PRODUCTS if p["id"] == item.product_id), {}).get("name"),
                    'quantity': item.quantity,
                    'price': item.price,
                    'total_price': item.total_price(),
                }
                for item in items
            ],
        }
        return Response({'checkout': checkout_data}, status=status.HTTP_200_OK)
