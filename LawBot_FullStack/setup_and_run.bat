@echo off
echo ====================================
echo LawBot Setup and Run
echo ====================================

echo.
echo Step 1: Installing core dependencies...
pip install --upgrade pip
pip install torch numpy
pip install transformers==4.44.2
pip install sentence-transformers
pip install datasets
pip install faiss-cpu
pip install "gradio>=4.0.0,<5.0.0"
pip install peft

echo.
echo Dependencies installed!
echo.

echo Step 2: Creating vectorstore (this takes 5-10 minutes)...
echo Press Ctrl+C if you want to skip vectorstore creation
echo.
python scripts\create_vectorstore_simple.py

if %errorlevel% neq 0 (
    echo Warning: Vectorstore creation had issues, but continuing...
)

echo.
echo Step 3: Launching Gradio interface...
echo Access at: http://localhost:7860
echo Press Ctrl+C to stop the server
echo.
python run_gradio.py

pause

