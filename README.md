# DeepVerify AI

AI-powered dashboard for detecting AI-generated media.

## Features
- Upload images/videos
- Analyze media
- AI-generated detection
- Dashboard analytics
- Detection history
- SQLite database
- Streamlit frontend
- FastAPI backend

- Technologies You Used
Python
Main programming language used for backend logic and processing.
FastAPI
Used to build the backend API that receives uploaded media and returns AI detection results.
Streamlit
Used to create the interactive dashboard UI where users upload files and view results.
SQLite
Stores scan history, predictions, confidence scores, timestamps, and uploaded file information.
Pandas
Used for reading and managing stored detection data inside the dashboard.
Plotly
Used for charts, analytics, and visual dashboards.
Requests
Allows the Streamlit frontend to communicate with the FastAPI backend.
MD5
Used to generate a unique hash from uploaded files so the same image produces consistent analysis results.


Simple Architecture Flow
User Uploads Image/Video
          ↓
Streamlit Dashboard (Frontend UI)
          ↓
FastAPI Backend API
          ↓
Detector Logic (Hash + Analysis)
          ↓
SQLite Database Stores Results
          ↓
Dashboard Shows Prediction + Confidence
