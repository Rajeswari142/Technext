from django.shortcuts import render, redirect
from .models import Product, Order


# 🛍️ PRODUCT LIST
def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'store/products.html', {
        'products': products,
        'cart_count': cart_count
    })


# 🛒 ADD TO CART
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart

    # 🔥 Better UX → go to cart page
    return redirect('view_cart')


# 🛒 VIEW CART
def view_cart(request):
    cart = request.session.get('cart', {})

    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ❌ REMOVE FROM CART
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('view_cart')


# 💳 CHECKOUT
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('product_list')

    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if not name or not email:
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'error': 'All fields are required'
            })

        # ✅ SAVE ORDERS
        for item in cart_items:
            Order.objects.create(
                product=item['product'],
                customer_name=name,
                customer_email=email,
                quantity=item['quantity']
            )

        request.session['cart'] = {}

        return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


# ✅ SUCCESS PAGE
def order_success(request):
    return render(request, 'store/success.html')


# 📦 ORDER LIST
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'store/orders.html', {'orders': orders})

def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if action == 'increase':
            cart[product_id] += 1

        elif action == 'decrease':
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]

    request.session['cart'] = cart
    return redirect('view_cart')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    return redirect('view_cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        # remove if quantity becomes 0
        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    return redirect('view_cart')


# ❤️ ADD TO WISHLIST
def add_to_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    product_id = str(product_id)

    if product_id not in wishlist:
        wishlist.append(product_id)

    request.session['wishlist'] = wishlist
    return redirect('product_list')


# 📄 VIEW WISHLIST
def view_wishlist(request):
    wishlist = request.session.get('wishlist', [])

    products = Product.objects.filter(id__in=wishlist)

    return render(request, 'store/wishlist.html', {
        'products': products
    })


# ❌ REMOVE FROM WISHLIST
def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    product_id = str(product_id)

    if product_id in wishlist:
        wishlist.remove(product_id)

    request.session['wishlist'] = wishlist
    return redirect('view_wishlist')