# MAD2 (Vehicle Parking App)
## Setup & Run Instructions

### 1. Backend Setup (First Time Only)

cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### Terminal1
redis-server
redis-cli ping(checking)

### Terminal2
cd backend
source venv/bin/activate
python main.py

### Terminal3
cd backend
celery -A main.celery worker --loglevel=info

### Terminal4
cd backend
celery -A main.celery beat --loglevel=info

### Terminal5(Email Server)
mailhog
http://localhost:8025

### Terminal6
cd frontend
npm install
npm run dev