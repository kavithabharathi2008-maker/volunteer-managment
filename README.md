# Community Needs Intelligence & Volunteer Matching Web Platform

A complete full-stack web application that solves the problem of scattered community data by collecting, analyzing, and prioritizing needs, and automatically matching volunteers to tasks.

## 🚀 Features

### 🌐 Frontend (Modern UI)
- **Home Page**: Platform overview with clear CTAs for NGOs and Volunteers.
- **NGO Dashboard**: Manual entry or CSV upload for community issues, plus a tracking table.
- **Volunteer Dashboard**: Profile management (skills/location) and task tracking with status updates.
- **Admin Dashboard**: Advanced analytics, urgency heatmaps, and intelligent volunteer assignment.
- **Live Map**: Real-time visualization of community needs using Leaflet.js.

### ⚙️ Backend & Intelligence
- **REST APIs**: Built with Python & Flask.
- **Smart Prioritization**: Algorithms that rank issues based on urgency and category impact.
- **Intelligent Matching**: Scoring system based on skill sets, location proximity, and availability.
- **AI Chatbot**: Integrated Google Gemini AI to assist users in navigating the platform.

---

## 🛠️ Local Setup Instructions

### 1. Prerequisites
- Python 3.8+
- [Optional] Google Gemini API Key (for the chatbot).

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Initialize Database & Sample Data
We've provided a script to set up the database and populate it with demo data.
```bash
python seed_data.py
```
This creates a `community.db` (SQLite) file with pre-configured Admin, NGO, and Volunteer accounts.

### 5. Run the App
```bash
python app.py
```
Visit: `http://127.0.0.1:5000`

---

## 🔑 Demo Accounts
For presentation/testing purposes, use these pre-seeded accounts:

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@example.com` | `admin123` |
| **NGO** | `ngo@example.com` | `any` |
| **Volunteer** | `john@example.com` | `any` |

---

## ☁️ Deployment Guide

### Backend & Database (Render / Railway)
1. **Database**: Create a MySQL or PostgreSQL instance on Render/Railway.
2. **Environment Variable**: Set `DATABASE_URL` in your deployment settings.
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn app:app`

### Firebase (Hosting + Functions)
1. **Initialize**: `firebase init` (Select Hosting and Functions).
2. **Project**: Select your existing Firebase project.
3. **Deploy**:
```bash
firebase deploy
```
*(Note: Ensure you have upgraded to the Firebase Blaze plan to use Cloud Functions for Python).*

---

## 🧠 Database Schema (MySQL)
If you prefer MySQL, use the provided `schema.sql` file. Update `app.py` to connect:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:pass@localhost/community_db'
```

---

*Built for the Community Needs Hackathon.*
