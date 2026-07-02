from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import ProductVariant
from .models import Order, OrderItem
from .forms import CheckoutForm


def cart_add(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart = request.session.get('cart', {})
    key = str(variant_id)
    quantity = int(request.POST.get('quantity', 1))

    if variant.stock < 1:
        messages.error(request, 'Sorry, this item is out of stock.')
        return redirect('products:detail', slug=variant.product.slug)

    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'variant_id': variant.id,
            'product_name': variant.product.name,
            'variant_details': f"{variant.color} / {variant.size}".strip(' /'),
            'quantity': quantity,
            'price': str(variant.final_price),
            'slug': variant.product.slug,
        }

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'"{variant.product.name}" added to your cart!')
    return redirect('products:detail', slug=variant.product.slug)


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for key, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        total += subtotal
        items.append({
            'key': key,
            'product_name': item['product_name'],
            'variant_details': item['variant_details'],
            'quantity': item['quantity'],
            'price': item['price'],
            'subtotal': subtotal,
            'slug': item['slug'],
        })

    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total,
    })


def cart_remove(request, key):
    cart = request.session.get('cart', {})
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('orders:cart')


def cart_update(request, key):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    if key in cart:
        if quantity > 0:
            cart[key]['quantity'] = quantity
        else:
            del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('orders:cart')


def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('orders:cart')

    items = []
    total = 0
    for key, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        total += subtotal
        items.append({**item, 'subtotal': subtotal})

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = total
            order.save()

            for item in items:
                try:
                    variant = ProductVariant.objects.get(id=item['variant_id'])
                except ProductVariant.DoesNotExist:
                    variant = None
                OrderItem.objects.create(
                    order=order,
                    variant=variant,
                    product_name=item['product_name'],
                    variant_details=item['variant_details'],
                    quantity=item['quantity'],
                    price=item['price'],
                )

            request.session['cart'] = {}
            request.session.modified = True
            return redirect('orders:confirmed', order_id=order.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'full_name': request.user.get_full_name(),
                'phone': request.user.phone,
                'address': request.user.address,
            }
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
    })


def order_confirmed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/confirmed.html', {'order': order})