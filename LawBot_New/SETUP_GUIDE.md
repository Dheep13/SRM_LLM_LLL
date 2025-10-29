# LawBot Setup Guide

## Quick Start (No Configuration Needed!)

This project requires **ZERO environment variables** by default. Just run the notebooks!

### Option 1: Google Colab (Recommended)

1. Upload the notebooks to Google Colab
2. Run notebooks in sequence (Phase 1 → 6)
3. Everything works out of the box!

### Option 2: Local Setup

```bash
# Clone/download the project
cd 80_LLL_LLM

# Install dependencies
pip install -r requirements.txt

# Run notebooks
jupyter notebook notebooks/
```

## What Works Without Any Setup?

✅ **Fine-tuning**: Uses public Hugging Face models  
✅ **RAG**: Uses local FAISS (no cloud services)  
✅ **Embeddings**: Uses public sentence-transformers  
✅ **Gradio**: Auto-creates public links  
✅ **All notebooks**: Fully self-contained  

## When Would You Need `.env` File?

Only if you want to extend with optional features:

### Scenario 1: Use Private Models
```bash
# Create .env file
cp env.example .env

# Add your token
echo "HF_TOKEN=hf_your_token_here" >> .env
```

### Scenario 2: Real Indian Kanoon API
```bash
# Add to .env
INDIAN_KANOON_API_KEY=your_key_here
INDIAN_KANOON_API_URL=https://api.indiankanoon.org
```

### Scenario 3: Use Pinecone (Cloud Vector Store)
```bash
# Add to .env
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=production
PINECONE_INDEX_NAME=lawbot-index
```

## For This Assignment

**You don't need any of the above!** Just:
1. Open Colab
2. Upload notebooks
3. Run Phase 1 → 6
4. Done! ✨

## Summary

| Item | Required? |
|------|-----------|
| API Keys | ❌ No |
| .env File | ❌ No |
| Configuration | ❌ No |
| GPU | ✅ Yes (Colab free tier OK) |
| Internet | ✅ Yes (download models) |

**Bottom line:** The project is ready to run as-is. No setup needed!

