from unicodedata import category

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, Category, ProductImage


# Create your views here.
def product_list(request):
    allproduct = Product.objects.all()
    allkategori = Category.objects.all()

    return render(request, 'landingpage/index.html', {'allproduct': allproduct, 'allkategori': allkategori})


def Product_by_filter(request, category_id):
    byfilter = Product.objects.filter(category=category_id)
    allkategori = Category.objects.all()

    return render(request, 'landingpage/index.html', {'allproduct': byfilter, 'allkategori': allkategori})

def product_detail(request, slug):
    # Ambil produk spesifik
    product = get_object_or_404(Product, slug=slug, is_active=True)

    image_byproduct = ProductImage.objects.filter(product=product)


    # Produk terkait (dalam kategori yang sama)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
        'image_byproduct': image_byproduct,
    }
    return render(request, 'landingpage/detail.html', context)


def create_order(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Ambil data untuk dropdown

    if request.method == 'POST':
        # Validasi stok
        quantity = int(request.POST.get('quantity', 1))
        if quantity > product.stock:
            messages.error(request, 'Jumlah melebihi stok yang tersedia')
            return redirect('landingpage:product_detail', slug=slug)

        # Ambil data alamat
        province = request.POST.get('province')
        city = request.POST.get('city')
        district = request.POST.get('district')

        # Hitung total harga
        harga_produk = product.discount or product.price
        total_price = harga_produk * quantity

        # Buat order
        order = Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price,
            customer_name=request.POST.get('name', ''),
            whatsapp=request.POST.get('whatsapp', ''),
            street_address=request.POST.get('street_address', ''),
            province=province,
            city=city,
            district=district,
            postal_code=request.POST.get('postal_code', ''),
            notes=request.POST.get('notes', '')
        )

        # Kurangi stok
        product.stock -= quantity
        product.save()

        # Siapkan pesan untuk WhatsApp
        wa_message = (
            f"Halo, saya ingin order *{product.name}*\n"
            f"Jumlah: {quantity} item\n"
            f"Total Harga: Rp {total_price:,.0f}\n"
            f"Nama: {order.customer_name}\n"
            f"Alamat: {order.street_address}, "
            f"{order.district}, "
            f"{order.city}, "
            f"{order.province} {order.postal_code}\n"
            f"Catatan: {order.notes or '-'}"
        )

        # Encode pesan untuk URL
        import urllib.parse
        encoded_message = urllib.parse.quote(wa_message)

        # Redirect ke WhatsApp
        return redirect(f"https://wa.me/6287742028130?text={encoded_message}")

    return redirect('landingpage:product_detail', slug=slug)


