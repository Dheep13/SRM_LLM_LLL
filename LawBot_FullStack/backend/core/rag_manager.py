"""
LawBot RAG Manager
Handles document retrieval and context generation using FAISS
"""

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging
from config.settings import RAG_CONFIG

logger = logging.getLogger(__name__)

class RAGManager:
    def __init__(self):
        self.embedding_model = None
        self.index = None
        self.chunks = []
        self.metadata_list = []
        self.is_loaded = False
        
    def load_components(self) -> bool:
        """Load FAISS index, chunks, and metadata"""
        try:
            logger.info("Loading embedding model...")
            self.embedding_model = SentenceTransformer(RAG_CONFIG["embedding_model"])
            
            # Load FAISS index
            if RAG_CONFIG["vectorstore_path"].exists():
                logger.info(f"Loading FAISS index from {RAG_CONFIG['vectorstore_path']}")
                self.index = faiss.read_index(str(RAG_CONFIG["vectorstore_path"] / "faiss_index.idx"))
                logger.info(f"✅ FAISS index loaded: {self.index.ntotal} vectors")
                
                # Load chunks and metadata
                with open(RAG_CONFIG["chunks_path"], 'r') as f:
                    self.chunks = json.load(f)
                with open(RAG_CONFIG["metadata_path"], 'r') as f:
                    self.metadata_list = json.load(f)
                logger.info(f"✅ Loaded {len(self.chunks)} chunks and metadata")
                
                self.is_loaded = True
                return True
            else:
                logger.warning(f"No FAISS index found at {RAG_CONFIG['vectorstore_path']}")
                logger.info("RAG will work in fallback mode")
                self.is_loaded = False
                return False
                
        except Exception as e:
            logger.error(f"❌ Error loading RAG components: {e}")
            self.is_loaded = False
            return False
    
    def retrieve_context(self, query: str, top_k: int = None) -> Dict[str, Any]:
        """Retrieve relevant context for a query"""
        if not self.is_loaded:
            return {
                "context": "",
                "citations": [],
                "confidence": "low",
                "message": "RAG not available - using model knowledge only"
            }
        
        try:
            top_k = top_k or RAG_CONFIG["top_k"]
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search FAISS index
            scores, indices = self.index.search(query_embedding, top_k)
            
            # Process results
            context_parts = []
            citations = []
            
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.chunks) and score < RAG_CONFIG["similarity_threshold"]:
                    context_parts.append(f"[{i+1}] {self.chunks[idx]}")
                    if idx < len(self.metadata_list):
                        source = self.metadata_list[idx].get('source', 'Unknown')
                        citations.append(source)
            
            context = "\n\n".join(context_parts)
            unique_citations = list(set(citations))
            
            confidence = "high" if len(context_parts) > 0 else "low"
            
            return {
                "context": context,
                "citations": unique_citations,
                "confidence": confidence,
                "message": f"Retrieved {len(context_parts)} relevant documents"
            }
            
        except Exception as e:
            logger.error(f"Error in RAG retrieval: {e}")
            return {
                "context": "",
                "citations": [],
                "confidence": "low",
                "message": f"RAG error: {str(e)}"
            }
    
    def get_rag_info(self) -> Dict[str, Any]:
        """Get RAG system information"""
        return {
            "is_loaded": self.is_loaded,
            "embedding_model": RAG_CONFIG["embedding_model"],
            "total_vectors": self.index.ntotal if self.index else 0,
            "total_chunks": len(self.chunks),
            "vectorstore_path": str(RAG_CONFIG["vectorstore_path"]),
        }
