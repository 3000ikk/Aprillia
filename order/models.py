from django.contrib.auth import get_user_model
from django.db import models

from product.models import Product

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('prodessing', 'Processing'),
    ('in_delivery', 'In delivery'),
    ('finished', 'Finished'),
    ('canceled', 'Canceled')
)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='ordrers', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    comment = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(OrderItem)


