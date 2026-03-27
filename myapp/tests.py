from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import (
    Cloths, Toy, Offers, NewArrivals, Cart, CartItem, Order, OrderItem,
    Inventory, Coupon, WishlistItem, ProductVariant, Review, ContactMessage,
)
from django.utils import timezone
from datetime import timedelta


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='TestPass123!')
        self.cloth = Cloths.objects.create(
            name='Test Shirt', price='1000', price1='1200', price2='1000',
            desccription='A test shirt', category='men'
        )
        self.toy = Toy.objects.create(
            name='Test Toy', description='A test toy', category='educational',
            age_range='3-5', price=Decimal('500'), imageUrl='toys/test.jpg'
        )

    def test_cloth_creation(self):
        self.assertEqual(self.cloth.name, 'Test Shirt')
        self.assertEqual(str(self.cloth), 'Test Shirt')

    def test_toy_creation(self):
        self.assertEqual(self.toy.name, 'Test Toy')
        self.assertEqual(self.toy.price, Decimal('500'))

    def test_toy_discount_percentage(self):
        self.toy.original_price = Decimal('1000')
        self.toy.save()
        self.assertEqual(self.toy.discount_percentage, 50)

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), 'Cart for testuser')
        self.assertEqual(cart.get_total(), 0.0)
        self.assertEqual(cart.get_item_count(), 0)

    def test_cart_item_operations(self):
        cart = Cart.objects.create(user=self.user)
        ci = CartItem.objects.create(cart=cart, item_type='toy', toy=self.toy, quantity=2)
        self.assertEqual(ci.get_price(), 500.0)
        self.assertEqual(ci.get_subtotal(), 1000.0)
        self.assertEqual(cart.get_item_count(), 2)

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user, order_number='ORD-TEST0001',
            full_name='Test User', email='test@test.com', phone='123',
            address='123 St', city='Colombo', postal_code='10100', country='LK',
            subtotal=Decimal('1000'), tax=Decimal('100'), total=Decimal('1110'),
        )
        self.assertEqual(order.status, 'pending')
        self.assertEqual(str(order), 'Order ORD-TEST0001 - testuser')

    def test_inventory(self):
        inv = Inventory.objects.create(product_type='toy', toy=self.toy, stock=10, low_stock_threshold=5)
        self.assertTrue(inv.is_in_stock)
        self.assertFalse(inv.is_low_stock)
        inv.stock = 3
        inv.save()
        self.assertTrue(inv.is_low_stock)
        inv.stock = 0
        inv.save()
        self.assertFalse(inv.is_in_stock)

    def test_coupon_validity(self):
        coupon = Coupon.objects.create(
            code='TEST20', discount_type='percentage', discount_value=Decimal('20'),
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=30),
            is_active=True,
        )
        self.assertTrue(coupon.is_valid())
        discount = coupon.get_discount(Decimal('1000'))
        self.assertEqual(discount, Decimal('200.00'))

    def test_expired_coupon(self):
        coupon = Coupon.objects.create(
            code='EXPIRED', discount_type='fixed', discount_value=Decimal('100'),
            valid_from=timezone.now() - timedelta(days=30),
            valid_until=timezone.now() - timedelta(days=1),
            is_active=True,
        )
        self.assertFalse(coupon.is_valid())

    def test_wishlist_item(self):
        wi = WishlistItem.objects.create(user=self.user, item_type='cloth', cloth=self.cloth)
        self.assertEqual(wi.get_item(), self.cloth)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='TestPass123!')
        self.cloth = Cloths.objects.create(
            name='View Test Shirt', price='1500', price2='1500',
            desccription='Test', category='men', imageUrl='cloths/test.jpg'
        )
        self.toy = Toy.objects.create(
            name='View Test Toy', description='Test', category='educational',
            age_range='3-5', price=Decimal('750'), imageUrl='toys/test.jpg'
        )

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_buy_page(self):
        response = self.client.get(reverse('buy'))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        response = self.client.get(reverse('search'), {'q': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        response = self.client.get(reverse('product_detail', args=['cloth', self.cloth.id]))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_and_redirect(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'TestPass123!'})
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_cart_page(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('add_to_cart', args=['toy', self.toy.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

    def test_wishlist_add(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('add_to_wishlist', args=['cloth', self.cloth.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WishlistItem.objects.filter(user=self.user).count(), 1)

    def test_checkout_empty_cart(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)

    def test_stock_status_api(self):
        Inventory.objects.create(product_type='toy', toy=self.toy, stock=10)
        response = self.client.get(reverse('stock_status_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('products', data)

    def test_api_products(self):
        response = self.client.get(reverse('api_products'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('products', data)

    def test_validate_coupon(self):
        Coupon.objects.create(
            code='TESTCPN', discount_type='percentage', discount_value=Decimal('10'),
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=30),
            is_active=True,
        )
        response = self.client.post(
            reverse('validate_coupon'),
            data='{"code": "TESTCPN", "subtotal": 1000}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['valid'])

    def test_validate_coupon_invalid(self):
        response = self.client.post(
            reverse('validate_coupon'),
            data='{"code": "NONEXISTENT", "subtotal": 1000}',
            content_type='application/json',
        )
        data = response.json()
        self.assertFalse(data['valid'])

    def test_shop_offers_page(self):
        response = self.client.get(reverse('shop_offers'))
        self.assertEqual(response.status_code, 200)

    def test_new_arrivals_page(self):
        response = self.client.get(reverse('new_arrivals'))
        self.assertEqual(response.status_code, 200)

    def test_kids_cloths_page(self):
        response = self.client.get(reverse('kids_cloths'))
        self.assertEqual(response.status_code, 200)

    def test_women_cloths_page(self):
        response = self.client.get(reverse('women_cloths'))
        self.assertEqual(response.status_code, 200)

    def test_mens_cloths_page(self):
        response = self.client.get(reverse('mens_cloths'))
        self.assertEqual(response.status_code, 200)

    def test_toys_page(self):
        response = self.client.get(reverse('toys_page'))
        self.assertEqual(response.status_code, 200)

    def test_cloths_page(self):
        response = self.client.get(reverse('cloths'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_page(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)

    def test_search_empty_query(self):
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertEqual(response.status_code, 200)

    def test_product_detail_toy(self):
        response = self.client.get(reverse('product_detail', args=['toy', self.toy.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_invalid_type(self):
        response = self.client.get(reverse('product_detail', args=['invalid', 1]))
        self.assertEqual(response.status_code, 302)

    def test_cart_details_page(self):
        response = self.client.get(reverse('cart_details'))
        self.assertEqual(response.status_code, 200)

    def test_get_cart_data_api(self):
        response = self.client.get(reverse('get_cart_data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 0)

    def test_add_to_cart_invalid_type(self):
        response = self.client.post(
            reverse('add_to_cart', args=['invalid', 1]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 400)

    def test_wishlist_requires_login(self):
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 302)

    def test_checkout_requires_login(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)

    def test_my_orders_requires_login(self):
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 302)

    def test_payment_page_requires_login(self):
        response = self.client.get(reverse('payment_page'))
        self.assertEqual(response.status_code, 302)

    def test_profile_authenticated(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_my_orders_authenticated(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 200)

    def test_wishlist_authenticated(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)

    def test_update_cart_item(self):
        self.client.login(username='testuser', password='TestPass123!')
        cart = Cart.objects.create(user=self.user)
        ci = CartItem.objects.create(cart=cart, item_type='toy', toy=self.toy, quantity=1)
        response = self.client.post(
            reverse('update_cart_item', args=[ci.id]),
            data='{"quantity": 3}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        ci.refresh_from_db()
        self.assertEqual(ci.quantity, 3)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='TestPass123!')
        cart = Cart.objects.create(user=self.user)
        ci = CartItem.objects.create(cart=cart, item_type='toy', toy=self.toy, quantity=1)
        response = self.client.post(reverse('remove_from_cart', args=[ci.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CartItem.objects.filter(id=ci.id).exists())

    def test_clear_cart(self):
        self.client.login(username='testuser', password='TestPass123!')
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, item_type='toy', toy=self.toy, quantity=1)
        response = self.client.post(reverse('clear_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items.count(), 0)

    def test_signup_flow(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser', 'email': 'new@test.com',
            'password': 'StrongPass123!', 'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser2', 'email': 'new2@test.com',
            'password': 'StrongPass123!', 'password2': 'DifferentPass123!',
        })
        self.assertEqual(response.status_code, 200)  # stays on signup page

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)  # stays on login page

    def test_logout(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_update_profile(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('update_profile'),
            data='{"first_name": "Test", "last_name": "User"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')

    def test_change_password(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('change_password'),
            data='{"current_password": "TestPass123!", "new_password": "NewStrongPass456!", "confirm_password": "NewStrongPass456!"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewStrongPass456!'))

    def test_change_password_wrong_current(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('change_password'),
            data='{"current_password": "wrong", "new_password": "New123!", "confirm_password": "New123!"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_product_variants_api(self):
        response = self.client.get(reverse('get_product_variants', args=[self.cloth.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('variants', data)

    def test_dashboard_requires_staff(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_dashboard_staff_access(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_api_products_with_filter(self):
        response = self.client.get(reverse('api_products'), {'type': 'cloth', 'q': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_search_ajax(self):
        response = self.client.get(
            reverse('search'), {'q': 'test'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)

    def test_checkout_full_flow(self):
        self.client.login(username='testuser', password='TestPass123!')
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, item_type='toy', toy=self.toy, quantity=1)
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test User', 'email': 'test@test.com', 'phone': '123456',
            'address': '123 Main St', 'city': 'Colombo', 'postal_code': '10100',
            'country': 'LK', 'payment_method': 'cash_on_delivery',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())

    def test_order_success_page(self):
        self.client.login(username='testuser', password='TestPass123!')
        order = Order.objects.create(
            user=self.user, order_number='ORD-VIEW0001',
            full_name='Test', email='t@t.com', phone='1', address='a',
            city='c', postal_code='p', country='c',
            subtotal=Decimal('100'), tax=Decimal('10'), total=Decimal('110'),
        )
        response = self.client.get(reverse('order_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)

    def test_order_tracking_page(self):
        self.client.login(username='testuser', password='TestPass123!')
        order = Order.objects.create(
            user=self.user, order_number='ORD-TRACK001',
            full_name='Test', email='t@t.com', phone='1', address='a',
            city='c', postal_code='p', country='c',
            subtotal=Decimal('100'), tax=Decimal('10'), total=Decimal('110'),
        )
        response = self.client.get(reverse('order_tracking', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)

    def test_reorder(self):
        self.client.login(username='testuser', password='TestPass123!')
        order = Order.objects.create(
            user=self.user, order_number='ORD-REORDER1',
            full_name='Test', email='t@t.com', phone='1', address='a',
            city='c', postal_code='p', country='c',
            subtotal=Decimal('750'), tax=Decimal('75'), total=Decimal('825'),
        )
        OrderItem.objects.create(
            order=order, item_name='View Test Toy', item_type='toy',
            quantity=1, price=Decimal('750'), subtotal=Decimal('750'),
        )
        response = self.client.get(reverse('reorder', args=[order.order_number]))
        self.assertEqual(response.status_code, 302)


class ContextProcessorTests(TestCase):
    def test_breadcrumbs_on_about(self):
        response = self.client.get(reverse('about'))
        self.assertIn('breadcrumbs', response.context)
        crumbs = response.context['breadcrumbs']
        self.assertEqual(len(crumbs), 1)
        self.assertEqual(crumbs[0]['label'], 'About Us')

    def test_breadcrumbs_on_home(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['breadcrumbs'], [])

    def test_cart_count_in_context(self):
        response = self.client.get(reverse('index'))
        self.assertIn('cart_count', response.context)
        self.assertEqual(response.context['cart_count'], 0)

    def test_admin_dashboard_requires_staff(self):
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)


class AuthenticationTests(TestCase):
    """Comprehensive tests for authentication flow"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='authuser', 
            email='auth@test.com', 
            password='SecurePass123!'
        )
    
    def test_signup_with_valid_data(self):
        """Test successful user signup with valid credentials"""
        response = self.client.post(reverse('signup'), {
            'username': 'validuser',
            'email': 'valid@test.com',
            'password': 'ValidPass123!',
            'password2': 'ValidPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='validuser').exists())
        new_user = User.objects.get(username='validuser')
        self.assertEqual(new_user.email, 'valid@test.com')
    
    def test_signup_duplicate_username(self):
        """Test signup fails with duplicate username"""
        response = self.client.post(reverse('signup'), {
            'username': 'authuser',  # existing username
            'email': 'new@test.com',
            'password': 'ValidPass123!',
            'password2': 'ValidPass123!',
        })
        self.assertEqual(response.status_code, 200)
        # Count should still be 1 (original user)
        self.assertEqual(User.objects.filter(username='authuser').count(), 1)
    
    def test_signup_duplicate_email(self):
        """Test signup fails with duplicate email"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'auth@test.com',  # existing email
            'password': 'ValidPass123!',
            'password2': 'ValidPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_signup_weak_password(self):
        """Test signup fails with weak password"""
        response = self.client.post(reverse('signup'), {
            'username': 'weakpass',
            'email': 'weak@test.com',
            'password': '123',  # too weak
            'password2': '123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='weakpass').exists())
    
    def test_signup_password_mismatch(self):
        """Test signup fails when passwords don't match"""
        response = self.client.post(reverse('signup'), {
            'username': 'mismatch',
            'email': 'mismatch@test.com',
            'password': 'ValidPass123!',
            'password2': 'DifferentPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatch').exists())
    
    def test_login_with_valid_credentials(self):
        """Test successful login with correct username/password"""
        response = self.client.post(reverse('login'), {
            'username': 'authuser',
            'password': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)
        # Check session contains user
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)
    
    def test_login_invalid_username(self):
        """Test login fails with non-existent username"""
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent',
            'password': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_login_wrong_password(self):
        """Test login fails with incorrect password"""
        response = self.client.post(reverse('login'), {
            'username': 'authuser',
            'password': 'WrongPassword123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_logout_clears_session(self):
        """Test logout properly clears session"""
        self.client.login(username='authuser', password='SecurePass123!')
        self.assertIn('_auth_user_id', self.client.session)
        
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_login_redirects_to_buy_page(self):
        """Test login redirects to buy page by default"""
        response = self.client.post(
            reverse('login'),
            {'username': 'authuser', 'password': 'SecurePass123!'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_signup_redirects_to_index(self):
        """Test signup redirects to index after success"""
        response = self.client.post(
            reverse('signup'), {
                'username': 'newuser',
                'email': 'new@test.com',
                'password': 'ValidPass123!',
                'password2': 'ValidPass123!',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_profile_view_authenticated(self):
        """Test authenticated user can access profile"""
        self.client.login(username='authuser', password='SecurePass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.context)
        self.assertIn('reviews', response.context)
    
    def test_profile_requires_authentication(self):
        """Test unauthenticated user is redirected from profile"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_update_profile_success(self):
        """Test updating user profile information"""
        self.client.login(username='authuser', password='SecurePass123!')
        response = self.client.post(
            reverse('update_profile'),
            data='{"first_name": "Auth", "last_name": "User"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Auth')
        self.assertEqual(self.user.last_name, 'User')
    
    def test_change_password_success(self):
        """Test password change with correct current password"""
        self.client.login(username='authuser', password='SecurePass123!')
        response = self.client.post(
            reverse('change_password'),
            data='{"current_password": "SecurePass123!", "new_password": "NewSecure456!", "confirm_password": "NewSecure456!"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecure456!'))
    
    def test_change_password_wrong_current(self):
        """Test password change fails with wrong current password"""
        self.client.login(username='authuser', password='SecurePass123!')
        response = self.client.post(
            reverse('change_password'),
            data='{"current_password": "WrongPassword", "new_password": "NewSecure456!", "confirm_password": "NewSecure456!"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('NewSecure456!'))
    
    def test_change_password_mismatch(self):
        """Test password change fails when new passwords don't match"""
        self.client.login(username='authuser', password='SecurePass123!')
        response = self.client.post(
            reverse('change_password'),
            data='{"current_password": "SecurePass123!", "new_password": "NewSecure456!", "confirm_password": "DifferentSecure456!"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
    
    def test_update_email(self):
        """Test updating user email address"""
        self.client.login(username='authuser', password='SecurePass123!')
        response = self.client.post(
            reverse('update_email'),
            data='{"new_email": "newemail@test.com", "password": "SecurePass123!"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@test.com')
    
    def test_update_email_duplicate(self):
        """Test email update fails if email already exists"""
        # Create another user
        User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='OtherPass123!'
        )
        
        self.client.login(username='authuser', password='SecurePass123!')
        response = self.client.post(
            reverse('update_email'),
            data='{"new_email": "other@test.com", "password": "SecurePass123!"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
    
    def test_session_cart_transfer_on_login(self):
        """Test session cart items are transferred to user cart on login"""
        # Add item to session cart (guest user)
        toy = Toy.objects.create(
            name='Cart Test Toy', 
            description='Test', 
            category='educational',
            age_range='3-5', 
            price=Decimal('500'), 
            imageUrl='toys/test.jpg'
        )
        
        # Create session
        session = self.client.session
        session.create()
        session_key = session.session_key
        
        # Create session cart
        session_cart = Cart.objects.create(session_key=session_key)
        CartItem.objects.create(cart=session_cart, item_type='toy', toy=toy, quantity=1)
        
        # Login (should transfer cart)
        response = self.client.post(reverse('login'), {
            'username': 'authuser',
            'password': 'SecurePass123!',
        })
        
        # Check user now has the cart item
        user_cart = Cart.objects.get(user=self.user)
        self.assertEqual(user_cart.items.count(), 1)


class SearchAndFilterTests(TestCase):
    """Comprehensive tests for search and filter functionality"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test products with different prices
        self.cloth1 = Cloths.objects.create(
            name='Budget T-Shirt', 
            price='500', price1='500', price2='500',
            desccription='Affordable basic t-shirt',
            category='men',
            subcategory='tops'
        )
        
        self.cloth2 = Cloths.objects.create(
            name='Premium Dress Shirt',
            price='2500', price1='2500', price2='2500',
            desccription='High-quality dress shirt',
            category='men',
            subcategory='formal'
        )
        
        self.cloth3 = Cloths.objects.create(
            name='Women Premium Top',
            price='1800', price1='1800', price2='1800',
            desccription='Elegant women top',
            category='women',
            subcategory='tops'
        )
        
        self.cloth4 = Cloths.objects.create(
            name='Kids T-Shirt Blue',
            price='700', price1='700', price2='700',
            desccription='Colorful kids shirt',
            category='kids-men',
            subcategory='tops'
        )
        
        self.toy1 = Toy.objects.create(
            name='Educational Robot',
            description='Learn coding with this robot',
            category='educational',
            age_range='8-12',
            price=Decimal('1500'),
            imageUrl='toys/robot.jpg'
        )
        
        self.toy2 = Toy.objects.create(
            name='Action Figure Marvel',
            description='Superhero action figure',
            category='action',
            age_range='5-10',
            price=Decimal('800'),
            imageUrl='toys/figure.jpg'
        )
        
        self.offer1 = Offers.objects.create(
            title='Summer Clearance Sale',
            description='Big discounts on summer items',
            price1=Decimal('999'),
            price2=Decimal('499'),
            category='discount',
            imageUrl='offers/summer.jpg'
        )

    # ==================== SEARCH TESTS ====================
    
    def test_search_by_clothing_name(self):
        """Test search finds clothing by name"""
        response = self.client.get(reverse('search'), {'q': 'Budget'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.cloth1, response.context['results'].object_list[0]['name'] if response.context['results'] else [])
    
    def test_search_empty_query(self):
        """Test search with empty query returns no results"""
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total'], 0)
    
    def test_search_across_product_types(self):
        """Test search works across multiple product types"""
        # Should find both toys and clothes
        response = self.client.get(reverse('search'), {'q': 'robot'})
        self.assertEqual(response.status_code, 200)
        results = response.context['results'].object_list
        self.assertGreater(len(results), 0)
    
    def test_search_case_insensitive(self):
        """Test search is case-insensitive"""
        response1 = self.client.get(reverse('search'), {'q': 'BUDGET'})
        response2 = self.client.get(reverse('search'), {'q': 'budget'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        # Both should return results
        self.assertGreater(response1.context['total'], 0)
    
    def test_search_by_description(self):
        """Test search finds products by description"""
        response = self.client.get(reverse('search'), {'q': 'coding'})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.context['total'], 0)
    
    def test_search_ajax_request(self):
        """Test search returns JSON for AJAX requests"""
        response = self.client.get(
            reverse('search'),
            {'q': 'shirt'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('has_next', data)
        self.assertIn('total', data)
    
    def test_search_pagination(self):
        """Test search results are paginated"""
        response = self.client.get(reverse('search'), {'q': 'shirt', 'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.context)
        self.assertTrue(hasattr(response.context['results'], 'paginator'))
    
    def test_search_returns_product_details(self):
        """Test search returns proper product details"""
        response = self.client.get(reverse('search'), {'q': 'Budget'})
        results = response.context['results'].object_list
        if results:
            result = results[0]
            self.assertIn('name', result)
            self.assertIn('price', result)
            self.assertIn('type', result)
            self.assertIn('url', result)

    # ==================== FILTER TESTS - PRICE ====================
    
    def test_filter_by_min_price(self):
        """Test filtering products by minimum price"""
        response = self.client.get(reverse('mens_cloths'), {
            'min_price': '1000'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        # Only Premium Dress Shirt (2500) should be in results
        prices = [p.price for p in products]
        self.assertTrue(all(int(p) >= 1000 for p in prices if p))
    
    def test_filter_by_max_price(self):
        """Test filtering products by maximum price"""
        response = self.client.get(reverse('mens_cloths'), {
            'max_price': '1000'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        # Products should be <= 1000
        prices = [p.price for p in products]
        self.assertTrue(all(int(p) <= 1000 for p in prices if p))
    
    def test_filter_by_price_range(self):
        """Test filtering products by price range"""
        response = self.client.get(reverse('mens_cloths'), {
            'min_price': '500',
            'max_price': '2000'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        # Products should be in range 500-2000
        prices = [p.price for p in products]
        self.assertTrue(all(500 <= int(p) <= 2000 for p in prices if p))
    
    def test_filter_price_with_invalid_input(self):
        """Test price filter handles invalid input gracefully"""
        response = self.client.get(reverse('mens_cloths'), {
            'min_price': 'invalid',
            'max_price': 'notanumber'
        })
        # Should not crash and return all products
        self.assertEqual(response.status_code, 200)
    
    def test_filter_women_cloths_by_price(self):
        """Test price filtering on women's clothing"""
        response = self.client.get(reverse('women_cloths'), {
            'min_price': '1000',
            'max_price': '2500'
        })
        self.assertEqual(response.status_code, 200)
        # Women Premium Top (1800) should be in results
        products = response.context['women_cloths'].object_list
        self.assertGreater(len(products), 0)

    # ==================== FILTER TESTS - CATEGORY ====================
    
    def test_filter_by_category_men(self):
        """Test filtering products by men category"""
        response = self.client.get(reverse('mens_cloths'))
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        # All should be men category
        self.assertTrue(all(p.category == 'men' for p in products))
    
    def test_filter_by_category_women(self):
        """Test filtering products by women category"""
        response = self.client.get(reverse('women_cloths'))
        self.assertEqual(response.status_code, 200)
        products = response.context['women_cloths'].object_list
        # All should be women category
        self.assertTrue(all(p.category == 'women' for p in products))
    
    def test_filter_by_category_kids(self):
        """Test filtering products by kids category"""
        response = self.client.get(reverse('kids_cloths'))
        self.assertEqual(response.status_code, 200)
        products = response.context['all_kids_cloths'].object_list
        # All should be kids category
        self.assertTrue(all(p.category in ['kids-men', 'kids-girl'] for p in products))
    
    def test_filter_toys_by_category(self):
        """Test filtering toys by category"""
        response = self.client.get(reverse('toys_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('toys', response.context)

    # ==================== FILTER TESTS - SUBCATEGORY ====================
    
    def test_filter_by_subcategory(self):
        """Test filtering by subcategory"""
        response = self.client.get(reverse('mens_cloths'), {
            'subcategory': 'tops'
        })
        self.assertEqual(response.status_code, 200)
        # Should have Budget T-Shirt only
        products = response.context['mens_cloths'].object_list
        self.assertGreater(len(products), 0)
    
    def test_filter_subcategory_formal(self):
        """Test filtering formal subcategory"""
        response = self.client.get(reverse('mens_cloths'), {
            'subcategory': 'formal'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        # Premium Dress Shirt should be in results
        self.assertGreater(len(products), 0)

    # ==================== FILTER TESTS - COMBINED ====================
    
    def test_filter_combined_category_and_price(self):
        """Test filtering with both category and price"""
        response = self.client.get(reverse('women_cloths'), {
            'min_price': '1000',
            'max_price': '2500'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['women_cloths'].object_list
        # Check all products are in range
        prices = [p.price for p in products]
        self.assertTrue(all(1000 <= int(p) <= 2500 for p in prices if p))
    
    def test_filter_combined_search_and_category(self):
        """Test filtering with search query and category"""
        response = self.client.get(reverse('mens_cloths'), {
            'q': 'shirt'
        })
        self.assertEqual(response.status_code, 200)
        # Should find shirts in men category

    # ==================== SORTING TESTS ====================
    
    def test_sort_by_price_ascending(self):
        """Test sorting products by price ascending"""
        response = self.client.get(reverse('mens_cloths'), {
            'sort': 'price_asc'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        if len(products) > 1:
            # Extract numeric prices
            prices = [int(p.price) for p in products if p.price]
            self.assertEqual(prices, sorted(prices))
    
    def test_sort_by_price_descending(self):
        """Test sorting products by price descending"""
        response = self.client.get(reverse('mens_cloths'), {
            'sort': 'price_desc'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        if len(products) > 1:
            prices = [int(p.price) for p in products if p.price]
            self.assertEqual(prices, sorted(prices, reverse=True))
    
    def test_sort_by_name_ascending(self):
        """Test sorting products by name ascending"""
        response = self.client.get(reverse('mens_cloths'), {
            'sort': 'name_asc'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        if len(products) > 1:
            names = [p.name.lower() for p in products]
            self.assertEqual(names, sorted(names))
    
    def test_sort_by_name_descending(self):
        """Test sorting products by name descending"""
        response = self.client.get(reverse('mens_cloths'), {
            'sort': 'name_desc'
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['mens_cloths'].object_list
        if len(products) > 1:
            names = [p.name.lower() for p in products]
            self.assertEqual(names, sorted(names, reverse=True))
    
    def test_sort_newest(self):
        """Test sorting by newest (reverse ID)"""
        response = self.client.get(reverse('mens_cloths'), {
            'sort': 'newest'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('mens_cloths', response.context)
    
    def test_sort_oldest(self):
        """Test sorting by oldest (ID)"""
        response = self.client.get(reverse('mens_cloths'), {
            'sort': 'oldest'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('mens_cloths', response.context)

    # ==================== API FILTER TESTS ====================
    
    def test_api_products_by_type(self):
        """Test API filtering by product type"""
        response = self.client.get(reverse('api_products'), {
            'type': 'cloth'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('products', data)
        # Should only have cloth products
        types = [p.get('type') for p in data['products']]
        self.assertTrue(all(t == 'cloth' for t in types))
    
    def test_api_products_by_search_query(self):
        """Test API filtering by search query"""
        response = self.client.get(reverse('api_products'), {
            'q': 'Budget'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('products', data)
        self.assertGreater(data['total'], 0)
    
    def test_api_products_pagination(self):
        """Test API products pagination"""
        response = self.client.get(reverse('api_products'), {
            'page': 1
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('pages', data)
        self.assertIn('current_page', data)
        self.assertIn('has_next', data)
    
    def test_api_products_combined_filters(self):
        """Test API with multiple filters"""
        response = self.client.get(reverse('api_products'), {
            'type': 'cloth',
            'q': 'shirt'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('products', data)


class NavbarSearchTests(TestCase):
    """Tests for navbar live search functionality"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test products
        self.cloth = Cloths.objects.create(
            name='Navy Blue T-Shirt',
            price='800', price1='800', price2='800',
            desccription='Comfortable everyday t-shirt',
            category='men',
            subcategory='tops'
        )
        
        self.toy = Toy.objects.create(
            name='Robot Toy Educational',
            description='Learn coding with robot',
            category='educational',
            age_range='8-12',
            price=Decimal('1500'),
            imageUrl='toys/robot.jpg'
        )
        
        self.offer = Offers.objects.create(
            title='Summer Sale Offer',
            description='Big discount on summer items',
            price1=Decimal('999'),
            price2=Decimal('499'),
            category='discount',
            imageUrl='offers/summer.jpg'
        )
    
    def test_api_products_returns_correct_format(self):
        """Test API returns products in correct JSON format"""
        response = self.client.get(reverse('api_products'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check required fields
        self.assertIn('products', data)
        self.assertIn('total', data)
        self.assertIn('pages', data)
        self.assertIn('current_page', data)
        self.assertIn('has_next', data)
        self.assertIn('has_previous', data)
    
    def test_api_products_search_cloth(self):
        """Test API search finds clothing products"""
        response = self.client.get(reverse('api_products'), {'q': 'Navy'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertGreater(data['total'], 0)
        products = data['products']
        self.assertGreater(len(products), 0)
        
        # Check product structure
        product = products[0]
        self.assertIn('id', product)
        self.assertIn('type', product)
        self.assertIn('name', product)
        self.assertIn('price', product)
        self.assertIn('image', product)
        self.assertIn('url', product)
    
    def test_api_products_search_toy(self):
        """Test API search finds toy products"""
        response = self.client.get(reverse('api_products'), {'q': 'Robot'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertGreater(data['total'], 0)
        # Should find the robot toy
        product_names = [p['name'] for p in data['products']]
        self.assertTrue(any('Robot' in name for name in product_names))
    
    def test_api_products_search_offer(self):
        """Test API search finds offer products"""
        response = self.client.get(reverse('api_products'), {'q': 'Summer'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertGreater(data['total'], 0)
        # Should find the summer sale offer
        product_names = [p['name'] for p in data['products']]
        self.assertTrue(any('Summer' in name for name in product_names))
    
    def test_api_products_filter_by_type(self):
        """Test API filtering by product type"""
        response = self.client.get(reverse('api_products'), {'type': 'cloth'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # All products should be cloth type
        for product in data['products']:
            self.assertEqual(product['type'], 'cloth')
    
    def test_api_products_empty_search(self):
        """Test API with empty search query returns all products"""
        response = self.client.get(reverse('api_products'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should return results
        self.assertGreater(data['total'], 0)
    
    def test_api_products_no_results(self):
        """Test API returns empty when no products match search"""
        response = self.client.get(reverse('api_products'), {
            'q': 'nonexistentproductxyz123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['total'], 0)
        self.assertEqual(len(data['products']), 0)
    
    def test_api_products_pagination_limit(self):
        """Test API pagination works correctly"""
        # Create many products
        for i in range(15):
            Cloths.objects.create(
                name=f'Test Shirt {i}',
                price='500', price1='500', price2='500',
                desccription=f'Test shirt {i}',
                category='men'
            )
        
        response = self.client.get(reverse('api_products'), {'page': 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should be paginated
        self.assertLessEqual(len(data['products']), 12)  # Default pagination is 12
    
    def test_api_products_case_insensitive_search(self):
        """Test API search is case-insensitive"""
        response1 = self.client.get(reverse('api_products'), {'q': 'NAVY'})
        response2 = self.client.get(reverse('api_products'), {'q': 'navy'})
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Both should return same results
        self.assertEqual(data1['total'], data2['total'])
    
    def test_api_products_partial_search(self):
        """Test API search with partial product name"""
        response = self.client.get(reverse('api_products'), {'q': 'Sh'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should find products starting with 'Sh'
        self.assertGreater(data['total'], 0)
    
    def test_navbar_search_form_exists(self):
        """Test navbar includes search form"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        
        # Check navbar search form exists
        self.assertIn('nav-search-input', content)
        self.assertIn('nav-search-results', content)
    
    def test_navbar_search_javascript_loaded(self):
        """Test navbar search JavaScript is included"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        
        # Check JavaScript file is referenced
        self.assertIn('navbar-search.js', content)
    
    def test_api_products_with_multiple_filters(self):
        """Test API with combined search and type filter"""
        response = self.client.get(reverse('api_products'), {
            'type': 'cloth',
            'q': 'Shirt'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # All products should be cloth type
        for product in data['products']:
            self.assertEqual(product['type'], 'cloth')
    
    def test_api_products_json_response_format(self):
        """Test API returns valid JSON format"""
        response = self.client.get(reverse('api_products'))
        self.assertEqual(response.status_code, 200)
        
        # Should be valid JSON
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Should be parseable
        data = response.json()
        self.assertIsInstance(data, dict)
    
    def test_api_products_includes_product_url(self):
        """Test API products include valid URLs"""
        response = self.client.get(reverse('api_products'), {'q': 'Navy'})
        data = response.json()
        
        if data['products']:
            product = data['products'][0]
            # URL should be present and valid
            self.assertIn('url', product)
            self.assertTrue(product['url'].startswith('/product/'))
    
    def test_search_navbar_accessibility(self):
        """Test search navbar is accessible on all pages"""
        pages = ['index', 'buy', 'about']
        
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200)
            content = response.content.decode()
            
            # Navbar search should be on every page
            self.assertIn('nav-search-input', content)
