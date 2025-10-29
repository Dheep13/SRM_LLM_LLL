# LawBot - Simple GitHub Push Script
# Repository: https://github.com/Dheep13/SRM_LLM_LLL.git

Write-Host "======================================================================"
Write-Host "  LawBot - Push to GitHub"
Write-Host "======================================================================"
Write-Host ""

$REPO_URL = "https://github.com/Dheep13/SRM_LLM_LLL.git"

# Check Git
Write-Host "Checking Git installation..."
try {
    git --version | Out-Null
    Write-Host "  OK: Git is installed" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Git not found. Install from https://git-scm.com" -ForegroundColor Red
    exit 1
}

# Check location
if (-not ((Test-Path "LawBot_FullStack") -and (Test-Path "LawBot_New"))) {
    Write-Host "ERROR: Run this from 80_LLL_LLM directory" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Files to push:"
Write-Host "  - LawBot_New/ (notebooks, data)"
Write-Host "  - LawBot_FullStack/ (inference, vectorstore)"
Write-Host "  - Documentation files"
Write-Host ""
Write-Host "Excluded (in .gitignore):"
Write-Host "  - models/adapters/ (use HuggingFace link instead)"
Write-Host ""

$confirm = Read-Host "Continue? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Cancelled"
    exit 0
}

# Initialize if needed
if (-not (Test-Path ".git")) {
    Write-Host ""
    Write-Host "Initializing Git repository..."
    git init
    git branch -M main
}

# Add files
Write-Host ""
Write-Host "Adding files..."
git add .

# Show what's staged
Write-Host ""
Write-Host "Files staged for commit:"
git status --short

# Commit
Write-Host ""
$message = Read-Host "Commit message (or Enter for default)"
if ([string]::IsNullOrWhiteSpace($message)) {
    $message = "Initial commit: LawBot project"
}

git commit -m "$message"

# Add remote
Write-Host ""
Write-Host "Setting up remote..."
$hasRemote = git remote 2>$null | Select-String "origin"
if ($hasRemote) {
    git remote set-url origin $REPO_URL
} else {
    git remote add origin $REPO_URL
}

# Push
Write-Host ""
Write-Host "======================================================================"
Write-Host "Pushing to: $REPO_URL"
Write-Host "======================================================================"
Write-Host ""
Write-Host "You may need to authenticate with your GitHub credentials."
Write-Host "Use Personal Access Token if asked for password."
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================================================"
    Write-Host "  SUCCESS!"
    Write-Host "======================================================================"
    Write-Host ""
    Write-Host "Repository: https://github.com/Dheep13/SRM_LLM_LLL"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Visit the repository URL above"
    Write-Host "  2. Verify files uploaded correctly"
    Write-Host "  3. Update README.md with HuggingFace model link"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "======================================================================"
    Write-Host "  Push failed - Common solutions:"
    Write-Host "======================================================================"
    Write-Host ""
    Write-Host "1. Authentication:"
    Write-Host "   - Create Personal Access Token at:"
    Write-Host "     https://github.com/settings/tokens"
    Write-Host "   - Use token as password when prompted"
    Write-Host ""
    Write-Host "2. If repo not empty:"
    Write-Host "   git push -u origin main --force"
    Write-Host ""
    Write-Host "3. Manual push:"
    Write-Host "   git push -u origin main"
    Write-Host ""
}

Write-Host "Press Enter to exit..."
Read-Host

