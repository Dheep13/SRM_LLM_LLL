"""
RAG Vectorstore Population Script
Creates FAISS index from legal documents for LawBot
"""

import json
import os
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Any

print("🚀 Starting RAG Vectorstore Population...")

# Check and install dependencies
print("\n📦 Checking dependencies...")
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    print("✅ All dependencies available")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Installing required packages...")
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "pip", "install", "sentence-transformers", "faiss-cpu"], check=True)
    print("✅ Dependencies installed")
    from sentence_transformers import SentenceTransformer
    import faiss

# Setup paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = DATA_DIR / "vectorstore" / "faiss_index"

# Create directories
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
print(f"✅ Vectorstore directory: {VECTORSTORE_DIR}")

def load_legal_documents() -> List[Dict[str, Any]]:
    """Load legal documents from processed data"""
    print("\n📚 Loading legal documents...")
    documents = []
    
    # Check for processed data
    processed_file = DATA_DIR / "processed" / "lawbot_cleaned.jsonl"
    
    if processed_file.exists():
        print(f"  Loading from: {processed_file}")
        with open(processed_file, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                doc_text = f"Question: {item['instruction']}\nAnswer: {item['output']}\nSource: {item['source']}"
                documents.append({
                    'text': doc_text,
                    'source': item['source'],
                    'metadata': {
                        'instruction': item['instruction'],
                        'output': item['output'],
                        'source': item['source']
                    }
                })
    else:
        # Load from original datasets
        print("  Processed data not found, loading from original datasets...")
        datasets_dir = DATA_DIR / "datasets"
        
        for dataset_file in ['constitution_qa.json', 'crpc_qa.json', 'ipc_qa.json']:
            file_path = datasets_dir / dataset_file
            if file_path.exists():
                source_name = dataset_file.replace('_qa.json', '').upper()
                print(f"  Loading: {dataset_file}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for item in data:
                    doc_text = f"Question: {item['question']}\nAnswer: {item['answer']}\nSource: {source_name}"
                    documents.append({
                        'text': doc_text,
                        'source': source_name,
                        'metadata': {
                            'instruction': item['question'],
                            'output': item['answer'],
                            'source': source_name
                        }
                    })
    
    print(f"✅ Loaded {len(documents)} legal documents")
    return documents

def chunk_documents(documents: List[Dict], chunk_size: int = 800, chunk_overlap: int = 100) -> tuple:
    """Chunk documents into smaller pieces"""
    print(f"\n✂️  Chunking documents (size={chunk_size}, overlap={chunk_overlap})...")
    
    chunks = []
    metadata_list = []
    
    for doc in documents:
        text = doc['text']
        
        # Simple chunking by character count
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk)
                metadata_list.append(doc['metadata'])
            
            start = end - chunk_overlap
            if start >= len(text):
                break
    
    print(f"✅ Created {len(chunks)} chunks")
    avg_length = np.mean([len(c) for c in chunks])
    print(f"  Average chunk length: {avg_length:.0f} characters")
    
    return chunks, metadata_list

def generate_embeddings(chunks: List[str], model_name: str = 'all-MiniLM-L6-v2') -> np.ndarray:
    """Generate embeddings for all chunks"""
    print(f"\n🧠 Loading embedding model: {model_name}")
    embedding_model = SentenceTransformer(model_name)
    print(f"  Embedding dimension: {embedding_model.get_sentence_embedding_dimension()}")
    
    print("  Generating embeddings...")
    embeddings = embedding_model.encode(
        chunks, 
        show_progress_bar=True, 
        batch_size=32,
        convert_to_numpy=True
    )
    
    print(f"✅ Embeddings generated: {embeddings.shape}")
    return embeddings, embedding_model

def create_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """Create FAISS index from embeddings"""
    print("\n🔍 Creating FAISS index...")
    
    dimension = embeddings.shape[1]
    
    # Convert to float32 for FAISS
    embeddings = embeddings.astype('float32')
    
    # Create index (using L2 distance)
    index = faiss.IndexFlatL2(dimension)
    
    # Add vectors to index
    index.add(embeddings)
    
    print(f"✅ FAISS index created with {index.ntotal} vectors")
    return index

def save_vectorstore(index: faiss.Index, chunks: List[str], metadata_list: List[Dict], 
                     embedding_model: SentenceTransformer):
    """Save FAISS index and metadata"""
    print("\n💾 Saving vectorstore...")
    
    # Save FAISS index
    index_file = VECTORSTORE_DIR / "faiss_index.idx"
    faiss.write_index(index, str(index_file))
    print(f"  ✅ FAISS index: {index_file}")
    
    # Save chunks
    chunks_file = VECTORSTORE_DIR / "chunks.json"
    with open(chunks_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Chunks: {chunks_file}")
    
    # Save metadata
    metadata_file = VECTORSTORE_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Metadata: {metadata_file}")
    
    # Save config
    config = {
        'embedding_model': 'all-MiniLM-L6-v2',
        'embedding_dimension': embedding_model.get_sentence_embedding_dimension(),
        'total_vectors': index.ntotal,
        'total_chunks': len(chunks),
        'chunk_size': 800,
        'chunk_overlap': 100,
    }
    
    config_file = VECTORSTORE_DIR / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(f"  ✅ Config: {config_file}")
    
    print("\n✅ Vectorstore saved successfully!")

def test_retrieval(index: faiss.Index, chunks: List[str], metadata_list: List[Dict],
                   embedding_model: SentenceTransformer):
    """Test the vectorstore with sample queries"""
    print("\n🧪 Testing retrieval...")
    
    test_queries = [
        "What is IPC Section 302?",
        "How do I file a criminal complaint?",
        "What is bail?"
    ]
    
    for query in test_queries:
        print(f"\n  Query: {query}")
        
        # Generate query embedding
        query_embedding = embedding_model.encode([query])
        
        # Search
        scores, indices = index.search(query_embedding, k=3)
        
        print(f"  Top results:")
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(chunks):
                chunk_preview = chunks[idx][:100] + "..." if len(chunks[idx]) > 100 else chunks[idx]
                print(f"    [{i+1}] Score: {score:.2f} | {chunk_preview}")

def main():
    """Main function"""
    try:
        # Load documents
        documents = load_legal_documents()
        
        if not documents:
            print("❌ No documents found! Please ensure data is available.")
            return
        
        # Chunk documents
        chunks, metadata_list = chunk_documents(documents)
        
        # Generate embeddings
        embeddings, embedding_model = generate_embeddings(chunks)
        
        # Create FAISS index
        index = create_faiss_index(embeddings)
        
        # Save vectorstore
        save_vectorstore(index, chunks, metadata_list, embedding_model)
        
        # Test retrieval
        test_retrieval(index, chunks, metadata_list, embedding_model)
        
        print("\n" + "="*60)
        print("🎉 RAG Vectorstore Population Complete!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  Total documents: {len(documents)}")
        print(f"  Total chunks: {len(chunks)}")
        print(f"  Embedding dimension: {embeddings.shape[1]}")
        print(f"  Index size: {index.ntotal} vectors")
        print(f"\n📁 Files created:")
        print(f"  {VECTORSTORE_DIR}/faiss_index.idx")
        print(f"  {VECTORSTORE_DIR}/chunks.json")
        print(f"  {VECTORSTORE_DIR}/metadata.json")
        print(f"  {VECTORSTORE_DIR}/config.json")
        print("\n✅ Ready to use with LawBot!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
