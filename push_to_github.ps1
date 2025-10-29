# LawBot - Push to GitHub Script
# Repository: https://github.com/Dheep13/SRM_LLM_LLL.git

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan
Write-Host "📤 LawBot - Push to GitHub" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan
Write-Host ""

# Configuration
$REPO_URL = "https://github.com/Dheep13/SRM_LLM_LLL.git"
$BRANCH = "main"

# Check if git is installed
Write-Host "🔍 Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "   Download from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Check if we're in the right directory
$currentDir = Get-Location
Write-Host "`n📁 Current directory: $currentDir" -ForegroundColor Cyan

if (-not (Test-Path "LawBot_FullStack") -or -not (Test-Path "LawBot_New")) {
    Write-Host "❌ Error: LawBot_FullStack or LawBot_New folder not found!" -ForegroundColor Red
    Write-Host "   Please run this script from: 80_LLL_LLM directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Project folders found" -ForegroundColor Green

# Check if already a git repo
if (Test-Path ".git") {
    Write-Host "`n⚠️  This is already a Git repository." -ForegroundColor Yellow
    $reinit = Read-Host "Do you want to reinitialize? (yes/no)"
    if ($reinit -eq "yes") {
        Write-Host "🗑️  Removing existing .git folder..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force .git
        Write-Host "✅ Removed" -ForegroundColor Green
    } else {
        Write-Host "📝 Using existing Git repository" -ForegroundColor Cyan
    }
}

# Initialize git repository
if (-not (Test-Path ".git")) {
    Write-Host "`n🔨 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Create/verify .gitignore
if (Test-Path ".gitignore") {
    Write-Host "`n✅ .gitignore already exists" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  .gitignore not found!" -ForegroundColor Yellow
    Write-Host "   Please ensure .gitignore is created before proceeding" -ForegroundColor Red
    exit 1
}

# Show what will be committed
Write-Host "`n📋 Files to be committed:" -ForegroundColor Cyan
Write-Host "   • LawBot_New/ (notebooks, data)" -ForegroundColor White
Write-Host "   • LawBot_FullStack/ (inference scripts, vectorstore)" -ForegroundColor White
Write-Host "   • Documentation files (.md)" -ForegroundColor White
Write-Host "   • README.md, .gitignore" -ForegroundColor White
Write-Host ""
Write-Host "❌ Excluded (too large / in .gitignore):" -ForegroundColor Yellow
Write-Host "   • models/adapters/ (hosted on HuggingFace)" -ForegroundColor DarkGray
Write-Host "   • __pycache__/, .ipynb_checkpoints/" -ForegroundColor DarkGray
Write-Host "   • .env, credentials files" -ForegroundColor DarkGray

# Confirm
Write-Host ""
$confirm = Read-Host "Continue with git add? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Cancelled by user" -ForegroundColor Red
    exit 0
}

# Add files
Write-Host "`n📦 Adding files to Git..." -ForegroundColor Yellow
git add .

# Show status
Write-Host "`n📊 Git status:" -ForegroundColor Cyan
git status --short

# Ask for commit message
Write-Host ""
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial commit: LawBot - Intelligent Legal Q&A Assistant"
}

# Commit
Write-Host "`n💾 Committing changes..." -ForegroundColor Yellow
git commit -m "$commitMessage"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Commit failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Changes committed!" -ForegroundColor Green

# Set branch to main
Write-Host "`n🔄 Setting branch to '$BRANCH'..." -ForegroundColor Yellow
git branch -M $BRANCH

# Add remote
Write-Host "`n🔗 Adding remote repository..." -ForegroundColor Yellow
Write-Host "   URL: $REPO_URL" -ForegroundColor Cyan

# Check if remote already exists
$remoteExists = git remote | Select-String -Pattern "origin"
if ($remoteExists) {
    Write-Host "⚠️  Remote 'origin' already exists" -ForegroundColor Yellow
    git remote set-url origin $REPO_URL
    Write-Host "✅ Updated remote URL" -ForegroundColor Green
} else {
    git remote add origin $REPO_URL
    Write-Host "✅ Remote added" -ForegroundColor Green
}

# Verify remote
Write-Host "`n📡 Remote repository:" -ForegroundColor Cyan
git remote -v

# Push
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan
Write-Host "🚀 Ready to push to GitHub!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan
Write-Host ""
$pushConfirm = Read-Host "Push to GitHub now? (yes/no)"

if ($pushConfirm -ne "yes") {
    Write-Host "`n📝 To push later, run:" -ForegroundColor Yellow
    Write-Host "   git push -u origin $BRANCH" -ForegroundColor White
    exit 0
}

Write-Host "`n📤 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Cyan

git push -u origin $BRANCH

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("="*69) -ForegroundColor Green
    Write-Host "✅ SUCCESS! Repository pushed to GitHub!" -ForegroundColor Green
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("="*69) -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Your repository is now live at:" -ForegroundColor Cyan
    Write-Host "   $REPO_URL" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Visit: https://github.com/Dheep13/SRM_LLM_LLL" -ForegroundColor White
    Write-Host "   2. Verify all files are uploaded" -ForegroundColor White
    Write-Host "   3. Update README.md with your HuggingFace model link" -ForegroundColor White
    Write-Host "   4. Add repository link to your PDF report" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 To update later:" -ForegroundColor Cyan
    Write-Host "   git add ." -ForegroundColor White
    Write-Host "   git commit -m 'Your message'" -ForegroundColor White
    Write-Host "   git push" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "   1. Authentication required:" -ForegroundColor White
    Write-Host "      - Use GitHub Personal Access Token as password" -ForegroundColor Gray
    Write-Host "      - Create at: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   2. Repository not empty:" -ForegroundColor White
    Write-Host "      - Use: git push -u origin $BRANCH --force (⚠️  overwrites)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   3. Network issues:" -ForegroundColor White
    Write-Host "      - Check internet connection" -ForegroundColor Gray
    Write-Host "      - Try again later" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📝 Manual push command:" -ForegroundColor Cyan
    Write-Host "   git push -u origin $BRANCH" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to exit..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

