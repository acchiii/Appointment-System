# SchoolDesk — Student Appointment System
### A Django Web Application for School Office Management

---

## 📋 Overview
SchoolDesk is a full-stack Django web application that allows students to book,
view, edit, and cancel appointments with school offices (Registrar, Enrollment,
Document Services). It streamlines office operations and reduces long queues.

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### 2. Clone / Extract the Project
```bash
cd appointment_system
```

### 3. Create a Virtual Environment (recommended)
```bash
python -m venv venv

# Activate (Windows):
venv\Scripts\activate

# Activate (macOS / Linux):
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser (Admin Access)
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 7. Run the Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
- **Home Page:**        http://127.0.0.1:8000/
- **Book Appointment:** http://127.0.0.1:8000/book/
- **View Appointments:**http://127.0.0.1:8000/appointments/
- **Admin Panel:**      http://127.0.0.1:8000/admin/

---

## 🗂️ Project Structure

```
appointment_system/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created after migrate
├── appointment_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── appointments/
    ├── models.py           ← Appointment model
    ├── views.py            ← CRUD views
    ├── forms.py            ← AppointmentForm + SearchForm
    ├── urls.py             ← App URL routing
    ├── admin.py            ← Django admin config
    ├── migrations/
    │   └── 0001_initial.py
    ├── templates/
    │   └── appointments/
    │       ├── base.html
    │       ├── home.html
    │       ├── book.html
    │       ├── appointments_list.html
    │       ├── edit_appointment.html
    │       └── confirm_delete.html
    └── static/
        └── css/
            └── style.css
```

---

## 📊 Database Model: Appointment

| Field        | Type          | Notes                             |
|--------------|---------------|-----------------------------------|
| id           | AutoField     | Primary Key                       |
| student_name | CharField     | Required                          |
| student_id   | CharField     | Optional                          |
| email        | EmailField    | Required                          |
| contact      | CharField     | Required (min 10 digits)          |
| office       | CharField     | Registrar / Enrollment / Document |
| date         | DateField     | Must be future Mon–Fri            |
| time         | TimeField     | Must be 8AM–5PM                   |
| purpose      | CharField     | Choices from dropdown             |
| notes        | TextField     | Optional                          |
| status       | CharField     | Pending / Approved / Done / Cancelled |
| created_at   | DateTimeField | auto_now_add=True                 |
| updated_at   | DateTimeField | auto_now=True                     |

---

## ✅ Features
- Full CRUD: Create, Read, Update, Delete appointments
- Input validation (date range, weekdays, time range, contact format)
- Search by name, student ID, email, or purpose
- Filter by office, status, and date
- Status workflow: Pending → Approved → Done / Cancelled
- Django Admin with bulk actions and list_editable status
- Responsive design (mobile-friendly)
- Success/error flash messages
- Clean editorial UI with DM Serif Display + DM Sans fonts

---

## 👤 Admin Panel Features
- URL: `/admin/`  (login with superuser credentials)
- View, search, filter all appointments
- Bulk actions: mark as Approved, Done, or Cancelled
- Inline status editing from list view
- Date hierarchy navigation
- Full fieldsets for detailed view/edit

---

## 📝 License
For academic / capstone project use.
