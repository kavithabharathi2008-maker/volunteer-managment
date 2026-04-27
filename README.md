# Community Needs Aggregator & Volunteer Matching System

A full-stack web application designed to help local NGOs and social groups collect, organize, and analyze community data, and intelligently match volunteers to urgent needs.

## Features
- **Data Collection**: Upload CSV files or manually enter community needs.
- **Dashboard**: View charts and a map visualizing the reported issues and their urgency.
- **Smart Prioritization**: Automatically calculate a priority score based on urgency and issue type.
- **Volunteer Management**: Register volunteers with their skills and availability.
- **Intelligent Matching**: Suggest the best volunteers for a specific task based on skill intersection and location proximity.
- **AI Chatbot**: Integrated Google Gemini AI assistant to help users navigate the platform.

## Setup Instructions (Local Development)

### 1. Prerequisites
- Python 3.8+
- [Optional] A Google Gemini API Key for the chatbot.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
To enable the AI Chatbot, create a `.env` file in the root directory and add your Gemini API Key:
```
GEMINI_API_KEY=your_actual_api_key_here
```
*(If you do not set this, the app will still run, but the chatbot will return a disabled message).*

### 4. Run the Application
```bash
python app.py
```
This will automatically create a local `community.db` SQLite database file and start the server.
By default, the application will run at `http://127.0.0.1:5000`.

### 5. Using the Application
1. **Initialize Data**: Go to **Report Issue** and upload the provided `sample_data.csv` to populate the database with tasks.
2. **Dashboard**: Navigate to the Dashboard to see the charts and map populate.
3. **Volunteers**: Go to **Volunteers** and register a new volunteer (e.g., Skills: "cooking, first aid", Location: "San Francisco").
4. **Matching**: Go to **Tasks**, find a pending task, and click "Find Match" to test the matching algorithm.

## Database Note
This prototype uses **SQLite** by default for a beginner-friendly, zero-configuration setup. 
To switch to **MySQL** (as requested), open `app.py`, comment out the SQLite line, uncomment the MySQL line, and update the connection string with your local MySQL credentials. You will also need to have the `pymysql` driver installed (it is included in `requirements.txt`).
