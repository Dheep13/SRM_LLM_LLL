"""
Setup and utility scripts for LawBot Full-Stack Application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_project():
    """Setup the LawBot project structure and dependencies"""
    print("🚀 Setting up LawBot Full-Stack Application...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Install backend dependencies
    print("\n📦 Installing backend dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Backend dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False
    
    # Setup frontend
    print("\n📦 Setting up frontend...")
    frontend_path = Path("frontend")
    if frontend_path.exists():
        try:
            subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    directories = [
        "models/adapters",
        "data/vectorstore",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created {directory}")
    
    # Copy model files if they exist
    print("\n📋 Checking for existing model files...")
    source_models = Path("../LawBot_New/models")
    if source_models.exists():
        print("  Found existing models, copying...")
        shutil.copytree(source_models, "models", dirs_exist_ok=True)
        print("  ✅ Models copied")
    else:
        print("  ⚠️ No existing models found - you'll need to run training first")
    
    # Copy data files if they exist
    print("\n📋 Checking for existing data files...")
    source_data = Path("../LawBot_New/data")
    if source_data.exists():
        print("  Found existing data, copying...")
        shutil.copytree(source_data, "data", dirs_exist_ok=True)
        print("  ✅ Data copied")
    else:
        print("  ⚠️ No existing data found - you'll need to run data preparation first")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Copy your trained model to models/adapters/lawbot_qwen_adapter/")
    print("2. Copy your vectorstore to data/vectorstore/")
    print("3. Run: python backend/main.py")
    print("4. In another terminal: cd frontend && npm start")
    
    return True

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python packages
    required_packages = [
        "fastapi", "uvicorn", "torch", "transformers", 
        "sentence-transformers", "faiss-cpu", "peft"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All Python packages available")
    
    # Check Node.js
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ Node.js and npm available")
    except subprocess.CalledProcessError:
        print("❌ Node.js or npm not found")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_requirements()
    else:
        setup_project()
