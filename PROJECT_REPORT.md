# Campus Connect - Project Technical Report

## Presentation Plan & Team Roles

This report is structured to be presented by the team members in the following order. Each member is responsible for explaining their assigned section, highlighting the software engineering principles and technical details involved.

| Order | Presenter          | Role                  | Section Assigned                                   |
| :---- | :----------------- | :-------------------- | :------------------------------------------------- |
| **1** | **Yasir (Leader)** | Introduction & Vision | **1. Project Overview**                            |
| **2** | **Hanan**          | Methodology Expert    | **2. Software Engineering Principles Applied**     |
| **3** | **Umer**           | Tech Stack Specialist | **3. Technology Stack & Roles**                    |
| **4** | **Ahad**           | System Architect      | **4. Detailed Code Workflow**                      |
| **5** | **Ajmal**          | QA Engineer           | **5. Testing & Quality Assurance**                 |
| **6** | **Yasir (Leader)** | Deployment Manager    | **6. Deployment Architecture** & **7. Conclusion** |

---

## 1. Project Overview (Presenter: Yasir)

**Campus Connect** is a centralized, digital "Lost & Found" platform designed specifically for university campuses. It addresses the inefficiency of manual lost and found systems by providing a secure, accessible, and real-time web application for students and administration.

### Key Objectives

- **Digitalization:** Transition from physical logbooks to a searchable digital database.
- **Security:** Restrict access to verified university students (email validation) and admin-approved accounts.
- **Real-time Communication:** Enable direct, secure chat between the finder and the owner of an item.
- **Efficiency:** Streamline the reporting and recovery process through categorization and search filters.

---

## 2. Software Engineering Principles Applied (Presenter: Hanan)

The development of Campus Connect follows standard Software Engineering practices, specifically the **Agile Methodology**, to ensure maintainability, scalability, and security.

### A. Process Model: Agile & Sprints

We adopted an iterative approach, dividing the development lifecycle into **Sprints** (2-week cycles).

- **Sprint 1 (Core):** Setup, Authentication (Login/Register), and Database Design.
- **Sprint 2 (Features):** CRUD operations for Lost/Found items, Image Uploads.
- **Sprint 3 (Real-time):** Chat system implementation using WebSockets.
- **Sprint 4 (Polish):** UI improvements, Testing, and Deployment.

### B. Umbrella Activities

Throughout the project, several "Umbrella Activities" were performed continuously across all phases:

- **Project Management:** Tracking progress using Trello/GitHub Projects.
- **Quality Assurance (QA):** Continuous testing of features as they were built.
- **Configuration Management:** Using **Git** for version control to manage code changes.

### C. Core Principles

| Stage                     | Principle / Methodology                 | Implementation Details                                                                                                              |
| :------------------------ | :-------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Requirement Analysis**  | **Problem-Solution Fit**                | Identified the "disconnect" in current manual systems and defined clear objectives (Security, Accessibility).                       |
| **Design & Architecture** | **MVT (Model-View-Template)**           | Leveraged Django's MVT architecture to separate data (Models), logic (Views), and presentation (Templates).                         |
| **Development**           | **Modularity (Separation of Concerns)** | The project is divided into distinct apps: `users` (Auth), `items` (Core Logic), and `chat` (Communication).                        |
| **Security**              | **Defense in Depth**                    | Implemented multiple layers of security: Email Domain Validation, Admin Approval (`is_verified`), CSRF Tokens, and Auth Middleware. |
| **Scalability**           | **Asynchronous Processing**             | Used **Django Channels** and **ASGI** to handle real-time WebSocket connections without blocking the main thread.                   |

---

## 3. Technology Stack & Roles (Presenter: Umer)

The project utilizes a modern, robust tech stack. Below is the breakdown of each component and its specific role in the system.

### Backend & Core

| Component            | Technology        | Role in Campus Connect                                                                         |
| :------------------- | :---------------- | :--------------------------------------------------------------------------------------------- |
| **Framework**        | **Django 5.0**    | The core web framework handling routing, ORM (database interactions), and business logic.      |
| **Language**         | **Python**        | The primary programming language, chosen for its readability and rich ecosystem.               |
| **Real-time Server** | **Daphne / ASGI** | An asynchronous server interface that allows Django to handle WebSockets for the chat feature. |

### Frontend & UI

| Component      | Technology                 | Role in Campus Connect                                                               |
| :------------- | :------------------------- | :----------------------------------------------------------------------------------- |
| **Styling**    | **Tailwind CSS**           | A utility-first CSS framework used for rapid, responsive, and modern UI development. |
| **Templating** | **Django Templates (DTL)** | Renders dynamic data (e.g., item lists, user profiles) directly into HTML.           |

---

## 4. Detailed Code Workflow (Request-Response Cycle) (Presenter: Ahad)

