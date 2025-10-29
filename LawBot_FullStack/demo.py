"""
LawBot Demo - Shows capabilities without interactive input
"""

import os
import sys
import json
from pathlib import Path

print("="*70)
print("⚖️  LawBot Demo - Automated Testing")
print("="*70)

BASE_DIR = Path(__file__).parent
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore" / "faiss_index"

# Test queries
TEST_QUERIES = [
    "What is IPC Section 302?",
    "Explain the procedure for bail",
    "What is the punishment for theft?",
]

print("\n🔄 Loading RAG System...")
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    index_file = VECTORSTORE_PATH / "faiss_index.idx"
    if index_file.exists():
        rag_index = faiss.read_index(str(index_file))
        
        with open(VECTORSTORE_PATH / "chunks.json", 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        with open(VECTORSTORE_PATH / "metadata.json", 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        print(f"✅ RAG Loaded: {rag_index.ntotal} vectors, {len(chunks)} chunks\n")
        
        # Run demo queries
        for i, query in enumerate(TEST_QUERIES, 1):
            print("="*70)
            print(f"Demo Query {i}: {query}")
            print("="*70)
            
            # Search
            query_embedding = embedding_model.encode([query])
            scores, indices = rag_index.search(query_embedding, 3)
            
            print("\n📚 Retrieved Context:")
            for j, (score, idx) in enumerate(zip(scores[0], indices[0]), 1):
                if idx < len(chunks):
                    context = chunks[idx]
                    source = metadata[idx].get('source', 'Unknown') if idx < len(metadata) else 'Unknown'
                    print(f"\n[{j}] (Score: {score:.4f}, Source: {source})")
                    print(f"    {context[:250]}...")
            
            print("\n")
        
        print("="*70)
        print("✅ Demo Complete!")
        print("="*70)
        print("\n💡 To chat interactively, run: python simple_chat.py")
        print("   Type your legal questions and get instant answers!")
        
    else:
        print(f"❌ FAISS index not found at: {index_file}")
        print("\nRun this first: python scripts/create_vectorstore_simple.py")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

