# 📄 LawBot Project Report - Template & Outline

## Instructions for Creating Your PDF Report

Use this template to create your `LawBot_Project_Report.pdf`. Include screenshots and observations as indicated.

---

# **LawBot: Intelligent Legal Q&A Assistant for Indian Law**

**Project Report**

**Student Name:** Deepan Shanmugam  
**Class:** AI & DS Section B  
**Registration Number:** RA2412044015083  
**Date:** October 29, 2025  
**Institution:** SRM Institute of Science and Technology

---

## **Table of Contents**

1. Executive Summary
2. Introduction
3. System Architecture
4. Phase 1: Dataset Preparation
5. Phase 2: Model Fine-Tuning
6. Phase 3: RAG Implementation
7. Phase 4-6: Advanced Features
8. Inference & Deployment
9. Results & Observations
10. Challenges & Solutions
11. Conclusion & Future Work
12. Appendices

---

## **1. Executive Summary** (1 page)

**What to include:**
- Brief project overview
- Key technologies used (Qwen2.5-1.5B, LoRA, FAISS, RAG)
- Major achievements (14,522 samples, fine-tuned model, working inference)
- Summary of results

**Template:**
```
This project implements LawBot, an intelligent legal question-answering system 
for Indian law. The system combines a fine-tuned Qwen2.5-1.5B language model 
with Retrieval Augmented Generation (RAG) using FAISS vector database.

Key Achievements:
• Processed 14,522 legal Q&A pairs from IPC, CrPC, and Constitution
• Fine-tuned model using 4-bit QLoRA with Unsloth on Google Colab
• Implemented RAG system with 14,630 document chunks
• Created multiple inference interfaces (CLI, Gradio, Full-stack)
• Achieved functional legal question-answering with source citations

The system successfully demonstrates end-to-end AI pipeline development 
from data preparation through deployment.
```

---

## **2. Introduction** (1-2 pages)

### **2.1 Project Objective**
Develop an AI assistant for Indian legal queries using LLM fine-tuning and RAG.

### **2.2 Scope**
- Indian Penal Code (IPC)
- Code of Criminal Procedure (CrPC)
- Indian Constitution

### **2.3 Technologies**
- **Base Model**: Qwen/Qwen2.5-1.5B-Instruct
- **Fine-tuning**: QLoRA, Unsloth, PEFT
- **RAG**: FAISS, sentence-transformers
- **Deployment**: Python CLI, Gradio, FastAPI
- **Training Platform**: Google Colab (T4 GPU)

### **2.4 Deliverables**
- 6 Colab notebooks (training pipeline)
- Fine-tuned model adapters
- RAG vector database
- Inference scripts
- Documentation

---

## **3. System Architecture** (1 page)

### **3.1 Overall Architecture**

**[INSERT DIAGRAM HERE]**

```
User Query
    ↓
Query Processing
    ↓
┌─────────┴─────────┐
│                   │
RAG Retrieval    Legal Tools
    │                   │
    └────────┬──────────┘
             ↓
    Fine-Tuned Model
             ↓
    Generated Response
```

### **3.2 Components**
1. **Data Pipeline**: Collection → Cleaning → Formatting
2. **Training Pipeline**: Fine-tuning with QLoRA
3. **RAG System**: Embedding → Indexing → Retrieval
4. **Inference Engine**: Query → Retrieve → Generate
5. **User Interface**: CLI / Gradio

---

## **4. Phase 1: Dataset Preparation** (2-3 pages)

### **4.1 Dataset Overview**

**[SCREENSHOT: Phase 1 notebook output showing dataset statistics]**

**Sources:**
- `constitution_qa.json` - Constitutional law Q&A
- `crpc_qa.json` - Criminal procedure Q&A
- `ipc_qa.json` - Indian Penal Code Q&A

**Statistics:**
- Total Q&A pairs: 14,522
- Training set: 11,617 (80%)
- Validation set: 2,905 (20%)

