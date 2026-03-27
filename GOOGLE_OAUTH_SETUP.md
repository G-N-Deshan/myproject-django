# Google OAuth Setup Guide

## Problem
When clicking "Continue with Google" on the login page, you get: `DoesNotExist at /accounts/google/login/`

## Root Cause
Django-allauth requires Google OAuth credentials to be configured in Django Admin.

## Solution

### Option 1: Quick Setup (Without Google OAuth)
If you want to disable Google OAuth temporarily and just use email/password login:

**Edit `templates/login.html` or navbar and remove:**
```html
<!-- Remove the "Continue with Google" button -->
```

---

### Option 2: Complete Google OAuth Setup (Recommended)

#### Step 1: Get Google OAuth Credentials

1. Go to **Google Cloud Console**: https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable **Google+ API**:
   - In left sidebar, click "APIs & Services"
   - Click "Enable APIs and Services"
   - Search for "Google+ API"
   - Click "Enable"

4. Create OAuth 2.0 Credentials:
   - Go to "Credentials" in left sidebar
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Web application"
   - Add Authorized redirect URIs:
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```
   - For production, also add:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Click "Create"
   - Copy the **Client ID** and **Client Secret**

#### Step 2: Configure Django Admin

1. Start Django server:
   ```bash
   python manage.py runserver
   ```

2. Go to Admin: http://127.0.0.1:8000/admin/
3. Login with superuser credentials (created during setup)

4. Navigate to **Social applications** (left sidebar)

5. Click **Add Social application**

6. Fill in the form:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client ID**: `<paste your Google Client ID>`
   - **Secret key**: `<paste your Google Client Secret>`
   - **Sites**: Select `127.0.0.1:8000` (or your domain)
   - Check the "Verified" checkbox

7. Click **Save**

#### Step 3: Test It

1. Go to http://127.0.0.1:8000/login/
2. Click "Continue with Google"
3. You should be redirected to Google's login page
4. After login, you'll be redirected back to your store

---

## Troubleshooting

### Error: "Site matching query does not exist"
**Fix:**
1. Go to Django Admin → Sites
2. Make sure there's a Site with domain `127.0.0.1:8000` (or your domain)
3. If not, create one

### Error: "DoesNotExist at /accounts/google/login/"
**Fix:**
1. Go to Django Admin → Social applications
2. Make sure a Google OAuth app exists
3. Make sure it's linked to your Site

### OAuth Returns Wrong Redirect
**Fix:**
1. Make sure the redirect URI in Google Cloud matches exactly:
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```

---

## For Production Deployment

When deploying to production (e.g., Vercel):

1. Update Site domain in Django Admin:
   - Change from `127.0.0.1:8000` to `yourdomain.com`

2. Add production redirect URI to Google Cloud:
   ```
   https://yourdomain.com/accounts/google/login/callback/
   ```

3. Update Django settings:
   ```python
   # In production .env or settings
   DOMAIN = 'yourdomain.com'
   ```

---

## Quick Test Command

Instead of manually setting up in admin, you can also run this command to check your setup:

```bash
python manage.py shell < setup_google_oauth.py
```

This will check if everything is configured and show you what's missing.

---

## Files Configured

✅ `myproject/settings.py` - Updated AUTHENTICATION_BACKENDS to include Google
✅ `setup_google_oauth.py` - Helper script for verification
✅ `templates/login.html` - Has Google OAuth button via allauth

No further code changes needed!
