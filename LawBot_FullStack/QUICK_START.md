# LawBot Quick Start Guide

## 🚀 Fast Setup (Recommended)

### Option 1: Automated Setup
```bash
cd LawBot_FullStack
python start.py
```

### Option 2: Manual Setup
```bash
# Install minimal dependencies
pip install -r requirements-minimal.txt

# Start backend
python backend/main.py

# In another terminal - Start frontend
cd frontend
npm install
npm start
```

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** (for frontend)
- **Git** (for cloning)

## 🔧 Troubleshooting

### PyTorch Installation Issues
```bash
# Install PyTorch separately
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Or for CUDA (if you have GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Missing Dependencies
```bash
# Install core dependencies one by one
pip install fastapi uvicorn pydantic
pip install transformers sentence-transformers
pip install faiss-cpu peft accelerate
```

### Frontend Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📁 File Structure Setup

After installation, ensure you have:
```
LawBot_FullStack/
├── models/adapters/lawbot_qwen_adapter/  # Your trained model
├── data/vectorstore/                     # Your FAISS index
├── backend/                              # FastAPI backend
├── frontend/                             # React frontend
└── config/settings.py                    # Configuration
```

## 🔗 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 Quick Test

1. Start the application
2. Open http://localhost:3000
3. Ask: "What is IPC Section 302?"
4. Check if you get a response with citations

## 📞 Support

If you encounter issues:
1. Check the logs in the terminal
2. Verify all dependencies are installed
3. Ensure model files are in the correct location
4. Check that ports 3000 and 8000 are available
