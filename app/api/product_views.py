from django.shortcuts import render, get_object_or_404

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .product_models import Product

# Product Views
class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        """Retrieve all products."""
        products = Product.objects.all().values(
            'id', 'name', 'price', 'stock', 'category', 'image', 'created_at', 'updated_at'
        )
        return Response({'products': list(products)}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Create a new product."""
        data = request.data
        product = Product.objects.create(
            name=data.get('name'),
            price=data.get('price'),
            stock=data.get('stock'),
            category=data.get('category'),
            image=data.get('image')  # Assuming image is handled separately
        )
        return Response({'message': 'Product created successfully!', 'id': product.id}, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        """Retrieve a single product by ID."""
        product = get_object_or_404(Product, pk=pk)
        data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'category': product.category,
            'image': product.image.url if product.image else None,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
        }
        return Response({'product': data}, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """Update an existing product."""
        data = request.data
        product = get_object_or_404(Product, pk=pk)
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        product.category = data.get('category', product.category)
        if 'image' in data:
            product.image = data.get('image')
        product.save()
        return Response({'message': 'Product updated successfully!'}, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        """Delete a product."""
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'message': 'Product deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


