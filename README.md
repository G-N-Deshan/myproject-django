# E-Commerce Platform - Kids & Family Products Store

A full-featured Django e-commerce platform for selling kids and family products including clothing, toys, and collectible cards.

## 🎯 Project Overview

This is a production-ready e-commerce web application built with Django that provides:
- **Multi-Product E-commerce**: Clothes (men's, women's, kids), Toys, Offers, New Arrivals, and Collectible Cards
- **Shopping Features**: Product catalog, cart management, wishlist, search & filters
- **Checkout & Payment**: Stripe payment integration with COD option
- **Order Management**: Order tracking, invoice generation, reorder functionality
- **Admin Dashboard**: Sales analytics, inventory management, order status tracking
- **User Accounts**: Registration, login, profile management, password recovery
- **Reviews & Ratings**: Customer product reviews and ratings system
- **Responsive Design**: Tailwind CSS frontend with vanilla JavaScript interactions

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 6.0.2
- **Database**: 
  - Local: MySQL (PyMySQL)
  - Production: PostgreSQL (via Neon with dj-database-url)
- **REST API**: Django REST Framework 3.16.1
- **Payment Gateway**: Stripe 14.4.1
- **Authentication**: Django built-in + django-allauth 65.15.0
- **Media Storage**: Cloudinary 1.41.0 (production CDN)
- **HTTP Server**: Gunicorn 23.0.0
- **Static Files Manager**: WhiteNoise 6.12.0

### Frontend
- **Styling**: Tailwind CSS (CDN) with custom brand colors
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla ES6+ (no framework)
- **State Management**: localStorage for cart/wishlist, session-based for authenticated users

### Deployment
- **Platform**: Vercel (serverless Python 3.12)
- **Configuration**: vercel.json with static file routing

## 📁 Project Structure

```
myproject/
├── myproject/              # Django project settings
│   ├── settings.py         # Configuration (dual database, Stripe, Cloudinary)
│   ├── urls.py             # Project URL routing
│   ├── wsgi.py             # WSGI for production
│   └── asgi.py             # ASGI for async
│
├── myapp/                  # Main application
│   ├── models.py           # Data models (13+ models)
│   ├── views.py            # View functions (80+ routes)
│   ├── urls.py             # URL patterns
│   ├── forms.py            # Form definitions
│   ├── admin.py            # Admin interface customization
│   ├── tests.py            # Test suite (70+ test cases)
│   ├── context_processors.py  # Global template context
│   ├── signals.py          # Cache invalidation signals
│   ├── middleware.py       # Custom middleware
│   └── migrations/         # Database migrations (18 migrations)
│
├── templates/              # HTML templates (33 templates)
├── static/                 # CSS/JS files (38 asset files)
│   ├── cart_utils.js       # Cart operations and CSRF handling
│   ├── global.js           # Toast, quick-view modal, live polling
│   ├── live_reload.js      # Admin change detection
│   └── [CSS files]         # Component and page styles
│
├── media/                  # User-uploaded media (images)
├── staticfiles/            # Collected static files (production)
│
├── manage.py               # Django management CLI
├── requirements.txt        # Python dependencies (14 packages)
├── .env.example            # Environment variables template
├── vercel.json             # Vercel deployment config
├── build_files.sh          # Pre-deployment script
├── DEPLOY.md               # Deployment guide
└── db.sqlite3              # SQLite database (development)
```

## 📊 Data Models

### Core Models
- **Products**: Cloths, Toy, Offers, NewArrivals, Card (polymorphic)
- **Shopping**: Cart, CartItem, WishlistItem
- **Orders**: Order, OrderItem, OrderTracking
- **Inventory**: Inventory (stock tracking), ProductVariant, ProductImage
- **Business**: Coupon (discounts), ProductReview, Review (ratings)
- **Content**: ContactMessage, SiteUpdate (cache invalidation)

### User Authentication
- Django User model extended with authentication views
- Profile customization through user fields
- Email-based password recovery

## 🚀 Quick Start

### Local Development Setup

1. **Clone the repository and navigate to project**
   ```bash
   cd myproject
   ```

