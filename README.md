# Modern Application Development 2 - Project (Vehicle Parking App)

##  Project Overview
This is a **full-stack application** developed for the **Modern Application Development 2 (MAD2)** course. It simulates a vehicle parking management system where users can interact with a frontend UI and backend services to handle parking data and related processes.

The project integrates a Vue.js frontend with a Python backend and uses Celery & Redis for task handling.

##  Key Features
- Full frontend UI built with Vue.js
- Backend API server in Python (Flask)
- Asynchronous task processing with Celery
- Redis for task queue management

##  Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Vue.js |
| Backend | Python (Flask) |
| Task Queue | Celery |
| Message Broker | Redis |

## Repo Structure

├── backend/                   ← Flask API & Celery workers
├── frontend/                  ← Vue.js web UI
├── MAD2_Report.pdf            ← Final course report

## Setup & Run Instructions
**Backend**
bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Then in separate terminals:
redis-server
celery -A main.celery worker --loglevel=info
celery -A main.celery beat --loglevel=info
python main.py

Frontend
cd frontend
npm install
npm run dev


📌 Project Highlights
	•	Real-time task queue with Celery
	•	Clean separation of frontend & backend
	•	Practical exposure to modern full-stack workflows

🎯 What I Learned
	•	How to orchestrate frontend and backend in a real project
	•	Use of Redis and Celery for asynchronous operations
	•	Deployment-ready architecture and task scheduling

  




