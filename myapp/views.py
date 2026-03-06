from urllib import request
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Card, Offers, NewArrivals, Cloths, Review, ContactMessage, Toy, WishlistItem, Cart, CartItem, Order, OrderItem
from .forms import ReviewForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
import uuid


# Helper function for cart management
def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        # Safe lookup + create (don't use user__isnull in get_or_create create kwargs)
        cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
        if not cart:
            cart = Cart.objects.create(session_key=session_key, user=None)

    return cart


# Create your views here.

def index(request):
    offers = Offers.objects.all()
    arrivals = NewArrivals.objects.all()
    cards = Card.objects.all()
    wishlist_items = []
    wishlist_count = 0
    cart_count = 0
    
    # Get cart count
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key, user__isnull=True)
                cart_count = cart.get_item_count()
            except Cart.DoesNotExist:
                cart_count = 0
    
    if request.user.is_authenticated:
        user_wishlist = WishlistItem.objects.filter(user=request.user)
        wishlist_count = user_wishlist.count()
        
        # Prepare wishlist data for template
        for item in user_wishlist[:6]:  # Show only first 6 items on home page
            wishlist_items.append({
                'id': item.id,
                'name': item.get_item().name,
                'price': item.get_price(),
                'image': item.get_item().imageUrl.url if item.get_item().imageUrl else '',
                'category': item.get_category(),
                'item_type': item.item_type,
            })
    
    context = {
        'cards': cards,
        'offers': offers,
        'arrivals': arrivals,
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
    }
    
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def buy(request):
    offers = Offers.objects.all()
    arrivals = NewArrivals.objects.all()
    
    # Get cart count
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            cart_count = 0
    
    context = {
        'offers': offers,
        'kids_arrivals': arrivals,
        'cart_count': cart_count,
    }
    
    return render(request, 'buy.html', context)

def shop_offers(request):
    offer = Offers.objects.all()
    return render(request, 'shop_offers.html', {
        'kids_offers' : offer.filter(category='kids'),
        'men_offers' : offer.filter(category='men'),
        'women_offers' : offer.filter(category='women'),
        })
    
def new_arrivals(request):
    new_arrivals = NewArrivals.objects.all()
    return render(request, 'new_arrivals.html', {
        'kids_arrivals' : new_arrivals.filter(category='kids'),
        'men_arrivals' : new_arrivals.filter(category='men'),
        'women_arrivals' : new_arrivals.filter(category='women'),
    })


# Authentication views
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Transfer session cart to user cart
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            
            try:
                session_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
                user_cart, created = Cart.objects.get_or_create(user=user)
                
                # Move items from session cart to user cart
                for item in session_cart.items.all():
                    item.cart = user_cart
                    item.save()
                
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
            
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        auth_login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('index')
    
    return render(request, 'signup.html')


def user_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')


def profile(request):
    return render(request, 'profile.html')

def product_detail(request, product_type, product_id):
    product = None
    product2 = None
    cart_count = 0
    
    # Get cart count
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            cart_count = 0
    
    if product_type == 'offer':
        try:
            product = Offers.objects.get(id=product_id)
        except Offers.DoesNotExist:
            messages.error(request, 'Product not found')
            return redirect('buy')
    elif product_type == 'arrival':
        try:
            product2 = NewArrivals.objects.get(id=product_id)
        except NewArrivals.DoesNotExist:
            messages.error(request, 'Product not found')
            return redirect('new_arrivals')
    elif product_type == 'toy':
        try:
            product = Toy.objects.get(id=product_id)
        except Toy.DoesNotExist:
            messages.error(request, 'Toy not found')
            return redirect('toys_page')
    elif product_type == 'cloth':
        try:
            product = Cloths.objects.get(id=product_id)
        except Cloths.DoesNotExist:
            messages.error(request, 'Cloth not found')
            return redirect('cloths')
    
    return render(request, 'product_detail.html', {
        'product': product,
        'product2': product2,
        'product_type': product_type,
        'cart_count': cart_count,
    })