2. **Create and activate virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file from template**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your local database credentials and API keys.

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files** (for production-like testing)
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```
   
   Access at: http://localhost:8000

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Local Database (MySQL)
DB_ENGINE=mysql
DB_NAME=myproject
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Production Database (PostgreSQL on Neon)
DATABASE_URL=postgresql://user:password@host/dbname

# Stripe Payment Gateway
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Cloudinary Media Storage
CLOUDINARY_URL=cloudinary://key:secret@cloud_name

# Email (for contact form)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Class
```bash
python manage.py test myapp.tests.ModelTests
python manage.py test myapp.tests.ViewTests
python manage.py test myapp.tests.AuthenticationTests
python manage.py test myapp.tests.ContextProcessorTests
```

### Run with Verbose Output
```bash
python manage.py test -v 2
```

### Test Coverage Summary
- **ModelTests**: 13 tests for data models and business logic
- **ViewTests**: 40+ tests for views, API endpoints, and workflows
- **AuthenticationTests**: 20+ comprehensive tests for user auth flow
- **ContextProcessorTests**: 4 tests for template context
- **Total**: 70+ test cases covering critical functionality

## 🔑 Key Features

### Authentication & Authorization
- User signup with email validation
- Secure login with session-based authentication
- Password strength validation
- Forgot password / reset flow
- User profile management
- Email update with verification
- Multiple authentication backends (Django + AllAuth)

### Shopping Experience
- Browse products by category (Men, Women, Kids)
- Search across all product types
- Product filtering and sorting
- Product variants (size, color, etc.)
- Product reviews and ratings
- Quick-view modal popup
- Add to cart / Update quantity
- Persistent cart (session-based for guests, database for logged-in users)
- Session to user cart transfer on login
- Wishlist functionality

### Checkout & Payment
- Cart summary with totals
- Coupon/discount code validation
- Multiple payment methods:
  - Stripe (credit/debit cards)
  - Cash on Delivery (COD)
- Order confirmation emails
- Tax calculation

### Order Management
- Order history and tracking
- Order status updates (pending → processing → shipped → delivered)
- Real-time status notifications
- Reorder functionality
- Order details page with invoice

### Admin Dashboard
- Sales analytics with charts
- Revenue tracking
- Order status overview
- Low stock alerts
- Inventory management
- Product management (CRUD)
- Customer management
- Coupon management
- Contact form submissions

### Real-time Features
- Live stock status polling (30-second intervals)
- Admin change detection (8-second polling)
- Toast notifications for user actions
- Cart update confirmation

## 📱 API Endpoints

### Product APIs
- GET `/api/products/` - List products with filters
- GET `/api/stock-status/` - Live inventory status
- GET `/product-variants/{product_id}/` - Product variants

### Cart APIs
- POST `/cart/add/{type}/{id}/` - Add item to cart
- POST `/cart/update/{item_id}/` - Update quantity
- POST `/cart/remove/{item_id}/` - Remove item
- POST `/cart/clear/` - Clear entire cart
- GET `/cart/data/` - Get cart data (JSON)

### Order APIs
- POST `/checkout/` - Create order
- GET `/payment/` - Payment page
- GET `/my-orders/` - User's order history
- GET `/order-tracking/{order_number}/` - Track order

### Validation APIs
- POST `/validate-coupon/` - Validate discount code
- GET `/api/products/` - Search products

### Admin APIs
- GET `/dashboard/` - Admin dashboard
- GET `/check-updates/` - SiteUpdate polling

## 🔐 Security Features

- **CSRF Protection**: Token-based CSRF in all forms
- **Password Security**: Django's built-in hashing and validation
- **SQL Injection Prevention**: ORM-based queries
- **SSL/TLS**: HTTPS in production
- **Secure Headers**: HSTS, X-Frame-Options, etc. in production
- **Stripe Webhook Validation**: Secret-key verification
- **Environment Variables**: Sensitive credentials not hardcoded

## 📈 Performance Optimizations

- **Lazy Image Loading**: IntersectionObserver with fallback
- **Static File Optimization**: WhiteNoise compression
- **Database Query Optimization**: select_related, prefetch_related
- **Caching**: Signal-based cache invalidation via SiteUpdate model
- **Frontend**: Minimal dependencies (vanilla JS)
- **API Response**: JSON optimized for minimal payload

## 🚢 Deployment

### Vercel Deployment Guide

See [DEPLOY.md](DEPLOY.md) for comprehensive step-by-step instructions including:
- GitHub repository setup
- Environment variables configuration
- Database migration from MySQL to Neon PostgreSQL
- Cloudinary media storage setup
- Static file handling
- Troubleshooting common issues

### Quick Deployment Summary
1. Push code to GitHub
2. Create Neon PostgreSQL database
3. Connect Cloudinary account
4. Deploy to Vercel with environment variables
5. Run migrations: `python manage.py migrate`
6. Create admin user: `python manage.py createsuperuser`

## 📧 Email Configuration

The application sends transactional emails for:
- Order confirmation
- Password reset
- Contact form submission

Configure SMTP settings in `.env` for email delivery.

## 🐛 Troubleshooting

### Common Issues

**Django not found**
```bash
pip install -r requirements.txt
```

**Database connection error**
- Check MySQL is running (local development)
- Verify .env database credentials
- Check DATABASE_URL format for PostgreSQL

**Static files not loading**
```bash
python manage.py collectstatic --noinput
```

**Stripe errors**
- Verify STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY in .env
- Check webhook secret (STRIPE_WEBHOOK_SECRET)
- Test with Stripe test keys

**Cloudinary image errors**
- Verify CLOUDINARY_URL format
- Check folder structure in Cloudinary dashboard

See [DEPLOY.md](DEPLOY.md) for more troubleshooting.

## 📚 Documentation

- [DEPLOY.md](DEPLOY.md) - Complete deployment guide with setup instructions
- Django Admin - Access at `/admin/` (requires superuser login)
- API Documentation - Available through Django REST Framework browsable API

## 🤝 Contributing

This is an academic project. For enhancements:
1. Create feature branch
2. Add tests for new functionality
3. Update and test locally
4. Deploy to staging for verification

## 📄 License

This project is for educational purposes.

## 👥 Support

For issues or questions:
1. Check existing test cases in `myapp/tests.py`
2. Review [DEPLOY.md](DEPLOY.md) for deployment issues
3. Check Django admin at `/admin/` for content review
4. Verify environment variables in `.env`

---

**Last Updated**: March 2026
**Django Version**: 6.0.2
**Python Version**: 3.12 (Vercel runtime)
