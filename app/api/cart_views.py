from django.shortcuts import render, get_object_or_404

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .cart_models import Cart, CartItem
from .product_models import Product

# Cart Views
class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        """Add a product to the cart."""
        data = request.data
        product = Product.objects.filter(id=data.get('product_id')).first()
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create()
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += data.get('quantity', 1)
        else:
            cart_item.quantity = data.get('quantity', 1)
        cart_item.save()
        return Response({'message': 'Product added to cart successfully!'}, status=status.HTTP_201_CREATED)


class ViewCartView(APIView):
    def get(self, request, *args, **kwargs):
        """Retrieve all items in the cart."""
        cart, _ = Cart.objects.get_or_create()
        items = cart.items.all().values(
            'id', 'product__name', 'product__price', 'quantity', 'product__image'
        )
        total_price = cart.total_price()
        return Response({'items': list(items), 'total_price': total_price}, status=status.HTTP_200_OK)


class CartItemView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        cart, created = Cart.objects.get_or_create(id=1)  # Replace with user-specific logic if needed
        product = next((p for p in PREDEFINED_PRODUCTS if p["id"] == data.get('product_id')), None)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        quantity = int(data.get('quantity', 1))
        if quantity > product["stock"]:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product["id"])
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        return Response({'message': 'Product added to cart successfully!'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        data = request.data
        cart = get_object_or_404(Cart, id=1)  # Replace with user-specific logic if needed
        product = next((p for p in PREDEFINED_PRODUCTS if p["id"] == data.get('product_id')), None)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product["id"])
        cart_item.delete()
        return Response({'message': 'Product removed from cart successfully!'}, status=status.HTTP_200_OK)
