# ⚖️ LawBot: Intelligent Legal Q&A Assistant for Indian Law

**Student Project Submission**  
**Date:** October 2025

---

## 📋 Project Overview

LawBot is an AI-powered legal question-answering system specializing in Indian law (IPC, CrPC, and Constitution). The system combines:
- **Fine-tuned LLM**: Qwen2.5-1.5B with LoRA adapters
- **RAG (Retrieval Augmented Generation)**: FAISS vector database with 14,630 legal document chunks
- **Legal Tools**: Dictionary, date calculator, case lookup

---

## 📦 Submission Contents

### **1. Training & Development** (`LawBot_New/`)
- **6 Colab Notebooks**: Complete training pipeline
  - Phase 1: Data Preparation
  - Phase 2: Model Fine-Tuning (QLoRA/Unsloth)
  - Phase 3: RAG Implementation (FAISS)
  - Phase 4: RLHF Framework
  - Phase 5: Tool Integration
  - Phase 6: Gradio Interface

- **Training Data**: 
  - 11,617 training samples
  - 2,905 validation samples
  - Merged from IPC, CrPC, Constitution datasets

- **Fine-Tuned Model**:
  - LoRA adapters (10 files)
  - Based on Qwen2.5-1.5B-Instruct
  - 4-bit quantization training

### **2. Deployment & Inference** (`LawBot_FullStack/`)
- **Inference Scripts**:
  - `simple_chat.py` - Fast RAG-only CLI (10s startup)
  - `full_inference.py` - Complete model + RAG (2-5min startup)
  - `demo.py` - Automated demonstration
  - `check_status.py` - System verification

- **Vector Store**:
  - FAISS index: 21.43 MB
  - 14,630 document chunks
  - Sentence-transformers embeddings (all-MiniLM-L6-v2)

- **Full-Stack Structure**:
  - FastAPI backend
  - React frontend (optional)
  - Docker configuration

### **3. Documentation**
- `README_COMPLETE.md` - Comprehensive guide
- `QUICK_START_GUIDE.txt` - Quick reference
- `INFERENCE_COMPARISON.md` - Inference modes explained
- `SUBMISSION_PACKAGE.md` - What to submit
- `LawBot_Project_Report.pdf` - Detailed report with observations

---

## 🚀 Quick Start Guide

### **Prerequisites**
```bash
Python 3.8+
pip install sentence-transformers faiss-cpu transformers torch peft numpy
```

### **Option 1: Fast Demo (Recommended for First Try)**
```powershell
cd LawBot_FullStack
python check_status.py        # Verify components
python simple_chat.py          # Start interactive chat
```

**Startup:** ~10 seconds  
**Memory:** ~500MB  
**Best for:** Quick demos, multiple queries

### **Option 2: Full Model Demo (Best Quality)**
```powershell
cd LawBot_FullStack
python full_inference.py       # Loads fine-tuned model + RAG
```

**Startup:** 2-5 minutes (CPU), 30s (GPU)  
**Memory:** 4-8GB  
**Best for:** High-quality responses, final demonstration

### **Example Queries**
Try these in either mode:
1. What is IPC Section 302?
2. How to file an FIR?
3. What are fundamental rights under the Constitution?
4. What is the punishment for theft?
5. Explain the procedure for bail

---

## 🎓 Training Pipeline (Google Colab)

### **Phase 1: Data Preparation**
- **Notebook**: `LawBot_New/notebooks/phase1_data_prep.ipynb`
- **Input**: 3 JSON datasets (IPC, CrPC, Constitution)
- **Output**: 14,522 processed Q&A pairs
- **Operations**: Merge, transform, clean, deduplicate, split

### **Phase 2: Fine-Tuning**
- **Notebook**: `LawBot_New/notebooks/phase2_finetune_lawbot.ipynb`
- **Model**: Qwen2.5-1.5B-Instruct
- **Method**: 4-bit QLoRA via Unsloth
- **Training**: ~3 epochs, batch size 2, gradient accumulation 4
- **Hardware**: Google Colab T4 GPU
- **Duration**: ~2-3 hours

### **Phase 3: RAG Setup**
- **Notebook**: `LawBot_New/notebooks/phase3_rag_lawbot.ipynb`
- **Process**: Document chunking → Embedding generation → FAISS indexing
- **Output**: Vector database with 14,630 chunks
- **Embedding Model**: all-MiniLM-L6-v2

### **Phase 4-6: Advanced Features**
- **Phase 4**: RLHF reward model framework
- **Phase 5**: Legal tool integration (dictionary, calculator)
- **Phase 6**: Gradio chat interface

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Query                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │   Query Processing Layer    │
         └──────────┬──────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐      ┌────────────────┐
