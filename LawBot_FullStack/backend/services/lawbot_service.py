"""
LawBot Service Layer
Orchestrates model, RAG, and tools for complete chat functionality
"""

import logging
from typing import Dict, Any, List
from backend.core.model_manager import ModelManager
from backend.core.rag_manager import RAGManager
from backend.core.tools_manager import ToolsManager

logger = logging.getLogger(__name__)

class LawBotService:
    def __init__(self):
        self.model_manager = ModelManager()
        self.rag_manager = RAGManager()
        self.tools_manager = ToolsManager()
        self.is_initialized = False
        
    def initialize(self) -> bool:
        """Initialize all components"""
        try:
            logger.info("Initializing LawBot service...")
            
            # Load model
            model_loaded = self.model_manager.load_model()
            
            # Load RAG components
            rag_loaded = self.rag_manager.load_components()
            
            # Tools are always available
            logger.info("✅ Tools manager initialized")
            
            self.is_initialized = model_loaded or rag_loaded
            
            if self.is_initialized:
                logger.info("🎉 LawBot service initialized successfully!")
            else:
                logger.warning("⚠️ LawBot service initialized in limited mode")
            
            return self.is_initialized
            
        except Exception as e:
            logger.error(f"❌ Error initializing LawBot service: {e}")
            self.is_initialized = False
            return False
    
    def chat(self, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Main chat function integrating all components"""
        if not query.strip():
            return {
                "response": "Please enter a question.",
                "citations": [],
                "tools_used": [],
                "confidence": "low",
                "error": None
            }
        
        try:
            # Step 1: RAG Retrieval
            rag_result = self.rag_manager.retrieve_context(query)
            context = rag_result["context"]
            citations = rag_result["citations"]
            
            # Step 2: Tool Detection
            tools_used = self.tools_manager.detect_tool_usage(query)
            
            # Step 3: Generate Response
            if self.model_manager.is_loaded:
                # Use fine-tuned model
                prompt = f"""Question: {query}

Context from legal documents:
{context}

Please provide a comprehensive answer about Indian law based on the context above."""
                
                response = self.model_manager.generate_response(prompt)
            else:
                # Fallback response
                response = self._generate_fallback_response(query, context, tools_used)
            
            # Step 4: Format Final Response
            final_response = self._format_response(response, citations, tools_used)
            
            return {
                "response": final_response,
                "citations": citations,
                "tools_used": tools_used,
                "confidence": rag_result["confidence"],
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error in chat function: {e}")
            return {
                "response": f"I apologize, but I encountered an error processing your question: '{query}'. Please try again.",
                "citations": [],
                "tools_used": [],
                "confidence": "low",
                "error": str(e)
            }
    
    def _generate_fallback_response(self, query: str, context: str, tools_used: List[Dict]) -> str:
        """Generate fallback response when model is not available"""
        response_parts = [
            f"I understand you're asking about: \"{query}\"",
            "",
            "This is a demo response. In a fully implemented system, I would:",
            "1. Search through legal documents using RAG",
            "2. Use my fine-tuned knowledge of Indian law", 
            "3. Provide accurate, cited responses",
            "4. Use legal tools when needed",
            "",
            "For now, here's a general response about legal queries:",
            "- Always consult qualified legal professionals for specific cases",
            "- Legal information changes frequently",
            "- This system is for educational purposes only"
        ]
        
        if context:
            response_parts.extend([
                "",
                "**Retrieved Context:**",
                context[:500] + "..." if len(context) > 500 else context
            ])
        
        if tools_used:
            response_parts.extend([
                "",
                "**Detected Tools:**",
                *[f"- {tool['tool']}: {tool.get('definition', tool.get('description', ''))}" for tool in tools_used]
            ])
        
        return "\n".join(response_parts)
    
    def _format_response(self, response: str, citations: List[str], tools_used: List[Dict]) -> str:
        """Format the final response with citations and disclaimers"""
        formatted_parts = [response]
        
        if citations:
            formatted_parts.append(f"\n**Sources:** {', '.join(citations)}")
        
        if tools_used:
            tool_info = []
            for tool in tools_used:
                if tool["tool"] == "legal_dictionary":
                    tool_info.append(f"Legal Dictionary: {tool['term']} - {tool['definition']}")
                else:
                    tool_info.append(f"{tool['tool']}: {tool.get('description', '')}")
            formatted_parts.append(f"\n**Tools Used:** {'; '.join(tool_info)}")
        
        # Add disclaimer
        formatted_parts.append("\n\n⚠️ *This is for educational purposes only. Consult a qualified lawyer for legal advice.*")
        
        return "\n".join(formatted_parts)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and component information"""
        return {
            "is_initialized": self.is_initialized,
            "model": self.model_manager.get_model_info(),
            "rag": self.rag_manager.get_rag_info(),
            "tools": self.tools_manager.get_tools_info()
        }
