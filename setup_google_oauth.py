"""
Setup script for Google OAuth in django-allauth
Run: python manage.py shell < setup_google_oauth.py
"""

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Step 1: Update Site (required by allauth)
site = Site.objects.get_current()
site.name = 'KidZone Store'
site.domain = '127.0.0.1:8000'  # For local - change to your domain in production
site.save()
print(f"✓ Updated Site: {site.name} ({site.domain})")

# Step 2: Check if Google SocialApp exists
try:
    google_app = SocialApp.objects.get(provider='google')
    print(f"✓ Google OAuth app already exists: {google_app.name}")
except SocialApp.DoesNotExist:
    print("⚠ Google OAuth app not found in database")
    print("\nTo add Google OAuth credentials:")
    print("1. Go to Django Admin: http://127.0.0.1:8000/admin/")
    print("2. Navigate to 'Social applications'")
    print("3. Click 'Add Social application'")
    print("4. Fill in:")
    print("   - Provider: Google")
    print("   - Name: Google OAuth")
    print("   - Client ID: <your Google OAuth Client ID>")
    print("   - Secret key: <your Google OAuth Client Secret>")
    print("   - Sites: Select 'KidZone Store'")
    print("\n5. To get credentials, visit: https://console.cloud.google.com/")
    print("   - Create OAuth 2.0 credentials")
    print("   - Authorize redirect URIs: http://127.0.0.1:8000/accounts/google/login/callback/")
    print("\nDone! Google login should now work.")