def cloths(request):
    return render(request, 'cloths.html')

def toys(request):  
    return render(request, 'toys.html')

    
def kids_cloths(request):
    kids_cloths = Cloths.objects.filter(category='kids-men')
    kids_girls_cloths = Cloths.objects.filter(category='kids-girl')
    return render(request, 'kids_cloths.html', {'kids_cloths': kids_cloths, 'kids_girls_cloths': kids_girls_cloths})

def women_cloths(request):
    women_cloths = Cloths.objects.filter(category='women')
    return render(request, 'women_cloths.html', {'women_cloths': women_cloths})


def mens_cloths(request):
    mens_cloths = Cloths.objects.filter(category='men')
    return render(request, 'mens_cloths.html', {'mens_cloths': mens_cloths})

def reviews(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('review_success')  
    else:
        form = ReviewForm()
    
    # Get latest 20 reviews
    latest_reviews = Review.objects.all()[:20]
    
    return render(request, 'reviews.html', {'form': form, 'latest_reviews': latest_reviews})

def review_success(request):
    return render(request, 'review_success.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! We received your message and will get back to you soon.')
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')


def toys_page(request):
    # Get filter parameters
    category = request.GET.get('category', 'all')
    age_range = request.GET.get('age', 'all')
    
    # Filter toys
    toys = Toy.objects.all()
    
    if category != 'all':
        toys = toys.filter(category=category)
    
    if age_range != 'all':
        toys = toys.filter(age_range=age_range)
    
    # Get featured toys
    featured_toys = Toy.objects.filter(is_bestseller=True)[:4]
    new_toys = Toy.objects.filter(is_new=True)[:4]
    
    context = {
        'toys': toys,
        'featured_toys': featured_toys,
        'new_toys': new_toys,
        'selected_category': category,
        'selected_age': age_range,
    }
    
    return render(request, 'toys.html', context)


# Cart views
def cart_page(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    items_data = []
    for item in cart_items:
        product = item.get_item()
        items_data.append({
            'id': item.id,
            'name': product.name if hasattr(product, 'name') else product.title,
            'price': item.get_price(),
            'quantity': item.quantity,
            'subtotal': item.get_subtotal(),
            'image': product.imageUrl.url if product.imageUrl else '',
            'item_type': item.item_type,
        })
    
    context = {
        'cart_items': items_data,
        'cart_count': cart.get_item_count(),
        'subtotal': cart.get_total(),
        'tax': cart.get_total() * Decimal('0.1'),
        'total': cart.get_total() * Decimal('1.1'),
    }
    
    return render(request, 'cart.html', context)


def _wants_json(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', '')

def add_to_cart(request, item_type, item_id):
    try:
        cart = get_or_create_cart(request)
        
        # Get the product based on item_type
        item = None
        if item_type == 'cloth':
            item = get_object_or_404(Cloths, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='cloth',
                cloth=item,
                defaults={'quantity': 1}
            )
        elif item_type == 'toy':
            item = get_object_or_404(Toy, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='toy',
                toy=item,
                defaults={'quantity': 1}
            )
        elif item_type == 'offer':
            item = get_object_or_404(Offers, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='offer',
                offer=item,
                defaults={'quantity': 1}
            )
        elif item_type == 'arrival':
            item = get_object_or_404(NewArrivals, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='arrival',
                arrival=item,
                defaults={'quantity': 1}
            )
        else:
            if _wants_json(request):
                return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)
            messages.error(request, 'Invalid item type')
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        item_name = item.name if hasattr(item, 'name') else item.title
        success_msg = f'✓ Added {item_name} to cart!'

        if request.method == 'POST' or _wants_json(request):
            return JsonResponse({
                'success': True,
                'message': success_msg,
                'cart_count': cart.get_item_count(),
                'cart_total': float(cart.get_total())
            })

        messages.success(request, success_msg)
        return redirect(request.META.get('HTTP_REFERER', 'cart'))

    except Exception as e:
        if request.method == 'POST' or _wants_json(request):
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        messages.error(request, f'Error: {str(e)}')
        return redirect(request.META.get('HTTP_REFERER', 'index'))


@require_POST
def update_cart_item(request, cart_item_id):
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'}, status=400)
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total()),
            'item_subtotal': float(cart_item.get_subtotal())
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def remove_from_cart(request, cart_item_id):
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        
        item = cart_item.get_item()
        item_name = item.name if hasattr(item, 'name') else item.title
        
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Removed {item_name} from cart',
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total())
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def clear_cart(request):
    try:
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared',
            'cart_count': 0,
            'cart_total': 0
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def get_cart_data(request):
    """API endpoint to get cart data as JSON"""
    try:
        cart = get_or_create_cart(request)
        items_data = []

        for item in cart.items.all():
            try:
                product = item.get_item()
                if not product:
                    continue
                items_data.append({
                    'id': item.id,
                    'name': product.name if hasattr(product, 'name') else product.title,
                    'price': float(item.get_price()),
                    'quantity': int(item.quantity),
                    'subtotal': float(item.get_subtotal()),
                    'image': product.imageUrl.url if getattr(product, 'imageUrl', None) else '',
                    'item_type': item.item_type,
                })
            except Exception:
                continue

        subtotal = float(cart.get_total())
        tax = round(subtotal * 0.1, 2)
        total = round(subtotal + tax, 2)

        return JsonResponse({
            'success': True,
            'items': items_data,
            'cart_count': cart.get_item_count(),
            'subtotal': round(subtotal, 2),
            'tax': tax,
            'total': total
        })

    except Exception as e:
        return JsonResponse({
            'success': True,  # keep frontend alive, show empty cart instead of breaking
            'items': [],
            'cart_count': 0,
            'subtotal': 0.0,
            'tax': 0.0,
            'total': 0.0,
            'error': str(e),
        })


