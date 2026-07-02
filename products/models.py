from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_main_image(self):
        image = self.images.filter(is_main=True).first()
        return image or self.images.first()

    @property
    def is_in_stock(self):
        return self.variants.filter(stock__gt=0).exists()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.product.name} - image"


class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('ONE_SIZE', 'One Size'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True)
    material = models.CharField(max_length=100, blank=True)
    stock = models.PositiveIntegerField(default=0)
    extra_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Extra cost added on top of base product price"
    )

    class Meta:
        unique_together = ('product', 'color', 'size', 'material')

    def __str__(self):
        return f"{self.product.name} | {self.color} | {self.size} | {self.material}"

    @property
    def final_price(self):
        return self.product.price + self.extra_price