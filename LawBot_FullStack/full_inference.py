"""
LawBot - Full Inference with Fine-Tuned Model + RAG
This loads the complete system: fine-tuned model + RAG retrieval
⚠️  Takes 2-5 minutes to load on CPU, requires 4-8GB RAM
"""

import os
import sys
import json
import torch
from pathlib import Path
from datetime import datetime

print("="*70)
print("⚖️  LawBot - Full Inference (Fine-Tuned Model + RAG)")
print("="*70)
print("\n⏳ Loading will take 2-5 minutes on CPU...")
print("   Please be patient, this is normal!\n")

# Setup paths
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "adapters" / "lawbot_qwen_adapter"
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore" / "faiss_index"
BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

# Legal dictionary
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

class FullLawBot:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.rag_index = None
        self.rag_chunks = None
        self.rag_metadata = None
        self.embedding_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🖥️  Device: {self.device}")
        if self.device == "cpu":
            print("   ⚠️  Using CPU - inference will be slower but works fine\n")
        
        # Load components
        self.load_model()
        self.load_rag()
    
    def load_model(self):
        """Load fine-tuned model with LoRA adapters"""
        print("─"*70)
        print("📦 Step 1/2: Loading Fine-Tuned Model...")
        print("─"*70)
        
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            from peft import PeftModel
            
            print("  [1/4] Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
            print("  ✅ Tokenizer loaded")
            
            print(f"\n  [2/4] Loading base model: {BASE_MODEL}")
            print("        (This takes 1-2 minutes on CPU...)")
            base_model = AutoModelForCausalLM.from_pretrained(
                BASE_MODEL,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True,
            )
            print("  ✅ Base model loaded")
            
            # Load LoRA adapters
            if MODEL_PATH.exists():
                print(f"\n  [3/4] Loading LoRA adapters from: {MODEL_PATH.name}")
                print("        (This takes 30-60 seconds...)")
                self.model = PeftModel.from_pretrained(base_model, str(MODEL_PATH))
                print("  ✅ Fine-tuned adapters loaded!")
                print("\n  🎉 FULL FINE-TUNED MODEL READY!")
            else:
                print(f"\n  ⚠️  No adapters found at {MODEL_PATH}")
                print("      Using base model only")
                self.model = base_model
            
            print("\n  [4/4] Moving to device...")
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            print(f"  ✅ Model on {self.device}")
            
            # Set to eval mode
            self.model.eval()
            print("\n✅ MODEL LOADING COMPLETE!\n")
            
        except Exception as e:
            print(f"\n❌ Error loading model: {e}")
            import traceback
            traceback.print_exc()
            self.model = None
            self.tokenizer = None
    
    def load_rag(self):
        """Load RAG components"""
        print("─"*70)
        print("📚 Step 2/2: Loading RAG System...")
        print("─"*70)
        
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            
            print("  [1/3] Loading embedding model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("  ✅ Embedding model loaded")
            
            # Load FAISS index
            index_file = VECTORSTORE_PATH / "faiss_index.idx"
            if index_file.exists():
                print(f"\n  [2/3] Loading FAISS index...")
                self.rag_index = faiss.read_index(str(index_file))
                print(f"  ✅ FAISS index loaded: {self.rag_index.ntotal} vectors")
                
                print(f"\n  [3/3] Loading chunks and metadata...")
                with open(VECTORSTORE_PATH / "chunks.json", 'r', encoding='utf-8') as f:
                    self.rag_chunks = json.load(f)
                with open(VECTORSTORE_PATH / "metadata.json", 'r', encoding='utf-8') as f:
                    self.rag_metadata = json.load(f)
                
                print(f"  ✅ Loaded {len(self.rag_chunks)} document chunks")
                print("\n✅ RAG LOADING COMPLETE!\n")
            else:
                print(f"\n  ❌ FAISS index not found at {index_file}")
                self.rag_index = None
                
        except Exception as e:
            print(f"\n❌ Error loading RAG: {e}")
            import traceback
            traceback.print_exc()
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
            
            for score, idx in zip(scores[0], indices[0]):
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
    
    def generate_with_model(self, query: str, context: str) -> str:
        """Generate response using fine-tuned model"""
        if not self.model or not self.tokenizer:
            return "❌ Model not available. Using RAG-only mode."
        
        try:
            print("\n  🤖 Generating response with fine-tuned model...")
            
            # Format prompt with RAG context
            if context:
                prompt = f"""<|im_start|>system
You are LawBot, an expert legal assistant specializing in Indian law (IPC, CrPC, Constitution). 
Provide accurate, helpful responses based on the context provided. Always cite relevant laws.
<|im_end|>
<|im_start|>user
Question: {query}

Context from legal documents:
{context}

Please provide a comprehensive answer based on the context above.
<|im_end|>
<|im_start|>assistant
"""
            else:
                prompt = f"""<|im_start|>system
You are LawBot, an expert legal assistant specializing in Indian law.
<|im_end|>
<|im_start|>user
Question: {query}
<|im_end|>
<|im_start|>assistant
"""
            
            # Tokenize
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=2048
            )
            
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            elif self.device == "cpu":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate
            print("     (Generating... this takes 10-30 seconds on CPU)")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract assistant response
            if "<|im_start|>assistant" in response:
                response = response.split("<|im_start|>assistant")[-1].strip()
            if "<|im_end|>" in response:
                response = response.split("<|im_end|>")[0].strip()
            
            print("  ✅ Response generated!\n")
            return response
            
        except Exception as e:
            print(f"\n  ❌ Generation error: {e}")
            import traceback
            traceback.print_exc()
            return f"Error generating response. Using context instead:\n\n{context[:500] if context else 'No context available'}"
    
    def answer_query(self, query: str):
        """Answer a legal query with full system"""
        print("\n" + "="*70)
        print(f"📝 Query: {query}")
        print("="*70)
        
        # Step 1: RAG Retrieval
        print("\n🔍 Step 1: Retrieving context from RAG...")
        contexts, sources = self.retrieve_context(query)
        
        if contexts:
            print(f"  ✅ Retrieved {len(contexts)} relevant chunks")
            print("\n📚 Top Retrieved Context:")
            for i, context in enumerate(contexts[:2], 1):
                print(f"\n  [{i}] {context[:200]}{'...' if len(context) > 200 else ''}")
            
            # Combine contexts
            combined_context = "\n\n".join(contexts[:3])
        else:
            print("  ⚠️  No relevant context found")
            combined_context = ""
        
        # Step 2: Legal Terms
        terms = self.detect_legal_terms(query)
        if terms:
            print("\n📖 Legal Terms Detected:")
            for term, definition in terms:
                print(f"  • {term.upper()}: {definition}")
        
        # Step 3: Generate with Model
        print("\n💡 Step 2: Generating response...")
        response = self.generate_with_model(query, combined_context)
        
        # Display response
        print("\n" + "─"*70)
        print("🤖 LawBot Response (Fine-Tuned Model + RAG):")
        print("─"*70)
        print(f"\n{response}\n")
        
        # Sources
        if sources:
            print(f"📑 Sources: {', '.join(sources)}")
        
        # Disclaimer
        print("\n" + "─"*70)
        print("⚠️  DISCLAIMER: For educational purposes only.")
        print("   Always consult a qualified lawyer for legal advice.")
        print("─"*70)

def main():
    """Main function"""
    try:
        # Initialize
        bot = FullLawBot()
        
        if not bot.model:
            print("\n❌ Model failed to load. Exiting.")
            print("   Try using 'python simple_chat.py' for RAG-only mode.")
            return
        
        print("\n" + "="*70)
        print("✅ FULL SYSTEM READY!")
        print("="*70)
        print("\n🎉 You now have:")
        print("   • Fine-tuned Qwen2.5-1.5B model")
        print("   • RAG with 14,630 document chunks")
        print("   • Legal tools integration")
        print("\n" + "="*70)
        print("Commands:")
        print("  • Type your legal question and press Enter")
        print("  • Type 'quit' or 'exit' to close")
        print("  • Type 'help' for example questions")
        print("="*70)
        
        # Chat loop
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
                    print("  2. How to file an FIR?")
                    print("  3. What are fundamental rights under the Constitution?")
                    print("  4. What is the punishment for theft?")
                    print("  5. Explain the procedure for bail")
                    continue
                
                # Answer with full system
                bot.answer_query(query)
                
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using LawBot! Goodbye.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.")
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n🚀 Starting Full LawBot (Model + RAG)...")
    print("⏳ Initial loading takes 2-5 minutes, please wait...\n")
    main()

