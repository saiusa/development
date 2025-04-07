from django.db import models
from .product_models import Product

class Checkout(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_address = models.TextField()
    payment_method = models.CharField(
        max_length=50,
        choices=[('COD', 'Cash on Delivery'), ('Card', 'Credit/Debit Card')],
        default='COD'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout {self.id} by {self.customer_name} - {self.payment_method}"


class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Checkout {self.checkout.id}"