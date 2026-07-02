from django.shortcuts import render
from products.models import Product, Category

def home(request):
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'categories': categories,
    })

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def shipping_info(request):
    return render(request, 'core/shipping_info.html')