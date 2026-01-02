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

## ⚙️ Setup Instructions

### Backend Setup
bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Run services in separate terminals:

redis-server
celery -A main.celery worker --loglevel=info
celery -A main.celery beat --loglevel=info
python main.py

Frontend Setup

cd frontend
npm install
npm run dev

📌 Highlights
	•	Implements asynchronous processing like real production systems
	•	Demonstrates scalable backend architecture
	•	Practical experience with task queues and message brokers

🎯 What I Learned
	•	Designing end-to-end full-stack systems
	•	Handling async workflows using Celery & Redis
	•	Coordinating multiple services in a single application