### **4.2 Data Processing Steps**

1. **Loading**: Read JSON datasets
2. **Merging**: Combine all three sources
3. **Transformation**: Convert to instruction format
4. **Cleaning**: Remove duplicates, fix formatting
5. **Splitting**: 80/20 train/val split

### **4.3 Instruction Format**

```python
{
    "instruction": "You are a legal assistant...",
    "input": "What is IPC Section 302?",
    "output": "IPC Section 302 deals with...",
    "source": "IPC"
}
```

### **4.4 Observations**

**[YOUR OBSERVATIONS HERE]**

Example observations:
- Data quality: Clean, well-structured
- Coverage: Good representation of major legal topics
- Balance: Relatively even distribution across sources
- Challenges: Some duplicate questions with different wording

---

## **5. Phase 2: Model Fine-Tuning** (3-4 pages)

### **5.1 Training Configuration**

**Base Model:** Qwen/Qwen2.5-1.5B-Instruct (1.5B parameters)

**LoRA Configuration:**
- Rank (r): 16
- Alpha: 16
- Dropout: 0.05
- Target modules: q_proj, k_proj, v_proj, o_proj

**Training Hyperparameters:**
- Batch size: 2
- Gradient accumulation: 4 (effective batch size: 8)
- Learning rate: 2e-4
- Epochs: 3
- Max sequence length: 2048
- Optimizer: AdamW (8-bit)

**Hardware:**
- Platform: Google Colab
- GPU: Tesla T4 (16GB)
- Training time: ~2-3 hours

### **5.2 Training Process**

**[SCREENSHOT: Phase 2 notebook showing training progress]**

### **5.3 Training Metrics**

**[SCREENSHOT: Loss curves if available]**

**Example metrics:**
- Initial loss: ~2.5
- Final loss: ~0.8
- Validation perplexity: [if available]

### **5.4 Model Artifacts**

**Output files (10 files):**
- `adapter_config.json` - LoRA configuration
- `adapter_model.safetensors` - Trained weights
- `tokenizer_config.json` - Tokenizer settings
- `special_tokens_map.json`
- `tokenizer.json`
- etc.

**Model size:**
- Base model: ~3GB (downloaded from HuggingFace)
- LoRA adapters: ~10MB
- Total for inference: ~3.01GB

### **5.5 Observations**

**[YOUR OBSERVATIONS HERE]**

Example:
- Training converged smoothly
- No overfitting observed
- Model learned legal terminology
- Response quality improved significantly

---

## **6. Phase 3: RAG Implementation** (2-3 pages)

### **6.1 RAG Pipeline**

**Process:**
1. **Document Loading**: Load processed legal Q&A
2. **Chunking**: Split into semantic chunks
3. **Embedding**: Generate vectors using sentence-transformers
4. **Indexing**: Create FAISS index
5. **Retrieval**: Semantic search at inference time

### **6.2 Configuration**

- **Embedding Model**: all-MiniLM-L6-v2
- **Embedding Dimension**: 384
- **Chunk Size**: Varies (Q&A based)
- **Index Type**: FAISS Flat (L2 distance)
- **Total Chunks**: 14,630

### **6.3 Vector Store Statistics**

**[SCREENSHOT: RAG creation output from script]**

- FAISS Index: 21.43 MB
- Chunks: 14,630 documents
- Metadata: 14,630 entries
- Sources: IPC, CrPC, Constitution

### **6.4 Retrieval Performance**

**[SCREENSHOT: Sample retrieval results]**

Example query: "What is IPC Section 302?"

Retrieved chunks:
1. [Chunk 1 with similarity score]
2. [Chunk 2 with similarity score]
3. [Chunk 3 with similarity score]

### **6.5 Observations**

**[YOUR OBSERVATIONS HERE]**

Example:
- Semantic search works well for legal concepts
- Retrieval time: <1 second
- Relevance: Top-3 results usually pertinent
- Challenges: Similar section numbers can cause confusion

