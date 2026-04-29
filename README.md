# 📚 Library Management System (LMS) API

A RESTful API built using **Django** and **Django REST Framework (DRF)** for managing books, authors, genres, borrow requests, and reviews.

---

## 🚀 Features

* 🔐 JWT Authentication (Login / Register)
* 👤 Role-based access (Student / Librarian)
* 📚 Book Management (CRUD operations)
* ✍️ Author & Genre Management
* 🔄 Borrow Request System (Approve / Reject / Return)
* ⭐ Book Reviews
* 📧 Email Notification on Approve/Reject
* 🔍 Search, Filtering & Ordering
* ⚡ Rate Limiting on Borrow API
* 📄 Pagination Support
* 📑 Swagger / API Documentation

---

## 🛠 Tech Stack

* Python 3.x
* Django
* Django REST Framework (DRF)
* Simple JWT
* SQLite
* drf-spectacular (Swagger API Docs)

---

## 📂 Project Structure

```
LMS/
│
├── library/
│   ├── __pycache__/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│
├── lms/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── utils/
│   ├── __pycache__/
│   ├── email_utils.py
│   ├── permissions.py
│
├── db.sqlite3
├── manage.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/Jenil49/lms.git
cd LMS
```

---

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Run migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Run server

```
python manage.py runserver
```

---

## 🔐 Authentication APIs

### Register

```
POST /api/register/
```

### Login (JWT)

```
POST /api/token/
```

---

## 📚 API Endpoints

### 📘 Books

* `GET /api/books/`
* `POST /api/books/`
* `GET /api/books/{id}/`
* `PUT /api/books/{id}/`
* `DELETE /api/books/{id}/`

---

### ✍️ Authors & Genres

* `GET /api/authors/`
* `POST /api/authors/`
* `GET /api/genres/`
* `POST /api/genres/`

---

### 🔄 Borrow Requests

* `POST /api/borrow/`
* `GET /api/borrow/`
* `PATCH /api/borrow/{id}/approve/`
* `PATCH /api/borrow/{id}/reject/`
* `PATCH /api/borrow/{id}/return_book/`

---

### ⭐ Reviews

* `POST /api/books/{id}/reviews/`
* `GET /api/books/{id}/reviews/`

---

## 🔍 Filtering, Search & Ordering

```
GET /api/books/?author=1
GET /api/books/?genres=2
GET /api/books/?search=django
GET /api/books/?ordering=title
```

---

## 📄 Pagination

```
GET /api/books/?page=1
```

---

## ⚡ Rate Limiting

Borrow requests are limited to:

```
3 requests per minute (configurable)
```

---

## 📧 Email Notifications

Emails are sent when:

* ✅ Borrow request is **approved**
* ❌ Borrow request is **rejected**

---

## 📑 API Documentation

* Swagger UI → http://127.0.0.1:8000/swagger/
* Redoc → http://127.0.0.1:8000/redoc/

---

## 🧠 Key Concepts Used

* Nested Serializers
* Custom Permissions
* JWT Authentication
* DRF Throttling
* Filtering & Pagination
* Clean Code Structure
* Utility-based Email Handling

---