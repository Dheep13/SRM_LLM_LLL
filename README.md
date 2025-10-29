# ⚖️ LawBot: Intelligent Legal Q&A Assistant for Indian Law - RA2412044015083 - Deepan Shanmugam

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/🤗-Model%20on%20HF-yellow.svg)](https://huggingface.co/)

An AI-powered legal question-answering system specializing in Indian law (IPC, CrPC, and Constitution). Built with fine-tuned LLMs, RAG, and legal tools.

---

## 🎯 Project Overview

LawBot combines:
- **Fine-Tuned LLM**: Qwen2.5-1.5B with LoRA adapters (hosted on HuggingFace)
- **RAG System**: FAISS vector database with 14,630 legal document chunks
- **Legal Tools**: Dictionary, date calculator, case lookup
- **Multiple Interfaces**: CLI, Gradio, Full-stack application

### Key Statistics
- 📊 **Training Data**: 14,522 legal Q&A pairs (11,617 train / 2,905 validation)
- 🤖 **Model**: Qwen2.5-1.5B-Instruct fine-tuned with 4-bit QLoRA
- 📚 **Vector Store**: 14,630 chunks, 21.43 MB FAISS index
- 🎓 **Domains**: Indian Penal Code (IPC), Criminal Procedure Code (CrPC), Constitution of India

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip install sentence-transformers faiss-cpu transformers torch peft gradio
```

### Installation
```bash
git clone https://github.com/Dheep13/SRM_LLM_LLL.git
cd SRM_LLM_LLL
```

### Quick Demo (RAG-Only, Fast)
```bash
cd LawBot_FullStack
python check_status.py          # Verify components
python simple_chat.py            # Interactive chat
```

**Startup:** ~10 seconds | **Memory:** ~500MB

### Full Model Demo (Best Quality)
```bash
python full_inference.py         # Loads fine-tuned model + RAG
```

**Startup:** 2-5 minutes (CPU) | **Memory:** 4-8GB

---

## 📂 Repository Structure

```
SRM_LLM_LLL/
│
├── LawBot_New/                          # Training & Notebooks
│   ├── notebooks/
│   │   ├── phase1_data_prep.ipynb      # Data preprocessing
│   │   ├── phase2_finetune_lawbot.ipynb # Model fine-tuning
│   │   ├── phase3_rag_lawbot.ipynb     # RAG implementation
│   │   ├── phase4_reward_model_lawbot.ipynb # RLHF framework
│   │   ├── phase5_lawbot_agent.ipynb   # Tool integration
│   │   └── phase6_gradio_app.ipynb     # Gradio interface
│   │
│   └── data/processed/                  # Training data
│       ├── train.jsonl                  # 11,617 samples
│       └── val.jsonl                    # 2,905 samples
│
├── LawBot_FullStack/                    # Inference & Deployment
│   ├── simple_chat.py                  # ⭐ Fast CLI interface
│   ├── full_inference.py               # Full model + RAG
│   ├── demo.py                         # Automated demo
│   ├── check_status.py                 # System verification
│   │
│   ├── data/
│   │   └── vectorstore/
│   │       └── faiss_index/            # 14,630 chunks, 21.43 MB
│   │
│   ├── backend/                        # FastAPI backend
│   ├── frontend/                       # React frontend
│   └── scripts/                        # Utility scripts
│
├── Indian_Legal_Dataset_Lawbot_Assignment/ # Original datasets
│
├── SUBMISSION_README.md                # Comprehensive guide
├── QUICK_START_GUIDE.txt              # Quick reference
├── PDF_REPORT_TEMPLATE.md             # Report template
└── FINAL_SUBMISSION_CHECKLIST.md      # Submission checklist
```

---

## 🎓 Training Pipeline (Google Colab)

### Phase 1: Data Preparation
- Merged IPC, CrPC, Constitution datasets
- Cleaned, deduplicated, formatted
- **Output**: 14,522 Q&A pairs

### Phase 2: Model Fine-Tuning
- **Base Model**: Qwen/Qwen2.5-1.5B-Instruct
- **Method**: 4-bit QLoRA via Unsloth
- **Hardware**: Google Colab T4 GPU
- **Duration**: ~2-3 hours
- **Output**: LoRA adapters (~10MB)

### Phase 3: RAG Implementation
- Document chunking
- Sentence-transformers embeddings (all-MiniLM-L6-v2)
- FAISS indexing
- **Output**: Vector store with 14,630 chunks

### Phase 4-6: Advanced Features
- RLHF reward model framework
- Legal tools (dictionary, calculator)
- Gradio chat interface

---

## 🤗 Fine-Tuned Model

The fine-tuned LoRA adapters are hosted on HuggingFace:

**Model URL**: `[Your HuggingFace model link]`

### Usage
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = PeftModel.from_pretrained(base_model, "YOUR_USERNAME/lawbot-qwen-2.5-1.5b-lora")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
```

The model automatically downloads when running `full_inference.py`.

---

## 🎥 Demo Video

**📹 Watch the complete demonstration:**

**[LawBot Demo Video - Watch Here](https://drive.google.com/drive/folders/1OVgxotidKSc6clLKpruU6h8-5135LjEU?usp=sharing)**

*Duration: ~5 minutes | File: FinalOutput_Recording.mp4 (168.7 MB)*

**Video demonstrates:**
- System status verification
- Interactive legal Q&A
- RAG context retrieval
- Response generation with citations
- Legal terminology detection
- Multiple query types (IPC, CrPC, Constitution)

**Note:** Video file (168 MB) is hosted on Google Drive due to GitHub size limits.  
See `VIDEO_DEMO_INSTRUCTIONS.md` for uploading instructions.

---

## 💡 Example Queries

Try these questions:

1. **"What is IPC Section 302?"** - Murder punishment
2. **"How to file an FIR?"** - Criminal complaint procedure
3. **"What are fundamental rights under the Constitution?"** - Constitutional law
4. **"What is the punishment for theft?"** - IPC penalties
5. **"Explain the procedure for bail"** - Criminal procedure

---

## 📊 System Architecture

```
User Query
    ↓
Query Processing
    ↓
┌─────────┴─────────┐
│                   │
RAG Retrieval    Legal Tools
(FAISS)          (Dictionary)
    │                │
    └────────┬───────┘
             ↓
    Fine-Tuned Model
    (Qwen2.5-1.5B + LoRA)
             ↓
    Generated Response
    + Citations
```

---

## 🔧 Inference Options

### Option 1: RAG-Only (`simple_chat.py`)
- ✅ Fast startup (~10 seconds)
- ✅ Low memory (~500MB)
- ✅ Good quality responses
- ❌ No LLM generation (rule-based)

### Option 2: Full Model (`full_inference.py`)
- ✅ High-quality LLM responses
- ✅ RAG + Fine-tuned model
- ⚠️ Slower startup (2-5 minutes)
- ⚠️ Higher memory (4-8GB)

**Recommendation**: Use `simple_chat.py` for quick demos, `full_inference.py` for best quality.

---

## 📸 Screenshots

### RAG Retrieval in Action
```
You: What is IPC Section 302?

📚 Retrieved Context:
[1] IPC Section 302 deals with punishment for murder...

📖 Legal Terms Detected:
  • IPC: Indian Penal Code - Criminal law of India

💡 Response:
Based on Indian legal documents:
IPC Section 302 deals with punishment for murder. The punishment can be:
• Death penalty, or
• Life imprisonment
```

*(See `LawBot_Project_Report.pdf` for detailed screenshots)*

---

## 🛠️ Technical Stack

### Training
- **Framework**: PyTorch, Transformers, Unsloth
- **Fine-tuning**: QLoRA (4-bit), PEFT
- **Platform**: Google Colab (T4 GPU)

### Inference
- **Embeddings**: sentence-transformers
- **Vector DB**: FAISS (CPU/GPU)
- **API**: FastAPI (optional)
- **UI**: Gradio, CLI

---

## 📦 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Dheep13/SRM_LLM_LLL.git
cd SRM_LLM_LLL
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or minimal:
```bash
pip install sentence-transformers faiss-cpu transformers torch peft gradio
```

### 3. Verify Setup
```bash
cd LawBot_FullStack
python check_status.py
```

Expected output:
```
✅ Fine-tuned Model (or HuggingFace link)
✅ Training Data
✅ RAG Vector Store
```

### 4. Run Inference
```bash
# Quick demo
python simple_chat.py

# Or full model
python full_inference.py
```

---

## 🎯 Use Cases

- 📚 **Legal Education**: Learn about Indian law
- 🔍 **Legal Research**: Quick access to legal provisions
- 💡 **Information Retrieval**: Find specific sections and procedures
- 🤖 **AI Research**: Study LLM fine-tuning and RAG systems

---

## ⚠️ Disclaimer

**Important**: LawBot is for **educational purposes only**.

- Not a substitute for professional legal advice
- Always consult qualified legal professionals for legal matters
- Responses should be verified with official legal sources
- Dataset may not reflect the most recent legal amendments

---

## 📄 Documentation

- **[SUBMISSION_README.md](SUBMISSION_README.md)** - Comprehensive project guide
- **[QUICK_START_GUIDE.txt](QUICK_START_GUIDE.txt)** - Quick reference
- **[INFERENCE_COMPARISON.md](LawBot_FullStack/INFERENCE_COMPARISON.md)** - Inference modes explained
- **[PDF_REPORT_TEMPLATE.md](PDF_REPORT_TEMPLATE.md)** - Report template with observations
- **[FINAL_SUBMISSION_CHECKLIST.md](FINAL_SUBMISSION_CHECKLIST.md)** - Submission preparation

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Contact

**Author**: Deepan Shanmugam  
**Class**: AI & DS Section B  
**Registration Number**: RA2412044015083  
**GitHub**: [@Dheep13](https://github.com/Dheep13)  
**Repository**: [SRM_LLM_LLL](https://github.com/Dheep13/SRM_LLM_LLL)

For questions or feedback, please open an issue.

---

## 🙏 Acknowledgments

- **Base Model**: Qwen Team (Alibaba Cloud) - [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
- **Fine-tuning**: Unsloth library for efficient QLoRA
- **Embeddings**: sentence-transformers
- **Vector DB**: FAISS (Meta AI)
- **Datasets**: Indian legal Q&A corpus (IPC, CrPC, Constitution)

---

## 📜 License

Apache 2.0 License - See [LICENSE](LICENSE) for details

---

## ⭐ Star History

If you find this project useful, please give it a star! ⭐

---

**Built with ❤️ for Indian Legal AI Research**

*Last Updated: October 2025*

