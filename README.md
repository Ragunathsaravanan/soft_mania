# Soft Mania

Soft Mania is a Django-based web application that allows users to register, log in, upload files (PDF, PNG, JPG, JPEG), and download them securely. The application uses a custom user model with email-based authentication and includes an admin panel for managing users and uploaded files.

---

## Features

- User signup and login with email.
- File upload with type and size restrictions (max 10 MB).
- File download for authenticated users.
- Dashboard to view user-specific files.
- Admin panel to manage users and uploaded files.

---

## Non-Functional Requirements Addressed

- **Modular and Clean Code:** Models, views, and admin customizations are separated in their respective files.  
- **Documentation:** Code is commented for clarity.  
- **Error Handling:** Invalid inputs, file types, and file sizes are validated with user-friendly error messages.  
- **Security Best Practices:**
  - Passwords are hashed using Django's default password hashing.  
  - Session-based authentication is used.  
  - File uploads are restricted to specific types and sizes.  

---

## Technology Stack

- **Backend:** Django 5.0.1, Python 3.11+  
- **Database:** MySQL  
- **Frontend:** HTML, CSS (Django templates)  
- **Hosting:** Render - https://soft-mania-7.onrender.com/

---

## Local Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Ragunathsaravanan/soft_mania.git
cd soft_mania
