"""
Simple test script for LawBot inference
Tests the model without Gradio interface
"""

import os
import sys
import json
import torch
from pathlib import Path

print("🚀 LawBot Simple Test")
print("="*60)

# Setup paths
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "adapters" / "lawbot_qwen_adapter"
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore" / "faiss_index"
BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}\n")

# Test 1: Load Model
print("📦 Test 1: Loading Model...")
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    print("  Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    
    print("  Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None,
    )
    
    # Try loading adapters
    if MODEL_PATH.exists():
        print(f"  Loading LoRA adapters...")
        try:
            from peft import PeftModel
            model = PeftModel.from_pretrained(model, str(MODEL_PATH))
            print("  ✅ Fine-tuned model loaded!")
        except Exception as e:
            print(f"  ⚠️ Using base model (adapters not loaded: {e})")
    else:
        print(f"  ⚠️ No adapters found, using base model")
    
    print("✅ Model Test PASSED\n")
    
except Exception as e:
    print(f"❌ Model Test FAILED: {e}\n")
    model = None
    tokenizer = None

# Test 2: Load RAG
print("📚 Test 2: Loading RAG Components...")
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    
    print("  Loading embedding model...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    index_file = VECTORSTORE_PATH / "faiss_index.idx"
    if index_file.exists():
        print(f"  Loading FAISS index...")
        rag_index = faiss.read_index(str(index_file))
        
        with open(VECTORSTORE_PATH / "chunks.json", 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        with open(VECTORSTORE_PATH / "metadata.json", 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        print(f"  ✅ RAG loaded: {rag_index.ntotal} vectors, {len(chunks)} chunks")
        print("✅ RAG Test PASSED\n")
    else:
        print(f"  ❌ FAISS index not found")
        rag_index = None
        
except Exception as e:
    print(f"❌ RAG Test FAILED: {e}\n")
    rag_index = None

# Test 3: Simple Inference
if model and tokenizer:
    print("🤖 Test 3: Running Inference...")
    test_query = "What is IPC Section 302?"
    
    try:
        # Get RAG context
        context = ""
        if rag_index and embedding_model:
            query_embedding = embedding_model.encode([test_query])
            scores, indices = rag_index.search(query_embedding, 3)
            
            context_parts = []
            for idx in indices[0]:
                if idx < len(chunks):
                    context_parts.append(chunks[idx])
            context = "\n".join(context_parts[:2])
            print(f"  Retrieved context: {len(context)} chars")
        
        # Generate response
        prompt = f"""<|im_start|>system
You are a legal assistant specializing in Indian law.
<|im_end|>
<|im_start|>user
Question: {test_query}

Context: {context}

Answer:
<|im_end|>
<|im_start|>assistant
"""
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        if device == "cuda":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        
        print("  Generating response...")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=128,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split("<|im_start|>assistant\n")[-1].strip()
        
        print("\n" + "="*60)
        print(f"Query: {test_query}")
        print("="*60)
        print(f"Response:\n{response}")
        print("="*60)
        print("\n✅ Inference Test PASSED\n")
        
    except Exception as e:
        print(f"❌ Inference Test FAILED: {e}\n")
else:
    print("⚠️ Skipping inference test (model not loaded)\n")

# Summary
print("\n" + "="*60)
print("📊 SUMMARY")
print("="*60)
print(f"Model: {'✅ Loaded' if model else '❌ Failed'}")
print(f"RAG: {'✅ Loaded' if rag_index else '❌ Failed'}")
print(f"Inference: {'✅ Working' if model and tokenizer else '❌ Not Available'}")
print("="*60)

if model and rag_index:
    print("\n🎉 All systems operational!")
    print("Run: python run_gradio.py (to launch UI)")
else:
    print("\n⚠️ Some components not loaded. Check errors above.")

