# LawBot Inference Guide

## Quick Start - Single Command

```bash
cd LawBot_FullStack
python run_inference.py
```

This will:
1. Check and install dependencies
2. Verify the fine-tuned model exists
3. Create vectorstore if needed (takes 5-10 minutes)
4. Launch Gradio interface at http://localhost:7860

## Manual Steps (Alternative)

### Step 1: Install Dependencies
```bash
pip install -r requirements-minimal.txt
```

### Step 2: Create Vectorstore (if not exists)
```bash
python scripts/create_vectorstore_simple.py
```

This will:
- Load legal documents from `data/datasets/` or `data/processed/`
- Chunk documents (800 chars with 100 overlap)
- Generate embeddings using sentence-transformers
- Create FAISS index
- Save to `data/vectorstore/faiss_index/`

### Step 3: Launch Gradio Interface
```bash
python run_gradio.py
```

Access at: http://localhost:7860

## What's Included

### Components
- **Fine-tuned Model**: Qwen2.5-1.5B with LoRA adapters
- **RAG Pipeline**: FAISS vectorstore with legal documents
- **Legal Tools**: Dictionary, date calculator, case lookup
- **Gradio UI**: Simple chat interface with citations

### Features
- Ask questions about Indian law (IPC, CrPC, Constitution)
- Get responses with RAG-retrieved context
- See citations from legal sources
- Tool usage for legal terms
- Conversation history
- Example questions

## Testing the System

### Example Queries
1. "What is IPC Section 302?"
2. "How do I file a criminal complaint?"
3. "What is the procedure for bail?"
4. "Explain the concept of arrest under CrPC"
5. "What are the fundamental rights under the Constitution?"

### Expected Behavior
- **With RAG**: Responses include citations like "Sources: IPC, CRPC"
- **With Tools**: Legal terms trigger dictionary definitions
- **Fine-tuned Model**: More accurate legal responses than base model

## Troubleshooting

### Dependency Issues
If you get import errors:
```bash
pip uninstall torchvision -y
pip install torch>=2.2.0,<2.5.0
pip install transformers>=4.35.0,<4.45.0
pip install sentence-transformers faiss-cpu gradio peft
```

### Model Not Found
The system will work with the base model if adapters aren't found.
Ensure: `models/adapters/lawbot_qwen_adapter/` exists

### Vectorstore Issues
If vectorstore creation fails:
- Check that datasets exist in `data/datasets/` or `data/processed/`
- Run manually: `python scripts/create_vectorstore_simple.py`
- Check output in `data/vectorstore/faiss_index/`

### GPU Issues
If CUDA errors occur:
- System will automatically fall back to CPU
- Inference will be slower but functional

## System Status

When running, check the "System Status" accordion in Gradio to see:
- ✅ Model Status (loaded/not available)
- ✅ RAG Status (active/not available)
- Device (cuda/cpu)
- Vector count

## Files Created

After running setup:
```
data/vectorstore/faiss_index/
├── faiss_index.idx      # FAISS vector index
├── chunks.json          # Document chunks
├── metadata.json        # Chunk metadata
└── config.json          # Vectorstore config
```

## Performance Notes

- **First Run**: 5-10 minutes (vectorstore creation)
- **Subsequent Runs**: <30 seconds (loads existing vectorstore)
- **Query Response**: 1-5 seconds depending on GPU/CPU
- **Memory Usage**: ~4-6 GB RAM, ~2GB VRAM (with GPU)

## Assignment Submission

This setup provides:
1. ✅ Fine-tuned model inference
2. ✅ RAG with document retrieval
3. ✅ Tool integration (legal dictionary)
4. ✅ Frontend UI (Gradio)
5. ✅ Citations and disclaimers
6. ✅ Local testing environment

Perfect for testing and demonstrating your LawBot implementation!

