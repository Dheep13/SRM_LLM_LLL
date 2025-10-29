"""
Simple RAG Vectorstore Creation Script
Creates FAISS index from legal documents without version conflicts
"""

import json
import os
import sys
from pathlib import Path
import numpy as np

print("🚀 Starting Simple RAG Vectorstore Creation...")

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = DATA_DIR / "vectorstore" / "faiss_index"

# Create directories
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
print(f"✅ Vectorstore directory: {VECTORSTORE_DIR}")

# Lazy import to avoid version conflicts
def lazy_import_sentence_transformers():
    """Lazy import with error handling"""
    try:
        print("\n📦 Importing sentence-transformers...")
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers imported successfully")
        return SentenceTransformer
    except Exception as e:
        print(f"❌ Error importing sentence-transformers: {e}")
        print("Installing/updating dependencies...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", 
                       "sentence-transformers", "torch<2.5.0", "transformers<4.45.0"], 
                      check=False)
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer

def lazy_import_faiss():
    """Lazy import FAISS"""
    try:
        import faiss
        return faiss
    except ImportError:
        print("Installing faiss-cpu...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "faiss-cpu"], check=True)
        import faiss
        return faiss

def load_legal_documents():
    """Load legal documents from available sources"""
    print("\n📚 Loading legal documents...")
    documents = []
    
    # Try processed data first
    processed_file = DATA_DIR / "processed" / "lawbot_cleaned.jsonl"
    
    if processed_file.exists():
        print(f"  Loading from: {processed_file}")
        with open(processed_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
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
                except Exception as e:
                    continue
    else:
        # Load from original datasets
        print("  Loading from original datasets...")
        datasets_dir = DATA_DIR / "datasets"
        
        for dataset_file in ['constitution_qa.json', 'crpc_qa.json', 'ipc_qa.json']:
            file_path = datasets_dir / dataset_file
            if file_path.exists():
                source_name = dataset_file.replace('_qa.json', '').upper()
                print(f"  Loading: {dataset_file}")
                
                try:
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
                except Exception as e:
                    print(f"  ⚠️ Error loading {dataset_file}: {e}")
                    continue
    
    print(f"✅ Loaded {len(documents)} legal documents")
    return documents

def chunk_documents(documents, chunk_size=800, chunk_overlap=100):
    """Simple chunking without external dependencies"""
    print(f"\n✂️  Chunking documents (size={chunk_size}, overlap={chunk_overlap})...")
    
    chunks = []
    metadata_list = []
    
    for doc in documents:
        text = doc['text']
        
        # Simple character-based chunking
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

def generate_embeddings(chunks, model_name='all-MiniLM-L6-v2'):
    """Generate embeddings with error handling"""
    print(f"\n🧠 Loading embedding model: {model_name}")
    
    SentenceTransformer = lazy_import_sentence_transformers()
    embedding_model = SentenceTransformer(model_name)
    
    print(f"  Embedding dimension: {embedding_model.get_sentence_embedding_dimension()}")
    print(f"  Generating embeddings for {len(chunks)} chunks...")
    
    # Generate in batches to avoid memory issues
    batch_size = 32
    all_embeddings = []
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_embeddings = embedding_model.encode(
            batch,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        all_embeddings.append(batch_embeddings)
        if (i // batch_size) % 10 == 0:
            print(f"  Progress: {i}/{len(chunks)} chunks processed")
    
    embeddings = np.vstack(all_embeddings)
    print(f"✅ Embeddings generated: {embeddings.shape}")
    
    return embeddings, embedding_model

def create_faiss_index(embeddings):
    """Create FAISS index"""
    print("\n🔍 Creating FAISS index...")
    
    faiss = lazy_import_faiss()
    
    dimension = embeddings.shape[1]
    embeddings = embeddings.astype('float32')
    
    # Use IndexFlatL2 for exact search
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    print(f"✅ FAISS index created with {index.ntotal} vectors")
    return index

def save_vectorstore(index, chunks, metadata_list, embedding_model):
    """Save all vectorstore components"""
    print("\n💾 Saving vectorstore...")
    
    faiss = lazy_import_faiss()
    
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

def test_retrieval(index, chunks, metadata_list, embedding_model):
    """Test retrieval"""
    print("\n🧪 Testing retrieval...")
    
    test_queries = [
        "What is IPC Section 302?",
        "How do I file a criminal complaint?",
        "What is bail?"
    ]
    
    for query in test_queries:
        print(f"\n  Query: {query}")
        query_embedding = embedding_model.encode([query])
        scores, indices = index.search(query_embedding, k=3)
        
        print(f"  Top results:")
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(chunks):
                chunk_preview = chunks[idx][:100].replace('\n', ' ')
                print(f"    [{i+1}] Score: {score:.2f} | {chunk_preview}...")

def main():
    """Main execution"""
    try:
        # Load documents
        documents = load_legal_documents()
        if not documents:
            print("❌ No documents found!")
            return False
        
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
        print("🎉 Vectorstore Creation Complete!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  Documents: {len(documents)}")
        print(f"  Chunks: {len(chunks)}")
        print(f"  Vectors: {index.ntotal}")
        print(f"  Dimension: {embeddings.shape[1]}")
        print(f"\n✅ Ready for inference!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

