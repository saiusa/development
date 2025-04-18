from rest_framework import serializers
from .product_models import Product, Cart, CartItem, Checkout
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, data):
        if data.get('price', 0) < 0:
            raise serializers.ValidationError({'price': 'Price cannot be negative.'})
        if data.get('stock', 0) < 0:
            raise serializers.ValidationError({'stock': 'Stock cannot be negative.'})
        return data

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')
        if product.stock < quantity:
            raise serializers.ValidationError(
                f"Insufficient stock for {product.name}. Available: {product.stock}"
            )
        return data

class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = Cart
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        quantity = validated_data.pop('quantity')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_id': 'Product not found'})
        cart = Cart.objects.create()
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        return cart

class CheckoutItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(source='product.name')
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price')

class CheckoutSerializer(serializers.ModelSerializer):
    cart_id = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), source='cart', write_only=True
    )
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Checkout
        fields = [
            'customer_name', 'customer_email', 'customer_address',
            'total_price', 'payment_method', 'items', 'cart_id'
        ]
        extra_kwargs = {
            'total_price': {'read_only': True},
        }

    def get_items(self, obj):
        cart_items = obj.cart.items.all()
        return CheckoutItemSerializer(cart_items, many=True).data

    def validate(self, data):
        cart = data.get('cart')
        if not cart.items.exists():
            raise serializers.ValidationError({'cart_id': 'Cart is empty.'})
        total_price = sum(
            Decimal(str(item.product.price)) * item.quantity for item in cart.items.all()
        )
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {item.product.name}. Available: {item.product.stock}"
                )
        data['total_price'] = total_price
        return data

    def create(self, validated_data):
        cart = validated_data.pop('cart')
        checkout = Checkout.objects.create(cart=cart, **validated_data)
        for item in cart.items.all():
            item.product.stock -= item.quantity
            item.product.save()
        return checkout