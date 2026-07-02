from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductVariant

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    selected_colors = request.GET.getlist('color')
    if selected_colors:
        products = products.filter(variants__color__in=selected_colors).distinct()

    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(price__lte=max_price)

    all_colors = ProductVariant.objects.values_list('color', flat=True).distinct()

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'colors': all_colors,
        'selected_colors': selected_colors,   # ← add this
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    colors = product.variants.values_list('color', flat=True).distinct()
    sizes = product.variants.values_list('size', flat=True).distinct()

    # Build variant map for JS
    variants_map = {}
    for v in product.variants.filter(stock__gt=0):
        key = f"{v.color}|{v.size}"
        variants_map[key] = v.id

    return render(request, 'products/product_detail.html', {
        'product': product,
        'colors': colors,
        'sizes': sizes,
        'variants_map': variants_map,
    })