"""
LawBot Model Manager
Handles loading and inference with the fine-tuned Qwen2.5-1.5B model
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
from typing import Optional, Dict, Any
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from config.settings import MODEL_CONFIG
except ImportError:
    # Fallback configuration if config module not available
    MODEL_CONFIG = {
        "base_model": "Qwen/Qwen2.5-1.5B-Instruct",
        "adapter_path": "models/adapters/lawbot_qwen_adapter",
        "max_length": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
    }

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_loaded = False
        
    def load_model(self) -> bool:
        """Load the fine-tuned model and tokenizer"""
        try:
            logger.info("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG["base_model"])
            
            logger.info("Loading base model...")
            base_model = AutoModelForCausalLM.from_pretrained(
                MODEL_CONFIG["base_model"],
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
            )
            
            # Load LoRA adapters if they exist
            adapter_path = MODEL_CONFIG["adapter_path"]
            if isinstance(adapter_path, str):
                adapter_path = os.path.abspath(adapter_path)
            
            if os.path.exists(adapter_path):
                logger.info(f"Loading LoRA adapters from {adapter_path}")
                try:
                    from peft import PeftModel
                    self.model = PeftModel.from_pretrained(base_model, adapter_path)
                    logger.info("✅ LoRA adapters loaded successfully!")
                except ImportError:
                    logger.warning("PEFT not available, using base model")
                    self.model = base_model
            else:
                logger.warning(f"No LoRA adapters found at {adapter_path}")
                logger.info("Using base model without fine-tuning")
                self.model = base_model
            
            self.is_loaded = True
            logger.info("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            self.is_loaded = False
            return False
    
    def generate_response(self, prompt: str, max_tokens: int = 256) -> str:
        """Generate response using the loaded model"""
        if not self.is_loaded:
            return "Model not loaded. Please check the model configuration."
        
        try:
            # Format prompt with chat template
            formatted_prompt = f"""<|im_start|>system
You are LawBot, an expert legal assistant specializing in Indian law. Provide accurate, helpful responses about Indian legal matters. Always cite relevant laws and be clear about limitations.
<|im_end|>
<|im_start|>user
{prompt}
<|im_end|>
<|im_start|>assistant
"""
            
            # Tokenize input
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=MODEL_CONFIG["temperature"],
                    top_p=MODEL_CONFIG["top_p"],
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.split("<|im_start|>assistant\n")[-1].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error processing your question. Please try again."
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        adapter_path = MODEL_CONFIG["adapter_path"]
        if isinstance(adapter_path, str):
            adapter_path = os.path.abspath(adapter_path)
            
        return {
            "is_loaded": self.is_loaded,
            "device": self.device,
            "base_model": MODEL_CONFIG["base_model"],
            "adapter_path": str(adapter_path),
            "has_adapters": os.path.exists(adapter_path),
        }
