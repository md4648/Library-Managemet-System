# 📚 Library Reservation System (Frappe App)

A modern **Library Reservation and Loan Management System** built with the [Frappe Framework](https://frappeframework.com/). This system streamlines book reservations, loans, and role-based access with a custom frontend and secure backend APIs.

---

## 🚀 Features

### 🔒 User Authentication & Role-Based Access

- Secure login using Frappe’s authentication system
- Role-based UI & permissions:
  - **Admin**: Full access to all features
  - **Librarian**: Can manage books, reservations, and loans
  - **Member**: Can browse, reserve, and view own loan history

### 📘 Book Management

- Add, edit, or delete books
- View real-time availability

### 📥 Book Reservation

- Members can reserve available books
- Prevents duplicate reservations
- Only one active reservation per book per member

### 📤 Loan Management

- Librarian can issue books directly or from existing reservations
- Tracks loan and return dates
- Book availability updates automatically

### 📃 Frontend Pages (HTML)

- `/loan` → Issue book page
- `/loanList` → View issued books
- `/reservation` → Make a reservation
- `/reservationList` → View reservations

### 🧩 API Integration

- Custom REST API for loan and reservation actions

---

## 🧑‍💻 Tech Stack

- Frappe Framework (v15)
- Python
- Tailwind CSS & Bootstrap for UI
- REST API via custom Python methods

---

## ⚙️ Installation

### 📋 Prerequisites

- Python 3.10+
- Node.js & npm
- Redis & MariaDB
- wkhtmltopdf
- Frappe Bench CLI

### 🧭 Setup Steps

```bash
# 1. Install Bench CLI
pip install frappe-bench

# 2. Create new bench
bench init lms-bench --frappe-branch version-15
cd lms-bench

# 3. Create a new site
bench new-site lms.com

# 4. Get the app (replace URL with your repo)
cd apps
git clone https://github.com/your-username/library_management.git
cd ..

# 5. Install the app
bench --site lms.com install-app library_management

# 6. Start development server
bench start
```

### 🧭 Screen Shoots

**Login Page**

![Image](https://github.com/user-attachments/assets/0a7e083e-5a3b-47c9-be0b-ac0b1e7e88b1)

**Book Page**

![Image](https://github.com/user-attachments/assets/f2d6f43b-ed94-4bf0-aa16-360901f0070f)

**Landing Page**
![Image](https://github.com/user-attachments/assets/ad1b2552-d0db-445f-84f2-ab2a81c58142)

**Dash Board**

![Image](https://github.com/user-attachments/assets/c3fc7c37-3a36-496c-89db-5f9f38684cb4)

**Loan List**

![Image](https://github.com/user-attachments/assets/039863c0-d541-4f0a-a7f0-b793b21f71b3)
