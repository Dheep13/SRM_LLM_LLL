"""
Quick Status Check - No heavy model loading
"""

import os
import json
from pathlib import Path

print("="*70)
print("⚖️  LawBot Status Check")
print("="*70)

BASE_DIR = Path(__file__).parent

# Check components
print("\n📦 Checking Components:\n")

# 1. Model Adapters
model_path = BASE_DIR / "models" / "adapters" / "lawbot_qwen_adapter"
if model_path.exists():
    files = list(model_path.glob("*"))
    print(f"✅ Model Adapters: {len(files)} files found")
    print(f"   Location: {model_path}")
else:
    print(f"❌ Model Adapters: Not found")
    print(f"   Expected at: {model_path}")

# 2. Processed Data
data_path = BASE_DIR / "data" / "processed"
if data_path.exists():
    train = data_path / "train.jsonl"
    val = data_path / "val.jsonl"
    print(f"\n✅ Processed Data:")
    if train.exists():
        with open(train, 'r', encoding='utf-8') as f:
            train_count = sum(1 for _ in f)
        print(f"   Training samples: {train_count}")
    if val.exists():
        with open(val, 'r', encoding='utf-8') as f:
            val_count = sum(1 for _ in f)
        print(f"   Validation samples: {val_count}")
else:
    print(f"\n❌ Processed Data: Not found")

# 3. Vector Store
vectorstore_path = BASE_DIR / "data" / "vectorstore" / "faiss_index"
if vectorstore_path.exists():
    index_file = vectorstore_path / "faiss_index.idx"
    chunks_file = vectorstore_path / "chunks.json"
    metadata_file = vectorstore_path / "metadata.json"
    config_file = vectorstore_path / "config.json"
    
    print(f"\n✅ Vector Store:")
    print(f"   Location: {vectorstore_path}")
    
    if index_file.exists():
        size_mb = index_file.stat().st_size / (1024*1024)
        print(f"   ✅ FAISS Index: {size_mb:.2f} MB")
    else:
        print(f"   ❌ FAISS Index: Missing")
    
    if chunks_file.exists():
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        print(f"   ✅ Chunks: {len(chunks)} documents")
    else:
        print(f"   ❌ Chunks: Missing")
    
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"   ✅ Metadata: {len(metadata)} entries")
    else:
        print(f"   ❌ Metadata: Missing")
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"   ✅ Config: {config.get('embedding_model', 'N/A')}")
    else:
        print(f"   ⚠️  Config: Missing")
        
else:
    print(f"\n❌ Vector Store: Not found")
    print(f"   Run: python scripts/create_vectorstore_simple.py")

# 4. Notebooks
notebooks_path = Path("../LawBot_New/notebooks")
if notebooks_path.exists():
    notebooks = list(notebooks_path.glob("*.ipynb"))
    print(f"\n✅ Colab Notebooks: {len(notebooks)} notebooks")
    for nb in sorted(notebooks):
        print(f"   • {nb.name}")
else:
    print(f"\n⚠️  Notebooks: Check ../LawBot_New/notebooks/")

# Summary
print("\n" + "="*70)
print("📊 SYSTEM STATUS SUMMARY")
print("="*70)

has_model = model_path.exists()
has_data = data_path.exists()
has_vectorstore = (vectorstore_path / "faiss_index.idx").exists()

print(f"\n{'✅' if has_model else '❌'} Fine-tuned Model")
print(f"{'✅' if has_data else '❌'} Training Data")
print(f"{'✅' if has_vectorstore else '❌'} RAG Vector Store")

if all([has_model, has_data, has_vectorstore]):
    print("\n🎉 All core components ready!")
    print("\n🚀 To use LawBot:")
    print("   • Simple CLI: python simple_chat.py")
    print("   • Demo: python demo.py")
    print("   • Gradio (if fixed): python run_gradio.py")
elif has_vectorstore:
    print("\n✅ RAG system is ready!")
    print("   Run: python simple_chat.py (for interactive chat)")
    print("   Run: python demo.py (for automated demo)")
else:
    print("\n⚠️  Setup needed:")
    if not has_vectorstore:
        print("   1. Create vector store: python scripts/create_vectorstore_simple.py")
    if not has_model:
        print("   2. Train model in Colab (notebooks in ../LawBot_New/)")

print("\n" + "="*70)