│  RAG System   │      │  Legal Tools   │
│               │      │                │
│ • FAISS Index │      │ • Dictionary   │
│ • 14,630      │      │ • Calculator   │
│   chunks      │      │ • Case Lookup  │
└───────┬───────┘      └────────┬───────┘
        │                       │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Fine-Tuned Model     │
        │  Qwen2.5-1.5B + LoRA  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Generated Response  │
        │   + Citations         │
        └───────────────────────┘
```

---

## 📈 Project Statistics

### **Data**
- Training samples: 11,617
- Validation samples: 2,905
- Total Q&A pairs: 14,522
- Vector store chunks: 14,630
- Sources: IPC, CrPC, Constitution

### **Model**
- Base model: Qwen2.5-1.5B-Instruct (1.5B parameters)
- Fine-tuning: LoRA adapters (~10MB)
- Training time: ~2-3 hours (T4 GPU)
- Inference: 10-30 seconds/query (CPU)

### **RAG**
- FAISS index size: 21.43 MB
- Embedding dimension: 384
- Retrieval time: <1 second
- Top-k results: 3-5 per query

---

## 🎯 Key Features

### ✅ Implemented
1. **Dataset Preparation** - Cleaned, merged, formatted 14,522 samples
2. **Model Fine-Tuning** - QLoRA on Qwen2.5-1.5B
3. **RAG System** - FAISS with semantic search
4. **Legal Tools** - Dictionary, calculators
5. **Multiple Interfaces** - CLI (simple & full), Gradio
6. **Complete Documentation** - Notebooks, README, guides

### 🔄 Optional Enhancements (Implemented)
- RLHF framework structure
- Tool calling integration
- Full-stack application architecture
- Docker deployment setup

---

## 📸 Screenshots & Demonstrations

**See `LawBot_Project_Report.pdf` for:**
- Training notebook outputs
- RAG retrieval examples
- Inference demonstrations
- Response quality analysis
- System architecture diagrams

---

## 🔧 Technical Stack

### **Training**
- Python 3.10+
- PyTorch 2.x
- Transformers 4.44+
- Unsloth (QLoRA optimization)
- Google Colab (T4 GPU)

### **Inference**
- sentence-transformers
- FAISS (CPU/GPU)
- Gradio (optional)
- FastAPI (optional)

### **Tools**
- Git for version control
- Jupyter/Colab for notebooks
- PowerShell for automation

---

## 📚 Documentation Structure

```
Documentation/
├── README_COMPLETE.md          # Comprehensive guide
├── QUICK_START_GUIDE.txt       # Quick reference
├── INFERENCE_COMPARISON.md     # Inference modes
├── SUBMISSION_README.md        # This file
└── LawBot_Project_Report.pdf   # Detailed report
```

---

## 🐛 Known Issues & Solutions

### **Issue 1: Gradio JSON Schema Error**
- **Problem**: TypeError in Gradio 5.x
- **Solution**: Use `simple_chat.py` (CLI) instead
- **Status**: Workaround implemented

### **Issue 2: Model Loading Time**
- **Problem**: 2-5 minutes on CPU
- **Solution**: Use `simple_chat.py` for quick demos, `full_inference.py` for quality
- **Status**: Expected behavior, documented

### **Issue 3: Dependency Conflicts**
- **Problem**: torch/transformers version mismatches
- **Solution**: Use provided requirements.txt
- **Status**: Resolved with version pinning

---

## ✅ Verification

To verify the submission works:

```powershell
# 1. Check all components
cd LawBot_FullStack
python check_status.py

# Expected output:
# ✅ Fine-tuned Model
# ✅ Training Data
# ✅ RAG Vector Store

# 2. Test RAG-only inference
python simple_chat.py
# Ask: "What is IPC Section 302?"

# 3. (Optional) Test full model
python full_inference.py
# Wait 2-5 minutes, then ask a question
```

---

## 📧 Support

For questions or issues:
1. Check `README_COMPLETE.md` for detailed documentation
2. Review `QUICK_START_GUIDE.txt` for common solutions
3. Verify setup with `check_status.py`

---

## 🎉 Conclusion

This submission demonstrates a complete AI legal assistant pipeline:
- ✅ Data preparation and cleaning
- ✅ Model fine-tuning with QLoRA
- ✅ RAG implementation with FAISS
- ✅ Multiple inference options
- ✅ Production-ready code structure
- ✅ Comprehensive documentation

**All components are functional and ready for evaluation.**

---

**Thank you for reviewing this submission!** ⚖️

