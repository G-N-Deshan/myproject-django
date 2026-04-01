# 🛍️ KidZone — Premium Django E-Commerce Platform

KidZone is a feature-rich, full-stack e-commerce application built with **Django**. It is designed to handle complex product variants, advanced inventory tracking, secure payments via Stripe, and a highly interactive shopping experience.

---

## 🌟 Key Features

### 🛒 Advanced Shopping Experience
* **Dynamic Product Catalog:** Segregated into Clothes (Men, Women, Kids), Toys (by age range), Offers, and New Arrivals.
* **Smart Cart:** Seamless cart updates with multi-item type support.
* **Wishlist Ecosystem:** Users can create wishlists, generate public share links/tokens, and enable **Price Drop Alerts** (e.g., get notified when a toy drops by 10%).

### 📦 Inventory & Order Management
* **Real-Time Stock Tracking:** Prevents adding items to the cart if they exceed available inventory.
* **Out of Stock Reservations:** Allows users to "Reserve" or subscribe to "Back-In-Stock" email notifications when an item's inventory is zero.
* **Order Tracking Pipeline:** Granular flow tracking orders from `Pending` → `Processing` → `Shipped` → `Delivered`.
* **Coupon Engine:** Supports percentage-based and fixed-amount discounts with usage limits and expiration dates.

### 💳 Payments & Security
* **Stripe Integration:** Secure checkout flow utilizing Stripe's API for processing payments and handling webhooks.
* **Google OAuth2:** Fast and secure social login via `django-allauth`.

### 🖼️ UI/UX & Media
* **Cloudinary Storage:** All product gallery images and user review image uploads are safely stored in the cloud.
* **Rich Product Details:** Care instructions, materials, dynamic color hex codes, size variants, safety info, and brand badges.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| **Backend Framework** | Django 6.0 |
| **Database** | PostgreSQL / MySQL |
| **Authentication** | Django-AllAuth (Google Provider) |
| **Payments** | Stripe |
| **Media Storage** | Cloudinary |
| **Static Files** | WhiteNoise |
| **Production Server** | Gunicorn |
| **Frontend** | HTML5, Vanilla CSS, JS |

---

## 🚀 Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/G-N-Deshan/myproject-django.git
cd myproject-django
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Environment Variables (`.env`)
Create a `.env` file in the root of the project and add the following keys:
```env
# Core Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Database (MySQL Local fallback)
DB_NAME=myproject
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

# Cloudinary (Images)
CLOUDINARY_URL=cloudinary://your_api_key:your_api_secret@cloud_name

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email configuration
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit the storefront at `http://127.0.0.1:8000` and the Admin Dashboard at `http://127.0.0.1:8000/admin/`.

---

## 🌐 Deployment (Render Free Tier)

This application is configured for seamless deployment on **Render**. 
Follow the comprehensive instructions found in `DEPLOY_TO_RENDER.md` which utilizes the included `render.yaml` Blueprint and `build_files.sh` execution script.

---

## 🗄️ Database Architecture Highlights
The project handles complex relational data across dozens of normalized tables, including:
* `Inventory` to strictly link multi-category products to available stock.
* `WishlistItem` & `WishlistShare` for tracking user preferences and price thresholds.
* `OrderTracking` to append shipping notes over time.
* `BackInStockNotification` & `OutOfStockReservation` tied directly to the global user model.

---

*Built with ❤️ utilizing modern Django engineering practices.*