Understanding how the code executes when a user interacts with the website.

### Scenario: A User Views the "Lost Items" Page

1.  **URL Routing (`urls.py`):**

    - The user visits `/items/`.
    - Django's URL dispatcher matches this path to the `items.urls` module.
    - It finds the specific path `path('', views.ItemList.as_view(), name='item-list')`.

2.  **View Logic (`views.py`):**

    - The request is passed to the `ItemList` view (a Class-Based View).
    - **Query:** The view queries the database using the ORM: `Item.objects.filter(status='active')`.
    - **Context:** The retrieved data is packaged into a "context" dictionary.

3.  **Template Rendering (`templates/items/item_list.html`):**
    - Django loads the HTML template.
    - It injects the context data into the placeholders (e.g., `{% for item in items %}`).
    - The final HTML is generated and sent back to the user's browser.

---

## 5. Testing & Quality Assurance (Presenter: Ajmal)

To ensure the reliability of Campus Connect, we implemented a structured testing strategy.

### A. Testing Levels

- **Unit Testing:** Testing individual components in isolation.
  - _Example:_ `test_email_validation.py` checks if the email validator correctly accepts `@pucit.edu.pk` and rejects others.
- **Integration Testing:** Verifying that different modules work together.
  - _Example:_ Testing if a user can successfully register, login, and then post an item (involving `users` and `items` apps).
- **System Testing:** Validating the complete application flow.
  - _Example:_ End-to-end flow of reporting an item -> searching for it -> chatting with the finder.

### B. QA Tools & Practices

- **Django Test Framework:** Used for writing and running automated test cases.
- **Manual Testing:** Performed UI/UX testing on different devices (Mobile vs Desktop) to ensure responsiveness.
- **Bug Tracking:** Issues found during testing were logged and assigned to developers for fixing before the next sprint.

---

## 6. Deployment Architecture (PythonAnywhere) (Presenter: Yasir)

Deploying to PythonAnywhere transforms the local development code into a live, accessible web service. This involves specific configurations for handling code execution and file storage.

### A. The Web Server Gateway Interface (WSGI)

- **Role:** In development, we use `python manage.py runserver`. In production on PythonAnywhere, we cannot use this.
- **Implementation:** PythonAnywhere uses **uWSGI** to serve the application.
- **Configuration:** The `wsgi.py` file in the project acts as the entry point. It exposes the Django application object that the web server communicates with to handle incoming HTTP requests.

### B. Static Files Handling (CSS/JS)

- **Challenge:** Django does not serve static files (like `custom.css` or `main.js`) efficiently in production.
- **Solution:**
  1.  We run `python manage.py collectstatic`. This command gathers all static files from all apps into a single folder called `staticfiles` or `static_root`.
  2.  **PythonAnywhere Configuration:** In the "Web" tab, a mapping is created:
      - **URL:** `/static/`
      - **Directory:** `/home/username/Campus-Connect/static`
  - **Result:** When a browser asks for `style.css`, the web server (NGINX/Apache) serves it directly from the folder, bypassing Django entirely for speed.

### C. Media Files & Image Upload Workflow (Critical)

Handling user-uploaded content (images) requires a specific flow in a deployed environment.

#### 1. The Upload Process

- **User Action:** A user fills out the "Report Lost Item" form and attaches an image.
- **Django Model:** The `Item` model has an `ImageField(upload_to='items/%Y/%m/%d/')`.
- **Storage:** When saved, Django renames the file (to prevent duplicates) and saves it to the server's filesystem under the `media/` directory (e.g., `/home/username/Campus-Connect/media/items/2025/12/15/lost_wallet.jpg`).
- **Database:** The database **does not** store the image itself. It stores the **path** (string) to the image: `items/2025/12/15/lost_wallet.jpg`.

#### 2. Serving the Image (The "Missing Link")

- **The Problem:** By default, for security, web servers do not allow public access to file uploads.
- **The Fix:** On PythonAnywhere, we must explicitly tell the server to allow access to the `media` folder.
- **Configuration:**
  - **URL:** `/media/`
  - **Directory:** `/home/username/Campus-Connect/media`
- **The Flow:**
  1.  Browser requests: `www.campusconnect.com/media/items/wallet.jpg`.
  2.  PythonAnywhere sees the `/media/` prefix.
  3.  It looks into the mapped folder on the hard drive.
  4.  It serves the image file back to the user.

---

## 7. Conclusion (Presenter: Yasir)

**Campus Connect** demonstrates a complete software engineering lifecycle. From the initial **Requirement Analysis** to the **MVT Architecture** design, and finally to the **Deployment** on PythonAnywhere. The separation of concerns ensures that logic, data, and presentation are distinct, while the specific deployment configuration ensures that static assets and user-uploaded media are served securely and efficiently in a production environment.
