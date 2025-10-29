"""
Simple startup script for LawBot Full-Stack Application
Handles installation and startup gracefully
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install Python requirements with error handling"""
    print("📦 Installing Python dependencies...")
    
    try:
        # Try to install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Python dependencies installed successfully!")
            return True
        else:
            print(f"❌ Error installing dependencies: {result.stderr}")
            
            # Try installing core dependencies individually
            print("🔄 Trying to install core dependencies individually...")
            core_deps = [
                "fastapi", "uvicorn", "pydantic", "python-multipart", 
                "python-dotenv", "torch", "transformers", "sentence-transformers"
            ]
            
            for dep in core_deps:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                 check=True, capture_output=True)
                    print(f"  ✅ {dep}")
                except subprocess.CalledProcessError:
                    print(f"  ❌ {dep}")
            
            return True
            
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def check_directories():
    """Check and create necessary directories"""
    print("📁 Checking directories...")
    
    directories = [
        "models/adapters",
        "data/vectorstore", 
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")

def copy_existing_files():
    """Copy existing model and data files if they exist"""
    print("📋 Checking for existing files...")
    
    # Check for models
    source_models = Path("../LawBot_New/models")
    if source_models.exists():
        print("  Found existing models, copying...")
        import shutil
        shutil.copytree(source_models, "models", dirs_exist_ok=True)
        print("  ✅ Models copied")
    else:
        print("  ⚠️ No existing models found")
    
    # Check for data
    source_data = Path("../LawBot_New/data")
    if source_data.exists():
        print("  Found existing data, copying...")
        import shutil
        shutil.copytree(source_data, "data", dirs_exist_ok=True)
        print("  ✅ Data copied")
    else:
        print("  ⚠️ No existing data found")

def start_backend():
    """Start the backend server"""
    print("🚀 Starting LawBot backend...")
    
    try:
        # Set PYTHONPATH
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], env=env)
        
    except KeyboardInterrupt:
        print("\n👋 Backend stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def main():
    """Main startup function"""
    print("🎯 LawBot Full-Stack Application Startup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return
    
    # Install dependencies
    if not install_requirements():
        print("❌ Failed to install dependencies")
        return
    
    # Setup directories
    check_directories()
    
    # Copy existing files
    copy_existing_files()
    
    print("\n🎉 Setup complete!")
    print("\n📝 Next steps:")
    print("1. Copy your trained model to: models/adapters/lawbot_qwen_adapter/")
    print("2. Copy your vectorstore to: data/vectorstore/")
    print("3. Start frontend: cd frontend && npm install && npm start")
    print("4. Backend will start automatically...")
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
