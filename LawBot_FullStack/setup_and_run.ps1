# LawBot Setup and Run Script
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "LawBot Setup and Run" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Installing dependencies..." -ForegroundColor Yellow
pip install transformers==4.44.2 sentence-transformers datasets torch faiss-cpu gradio peft numpy

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing packages!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 2: Creating vectorstore..." -ForegroundColor Yellow
python scripts\create_vectorstore_simple.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Vectorstore creation had issues, but continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 3: Launching Gradio interface..." -ForegroundColor Yellow
python run_gradio.py

Read-Host "Press Enter to exit"

