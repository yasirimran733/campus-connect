✅ AI (Windsurf) Behavior Instructions
Every time writing code consider this file for project.
Always ask Yasir before using any database or credentials

Never use dummy credentials

Follow Tailwind theme (Blue & White) consistently

Add detailed comments for learning

Ensure code readability and security best practices

Use modular, scalable Django structure

🧩 CURSOR CONTEXT FILE: Campus Connect (Django + Tailwind + JavaScript)
Final Production-Level Web App Version

🏫 Project Overview

Project Name: Campus Connect
Tagline: “Smart Lost & Found System for University Students”

Description:
Campus Connect is a smart web-based lost & found management system built for universities.
Students can register, report lost/found items, and chat securely with each other once verified by an admin.
Admins manage users and posts through an admin dashboard.

✅ Everyone can register, but users will only gain full access after being verified by the admin.

🎯 Core Objectives

Digitalize the lost & found system on campus

Ensure user verification for security

Allow real-time item updates and chats

Provide a clean, modern, responsive web UI

🧠 Tech Stack
Layer	Technology	Purpose
Backend	Django 5+ (Python 3.12)	Core web logic & APIs
Frontend	Tailwind CSS + Vanilla JS	Modern UI and interactivity
Database	PostgreSQL / SQLite	Store users, items, chats
Authentication	Django Auth	User login, registration, admin control
Media Storage	Django Media (local / Cloudinary optional)	Store uploaded images
Real-Time Chat	Django Channels + WebSockets	Live communication
Notifications	Django Signals + Email (or WebPush optional)	Notify users of approvals or chats
Admin Panel	Django Admin	Admin approvals and management
Deployment	Render / Railway (Free hosting)	Deployment platform
🎨 UI / UX Theme

Primary color: #003366 (University Blue)

Secondary color: #FFFFFF (White)

Font: Poppins or Inter (Google Fonts)

Style: Clean, minimal university aesthetic

Layout: Responsive with Tailwind grid system

🧩 Core Modules
1. 🔐 Authentication & User Management

Register with university email

Everyone can register, but verification (is_verified=False) by admin is required for full access

Login, logout, forgot password

Admin can approve users from Django Admin Panel

Models:

User (extends AbstractUser):
{username, email, role, is_verified, date_joined}

2. 🏷️ Lost & Found Items

Add item (lost/found)

Upload image (stored in /media/items/)

Fields: {title, description, category, image, location, status, user, created_at}

Admin approves before public display (is_approved=False default)

Flow:

User posts → Admin approves → Item appears on homepage

3. 💬 Chat System

Real-time chat between two verified users

Powered by Django Channels (WebSockets)

Chat model:
{sender, receiver, message, timestamp}

Optional image messaging

4. 🔔 Notifications

On item approval → user receives an email or in-app alert

On new message → receiver gets notification

Uses Django Signals or WebPush

5. 🧑‍💻 Admin Dashboard

Manage users & approve verification

Manage all items (approve/reject)

View chat logs (optional)

🧱 Folder Structure
campus_connect/
│
├── manage.py
├── requirements.txt
├── campus_connect/        # Main settings & URLs
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── users/                 # Auth app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│
├── items/                 # Lost & Found
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── chat/                  # Chat system
│   ├── consumers.py
│   ├── models.py
│   ├── routing.py
│
├── templates/             # HTML Templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── dashboard.html
│
├── static/                # JS, Tailwind CSS, images
│
└── media/                 # Uploaded item images

🚀 Development Flow for Cursor (AI)
🟦 Phase 1: Project Setup & Authentication




🟩 Phase 2: Lost & Found Module



🟨 Phase 3: Chat System



🟧 Phase 4: Notifications


🟥 Phase 5: Testing & Deployment




🧑‍💻 Owner

Name: Yasir Imran
University: Punjab University College of Information Technology (PUCIT)
Role: Scrum Master & Developer
Project Type: FYP / Smart Lost & Found System
Goal: Learn Django full-stack development through AI-guided building

