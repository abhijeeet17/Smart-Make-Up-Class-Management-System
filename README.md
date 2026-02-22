🎓 Smart Make-Up Class Management System
🚀 Digitizing Remedial Attendance with Secure Expiring Codes

A Django-based web application built to modernize and automate the management of make-up and remedial classes in universities.

Instead of paper signatures and manual tracking, this system generates time-bound secure attendance codes that ensure real-time validation and prevent proxy attendance.

📌 Project Overview

Large universities often struggle with unstructured remedial class tracking. Faculty manually record attendance, and there is no validation mechanism.

🔎 This project solves that problem by:

Generating unique session-based attendance codes

Enforcing expiry-based validation

Preventing duplicate attendance entries

Providing real-time tracking dashboards

✨ Core Features
👩‍🏫 Faculty Portal

Create and schedule make-up/remedial classes

Generate unique 6-character alphanumeric codes

Set custom expiry durations (15 min / 30 min / 1 hr / 2 hrs)

View real-time attendance data

Edit or delete scheduled classes

👨‍🎓 Student Portal

Enter remedial code to mark attendance

Prevent duplicate attendance submissions

View attendance history

Instant validation feedback (Valid / Expired / Invalid)

🔐 Security & Validation Layer

✔ Code must exist
✔ Code must not be expired
✔ Student must not have already marked attendance
✔ Session must be active

This ensures data integrity and academic transparency.

🛠 Tech Stack
🔹 Backend

Python + Django

🔹 Database

SQLite (default Django DB)

🔹 Frontend

HTML + CSS + Bootstrap

🔹 Authentication

Django Built-in Authentication System

🔹 Dynamic Features

AJAX + JSON for real-time validation

⚙️ How the System Works
Step 1️⃣ – Faculty Creates Session

A remedial class session is scheduled in the system.

Step 2️⃣ – Unique Code Generation

A secure 6-character alphanumeric code is generated.

Step 3️⃣ – Student Marks Attendance

Students enter the code in the portal.

Step 4️⃣ – Backend Validation

The system checks:

Expiry timestamp

Duplicate entry

Valid session

If valid → Attendance recorded
If invalid → Error message displayed

🧩 Project Structure
Smart-Make-Up-Class-Management-System/
│
├── attendance/                 # Core Django app
│   ├── models.py               # Database models
│   ├── views.py                # Business logic
│   ├── forms.py                # Form handling
│   ├── urls.py                 # Routing
│   └── templates/attendance/   # Frontend templates
│
├── manage.py
├── requirements.txt
└── README.md
▶️ How to Run Locally
1️⃣ Clone the Repository
git clone https://github.com/abhijeeet17/Smart-Make-Up-Class-Management-System.git
cd Smart-Make-Up-Class-Management-System
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate
5️⃣ Create Superuser
python manage.py createsuperuser
6️⃣ Start Server
python manage.py runserver

Open in browser:

http://127.0.0.1:8000/
🎯 Problem Solved

✔ Eliminates manual attendance sheets
✔ Prevents proxy attendance
✔ Enforces time-based validation
✔ Centralizes remedial session management
✔ Improves institutional efficiency

📈 Future Enhancements

📱 QR-based attendance marking

📊 Analytics dashboard

☁️ Cloud deployment

📤 Email/SMS code notification

🔗 ERP integration
