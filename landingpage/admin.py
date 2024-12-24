from django.contrib import admin
from .models import Order,Product,Category,ProductImage
# Register your models here.



class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name','product','status','created_at')
    list_filter = ('status',)
    search_fields = ('customer_name','whatsapp')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(status='completed')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Menambahkan satu form kosong untuk gambar tambahan saat menambah produk

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Menambahkan inline untuk gambar pada produk
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
