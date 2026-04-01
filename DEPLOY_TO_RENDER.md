# 🚀 KidZone — Deploy to Render (100% Free, Manual Setup)

> ✅ No Blueprint needed. Manual setup is completely free.
> ✅ Branch: `newrender`

---

## Prerequisites

- [ ] GitHub account with this project pushed to the `newrender` branch
- [ ] Render account — free at [render.com](https://render.com)
- [ ] Cloudinary account — free at [cloudinary.com](https://cloudinary.com) (for image storage)

---

## Step 1 — Push Your Code to GitHub (`newrender` branch)

```bash
# Make sure you're on the newrender branch
git checkout newrender

# Add all the new Render config files
git add .
git commit -m "chore: configure for Render deployment"
git push origin newrender
```

---

## Step 2 — Get Your Free Cloudinary URL

1. Go to [cloudinary.com](https://cloudinary.com) → click **Sign Up For Free**
2. After login → go to your **Dashboard**
3. Find the box that says **API Environment variable**, it looks like:
   ```
   CLOUDINARY_URL=cloudinary://123456789012345:AbCdEfGhIjKlMnOp@your-cloud-name
   ```
4. Copy the full value including `cloudinary://...` — you'll need it later.

---

## Step 3 — Create Free PostgreSQL Database on Render

1. Go to [render.com](https://render.com) → Login
2. Click **New +** → **PostgreSQL**
3. Fill in:
   - **Name**: `kidzone-db`
   - **Database**: `kidzone`
   - **User**: `kidzone`
   - **Region**: Choose closest to you (e.g. Singapore for South Asia)
   - **Plan**: Select **Free** ✅
4. Click **Create Database**
5. Wait ~1 minute for it to be ready
6. Once ready, click on it and **copy the "Internal Database URL"** — it looks like:
   ```
   postgresql://kidzone:password@dpg-xxxx-a/kidzone
   ```

---

## Step 4 — Create Free Web Service on Render

1. Click **New +** → **Web Service**
2. Choose **Build and deploy from a Git repository** → click **Next**
3. Connect your GitHub account → find and select your repository
4. Fill in these settings:

   | Field | Value |
   |---|---|
   | **Name** | `kidzone` |
   | **Branch** | `newrender` ← important! |
   | **Region** | Same as your database |
   | **Runtime** | `Python` |
   | **Build Command** | `./build_files.sh` |
   | **Start Command** | `gunicorn myproject.wsgi:application --workers 2 --timeout 120 --bind 0.0.0.0:$PORT` |
   | **Plan** | **Free** ✅ |

5. Scroll down to **Environment Variables** and add ALL of these:

   | Key | Value |
   |---|---|
   | `DEBUG` | `False` |
   | `SECRET_KEY` | Go to https://djecrety.ir/ → copy the generated key |
   | `DATABASE_URL` | Paste the **Internal Database URL** from Step 3 |
   | `ALLOWED_HOSTS` | `kidzone.onrender.com` |
   | `CSRF_TRUSTED_ORIGINS` | `https://kidzone.onrender.com` |
   | `CLOUDINARY_URL` | Your Cloudinary URL from Step 2 |
   | `STRIPE_PUBLISHABLE_KEY` | Your Stripe publishable key |
   | `STRIPE_SECRET_KEY` | Your Stripe secret key |
   | `STRIPE_WEBHOOK_SECRET` | Your Stripe webhook secret |
   | `EMAIL_HOST_USER` | Your Gmail address |
   | `EMAIL_HOST_PASSWORD` | Your Gmail App Password |

6. Click **Create Web Service**

---

## Step 5 — Wait for the Build to Complete

Watch the deploy logs. You should see:

```
==> Installing dependencies...
==> Collecting static files...
==> Running database migrations...
==> Build complete!
==> Your service is live 🎉
```

Your app will be live at: **`https://kidzone.onrender.com`**

> ⚠️ If the name `kidzone` is taken, Render will use something like `kidzone-abc1`.
> Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to match the exact URL shown.

---

## Step 6 — Create Admin Superuser

1. On Render → click your **Web Service** → go to **Shell** tab
2. Type and run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter your username, email, and password

---

## Step 7 — Fix Django Site (Required for Google OAuth & Allauth)

1. Go to `https://kidzone.onrender.com/admin/`
2. Login with your superuser
3. Go to **Sites** → click the one entry that exists
4. Update both fields:
   - **Domain name**: `kidzone.onrender.com`
   - **Display name**: `KidZone`
5. Click **Save**

---

## Step 8 — Update Google OAuth Redirect URI

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project → **APIs & Services** → **Credentials**
3. Click your OAuth 2.0 Client ID
4. Under **Authorized redirect URIs**, add:
   ```
   https://kidzone.onrender.com/accounts/google/callback/
   ```
5. Click **Save**

Then in Django Admin → **Social Applications** → edit your Google app → move your Render site to **Chosen Sites**.

---

## Step 9 — Update Stripe Webhook (If Using Payments)

1. [Stripe Dashboard](https://dashboard.stripe.com/) → **Developers** → **Webhooks**
2. **Add endpoint**: `https://kidzone.onrender.com/payment/webhook/`
3. Copy the new signing secret → update `STRIPE_WEBHOOK_SECRET` in Render env vars

---

## ⚠️ Free Tier Limitations

| Limitation | Details |
|---|---|
| **Spin-down** | App sleeps after 15 min of no traffic; first request takes ~30 sec to wake |
| **PostgreSQL** | Free DB expires after **90 days** — you'll need to recreate it |
| **No persistent disk** | Media files MUST use Cloudinary (already configured ✅) |
| **750 hrs/month** | Enough for 1 service running 24/7 |

---

## 🔁 Updating Your App Later

Every time you push to the `newrender` branch, Render auto-redeploys:

```bash
git checkout newrender
git add .
git commit -m "your update"
git push origin newrender
# Render auto-deploys! ✅
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `DisallowedHost` error | Update `ALLOWED_HOSTS` in Render env vars to your exact URL |
| `CSRF verification failed` | Update `CSRF_TRUSTED_ORIGINS` to `https://your-exact-url.onrender.com` |
| Images not showing | Check `CLOUDINARY_URL` is correct — no spaces, starts with `cloudinary://` |
| Build fails | Check Render logs — usually a missing env var or migration error |
| 500 errors | Temporarily set `DEBUG=True` in env vars, check logs, then set back to `False` |
| Google login broken | Make sure Django Site domain matches your Render URL exactly |
