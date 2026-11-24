# Student Attendance Management System

A web app built with Django where teachers mark attendance and students track their attendance percentage.

## Features
- Teacher and student login (role-based redirect)
- Mark attendance for all students in one page
- Student dashboard with attendance % per course and a bar chart
- Low attendance warning (below 75%)
- Defaulters list for teachers
- Email alerts to defaulters (console backend for demo)

## Tech Stack
Python, Django, SQLite, HTML, Bootstrap, Chart.js

## How to Run
```
git clone https://github.com/utkarsha-pansare/student-attendance-system.git
cd student-attendance-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Then open http://127.0.0.1:8000/admin to add students, courses and users, and http://127.0.0.1:8000/login/ to log in.

## Future Improvements
- QR code based attendance
- Defaulter prediction using scikit-learn
- Deployment on Render