from rest_framework import serializers
from .store_models import Products, CartItem, Payment

class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'product_image', 'price', 'stock', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.product_image:
            # Manually construct the URL with the port (if necessary, otherwise leave it to Django's default behavior)
            base_url = "http://172.17.100.14:3329"
            relative_url = instance.product_image.url
            representation['product_image'] = f"{base_url}{relative_url}"
        else:
            representation['product_image'] = None
        return representation

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'created_at']  # Assuming CartItem references a Product, using 'product'
        read_only_fields = ['created_at']

    def validate(self, data):
        product_id = self.context.get('request').data.get('product_id')
        if not product_id:
            raise serializers.ValidationError("Product ID is required")
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            raise serializers.ValidationError(f"Product with ID {product_id} does not exist")

        # Ensure CartItem has proper data
        cart_item = data.get('product')
        if cart_item:
            if cart_item.name != product.name:
                raise serializers.ValidationError("Product name does not match")
            if cart_item.description != product.description:
                raise serializers.ValidationError("Product description does not match")
            if cart_item.price != product.price:
                raise serializers.ValidationError("Product price does not match")
            if cart_item.stock < 1:
                raise serializers.ValidationError(f"Product {product.name} is out of stock")

        return data

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value

class PaymentSerializer(serializers.ModelSerializer):
    receipt_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Payment
        fields = ['id', 'name', 'email', 'address', 'payment_method', 'total_amount', 'products', 'receipt_image', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.receipt_image:
            # Manually construct the URL for receipt image (you can adjust this as per your requirements)
            base_url = "http://172.17.100.14:3329"
            relative_url = instance.receipt_image.url  # Correct the field name
            representation['receipt_image'] = f"{base_url}{relative_url}"
        else:
            representation['receipt_image'] = None
        return representation

    def validate_products(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Products must be a list")
        for item in value:
            if not all(key in item for key in ['id', 'name', 'quantity', 'price']):
                raise serializers.ValidationError("Each product must have id, name, quantity, and price")
            if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be a positive integer")
            if not isinstance(item['price'], (int, float)) or item['price'] <= 0:
                raise serializers.ValidationError("Price must be a positive number")
        return value

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total amount must be positive")
        return value