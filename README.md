# Campus Connect - Smart Lost & Found System

**Tagline:** "Smart Lost & Found System for University Students"

## 🏫 Project Overview

Campus Connect is a smart web-based lost & found management system built for universities. Students can register, report lost/found items, and chat securely with each other once verified by an admin.

## 🧠 Tech Stack

- **Backend:** Django 5+ (Python 3.12)
- **Frontend:** Tailwind CSS + Vanilla JavaScript
- **Database:** PostgreSQL / SQLite
- **Authentication:** Django Auth with custom User model
- **Real-Time Chat:** Django Channels + WebSockets (coming soon)

## 🚀 Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`
2. Update the database credentials and other settings

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## 📁 Project Structure

```
campus_connect/
├── manage.py
├── requirements.txt
├── campus_connect/        # Main settings & URLs
├── users/                 # Authentication app
├── templates/             # HTML Templates
├── static/                # CSS, JS, images
└── media/                 # Uploaded files
```

## ✨ Features

### **Phase 1: Authentication ✅**
- ✅ User registration (PUCIT email required: @pucit.edu.pk)
- ✅ Email domain validation (only PUCIT students/staff)
- ✅ Admin approval system (is_verified field)
- ✅ Login/Logout functionality
- ✅ User profiles and dashboard

### **Phase 2: Lost & Found Items ✅**
- ✅ Post lost/found items with images
- ✅ Admin approval workflow
- ✅ Search and filter items
- ✅ Category-based organization
- ✅ Item status management (active/claimed/returned)
- ✅ Reward system
- ✅ View counter and statistics
- ✅ User item management

### **Coming Soon**
- 🔄 Real-time chat system (Phase 3)
- 🔄 Notifications (Phase 4)
- 🔄 Email verification

## 👨‍💻 Developer

**Name:** Yasir Imran  
**University:** Punjab University College of Information Technology (PUCIT)  
**Project Type:** FYP - Smart Lost & Found System

## 📝 License

This project is for educational purposes.
