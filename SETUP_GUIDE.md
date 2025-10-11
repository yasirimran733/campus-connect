# Campus Connect - Setup Guide

## 📋 Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- PostgreSQL (optional, can use SQLite for development)
- Git (optional, for version control)

## 🚀 Step-by-Step Setup

### 1. Create Virtual Environment

Open PowerShell in the project directory and run:

```powershell
python -m venv venv
```

### 2. Activate Virtual Environment

```powershell
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

**Option A: SQLite (Recommended for Development)**

1. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```

2. Edit `.env` file and use these settings:
   ```
   SECRET_KEY=your-secret-key-here-change-this
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # SQLite Database (Default)
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   ```

**Option B: PostgreSQL (Recommended for Production)**

1. Install PostgreSQL on your system
2. Create a new database:
   ```sql
   CREATE DATABASE campus_connect_db;
   CREATE USER your_username WITH PASSWORD 'your_password';
   ALTER ROLE your_username SET client_encoding TO 'utf8';
   ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
   ALTER ROLE your_username SET timezone TO 'Asia/Karachi';
   GRANT ALL PRIVILEGES ON DATABASE campus_connect_db TO your_username;
   ```

3. Edit `.env` file:
   ```
   SECRET_KEY=your-secret-key-here-change-this
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # PostgreSQL Database
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=campus_connect_db
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

### 5. Generate Secret Key

Run this Python command to generate a secure secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as your `SECRET_KEY` in `.env` file.

### 6. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

This will create all necessary database tables.

### 7. Create Superuser (Admin)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account. This account will have full access to the admin panel.

### 8. Run Development Server

```powershell
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

### 9. Access Admin Panel

Navigate to: `http://127.0.0.1:8000/admin/`

Login with the superuser credentials you created in step 7.

## 🎯 Testing the Application

### Test User Registration

1. Go to: `http://127.0.0.1:8000/users/register/`
2. Fill in the registration form
3. Submit the form
4. You should see a success message

### Test User Approval (Admin)

1. Login to admin panel: `http://127.0.0.1:8000/admin/`
2. Click on "Users" under "User Management"
3. Find the newly registered user
4. Check the "is_verified" checkbox
5. Click "Save"

### Test User Login

1. Go to: `http://127.0.0.1:8000/users/login/`
2. Login with the registered user credentials
3. You should be redirected to the home page
4. If verified, you'll see a success message
5. If not verified, you'll see a warning about pending approval

## 📁 Project Structure

```
campus_connect/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .env.example              # Example environment file
├── .gitignore                # Git ignore file
├── README.md                 # Project documentation
├── SETUP_GUIDE.md           # This file
│
├── campus_connect/           # Main project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
│
├── users/                    # Users app
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # User forms
│   ├── models.py            # User model
│   ├── tests.py             # Unit tests
│   ├── urls.py              # App URLs
│   └── views.py             # View functions
│
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── home.html           # Home page
│   └── users/              # User templates
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       └── dashboard.html
│
├── static/                  # Static files
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── main.js
│
└── media/                   # User uploaded files (created automatically)
```

## 🔧 Common Issues & Solutions

### Issue: "No module named 'decouple'"

**Solution:** Make sure you've installed all dependencies:
```powershell
pip install -r requirements.txt
```

### Issue: "django.db.utils.OperationalError: no such table"

**Solution:** Run migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Issue: "CSRF verification failed"

**Solution:** Make sure you have `{% csrf_token %}` in all forms and that cookies are enabled in your browser.

### Issue: Static files not loading

**Solution:** Run collectstatic command:
```powershell
python manage.py collectstatic
```

## 📝 Next Steps

After completing the setup:

1. ✅ Test user registration
2. ✅ Test admin approval system
3. ✅ Test user login/logout
4. 🔄 Add Lost & Found items module (Phase 2)
5. 🔄 Add Chat system (Phase 3)
6. 🔄 Add Notifications (Phase 4)
7. 🔄 Deploy to production (Phase 5)

## 🆘 Need Help?

If you encounter any issues:

1. Check the Django error page for detailed error messages
2. Review the console output for any error logs
3. Verify that all environment variables are set correctly in `.env`
4. Make sure the virtual environment is activated
5. Check that all migrations have been applied

## 👨‍💻 Developer Notes

- Always activate the virtual environment before working on the project
- Run migrations after any model changes
- Test thoroughly before deploying to production
- Keep the `.env` file secure and never commit it to version control
- Use meaningful commit messages if using Git

---

**Developed by:** Yasir Imran  
**University:** Punjab University College of Information Technology (PUCIT)  
**Project:** Campus Connect - Smart Lost & Found System