def cart_details(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart_details_page.html', {
        'cart': cart,
        'cart_count': cart.get_item_count(),
    })


# Wishlist views
@login_required(login_url='login')
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    
    cloth_items = wishlist_items.filter(item_type='cloth')
    toy_items = wishlist_items.filter(item_type='toy')
    
    total_count = wishlist_items.count()
    cloth_count = cloth_items.count()
    toy_count = toy_items.count()
    
    context = {
        'wishlist_items': wishlist_items,  
        'toy_items': toy_items,             
        'total_count': total_count,
        'cloth_count': cloth_count,
        'toy_count': toy_count,
    }
    
    return render(request, 'wishlist.html', context)
    
    
@login_required(login_url='login')
def add_to_wishlist(request, item_type, item_id):
    try:
        
        if item_type == 'cloth':
            item = get_object_or_404(Cloths, id=item_id)
            
            
            wishlist_item, created = WishlistItem.objects.get_or_create(
                user=request.user,
                item_type='cloth',
                cloth=item
            )
        
        elif item_type == 'toy':
            item = get_object_or_404(Toy, id=item_id)
            
            
            wishlist_item, created = WishlistItem.objects.get_or_create(
                user=request.user,
                item_type='toy',
                toy=item
            )
        
        else:
            messages.error(request, 'Invalid item type')
            return redirect('wishlist')
        
        if created:
            messages.success(request, f'✓ Added {item.name} to wishlist!')
        else:
            messages.info(request, f'{item.name} is already in your wishlist')
            
            
        return redirect('wishlist')
    
    except Cloths.DoesNotExist:
        messages.error(request, 'Cloth product not found')
        return redirect('buy')
    except Toy.DoesNotExist:
        messages.error(request, 'Toy product not found')
        return redirect('toys')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('wishlist')


