"""
LawBot - Simple Command Line Chat Interface
No Gradio required - pure Python CLI
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

print("="*70)
print("⚖️  LawBot - Indian Legal Q&A Assistant")
print("="*70)

# Setup paths
BASE_DIR = Path(__file__).parent
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore" / "faiss_index"

# Legal Tools Dictionary
LEGAL_DICTIONARY = {
    "ipc": "Indian Penal Code - Criminal law of India",
    "crpc": "Code of Criminal Procedure - Procedure for criminal cases",
    "constitution": "Constitution of India - Supreme law of India",
    "bail": "Release of accused from custody pending trial",
    "arrest": "Taking of a person into custody for alleged offence",
    "murder": "Causing death with intention under IPC Section 300",
    "theft": "Taking movable property without consent under IPC Section 378",
    "section 302": "IPC Section 302 - Punishment for murder",
    "section 420": "IPC Section 420 - Cheating and dishonestly inducing delivery",
    "fir": "First Information Report - First step in criminal justice",
}

class SimpleLawBot:
    def __init__(self):
        self.rag_index = None
        self.rag_chunks = None
        self.rag_metadata = None
        self.embedding_model = None
        
        print("\n🔄 Initializing LawBot...")
        self.load_rag()
    
    def load_rag(self):
        """Load RAG components"""
        try:
            print("  📚 Loading RAG system...")
            from sentence_transformers import SentenceTransformer
            import faiss
            
            # Load embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load FAISS index
            index_file = VECTORSTORE_PATH / "faiss_index.idx"
            if index_file.exists():
                self.rag_index = faiss.read_index(str(index_file))
                
                with open(VECTORSTORE_PATH / "chunks.json", 'r', encoding='utf-8') as f:
                    self.rag_chunks = json.load(f)
                with open(VECTORSTORE_PATH / "metadata.json", 'r', encoding='utf-8') as f:
                    self.rag_metadata = json.load(f)
                
                print(f"  ✅ RAG loaded: {self.rag_index.ntotal} vectors, {len(self.rag_chunks)} chunks")
            else:
                print(f"  ⚠️  RAG not available (run: python scripts/create_vectorstore_simple.py)")
                
        except Exception as e:
            print(f"  ⚠️  RAG loading error: {e}")
            self.rag_index = None
    
    def retrieve_context(self, query: str, top_k: int = 3):
        """Retrieve relevant context using RAG"""
        if not self.rag_index or not self.embedding_model:
            return [], []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search FAISS index
            scores, indices = self.rag_index.search(query_embedding, top_k)
            
            # Collect relevant chunks
            contexts = []
            sources = []
            
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.rag_chunks) and score < 2.0:
                    contexts.append(self.rag_chunks[idx])
                    if idx < len(self.rag_metadata):
                        source = self.rag_metadata[idx].get('source', 'Unknown')
                        if source not in sources:
                            sources.append(source)
            
            return contexts, sources
            
        except Exception as e:
            print(f"  ⚠️  RAG retrieval error: {e}")
            return [], []
    
    def detect_legal_terms(self, query: str):
        """Detect legal terms in query"""
        terms_found = []
        query_lower = query.lower()
        
        for term, definition in LEGAL_DICTIONARY.items():
            if term in query_lower:
                terms_found.append((term, definition))
        
        return terms_found
    
    def answer_query(self, query: str):
        """Answer a legal query"""
        print("\n" + "─"*70)
        print(f"📝 Query: {query}")
        print("─"*70)
        
        # Step 1: RAG Retrieval
        contexts, sources = self.retrieve_context(query)
        
        if contexts:
            print("\n📚 Retrieved Context:")
            for i, context in enumerate(contexts[:3], 1):
                print(f"\n[{i}] {context[:300]}{'...' if len(context) > 300 else ''}")
        else:
            print("\n⚠️  No relevant context found in database")
        
        # Step 2: Legal Terms
        terms = self.detect_legal_terms(query)
        if terms:
            print("\n📖 Legal Terms Detected:")
            for term, definition in terms:
                print(f"  • {term.upper()}: {definition}")
        
        # Step 3: Sources
        if sources:
            print(f"\n📑 Sources: {', '.join(sources)}")
        
        # Step 4: Generate basic response
        print("\n💡 Response:")
        if contexts:
            # Simple rule-based response based on retrieved context
            response = self._generate_simple_response(query, contexts[0] if contexts else "")
            print(f"\n{response}")
        else:
            print("\nI don't have specific information about this in my database.")
            print("Please consult a qualified legal professional for accurate advice.")
        
        # Disclaimer
        print("\n" + "─"*70)
        print("⚠️  DISCLAIMER: This is for educational purposes only.")
        print("   Always consult a qualified lawyer for legal advice.")
        print("─"*70)
    
    def _generate_simple_response(self, query: str, context: str):
        """Generate a simple response based on context"""
        query_lower = query.lower()
        
        # Pattern-based responses
        if "what is" in query_lower or "explain" in query_lower:
            return f"Based on Indian legal documents:\n\n{context[:500]}"
        
        elif "punishment" in query_lower or "penalty" in query_lower:
            if "302" in query:
                return "IPC Section 302 deals with punishment for murder. The punishment can be:\n• Death penalty, or\n• Life imprisonment\n• Fine may also be imposed"
            elif "420" in query:
                return "IPC Section 420 deals with cheating. The punishment can be:\n• Imprisonment up to 7 years\n• Fine\n• Both"
            else:
                return f"Based on the legal provisions:\n\n{context[:500]}"
        
        elif "procedure" in query_lower or "how" in query_lower:
            return f"Based on the legal procedures:\n\n{context[:500]}"
        
        else:
            return f"According to Indian law:\n\n{context[:500]}"

def main():
    """Main chat loop"""
    bot = SimpleLawBot()
    
    print("\n✅ LawBot ready!")
    print("\n" + "="*70)
    print("Commands:")
    print("  • Type your legal question and press Enter")
    print("  • Type 'quit' or 'exit' to close")
    print("  • Type 'help' for example questions")
    print("="*70)
    
    while True:
        try:
            print("\n")
            query = input("🔍 You: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using LawBot! Goodbye.")
                break
            
            if query.lower() == 'help':
                print("\n📚 Example Questions:")
                print("  1. What is IPC Section 302?")
                print("  2. Explain the procedure for filing an FIR")
                print("  3. What is the punishment for theft?")
                print("  4. How to get bail in a criminal case?")
                print("  5. What are fundamental rights under the Constitution?")
                continue
            
            # Answer the query
            bot.answer_query(query)
            
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using LawBot! Goodbye.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()

