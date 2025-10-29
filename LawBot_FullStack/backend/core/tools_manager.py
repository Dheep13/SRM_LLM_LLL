"""
LawBot Tools Manager
Handles legal tools: dictionary, date calculator, case lookup
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
from config.settings import LEGAL_TOOLS

logger = logging.getLogger(__name__)

class ToolsManager:
    def __init__(self):
        self.legal_dictionary = LEGAL_TOOLS["dictionary"]
        self.date_calculator_enabled = LEGAL_TOOLS["date_calculator"]
        self.case_lookup_enabled = LEGAL_TOOLS["case_lookup"]
        
    def lookup_legal_term(self, term: str) -> Dict[str, Any]:
        """Lookup legal term definition"""
        term_lower = term.lower().strip()
        
        # Direct lookup
        if term_lower in self.legal_dictionary:
            return {
                "term": term,
                "definition": self.legal_dictionary[term_lower],
                "found": True,
                "source": "Legal Dictionary"
            }
        
        # Partial match
        partial_matches = []
        for key, definition in self.legal_dictionary.items():
            if term_lower in key or key in term_lower:
                partial_matches.append({"term": key, "definition": definition})
        
        if partial_matches:
            return {
                "term": term,
                "definition": f"Partial matches found: {partial_matches[0]['definition']}",
                "found": True,
                "partial_matches": partial_matches,
                "source": "Legal Dictionary"
            }
        
        # No match
        available_terms = list(self.legal_dictionary.keys())
        return {
            "term": term,
            "definition": f"No definition found for '{term}'",
            "found": False,
            "available_terms": available_terms,
            "source": "Legal Dictionary"
        }
    
    def calculate_deadline(self, days: int, start_date: str = None) -> Dict[str, Any]:
        """Calculate legal deadline"""
        if not self.date_calculator_enabled:
            return {
                "error": "Date calculator not enabled",
                "success": False
            }
        
        try:
            if start_date:
                base_date = datetime.strptime(start_date, "%Y-%m-%d")
            else:
                base_date = datetime.now()
            
            deadline = base_date + timedelta(days=days)
            
            return {
                "start_date": base_date.strftime("%Y-%m-%d"),
                "deadline": deadline.strftime("%Y-%m-%d"),
                "days": days,
                "success": True,
                "source": "Date Calculator"
            }
            
        except Exception as e:
            logger.error(f"Date calculation error: {e}")
            return {
                "error": f"Invalid date format: {e}",
                "success": False
            }
    
    def lookup_legal_case(self, case_reference: str) -> Dict[str, Any]:
        """Lookup legal case information (mock implementation)"""
        if not self.case_lookup_enabled:
            return {
                "error": "Case lookup not enabled",
                "success": False
            }
        
        # Mock implementation - would integrate with Indian Kanoon API
        return {
            "case_reference": case_reference,
            "status": "Mock response",
            "description": f"Case information for {case_reference}: This would fetch real case data from Indian Kanoon API or Court Listener. Example: Case facts, judgment, citations, etc.",
            "success": True,
            "source": "Case Lookup (Mock)"
        }
    
    def detect_tool_usage(self, query: str) -> List[Dict[str, Any]]:
        """Detect which tools might be needed for a query"""
        tools_used = []
        query_lower = query.lower()
        
        # Check for legal terms
        for term in self.legal_dictionary.keys():
            if term in query_lower:
                tools_used.append({
                    "tool": "legal_dictionary",
                    "term": term,
                    "definition": self.legal_dictionary[term]
                })
        
        # Check for date-related queries
        date_keywords = ["deadline", "limitation", "days", "date", "time", "period"]
        if any(keyword in query_lower for keyword in date_keywords):
            tools_used.append({
                "tool": "date_calculator",
                "description": "Query contains date-related terms"
            })
        
        # Check for case-related queries
        case_keywords = ["case", "judgment", "court", "ruling", "decision"]
        if any(keyword in query_lower for keyword in case_keywords):
            tools_used.append({
                "tool": "case_lookup",
                "description": "Query contains case-related terms"
            })
        
        return tools_used
    
    def get_tools_info(self) -> Dict[str, Any]:
        """Get tools information"""
        return {
            "legal_dictionary": {
                "enabled": True,
                "terms_count": len(self.legal_dictionary),
                "terms": list(self.legal_dictionary.keys())
            },
            "date_calculator": {
                "enabled": self.date_calculator_enabled
            },
            "case_lookup": {
                "enabled": self.case_lookup_enabled,
                "note": "Mock implementation - integrate with Indian Kanoon API"
            }
        }
