# Deployment Guide - Prompt2Action AI Platform

## ✅ SUCCESSFULLY DEPLOYED!
**Live Application**: https://prompt2action-ai-production.up.railway.app  
**Admin Access**: https://prompt2action-ai-production.up.railway.app/admin  
**Status**: Active on Railway with gunicorn server  
**Deployment Date**: November 15, 2025

---

## 📋 Table of Contents

1. [Railway Deployment (Recommended - Free Tier)](#railway-deployment)
2. [Heroku Deployment](#heroku-deployment)
3. [DigitalOcean App Platform](#digitalocean-deployment)
4. [AWS Elastic Beanstalk](#aws-deployment)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment Steps](#post-deployment)

---

## 🚂 Railway Deployment (Recommended - Free Tier)

Railway is **highly recommended** because:
- ✅ Free tier available ($5 credit/month)
- ✅ Easy GitHub integration
- ✅ Built-in PostgreSQL and Redis
- ✅ Automatic deployments on git push
- ✅ No credit card required for trial

### Step-by-Step Railway Deployment

#### 1. Create Railway Account

1. Visit [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Log in with your GitHub account
4. Authorize Railway to access your repositories

#### 2. Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `OumaCavin/prompt2action-ai` repository
4. Railway will auto-detect Django and start building

#### 3. Add PostgreSQL Database

1. In your project dashboard, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically set `DATABASE_URL` environment variable

#### 4. Add Redis

1. Click "New" again
2. Select "Database" → "Add Redis"
3. Railway will automatically set `REDIS_URL` environment variable

#### 5. Configure Environment Variables

In Railway dashboard, go to your service → Variables tab:

```env
# Django Settings
DJANGO_SECRET_KEY=your-very-secure-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app,yourdomain.com

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-from-google

# Email Settings
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Database (Auto-configured by Railway)
# DATABASE_URL - Already set by PostgreSQL addon

# Redis (Auto-configured by Railway)
# REDIS_URL - Already set by Redis addon
```

#### 6. Configure Build & Start Commands

In Settings → Deploy:

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
daphne -b 0.0.0.0 -p $PORT config.asgi:application
```

#### 7. Deploy

1. Click "Deploy" or push to your GitHub repository
2. Railway will automatically deploy on every git push
3. Your app will be available at: `https://your-app.railway.app`

### Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and add it to Railway environment variables

### Getting Gmail App Password

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification (must be enabled)
3. App Passwords → Generate new app password
4. Select "Mail" and "Other (Custom name)"
5. Enter "Railway Prompt2Action"
6. Copy the 16-character password (remove spaces)
7. Add to Railway as `EMAIL_HOST_PASSWORD`

---

## 🔷 Heroku Deployment

### Prerequisites

1. Heroku account (free tier available)
2. Heroku CLI installed

### Step 1: Install Heroku CLI

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Windows:**
Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App

```bash
# Login to Heroku
heroku login

# Create new app
heroku create prompt2action-ai
# Or with custom name: heroku create your-custom-name
```

### Step 3: Add Addons

```bash
# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Add Redis
heroku addons:create heroku-redis:mini
```

**Note:** `mini` plans are free but limited. Use `hobby-dev` for more resources ($7/month each).

### Step 4: Set Environment Variables

```bash
# Django secret key
heroku config:set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Gemini API key
heroku config:set GEMINI_API_KEY=your-gemini-api-key

# Email password
heroku config:set EMAIL_HOST_PASSWORD=your-gmail-app-password

# Django settings
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=.herokuapp.com
```

### Step 5: Create Procfile

Create a file named `Procfile` in your project root:

```
web: daphne -b 0.0.0.0 -p $PORT config.asgi:application
worker: celery -A config worker --loglevel=info
```

### Step 6: Deploy

```bash
# Add Heroku remote
heroku git:remote -a prompt2action-ai

# Push to Heroku
git push heroku master

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Scale workers
heroku ps:scale web=1 worker=1
```

### Step 7: View App

```bash
heroku open
```

---

## 🌊 DigitalOcean App Platform

### Step 1: Create DigitalOcean Account

1. Visit [digitalocean.com](https://digitalocean.com)
2. Sign up for an account
3. Get $200 credit for 60 days with promo code

### Step 2: Create New App

1. Go to Apps → Create App
2. Connect to GitHub repository
3. Select `OumaCavin/prompt2action-ai`
4. Choose branch: `master` or `main`

### Step 3: Configure Build Settings

**Build Command:**
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

**Run Command:**
```bash
daphne -b 0.0.0.0 -p 8080 config.asgi:application
```

### Step 4: Add Managed Databases

1. In app settings, add PostgreSQL database ($15/month)
2. Add Redis database ($15/month)
3. DigitalOcean will auto-configure connection strings

### Step 5: Environment Variables

Add in App Platform dashboard → Settings → Environment Variables

### Step 6: Deploy

Click "Deploy" and monitor the build process.

---

## ☁️ AWS Elastic Beanstalk

### Prerequisites

```bash
pip install awsebcli
```

### Setup

```bash
# Initialize EB application
eb init -p python-3.12 prompt2action-ai --region us-east-1

# Create environment
eb create prompt2action-production

# Set environment variables
eb setenv DJANGO_SECRET_KEY=your-secret-key \
         GEMINI_API_KEY=your-api-key \
         EMAIL_HOST_PASSWORD=your-password \
         DEBUG=False

# Deploy
eb deploy

# Open in browser
eb open
```

### Configure Database (RDS)

1. AWS Console → RDS → Create Database
2. Choose PostgreSQL
3. Free tier available
4. Add connection string to EB environment variables

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | How to Get |
|----------|-------------|------------|
| `DJANGO_SECRET_KEY` | Django secret key | Generate: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `GEMINI_API_KEY` | Google Gemini API key | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `EMAIL_HOST_PASSWORD` | Gmail app password | [Gmail App Passwords](https://myaccount.google.com/apppasswords) |
| `DATABASE_URL` | PostgreSQL connection | Auto-set by hosting provider |
| `REDIS_URL` | Redis connection | Auto-set by hosting provider |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | False |
| `ALLOWED_HOSTS` | Allowed domains | .railway.app,.herokuapp.com |
| `CELERY_BROKER_URL` | Celery broker | Same as REDIS_URL |

---

## ✅ Post-Deployment Steps

### 1. Create Superuser

```bash
# Railway
railway run python manage.py createsuperuser

# Heroku
heroku run python manage.py createsuperuser

# DigitalOcean
doctl apps exec <app-id> -- python manage.py createsuperuser
```

### 2. Verify Deployment

Visit these URLs:
- Homepage: `https://your-app.railway.app/`
- Admin: `https://your-app.railway.app/admin/`
- API: `https://your-app.railway.app/api/` (when implemented)

### 3. Configure Custom Domain (Optional)

#### Railway
1. Settings → Domains
2. Add custom domain
3. Update DNS records with provided values

#### Heroku
```bash
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com
```

### 4. Enable HTTPS

All platforms (Railway, Heroku, DigitalOcean, AWS) provide automatic HTTPS/SSL certificates.

### 5. Monitor Logs

```bash
# Railway
railway logs

# Heroku
heroku logs --tail

# DigitalOcean
doctl apps logs <app-id> --follow
```

---

## 🔧 Troubleshooting

### Static Files Not Loading

Add to `settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

Run:
```bash
python manage.py collectstatic --noinput
```

### Database Connection Issues

Ensure `DATABASE_URL` is set and install `dj-database-url`:
```bash
pip install dj-database-url
```

Update `settings.py`:
```python
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='sqlite:///db.sqlite3')}
```

### WebSocket Issues

Ensure your hosting platform supports WebSocket connections:
- ✅ Railway: Supported
- ✅ Heroku: Supported (with Daphne)
- ✅ DigitalOcean: Supported
- ✅ AWS: Supported (requires configuration)

---

## 📊 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Railway** | $5 credit/month | $10+/month | Quick deployment, hobby projects |
| **Heroku** | 550-1000 hours/month | $7+/month | Small to medium apps |
| **DigitalOcean** | $200 credit (60 days) | $5+/month | Production apps, full control |
| **AWS** | 12 months free tier | Variable | Enterprise, scalability |

---

## 🎯 Recommendation

**For this project, I recommend:**

1. **Development/Testing**: Railway (free tier)
2. **Small Production**: Heroku ($20-30/month with add-ons)
3. **Medium/Large Production**: DigitalOcean App Platform ($40-60/month)
4. **Enterprise**: AWS Elastic Beanstalk (custom pricing)

---

## 📞 Support

If you need help with deployment:

**Cavin Otieno**
- 📧 Email: cavin.otieno012@gmail.com
- 📱 Phone: +254708101604
- 💬 WhatsApp: https://wa.me/+254708101604
- 💼 LinkedIn: https://www.linkedin.com/in/cavin-otieno-9a841260/

---

**Created by:** Cavin Otieno  
**Last Updated:** November 2024  
**Version:** 1.0
