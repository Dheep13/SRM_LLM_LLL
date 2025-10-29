# LawBot Architecture

## System Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Gradio Chat Interface]
        Input[User Query]
        Output[Generated Response]
        Citations[Citation Display]
        Disclaimers[Legal Disclaimers]
    end
    
    subgraph "RAG Pipeline"
        Query[Query Processing]
        History[Conversation History]
        Reformulate[Query Reformulation]
        Retrieve[FAISS Vector Retrieval]
        Context[Context Chunks]
    end
    
    subgraph "Model Layer"
        FineTuned[Fine-tuned Qwen2.5-1.5B]
        LoRA[LoRA Adapters]
        RewardModel[Reward Model]
        GRPO[GRPO Optimizer]
    end
    
    subgraph "Tool Integration"
        CaseLookup[Case Lookup Tool]
        LegalDict[Legal Dictionary]
        DateCalc[Date Calculator]
        Tools[LangChain Agent]
    end
    
    subgraph "Data Layer"
        VectorStore[(FAISS Vector Store)]
        Docs[Legal Documents]
        AdapterWeights[LoRA Weights]
    end
    
    Input --> UI
    UI --> Query
    Query --> History
    History --> Reformulate
    Reformulate --> Retrieve
    Retrieve --> VectorStore
    VectorStore --> Context
    
    Context --> FineTuned
    FineTuned --> LoRA
    LoRA --> AdapterWeights
    FineTuned --> RewardModel
    RewardModel --> GRPO
    
    FineTuned --> Tools
    Tools --> CaseLookup
    Tools --> LegalDict
    Tools --> DateCalc
    Tools --> Output
    
    Output --> UI
    Output --> Citations
    Citations --> UI
    Disclaimers --> UI
    
    style UI fill:#e1f5ff
    style FineTuned fill:#fff4e6
    style VectorStore fill:#f3e5f5
    style Tools fill:#e8f5e9
```

## Data Flow

1. **User Input**: User submits a legal question through Gradio interface
2. **Query Processing**: System captures query and conversation history
3. **Query Reformulation**: Enhance query with context for better retrieval
4. **Vector Retrieval**: Search FAISS index for relevant legal document chunks
5. **Context Assembly**: Combine retrieved chunks into context
6. **Model Inference**: Pass context + query to fine-tuned Qwen2.5-1.5B model
7. **Tool Call Decision**: Agent decides if tool calling is needed
   - Case lookup for specific case details
   - Legal dictionary for term definitions
   - Date calculator for deadlines
8. **Response Generation**: Generate grounded response with citations
9. **RLHF Post-processing**: Apply reward model scoring and GRPO optimization
10. **Output Display**: Show response with citations and tool traces in Gradio UI

## Component Details

### Fine-Tuning Pipeline
- Base Model: Qwen2.5-1.5B-Instruct
- Quantization: 4-bit QLoRA via Unsloth
- Adapters: LoRA (rank=16, alpha=32)
- Training: 3 epochs with gradient accumulation
- Dataset: Indian legal Q&A (IPC, CrPC, Constitution)

### RAG Pipeline
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Chunking: 600-1000 tokens with 100-token overlap
- Retrieval: Top-k (k=5) with FAISS similarity search
- Sources: Bare Acts, case summaries, legal documents

### Tool Integration
- LangChain Agent with function calling
- Tools: Case lookup, legal dictionary, date calculator
- Trace visualization for transparency

### RLHF Pipeline
- Reward Model: Trained on 30+ preference pairs
- Criteria: Accuracy, clarity, citations, legal tone
- Optimization: GRPO via Unsloth Trainer

## Deployment Architecture

```mermaid
graph LR
    subgraph "Google Colab Environment"
        Notebook[Phase Notebooks]
        GPU[T4 GPU]
    end
    
    subgraph "Model Serving"
        Load[Load Fine-tuned Model]
        RAG[RAG Pipeline]
        Tools[Tool Integration]
    end
    
    subgraph "Gradio Cloud"
        GradioApp[Public Gradio Link]
        Chat[Chat Interface]
    end
    
    Notebook --> GPU
    GPU --> Load
    Load --> RAG
    RAG --> Tools
    Tools --> GradioApp
    GradioApp --> Chat
    
    style GPU fill:#ff6b6b
    style GradioApp fill:#4ecdc4
```

