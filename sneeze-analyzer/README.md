<img width="1280" height="640" alt="image" src="https://github.com/user-attachments/assets/08bd5b05-fb61-4141-ac3e-d408eeac67ec" />

# Sneeze Analyzer

An AI-powered audio analysis platform that captures sneeze recordings, extracts acoustic features, generates performance scores, produces humorous AI commentary, and ranks users.

## Prerequisites

You will need the following installed on your system to run this project:
1. **Node.js** (v18+ recommended) - [Download here](https://nodejs.org/)
2. **Python** (v3.8+ recommended) - [Download here](https://www.python.org/downloads/)
3. **OpenAI API Key** (Optional for now, mocked in code)

## Setup Instructions

### 1. Backend Setup
The backend runs on Express and uses Python to process the audio.

Open a terminal and navigate to the backend folder:
```bash
cd backend
npm install
```

*(Optional)* Install Python dependencies for real audio analysis (otherwise it uses mock data):
```bash
pip install librosa numpy
```

Start the backend server:
```bash
npm run dev
```
*The backend will run on http://localhost:5000*

### 2. Frontend Setup
The frontend runs on Vite + React.

Open a *new* terminal and navigate to the frontend folder:
```bash
cd frontend
npm install
```

Start the frontend development server:
```bash
npm run dev
```
*The frontend will run on http://localhost:5173*

## Next Steps
- **Database Integration:** The MVP currently mocks database operations. You can expand `server.js` with `mongoose` to connect to MongoDB Atlas.
- **AI Commentary:** In `backend/server.js`, uncomment the OpenAI integration and provide your `OPENAI_API_KEY` to dynamically generate hilarious roasts!
