# LawBot Full-Stack Application

## Project Structure

```
LawBot_FullStack/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   ├── core/               # Core modules (model, RAG, tools)
│   ├── services/           # Business logic
│   └── main.py             # FastAPI app entry point
├── frontend/               # React frontend
│   ├── src/                # React components
│   └── public/             # Static assets
├── models/                 # Model files and adapters
├── data/                   # Data files and vectorstore
├── config/                 # Configuration files
├── scripts/                # Utility scripts
└── docs/                   # Documentation
```

## Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Access Application
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Features

✅ **Fine-tuned Qwen2.5-1.5B Model** - Custom legal knowledge  
✅ **RAG Pipeline** - Document retrieval and grounding  
✅ **Tool Integration** - Legal dictionary, date calculator, case lookup  
✅ **FastAPI Backend** - RESTful API with async support  
✅ **React Frontend** - Modern chat interface  
✅ **Docker Support** - Easy deployment  

## API Endpoints

- `POST /api/chat` - Chat with LawBot
- `GET /api/health` - Health check
- `GET /api/models` - Model status
- `POST /api/tools/lookup` - Tool usage

## Configuration

Update `config/settings.py` for:
- Model paths
- API keys
- Database settings
- Deployment settings
