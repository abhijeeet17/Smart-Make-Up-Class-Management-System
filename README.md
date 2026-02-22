🎓 LPU Smart Campus Management System
Smart Make-Up & Remedial Class Management Platform

Course: Python and Full Stack
Project: Project II
Framework: Django
Database: SQLite

📌 Project Overview

The LPU Smart Campus Management System is a web-based platform designed to digitize and streamline the management of Make-Up and Remedial Classes at Lovely Professional University.

Traditional remedial attendance systems rely on manual tracking and paper signatures. This system replaces that process with a secure, time-bound remedial code system, ensuring real-time validation and structured record keeping.

🚀 Core Features
👩‍🏫 Faculty Portal

Schedule make-up / remedial classes

Generate unique 6-character remedial codes per session

Set code expiry duration (15 min / 30 min / 1 hr / 2 hrs)

View real-time student attendance

Manage class lifecycle (Upcoming → Active → Completed)

Edit and delete classes

🎓 Student Portal

Mark attendance using remedial code

Prevent duplicate attendance marking

View complete make-up attendance history

User-friendly 6-box visual code entry UI

🔐 Admin Panel

Full system access via Django Admin

Manage users, classes, and attendance records

🛠️ Tech Stack
Layer	Technology
Backend	Django (Python)
Database	SQLite
Authentication	Django Auth System
Frontend	HTML, CSS, Bootstrap
Real-Time Features	AJAX + JSON Responses
⚙️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/abhijeeet17/Smart-Make-Up-Class-Management-System.git
cd Smart-Make-Up-Class-Management-System
2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Apply Migrations (Creates SQLite Database)
python manage.py makemigrations
python manage.py migrate
5️⃣ Create Superuser
python manage.py createsuperuser
6️⃣ Run Development Server
python manage.py runserver
7️⃣ Open in Browser
http://127.0.0.1:8000/
📂 Project Structure
lpu_campus/
│
├── lpu_campus/                # Django project configuration
│   ├── settings.py            # App settings (SQLite, installed apps)
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py
│
├── attendance/                # Main application
│   ├── models.py              # UserProfile, MakeUpClass, RemedialCode, MakeUpAttendance
│   ├── views.py               # Authentication + portal logic
│   ├── forms.py               # Django ModelForms
│   ├── urls.py                # App URL patterns
│   ├── admin.py               # Admin registrations
│   └── templates/
│       └── attendance/
│           ├── base.html
│           ├── login.html
│           ├── register.html
│           ├── dashboard.html
│           ├── faculty_classes.html
│           ├── schedule_class.html
│           ├── class_detail.html
│           ├── mark_attendance.html
│           ├── my_attendance.html
│           └── confirm_delete.html
│
├── manage.py
├── requirements.txt
└── README.md
🔑 Remedial Code System – Workflow

Faculty schedules a make-up class.

On the session day, faculty generates a remedial code.

System creates a unique 6-character alphanumeric code (e.g., AB1C2D).

The code has a defined expiry time.

Students enter the code in the attendance portal.

System validates:

Code exists

Code is active

Code is not expired

Student has not already marked attendance

Attendance is stored in a separate table (MakeUpAttendance).

Faculty can view attendance in real-time.

🧠 Django & Python Concepts Implemented

Django ORM (Models, ForeignKey, OneToOneField)

User role extension using UserProfile

ModelForms with custom validation (clean())

Django Authentication (login, logout, @login_required)

Django Messages Framework

Timezone-aware expiry using timezone.now()

Secure code generation using random.choices()

AJAX with JsonResponse for live countdown

Django Admin customization

👥 User Roles
Role	Permissions
Faculty	Schedule classes, generate codes, view attendance
Student	Mark attendance, view own records
Admin	Full system control via /admin/
🎯 Problem Solved

✔ Eliminates paper-based attendance
✔ Prevents proxy attendance
✔ Ensures time-bound validation
✔ Provides structured make-up attendance records
✔ Enables real-time faculty monitoring

📌 Future Enhancements

QR-based attendance marking

SMS / Email code sharing

Analytics dashboard (attendance insights)

Deployment on cloud (AWS / Render / Railway)

Integration with main university ERP

👨‍💻 Developed For

Lovely Professional University
Project II – Python and Full Stack