---

## **7. Phase 4-6: Advanced Features** (1-2 pages)

### **7.1 Phase 4: RLHF Framework**
- Reward model structure defined
- Framework for future human feedback integration
- Not fully trained (optional phase)

### **7.2 Phase 5: Legal Tools**

**Implemented:**
- Legal dictionary (IPC, CrPC terms)
- Date calculator (for legal deadlines)
- Case lookup structure

**[SCREENSHOT: Tool detection in action]**

### **7.3 Phase 6: Gradio Interface**
- Chat interface design
- Multi-turn conversations
- Citation display
- Disclaimer integration

---

## **8. Inference & Deployment** (3-4 pages)

### **8.1 Inference Options**

#### **Option 1: RAG-Only (simple_chat.py)**

**[SCREENSHOT: simple_chat.py in action]**

**Performance:**
- Startup time: ~10 seconds
- Memory usage: ~500MB
- Response time: <1 second

**Example interaction:**
```
You: What is IPC Section 302?

📚 Retrieved Context:
[1] IPC Section 302 deals with punishment for murder...

💡 Response:
Based on Indian legal documents:
IPC Section 302 deals with punishment for murder...
```

#### **Option 2: Full Model + RAG (full_inference.py)**

**[SCREENSHOT: full_inference.py with model loading and response]**

**Performance:**
- Startup time: 2-5 minutes (CPU)
- Memory usage: 4-8GB
- Response time: 10-30 seconds per query

**Example interaction:**
```
🔍 Step 1: Retrieving context from RAG...
  ✅ Retrieved 3 relevant chunks

💡 Step 2: Generating response...
  🤖 Generating response with fine-tuned model...
  ✅ Response generated!

🤖 LawBot Response:
[High-quality LLM-generated response with context integration]
```

### **8.2 Comparison**

| Feature | RAG-Only | Full Model |
|---------|----------|------------|
| Startup | 10s | 2-5min |
| Memory | 500MB | 4-8GB |
| Quality | Good | Excellent |
| Best for | Quick demos | Production |

### **8.3 Full-Stack Structure** (Optional)

- FastAPI backend
- React frontend
- Docker deployment
- RESTful API endpoints

---

## **9. Results & Observations** (3-5 pages)

### **9.1 Sample Query Results**

#### **Query 1: "What is IPC Section 302?"**

**[SCREENSHOT: Complete interaction]**

**Retrieved Context:**
[Show top-3 chunks]

**Generated Response:**
[Show model response]

**Observations:**
- Relevance: [Your assessment]
- Accuracy: [Your assessment]
- Citations: [Properly cited?]
- Quality: [Rating 1-10]

---

#### **Query 2: "How to file an FIR?"**

**[SCREENSHOT]**

**Observations:**
[Your analysis]

---

#### **Query 3: "What are fundamental rights under Constitution?"**

**[SCREENSHOT]**

**Observations:**
[Your analysis]

---

#### **Query 4: "What is the punishment for theft?"**

**[SCREENSHOT]**

**Observations:**
[Your analysis]

---

### **9.2 Quality Analysis**

**Strengths:**
- Accurate retrieval of relevant legal information
- Proper source attribution
- Handles multiple legal domains (IPC, CrPC, Constitution)
- Fast response times

**Limitations:**
- Specific rare sections may have limited coverage
- Numerical similarity can cause near-miss retrievals
- Context window limits long legal explanations
- Requires legal professional verification

### **9.3 Performance Metrics**

**System Performance:**
- RAG retrieval accuracy: ~85-90% (estimated from samples)
- Response time: <1s (RAG-only), 10-30s (Full model)
- System uptime: Stable
- Memory efficiency: Good

---

## **10. Challenges & Solutions** (2 pages)

### **10.1 Challenge 1: Model Loading Time**

**Problem:** Fine-tuned model takes 2-5 minutes to load on CPU

