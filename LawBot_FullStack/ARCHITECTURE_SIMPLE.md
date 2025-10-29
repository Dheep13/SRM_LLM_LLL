# LawBot Simple Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (Web Browser)                        │
│                  http://localhost:7860                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Gradio Interface (run_gradio.py)               │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Chat UI  │  Examples  │  Status  │  Disclaimers  │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LawBotInference Class                           │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Model     │  │    RAG      │  │   Tools     │        │
│  │  Qwen2.5    │  │   FAISS     │  │ Dictionary  │        │
│  │ + LoRA      │  │   Index     │  │ Calculator  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Response Pipeline                          │
│                                                               │
│  Query → RAG Retrieval → Tool Detection → Model Inference  │
│           ↓                ↓                  ↓              │
│        Context         Tool Info          Response           │
│                                              ↓                │
│                     Format with Citations                    │
│                                              ↓                │
│                     Add Disclaimers                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                   Final Response
```

## Data Flow

```
1. User enters query: "What is IPC Section 302?"
   │
   ▼
2. RAG retrieves relevant chunks from FAISS
   ├─ Query embedding generated
   ├─ FAISS similarity search
   └─ Top-5 chunks retrieved with metadata
   │
   ▼
3. Tools detect legal terms
   ├─ "IPC" found in query
   ├─ "Section 302" found
   └─ Dictionary definitions fetched
   │
   ▼
4. Model generates response
   ├─ Prompt formatted with context
   ├─ Fine-tuned model inference
   └─ Response decoded
   │
   ▼
5. Response formatted
   ├─ Add RAG citations: "Sources: IPC"
   ├─ Add tool info: "Tools: Legal Dictionary"
   └─ Add disclaimer
   │
   ▼
6. Display in Gradio chat
```

## Component Details

### 1. Fine-Tuned Model
```
Location: models/adapters/lawbot_qwen_adapter/
Type: Qwen2.5-1.5B-Instruct + LoRA adapters
Purpose: Generate accurate legal responses
Input: Query + RAG context
Output: Legal answer
```

### 2. RAG Pipeline
```
Location: data/vectorstore/faiss_index/
Components:
  - FAISS index (faiss_index.idx)
  - Document chunks (chunks.json)
  - Metadata (metadata.json)
  - Config (config.json)
Purpose: Retrieve relevant legal context
Input: User query
Output: Top-K relevant chunks + citations
```

### 3. Legal Tools
```
Built-in Tools:
  - Legal Dictionary (LEGAL_DICTIONARY)
  - Date Calculator (calculate_deadline)
  - Case Lookup (mock implementation)
Purpose: Enhance responses with specific information
Input: Detected keywords
Output: Tool-specific information
```

### 4. Gradio Interface
```
File: run_gradio.py
Features:
  - Chat history
  - Example questions
  - System status
  - Citations display
  - Tool usage display
  - Legal disclaimers
Port: 7860
```

## File Structure

```
LawBot_FullStack/
├── run_inference.py          # One-command startup
├── run_gradio.py             # Gradio interface
├── requirements-minimal.txt   # Dependencies
│
├── scripts/
│   └── create_vectorstore_simple.py  # Create FAISS index
│
├── models/
│   └── adapters/
│       └── lawbot_qwen_adapter/      # Fine-tuned model
│
├── data/
│   ├── datasets/             # Original datasets
│   ├── processed/            # Processed data
│   └── vectorstore/
│       └── faiss_index/      # RAG vectorstore
│
└── config/
    └── settings.py           # Configuration
```

## Startup Sequence

```
1. run_inference.py starts
   ↓
2. Check dependencies
   ├─ Install if missing
   ↓
3. Check model
   ├─ Verify adapters exist
   ↓
4. Check vectorstore
   ├─ Create if missing (calls create_vectorstore_simple.py)
   ↓
5. Launch run_gradio.py
   ↓
6. Load model
   ├─ Load tokenizer
   ├─ Load base model
   └─ Load LoRA adapters
   ↓
7. Load RAG
   ├─ Load embedding model
   ├─ Load FAISS index
   ├─ Load chunks
   └─ Load metadata
   ↓
8. Initialize tools
   ├─ Legal dictionary
   ├─ Date calculator
   └─ Case lookup
   ↓
9. Create Gradio interface
   ├─ Chat UI
   ├─ Examples
   └─ Status display
   ↓
10. Launch at localhost:7860
```

## Integration Points

### Model + RAG Integration
```python
# In run_gradio.py LawBotInference.chat()

1. User query received
2. RAG retrieval:
   - Generate query embedding
   - Search FAISS index
   - Return context + citations
3. Model inference:
   - Format prompt with RAG context
   - Generate response
4. Combine outputs:
   - Response + Citations + Tools
```

### RAG + Tools Integration
```python
# In run_gradio.py

1. Query: "What is bail?"
2. RAG finds: Relevant legal documents about bail
3. Tools detect: "bail" in legal dictionary
4. Response includes:
   - Model answer (based on RAG context)
   - RAG citations (sources)
   - Tool definition (from dictionary)
```

## Key Features

1. **Modular Design**: Each component can work independently
2. **Graceful Degradation**: System works even if components fail
3. **Error Handling**: Comprehensive try-catch blocks
4. **Lazy Loading**: Imports only when needed
5. **Status Tracking**: System reports what's loaded
6. **User Feedback**: Clear progress indicators

## Performance Characteristics

```
Component          | Load Time | Query Time
-------------------|-----------|------------
Model Loading      | ~20-30s   | -
RAG Loading        | ~5-10s    | ~100-200ms
Tool Detection     | -         | ~1-2ms
Model Inference    | -         | ~1-3s (GPU) / 5-10s (CPU)
Total per Query    | -         | ~1-5s
```

This architecture provides a complete, working LawBot system for local testing and demonstration!

