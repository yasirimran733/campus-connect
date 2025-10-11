# 🚀 Campus Connect - Quick Start Guide

## ✅ Configuration Complete!

Your `.env` file has been created with the following configuration:

- **Database:** SQLite (db.sqlite3)
- **SECRET_KEY:** Generated securely
- **DEBUG:** Enabled (for development)
- **Email Backend:** Console (emails will print to terminal)

## 📋 Next Steps

### Option 1: Automated Setup (Recommended)

Run the setup script in PowerShell:

```powershell
.\setup.ps1
```

This will automatically:
1. ✅ Create virtual environment (if not exists)
2. ✅ Install all dependencies
3. ✅ Run database migrations
4. ✅ Prompt you to create a superuser
5. ✅ Collect static files

### Option 2: Manual Setup

If you prefer manual setup, follow these steps:

#### 1. Activate Virtual Environment

```powershell
venv\Scripts\activate
```

#### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

#### 3. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

#### 4. Create Superuser (Admin Account)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create your admin account:
- Username: (choose a username)
- Email: (your email)
- Password: (choose a strong password)
- Password (again): (confirm password)

#### 5. Run Development Server

```powershell
python manage.py runserver
```

## 🌐 Access the Application

Once the server is running, visit:

- **Home Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Register:** http://127.0.0.1:8000/users/register/
- **Login:** http://127.0.0.1:8000/users/login/

## 🧪 Testing the System

### 1. Test User Registration

1. Go to: http://127.0.0.1:8000/users/register/
2. Fill in the registration form
3. Submit - you'll see a success message
4. The new user will have `is_verified=False` by default

### 2. Test Admin Approval

1. Login to admin panel: http://127.0.0.1:8000/admin/
2. Navigate to **User Management > Users**
3. Find the newly registered user
4. Check the **"is_verified"** checkbox
5. Click **Save**

### 3. Test User Login

1. Go to: http://127.0.0.1:8000/users/login/
2. Login with the registered user credentials
3. If verified: You'll see a success message with full access
4. If not verified: You'll see a warning about pending approval

## 📁 Important Files

- **`.env`** - Environment variables (DATABASE, SECRET_KEY, etc.)
- **`db.sqlite3`** - SQLite database (created after migrations)
- **`manage.py`** - Django management script
- **`requirements.txt`** - Python dependencies

## 🎨 Features Implemented

✅ **User Registration** - Anyone can register  
✅ **Admin Approval** - Users need verification (is_verified field)  
✅ **Login/Logout** - Full authentication system  
✅ **User Profile** - View account information  
✅ **Dashboard** - User dashboard with stats  
✅ **Admin Panel** - Manage users and approvals  
✅ **Tailwind CSS** - Modern, responsive UI (Blue & White theme)  
✅ **Detailed Comments** - Code is well-documented for learning  

## 🔐 Admin Panel Features

- View all registered users
- Approve/reject users (toggle is_verified)
- Bulk actions to verify multiple users
- Filter by verification status, role, date
- Search users by username, email, name
- Detailed user information display

## 📝 Common Commands

```powershell
# Activate virtual environment
venv\Scripts\activate

# Run development server
python manage.py runserver

# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

## 🆘 Troubleshooting

### Virtual environment not activating?

Try:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module not found errors?

Make sure virtual environment is activated and dependencies are installed:
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

### Database errors?

Delete `db.sqlite3` and run migrations again:
```powershell
python manage.py makemigrations
python manage.py migrate
```

## 🎯 What's Next?

After testing the authentication system:

1. **Phase 2:** Lost & Found Items Module
2. **Phase 3:** Real-time Chat System (Django Channels)
3. **Phase 4:** Notifications System
4. **Phase 5:** Testing & Deployment

## 📞 Need Help?

Check these files for more information:
- `README.md` - Project overview
- `SETUP_GUIDE.md` - Detailed setup instructions
- `context.md` - Project requirements and specifications

---

**Developed by:** Yasir Imran  
**University:** PUCIT (Punjab University College of Information Technology)  
**Project:** FYP - Campus Connect (Smart Lost & Found System)

🎓 **Learning Goal:** Master Django full-stack development through AI-guided building