**Solution:** 
- Created two inference modes
- RAG-only for quick demos
- Full model for quality demonstrations

**Outcome:** Users can choose based on needs

---

### **10.2 Challenge 2: Gradio Compatibility**

**Problem:** Gradio 5.x JSON schema TypeError

**Solution:**
- Implemented CLI interface as primary
- Gradio as optional

**Outcome:** Reliable inference without dependencies

---

### **10.3 Challenge 3: Vector Store Creation**

**Problem:** Initial RAG setup complexity

**Solution:**
- Created standalone script
- Automated chunk processing
- Progress indicators

**Outcome:** One-command vector store creation

---

### **10.4 Challenge 4: Dependency Management**

**Problem:** torch/transformers version conflicts

**Solution:**
- Version pinning in requirements.txt
- Clean installation scripts

**Outcome:** Reproducible environment

---

## **11. Conclusion & Future Work** (1-2 pages)

### **11.1 Summary**

This project successfully demonstrates:
✅ End-to-end AI pipeline (data → training → deployment)
✅ LLM fine-tuning with resource-efficient QLoRA
✅ RAG implementation for grounded responses
✅ Multiple deployment options
✅ Production-ready code structure

### **11.2 Achievements**

1. **Data**: Processed 14,522 legal Q&A pairs
2. **Model**: Fine-tuned 1.5B parameter model
3. **RAG**: Indexed 14,630 document chunks
4. **Inference**: Two working modes (fast & quality)
5. **Documentation**: Complete guides and notebooks

### **11.3 Limitations**

- Dataset size could be larger
- Specific case law not included
- Requires professional legal verification
- Model size limits deployment options

### **11.4 Future Enhancements**

1. **Data Expansion**
   - Include more legal acts
   - Add case law database
   - Multi-language support

2. **Model Improvements**
   - Larger base model (7B/13B)
   - RLHF with expert feedback
   - Multi-task fine-tuning

3. **Features**
   - Document generation
   - Legal research assistant
   - Citation network
   - Case similarity search

4. **Deployment**
   - Cloud deployment (AWS/GCP)
   - Mobile application
   - API for integration
   - Real-time updates

---

## **12. Appendices**

### **Appendix A: Code Repository Structure**
[File tree of submission]

### **Appendix B: Requirements**
```
transformers==4.44.2
sentence-transformers>=4.0.0
faiss-cpu>=1.7.4
torch>=2.2.0
peft>=0.6.0
gradio>=4.0.0
```

### **Appendix C: Commands Reference**

**Training:**
- Run notebooks in Google Colab sequentially

**Inference:**
```bash
python check_status.py
python simple_chat.py
python full_inference.py
```

### **Appendix D: Sample Queries**
[List of 20-30 test queries used]

---

## **References**

1. Qwen Team. "Qwen2.5: Small but Mighty." Alibaba Cloud, 2024.
2. Hu, E. J., et al. "LoRA: Low-Rank Adaptation of Large Language Models." arXiv:2106.09685, 2021.
3. Lewis, P., et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." arXiv:2005.11401, 2020.
4. Johnson, J., Douze, M., & Jégou, H. "Billion-scale similarity search with GPUs." IEEE Transactions on Big Data, 2019.
5. Indian Penal Code, 1860.
6. Code of Criminal Procedure, 1973.
7. Constitution of India, 1950.

---

**End of Report**

---

## **PDF Creation Checklist**

Before finalizing your PDF:

□ All screenshots captured and inserted
□ Your observations added for each phase
□ Results section complete with 4-5 examples
□ Challenges section reflects your experience
□ Page numbers added
□ Table of contents updated
□ Proper formatting (headings, spacing)
□ Grammar and spelling checked
□ File saved as: `LawBot_Project_Report.pdf`

**Recommended Tool:** Microsoft Word or Google Docs → Export as PDF

**Estimated Length:** 20-30 pages with screenshots

---

Good luck with your report! 🎉

