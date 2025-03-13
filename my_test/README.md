# Multi-Agent Chat Application

This is a full-stack application that demonstrates multi-agent conversations using AgentScope, React, and Flask.

## Project Structure
```
my_test/
├── backend/           # Flask backend
│   ├── app.py        # Flask application
│   └── multiagents.py # Agent logic
├── frontend/         # React frontend
└── requirements.txt  # Python dependencies
```

## Setup Instructions

### Backend Setup
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask backend:
   ```bash
   cd backend
   python app.py
   ```
   The backend will run on http://localhost:5000

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```
   The frontend will run on http://localhost:3000

## Usage
1. Open http://localhost:3000 in your browser
2. Click the "Start Conversation" button to begin a new multi-agent conversation
3. Watch as Alice, Bob, and Charlie interact with each other

## Deployment
For production deployment:
1. Build the React frontend:
   ```bash
   cd frontend
   npm run build
   ```
2. Configure your web server to serve the static files from the `frontend/build` directory
3. Set up the Flask backend with a production WSGI server like Gunicorn 