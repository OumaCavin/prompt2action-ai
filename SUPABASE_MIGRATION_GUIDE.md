# 🔑 SUPABASE DATABASE MIGRATION GUIDE

## Current Status
- ✅ Database configuration updated to use Supabase PostgreSQL
- ✅ Added `psycopg2-binary` dependency for PostgreSQL support
- ⏳ **Need actual Supabase credentials**

## 🔍 How to Get Your Supabase Database Credentials

### 1. Log into Supabase Dashboard
- Go to: https://supabase.com/dashboard
- Login with your account

### 2. Select Your Project
- Click on your project: `umetddwitujrcvezjswc`

### 3. Get Database Credentials
Navigate to **Settings** → **Database** in your Supabase dashboard:

#### Required Information:
- **Database Password**: This is the password you set when creating the project
- **Service Role Key**: Go to **Settings** → **API** → Copy the "service_role" key (not anon)

### 4. Environment Variables to Update
Replace these placeholder values in your environment:

```bash
# In Railway environment variables or .env file:
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (your actual service key)
SUPABASE_DB_PASSWORD=your-actual-database-password
```

## 🚀 Next Steps

1. **Get your credentials** from Supabase dashboard
2. **Update Railway environment variables**:
   - Go to your Railway project settings
   - Add the SUPABASE_SERVICE_KEY and SUPABASE_DB_PASSWORD
3. **Redeploy** the application

## 📝 Migration Commands
Once credentials are set, run these in Railway:

```bash
# Remove old SQLite database
rm db.sqlite3

# Run migrations on Supabase
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## ✅ Benefits of Supabase Migration
- **Persistent storage** (no data loss on Railway restarts)
- **Better performance** and scalability
- **Professional production database**
- **Built-in backups and monitoring**
