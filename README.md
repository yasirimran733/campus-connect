# Campus Connect - Smart Lost & Found System

**Tagline:** "Smart Lost & Found System for University Students"

## 1. Problem Statement

University campuses often struggle with inefficient, manual lost and found systems. Students rely on scattered notice boards, social media groups, or physical lost and found offices that are not easily accessible. This leads to:

- Low recovery rates for lost items.
- Lack of centralized information.
- Security concerns regarding who is claiming items.
- Difficulty in searching for specific lost items.

## 2. Why We Built This Project

We built **Campus Connect** to solve the disconnect between students who lose items and those who find them. The goal was to create a **centralized, digital platform** specifically for the **PUCIT** campus that is:

- **Secure:** Ensuring only verified students and staff can participate.
- **Accessible:** Available 24/7 via the web.
- **Efficient:** Making it easy to search, filter, and report items.

## 3. Project Objectives

- **Digitalize the Process:** Move from physical logs to a digital database.
- **Ensure Security:** Implement strict user verification (PUCIT email + Admin approval) to prevent fraud.
- **Improve Recovery Rates:** Make lost items easily searchable with images and detailed descriptions.
- **Facilitate Communication:** Enable secure communication between the finder and the owner.
- **User-Friendly Interface:** Provide a modern, responsive UI that works on all devices.

## 4. Key Features

### Phase 1: Authentication & Security

- **PUCIT Email Validation:** Restricts registration to `@pucit.edu.pk` email addresses.
- **Admin Verification:** New accounts require manual admin approval (`is_verified`) before accessing full features.
- **User Profiles:** Dashboard to manage personal details and posted items.

### Phase 2: Lost & Found Management

- **Report Items:** Users can post "Lost" or "Found" items with titles, descriptions, and locations.
- **Image Uploads:** Support for uploading images to help identify items.
- **Categorization:** Items are organized into categories (Electronics, Documents, Clothing, etc.).
- **Search & Filter:** Powerful search functionality to filter by keyword, category, type, and date.
- **Status Tracking:** Items can be marked as Active, Claimed, Returned, or Closed.
- **Admin Moderation:** All posts must be approved by an admin before going live.

### Phase 3: Communication (Backend Ready)

- **Conversation Model:** Structure in place for 1-on-1 chats between users.
- **Message History:** Persistent storage of chat history linked to specific items.

## 5. Tech Stack

- **Backend:** Django 5+ (Python 3.12)
- **Frontend:** Tailwind CSS + Vanilla JavaScript
- **Database:** PostgreSQL / SQLite
- **Authentication:** Django Auth System with Custom User Model
- **Media:** Django Media Framework for image handling
- **Testing:** Django Test Framework (100% coverage for core features)

## 6. Workflow / Process Flow

1.  **Registration:** Student registers with their university email.
2.  **Verification:** Admin reviews the registration and approves the account.
3.  **Reporting:** Verified user posts a "Lost" or "Found" item with details and photos.
4.  **Moderation:** Admin reviews the post content and approves it.
5.  **Discovery:** The item becomes visible on the public feed. Other users can search and view details.
6.  **Connection:** Users connect via built-in chat to arrange return.
7.  **Resolution:** The item status is updated to "Returned" or "Claimed".

## 7. Results & Achievements

- **Fully Functional Auth System:** Secure registration flow with domain validation is live.
- **Robust Item Management:** Complete CRUD operations for lost/found items are operational.
- **High Code Quality:** The project maintains **100% test coverage** across models, views, and forms.
- **Modern UI:** A responsive, clean interface built with Tailwind CSS.
- **Scalable Architecture:** The codebase is modular (Users, Items, Chat apps) and ready for future expansion.

## 8. Setup Instructions

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

## 9. Project Structure

```
campus_connect/
├── manage.py
├── requirements.txt
├── campus_connect/        # Main settings & URLs
├── users/                 # Authentication app
├── items/                 # Items app
├── chat/                  # Chat app
├── templates/             # HTML Templates
├── static/                # CSS, JS, images
└── media/                 # Uploaded files
```

## 10. Conclusion

**Campus Connect** successfully bridges the gap in campus logistics by providing a secure and efficient platform for managing lost and found items. By leveraging modern web technologies and enforcing strict security measures, it ensures that the system is trustworthy and effective for the university community. The project is well-structured for future enhancements like real-time chat and notifications, making it a solid foundation for a smart campus utility.