@login_required(login_url='login')
def remove_from_wishlist(request, wishlist_id):
    try:
        wishlist_item = get_object_or_404(
            WishlistItem,
            id=wishlist_id,
            user=request.user
        )
        
        product_name = wishlist_item.get_item().name
        
        wishlist_item.delete()
        
        messages.success(request, f'✓ Removed {product_name} from wishlist')
    
    except WishlistItem.DoesNotExist:
        messages.error(request, 'Item not found in your wishlist')
    except Exception as e:
        messages.error(request, f'Error removing item: {str(e)}')
    
    return redirect('wishlist')


@login_required(login_url='login')
def move_to_cart(request, wishlist_id):
    try:
        wishlist_item = get_object_or_404(
            WishlistItem,
            id=wishlist_id,
            user=request.user
        )
        
        item = wishlist_item.get_item()
        product_name = item.name
        
        # Add to cart
        cart = get_or_create_cart(request)
        
        if wishlist_item.item_type == 'cloth':
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='cloth',
                cloth=wishlist_item.cloth,
                defaults={'quantity': 1}
            )
        elif wishlist_item.item_type == 'toy':
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='toy',
                toy=wishlist_item.toy,
                defaults={'quantity': 1}
            )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        # Remove from wishlist
        wishlist_item.delete()
        
        messages.success(request, f'✓ Moved {product_name} to cart!')
    
    except WishlistItem.DoesNotExist:
        messages.error(request, 'Item not found')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('wishlist')


# Checkout and Order views
@login_required(login_url='login')
def checkout(request):
    cart = get_or_create_cart(request)
    
    if cart.get_item_count() == 0:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart_details')
    
    if request.method == 'POST':
        # Validate required fields
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        country = request.POST.get('country', '').strip()
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')
        
        # Check all required fields are filled
        if not all([full_name, email, phone, address, city, postal_code, country]):
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'checkout.html', {
                'cart': cart,
                'cart_items': cart.items.all(),
                'subtotal': float(Decimal(str(cart.get_total()))),
                'tax': float(Decimal(str(cart.get_total())) * Decimal('0.10')),
                'shipping': 10.00,
                'total': float(Decimal(str(cart.get_total())) * Decimal('1.10') + Decimal('10.00'))
            })
        
        try:
            # Create order
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            subtotal = Decimal(str(cart.get_total()))
            tax = subtotal * Decimal('0.10')
            shipping = Decimal('10.00')
            total = subtotal + tax + shipping
            
            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                country=country,
                subtotal=subtotal,
                tax=tax,
                shipping=shipping,
                total=total,
                payment_method=payment_method
            )
            
            # Create order items
            for cart_item in cart.items.all():
                item = cart_item.get_item()
                item_name = item.name if hasattr(item, 'name') else item.title
                OrderItem.objects.create(
                    order=order,
                    item_name=item_name,
                    item_type=cart_item.item_type,
                    quantity=cart_item.quantity,
                    price=Decimal(str(cart_item.get_price())),
                    subtotal=Decimal(str(cart_item.get_subtotal()))
                )
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, f'Order {order_number} placed successfully!')
            return redirect('order_success', order_number=order_number)
        
        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
            return render(request, 'checkout.html', {
                'cart': cart,
                'cart_items': cart.items.all(),
                'subtotal': float(Decimal(str(cart.get_total()))),
                'tax': float(Decimal(str(cart.get_total())) * Decimal('0.10')),
                'shipping': 10.00,
                'total': float(Decimal(str(cart.get_total())) * Decimal('1.10') + Decimal('10.00'))
            })
    
    # GET request - show checkout form
    subtotal = Decimal(str(cart.get_total()))
    tax = subtotal * Decimal('0.10')
    shipping = Decimal('10.00')
    total = subtotal + tax + shipping
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'subtotal': float(subtotal),
        'tax': float(tax),
        'shipping': float(shipping),
        'total': float(total)
    }
    
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    
    return render(request, 'order_success.html', context)