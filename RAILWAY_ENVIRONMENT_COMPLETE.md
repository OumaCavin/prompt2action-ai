# ===============================================
# PROMPT2ACTION AI - LIVE DEPLOYMENT
# ===============================================
# Author: Cavin Otieno
# Date: 2025-11-15
# Project: Prompt2Action AI Multi-Agent Platform
# Live URL: https://prompt2action-ai-production.up.railway.app
# Status: ✅ ACTIVE & DEPLOYED
# ===============================================

## 🚀 LIVE DEMO ACCESS
- **Application URL**: https://prompt2action-ai-production.up.railway.app
- **Admin Panel**: https://prompt2action-ai-production.up.railway.app/admin
- **Default Admin**: Username: admin, Password: admin

# ===============================================
# COMPLETE PROMPT2ACTION AI ENVIRONMENT SETUP
# ===============================================

# ===============================================
# DJANGO CORE SETTINGS
# ===============================================
SECRET_KEY=django-insecure-(s2p=ni0oc9p9kqr03burdmwjk$i$oooyd+d_5vidwy_1^)-1
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,prompt2action-ai-production.up.railway.app
DJANGO_SETTINGS_MODULE=config.settings

# ===============================================
# GOOGLE GEMINI AI INTEGRATION
# ===============================================
GEMINI_API_KEY=AIzaSyA2bBKF7GCYi_OmUCcaZ3dOXFwfzQzeDug
GEMINI_PROJECT_ID=prompt2action-ai
GEMINI_API_LOCATION=global

# ===============================================
# SUPABASE DATABASE CONFIGURATION
# ===============================================
SUPABASE_URL=https://umetddwitujrcvezjswc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVtZXRkZHdpdHVqcmN2ZXpqc3djIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxOTgxMDUsImV4cCI6MjA3ODc3NDEwNX0.jd4R8hRlefk8u54BTwSh5cPtpb2KUlDZ2Z4SCJZheEE
SUPABASE_SERVICE_KEY=your-supabase-service-key-here
DATABASE_URL=postgresql://postgres:[your-password]@db.umetddwitujrcvezjswc.supabase.co:5432/postgres
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-db-password-here

# ===============================================
# EMAIL CONFIGURATION (GMAIL SMTP)
# ===============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=cavin.otieno012@gmail.com
EMAIL_HOST_PASSWORD=oakjazoekos
DEFAULT_FROM_EMAIL=cavin.otieno012@gmail.com
EMAIL_SUBJECT_PREFIX=[Prompt2Action AI]

# ===============================================
# RAILWAY DEPLOYMENT CONFIGURATION
# ===============================================
RAILWAY_TOKEN=65ae1056-f51d-4242-9471-f7abf1f2897c
RAILWAY_PROJECT_NAME=prompt2action-ai
RAILWAY_ENVIRONMENT=production
PORT=8000
WEB_CONCURRENCY=4

# ===============================================
# REDIS CONFIGURATION
# ===============================================
# Railway Redis will be automatically configured
REDIS_URL=${{REDIS_URL}}
REDIS_HOST=${{REDIS_HOST}}
REDIS_PORT=${{REDIS_PORT}}
REDIS_PASSWORD=${{REDIS_PASSWORD}}
REDIS_DB=0

# ===============================================
# CELERY CONFIGURATION
# ===============================================
CELERY_BROKER_URL=${{REDIS_URL}}
CELERY_RESULT_BACKEND=${{REDIS_URL}}
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE=UTC
CELERY_BEAT_SCHEDULER=django_celery_beat.schedulers:DatabaseScheduler

# ===============================================
# DJANGO CHANNELS (WEBSOCKETS)
# ===============================================
CHANNEL_LAYERS_URL=${{REDIS_URL}}
CHANNEL_LAYERS_BACKEND=channels_redis.core.RedisChannelLayer
CHANNEL_LAYERS_CONFIG={"hosts": ["${{REDIS_URL}}"]}

# ===============================================
# SECURITY CONFIGURATION
# ===============================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://prompt2action-ai-production.up.railway.app
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://prompt2action-ai-production.up.railway.app
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True

# ===============================================
# CACHING CONFIGURATION
# ===============================================
CACHES={
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "${{REDIS_URL}}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "prompt2action_ai"
    }
}

# ===============================================
# AGENT SYSTEM CONFIGURATION
# ===============================================
MAX_CONCURRENT_WORKFLOWS=10
WORKFLOW_TIMEOUT=3600
MAX_RETRIES=3
RETRY_DELAY=5
AGENT_LLM_PROVIDER=google-gemini
AGENT_MAX_TOKENS=4096
AGENT_TEMPERATURE=0.7

# ===============================================
# LOGGING CONFIGURATION
# ===============================================
LOG_LEVEL=INFO
LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# ===============================================
# FILE UPLOAD CONFIGURATION
# ===============================================
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880
FILE_UPLOAD_PERMISSIONS=0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS=0o755

# ===============================================
# INTERNATIONALIZATION
# ===============================================
USE_TZ=True
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
USE_I18N=True

# ===============================================
# DEVELOPMENT OVERRIDES
# ===============================================
# Set to True for local development, False for production
DEV_MODE=False
USE_CACHING=True
USE_WEBSOCKETS=True
USE_CELERY=True

# ===============================================
# END OF ENVIRONMENT CONFIGURATION
# ===============================================