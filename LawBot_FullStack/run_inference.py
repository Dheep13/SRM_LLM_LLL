"""
LawBot Inference Startup Script
One-command setup and launch for testing
"""

import os
import sys
import subprocess
from pathlib import Path

print("="*60)
print("🤖 LawBot Inference Setup & Launch")
print("="*60)

# Setup paths
BASE_DIR = Path(__file__).parent
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore" / "faiss_index"
MODEL_PATH = BASE_DIR / "models" / "adapters" / "lawbot_qwen_adapter"

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'torch', 'transformers', 'sentence-transformers', 
        'faiss-cpu', 'gradio', 'peft', 'numpy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}")
        print("Installing dependencies...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", 
                "requirements-minimal.txt"
            ], check=True)
            print("✅ Dependencies installed!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run manually: pip install -r requirements-minimal.txt")
            return False
    else:
        print("✅ All dependencies available")
    
    return True

def check_model():
    """Check if model is available"""
    print("\n🧠 Checking model...")
    
    if MODEL_PATH.exists():
        print(f"✅ Fine-tuned model found at: {MODEL_PATH}")
        return True
    else:
        print(f"⚠️  Model not found at: {MODEL_PATH}")
        print("The base model will be used for inference")
        return True  # Continue anyway with base model

def check_vectorstore():
    """Check if vectorstore exists, create if needed"""
    print("\n📚 Checking vectorstore...")
    
    index_file = VECTORSTORE_PATH / "faiss_index.idx"
    
    if index_file.exists():
        print(f"✅ Vectorstore found at: {VECTORSTORE_PATH}")
        return True
    else:
        print(f"⚠️  Vectorstore not found at: {VECTORSTORE_PATH}")
        print("\n🔧 Creating vectorstore...")
        
        try:
            # Run vectorstore creation script
            result = subprocess.run([
                sys.executable, 
                str(BASE_DIR / "scripts" / "create_vectorstore_simple.py")
            ], check=True, capture_output=False)
            
            if index_file.exists():
                print("✅ Vectorstore created successfully!")
                return True
            else:
                print("⚠️  Vectorstore creation completed but file not found")
                print("RAG will not be available")
                return True  # Continue anyway without RAG
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating vectorstore: {e}")
            print("Continuing without RAG...")
            return True  # Continue anyway

def launch_gradio():
    """Launch Gradio interface"""
    print("\n🚀 Launching Gradio interface...")
    print("="*60)
    print("\n📝 Instructions:")
    print("  1. The interface will open at: http://localhost:7860")
    print("  2. Ask legal questions in the chat")
    print("  3. Press Ctrl+C to stop the server")
    print("\n" + "="*60 + "\n")
    
    try:
        # Launch Gradio
        subprocess.run([
            sys.executable,
            str(BASE_DIR / "run_gradio.py")
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down LawBot...")
    except Exception as e:
        print(f"\n❌ Error launching Gradio: {e}")
        return False
    
    return True

def main():
    """Main execution"""
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed. Please install dependencies manually.")
        return False
    
    # Check model
    check_model()
    
    # Check/create vectorstore
    check_vectorstore()
    
    # Launch Gradio
    print("\n✅ Setup complete!")
    launch_gradio()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

