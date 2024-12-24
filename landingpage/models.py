from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, editable=False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)




class Product(models.Model):
    hook = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(blank=True,upload_to='products/')
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('Completed', 'Completed'),
#         ('canceled', 'Canceled'),
#     ]
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     customer_name = models.CharField(max_length=100)
#     whatsapp = models.CharField(max_length=20)
#     quantity = models.PositiveIntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)  # Tambahkan field ini
#     notes = models.TextField(blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.customer_name} - {self.product.name}"
#




class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)

    # Nomor HP dengan validator
    phone_regex = RegexValidator(
        regex=r'^^\+?1?\d{9,15}$',
        message="Nomor HP harus dalam format: '+628123456789'"
    )
    whatsapp = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=False
    )

    # Detail Alamat Lengkap
    street_address = models.CharField(max_length=255,blank=True,null=True)
    province = models.CharField(max_length=255,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    district = models.CharField(max_length=255,null=True,blank=True)

    postal_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{5}$',
                message="Kode pos harus 5 digit"
            )
        ]
    )

    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"