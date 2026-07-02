from django.db import models
from users.models import CustomUser
from products.models import ProductVariant

WILAYA_CHOICES = [
    ('ariana', 'Ariana'), ('beja', 'Béja'), ('ben_arous', 'Ben Arous'),
    ('bizerte', 'Bizerte'), ('gabes', 'Gabès'), ('gafsa', 'Gafsa'),
    ('jendouba', 'Jendouba'), ('kairouan', 'Kairouan'), ('kasserine', 'Kasserine'),
    ('kebili', 'Kébili'), ('kef', 'Le Kef'), ('mahdia', 'Mahdia'),
    ('manouba', 'Manouba'), ('medenine', 'Médenine'), ('monastir', 'Monastir'),
    ('nabeul', 'Nabeul'), ('sfax', 'Sfax'), ('sidi_bouzid', 'Sidi Bouzid'),
    ('siliana', 'Siliana'), ('sousse', 'Sousse'), ('tataouine', 'Tataouine'),
    ('tozeur', 'Tozeur'), ('tunis', 'Tunis'), ('zaghouan', 'Zaghouan'),
]

ORDER_STATUS = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    wilaya = models.CharField(max_length=50, choices=WILAYA_CHOICES)
    city = models.CharField(max_length=100)
    address = models.TextField()
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    variant_details = models.CharField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity