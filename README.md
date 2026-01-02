# MAD2 Project – Full-Stack Vehicle Parking Management System

##  Overview
This is a full-stack web application developed as part of **Modern Application Development 2 (MAD2)**.  
The system simulates a vehicle parking management platform with a modern frontend, backend APIs, and asynchronous task processing.

The project demonstrates real-world full-stack architecture used in production systems.

---

##  Key Features
- Modern frontend built using Vue.js
- Backend REST APIs using Python (Flask)
- Asynchronous background task execution using Celery
- Redis used as a message broker
- Clean separation of frontend and backend services

---

##  System Architecture
- **Frontend** communicates with backend APIs
- **Backend** handles business logic and database operations
- **Celery workers** process background tasks
- **Redis** manages task queues

---

##  Tech Stack
| Layer | Technology |
|-----|-----------|
| Frontend | Vue.js |
| Backend | Python (Flask) |
| Async Tasks | Celery |
| Message Broker | Redis |
| Tools | Git, GitHub |

---

##  Repository Structure

MAD2-Project/
│
├── backend/          # Flask backend & Celery configuration


├── frontend/         # Vue.js frontend application


├── MAD2_Report.pdf   # Detailed project report


└── README.md


---


##  Setup Instructions

### Backend Setup
bash

1. cd backend

2. python -m venv venv

3. source venv/bin/activate

4. pip install -r requirements.txt

Run services in separate terminals:

1. redis-server
2. celery -A main.celery worker --loglevel=info
3. celery -A main.celery beat --loglevel=info
4. python main.py

Frontend Setup
1. cd frontend
2. npm install
3. npm run dev

---

📌 Highlights
	•	Implements asynchronous processing like real production systems
	•	Demonstrates scalable backend architecture
	•	Practical experience with task queues and message brokers

🎯 What I Learned
	•	Designing end-to-end full-stack systems
	•	Handling async workflows using Celery & Redis
	•	Coordinating multiple services in a single application
