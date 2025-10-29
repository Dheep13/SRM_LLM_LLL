"""
LawBot Gradio Inference Interface
Simple interface for testing fine-tuned model with RAG and tools
"""

import os
import sys
import json
import torch
import gradio as gr
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

print("🚀 Starting LawBot Gradio Interface...")

# Setup paths
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

# Configuration
MODEL_PATH = BASE_DIR / "models" / "adapters" / "lawbot_qwen_adapter"
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore" / "faiss_index"
BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

# Legal Tools Dictionary
LEGAL_DICTIONARY = {
    "ipc": "Indian Penal Code - Criminal law of India",
    "crpc": "Code of Criminal Procedure - Procedure for criminal cases",
    "constitution": "Constitution of India - Supreme law of India",
    "bail": "Release of accused from custody pending trial",
    "arrest": "Taking of a person into custody for alleged offence",
    "murder": "Causing death with intention under IPC Section 300",
    "theft": "Taking movable property without consent under IPC Section 378",
    "section 302": "IPC Section 302 - Punishment for murder (death or life imprisonment)",
    "section 420": "IPC Section 420 - Cheating and dishonestly inducing delivery of property",
    "fir": "First Information Report - First step in criminal justice process",
}

class LawBotInference:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.rag_index = None
        self.rag_chunks = None
        self.rag_metadata = None
        self.embedding_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Device: {self.device}")
        
        # Load components
        self.load_model()
        self.load_rag()
    
    def load_model(self):
        """Load fine-tuned model"""
        print("\n📦 Loading Model...")
        
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            print(f"  Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
            
            print(f"  Loading base model: {BASE_MODEL}")
            base_model = AutoModelForCausalLM.from_pretrained(
                BASE_MODEL,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
            )
            
            # Load LoRA adapters if available
            if MODEL_PATH.exists():
                print(f"  Loading LoRA adapters from: {MODEL_PATH}")
                try:
                    from peft import PeftModel
                    self.model = PeftModel.from_pretrained(base_model, str(MODEL_PATH))
                    print("  ✅ Fine-tuned model loaded!")
                except Exception as e:
                    print(f"  ⚠️ Could not load adapters: {e}")
                    print("  Using base model")
                    self.model = base_model
            else:
                print(f"  ⚠️ No adapters found at {MODEL_PATH}")
                print("  Using base model")
                self.model = base_model
            
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
            self.tokenizer = None
    
    def load_rag(self):
        """Load RAG components"""
        print("\n📚 Loading RAG Components...")
        
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            
            # Load embedding model
            print("  Loading embedding model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load FAISS index
            index_file = VECTORSTORE_PATH / "faiss_index.idx"
            if index_file.exists():
                print(f"  Loading FAISS index from: {index_file}")
                self.rag_index = faiss.read_index(str(index_file))
                
                # Load chunks and metadata
                with open(VECTORSTORE_PATH / "chunks.json", 'r', encoding='utf-8') as f:
                    self.rag_chunks = json.load(f)
                with open(VECTORSTORE_PATH / "metadata.json", 'r', encoding='utf-8') as f:
                    self.rag_metadata = json.load(f)
                
                print(f"  ✅ RAG loaded: {self.rag_index.ntotal} vectors, {len(self.rag_chunks)} chunks")
            else:
                print(f"  ⚠️ FAISS index not found at {index_file}")
                print("  RAG will not be available. Run: python scripts/create_vectorstore_simple.py")
                
        except Exception as e:
            print(f"❌ Error loading RAG: {e}")
            self.rag_index = None
    
    def retrieve_context(self, query: str, top_k: int = 5) -> Tuple[str, List[str]]:
        """Retrieve relevant context using RAG"""
        if not self.rag_index or not self.embedding_model:
            return "", []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search FAISS index
            scores, indices = self.rag_index.search(query_embedding, top_k)
            
            # Collect relevant chunks
            context_parts = []
            citations = []
            
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.rag_chunks) and score < 2.0:  # Relevance threshold
                    context_parts.append(f"[{i+1}] {self.rag_chunks[idx]}")
                    if idx < len(self.rag_metadata):
                        source = self.rag_metadata[idx].get('source', 'Unknown')
                        if source not in citations:
                            citations.append(source)
            
            context = "\n\n".join(context_parts)
            return context, citations
            
        except Exception as e:
            print(f"RAG retrieval error: {e}")
            return "", []
    
    def detect_tools(self, query: str) -> List[Dict[str, str]]:
        """Detect which legal tools might be needed"""
        tools_used = []
        query_lower = query.lower()
        
        # Check for legal terms
        for term, definition in LEGAL_DICTIONARY.items():
            if term in query_lower:
                tools_used.append({
                    "tool": "Legal Dictionary",
                    "term": term,
                    "definition": definition
                })
        
        # Check for date calculations
        date_keywords = ["deadline", "limitation", "days", "time period"]
        if any(keyword in query_lower for keyword in date_keywords):
            tools_used.append({
                "tool": "Date Calculator",
                "description": "Can calculate legal deadlines and time periods"
            })
        
        return tools_used
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using fine-tuned model"""
        if not self.model or not self.tokenizer:
            return "Model not available. Please check model loading."
        
        try:
            # Format prompt
            prompt = f"""<|im_start|>system
You are LawBot, an expert legal assistant specializing in Indian law. Provide accurate, helpful responses about Indian legal matters. Always cite relevant laws and be clear about limitations.
<|im_end|>
<|im_start|>user
Question: {query}

Context from legal documents:
{context}

Please provide a comprehensive answer based on the context above.
<|im_end|>
<|im_start|>assistant
"""
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.split("<|im_start|>assistant\n")[-1].strip()
            
            return response
            
        except Exception as e:
            print(f"Generation error: {e}")
            return f"I encountered an error generating a response. Please try again."
    
    def chat(self, query: str, history: List[List[str]]) -> Tuple[List[List[str]], str]:
        """Main chat function"""
        if not query.strip():
            return history, ""
        
        # Step 1: RAG Retrieval
        context, citations = self.retrieve_context(query)
        
        # Step 2: Tool Detection
        tools_used = self.detect_tools(query)
        
        # Step 3: Generate Response
        if self.model:
            response = self.generate_response(query, context)
        else:
            # Fallback response
            response = f"I understand you're asking about: '{query}'\n\n"
            if context:
                response += f"Based on the legal documents:\n{context[:500]}...\n\n"
            else:
                response += "I don't have specific legal documents for this query, but I can provide general information.\n\n"
            response += "Note: Model is not available for inference. Please check model loading."
        
        # Step 4: Format final response
        if citations:
            response += f"\n\n**📚 Sources:** {', '.join(citations)}"
        
        if tools_used:
            tool_info = []
            for tool in tools_used:
                if "term" in tool:
                    tool_info.append(f"{tool['term']}: {tool['definition']}")
                else:
                    tool_info.append(f"{tool['tool']}: {tool.get('description', '')}")
            response += f"\n\n**🔧 Tools Used:** {' | '.join(tool_info)}"
        
        # Add disclaimer
        response += "\n\n⚠️ *Disclaimer: This is for educational purposes only. Consult a qualified lawyer for legal advice.*"
        
        # Update history
        history.append([query, response])
        
        return history, ""

# Initialize LawBot
print("\n🤖 Initializing LawBot...")
lawbot = LawBotInference()

# Create Gradio Interface
print("\n🎨 Creating Gradio Interface...")

with gr.Blocks(title="LawBot - Legal Q&A Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # ⚖️ LawBot: Intelligent Legal Q&A Assistant
    
    Ask questions about Indian law (IPC, CrPC, Constitution). 
    Powered by fine-tuned Qwen2.5-1.5B + RAG + Legal Tools.
    """)
    
    with gr.Accordion("⚠️ Important Disclaimers", open=False):
        gr.Markdown("""
        **This tool is for educational purposes only.**
        
        - LawBot provides general legal information, not professional legal advice
        - Always consult a qualified lawyer for legal matters
        - Information may not reflect the most current legal developments
        - We are not responsible for decisions based on information provided
        """)
    
    # Chat interface
    chatbot = gr.Chatbot(
        label="LawBot Chat",
        height=500,
        show_copy_button=True,
    )
    
    with gr.Row():
        msg = gr.Textbox(
            label="Ask a legal question",
            placeholder="e.g., What is the punishment for murder under IPC Section 302?",
            scale=4
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)
        clear_btn = gr.Button("Clear", scale=1)
    
    # System status
    with gr.Accordion("📊 System Status", open=False):
        status_text = f"""
        **Model Status:** {'✅ Loaded' if lawbot.model else '❌ Not Available'}  
        **RAG Status:** {'✅ Active' if lawbot.rag_index else '❌ Not Available'}  
        **Device:** {lawbot.device}  
        **Vectors:** {lawbot.rag_index.ntotal if lawbot.rag_index else 0}
        """
        gr.Markdown(status_text)
    
    # Example questions
    gr.Examples(
        examples=[
            "What is IPC Section 302?",
            "How do I file a criminal complaint?",
            "What is the procedure for bail?",
            "Explain the concept of arrest under CrPC",
            "What are the fundamental rights under the Constitution?",
        ],
        inputs=msg
    )
    
    # Event handlers
    submit_btn.click(lawbot.chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
    msg.submit(lawbot.chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])

print("\n✅ Gradio interface ready!")
print("\n🌐 Launching interface...")
print("="*60)

if __name__ == "__main__":
    try:
        # Try local first
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_error=True,
            inbrowser=True,
        )
    except Exception as e:
        print(f"\n⚠️ Local launch failed: {e}")
        print("Trying with share=True to create a public link...")
        demo.launch(
            share=True,
            show_error=True,
            inbrowser=True,
        )

