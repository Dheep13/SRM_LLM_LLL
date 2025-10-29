# Using Google Drive with Colab for LawBot

## Option 1: Mount Google Drive (Recommended!)

### Why Use Drive?
✅ **Keep your datasets in Drive** - Upload once, use forever  
✅ **Save outputs to Drive** - Never lose your work  
✅ **Access notebooks from anywhere**  
✅ **Persistent storage** - Session doesn't reset  

### How to Mount Drive

**Add this as the FIRST cell in your Colab notebook:**

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')
```

When you run this:
1. It will show a link - click it
2. Allow access to your Google account
3. Copy the authorization code
4. Paste it in the notebook
5. Done! Drive is mounted at `/content/drive/`

### Directory Structure in Drive

Upload your project to Google Drive like this:

```
MyDrive/                          ← Your Drive root
└── LawBot/                       ← Create this folder
    ├── notebooks/
    │   ├── phase1_data_prep.ipynb
    │   ├── phase2_finetune_lawbot.ipynb
    │   ├── phase3_rag_lawbot.ipynb
    │   ├── phase4_reward_model_lawbot.ipynb
    │   ├── phase5_lawbot_agent.ipynb
    │   └── phase6_gradio_app.ipynb
    └── datasets/                 ← Upload your 3 JSON files here
        ├── constitution_qa.json
        ├── crpc_qa.json
        └── ipc_qa.json
```

### Updated Path Configuration

**Option A: Use Drive paths (Recommended)**

```python
# Cell 1: Mount Drive and setup paths
from google.colab import drive
drive.mount('/content/drive')

import os
base_dir = '/content/drive/MyDrive/LawBot'

# Create directories
dirs_to_create = [
    f'{base_dir}/data',
    f'{base_dir}/data/processed',
    f'{base_dir}/models',
    f'{base_dir}/models/adapters',
    f'{base_dir}/vectorstore',
    f'{base_dir}/vectorstore/faiss_index'
]

for dir_path in dirs_to_create:
    os.makedirs(dir_path, exist_ok=True)

print(f"Using Drive directory: {base_dir}")
```

**Then upload datasets to:** `/content/drive/MyDrive/LawBot/datasets/`

**Advantages of Drive:**
- ✅ Data persists across sessions
- ✅ Can share folders with collaborators
- ✅ Backup in cloud
- ✅ Can download outputs easily

**Option B: Use Colab Session Storage**

Use the current setup we have:
- Path: `/content/LawBot`
- Data is uploaded each session
- Files disappear when session ends

**Advantages of Session Storage:**
- ✅ Faster (local disk)
- ✅ No mounting needed
- ✅ Simpler setup

**Disadvantages of Session Storage:**
- ❌ Loses files when session ends
- ❌ Have to re-upload each time
- ❌ Can't share easily

## My Recommendation

**Use Google Drive!** Here's why:

1. **Upload datasets once** - Put them in Drive, mount Drive in Colab
2. **Save outputs to Drive** - Keep your trained models, processed data
3. **Work on any computer** - Just mount Drive and continue
4. **Share easily** - Give access to Drive folder for collaboration

## Quick Start with Drive

### Step 1: Upload to Google Drive
1. Create `MyDrive/LawBot/` folder in Google Drive
2. Upload your 6 notebooks to `LawBot/notebooks/` 
3. Upload your 3 JSON files to `LawBot/datasets/`

### Step 2: Open in Colab
1. Right-click on a notebook in Drive
2. Select "Open with" → "Google Colab"
3. Add this as first cell:

```python
from google.colab import drive
drive.mount('/content/drive')
base_dir = '/content/drive/MyDrive/LawBot'
```

### Step 3: Run Notebooks
Now all your paths work:
- Datasets: `/content/drive/MyDrive/LawBot/datasets/`
- Outputs: `/content/drive/MyDrive/LawBot/data/processed/`
- Models: `/content/drive/MyDrive/LawBot/models/adapters/`

## Which Path Should I Use?

| Scenario | Use This |
|----------|----------|
| Quick test run | `/content/LawBot` (current setup) |
| Serious work, keep outputs | `/content/drive/MyDrive/LawBot` |
| Collaborating | Drive (share folder) |
| Training models for hours | Drive (persistent storage) |

## Quick Decision Guide

**Use Drive if:**
- ✅ You want to save outputs
- ✅ You're training big models
- ✅ You'll work across multiple sessions
- ✅ You want backups

**Use Session Storage if:**
- ✅ Just testing quickly
- ✅ Don't care about keeping files
- ✅ Want fastest performance

## Hybrid Approach

You can do both:

```python
# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Work on local (fast) but save to Drive (persistent)
work_dir = '/content/LawBot'  # Fast local storage
save_dir = '/content/drive/MyDrive/LawBot'  # Persistent Drive storage

# Process locally
# ... your code here ...

# Copy results to Drive periodically
import shutil
shutil.copytree(f'{work_dir}/data', f'{save_dir}/data', dirs_exist_ok=True)
shutil.copytree(f'{work_dir}/models', f'{save_dir}/models', dirs_exist_ok=True)
```

This gives you:
- ⚡ Fast local processing
- 💾 Persistent Drive backups
- 🔄 Best of both worlds

## Next Steps

1. **Upload to Google Drive** - Create LawBot folder structure
2. **Mount Drive in Colab** - Add mount cell to notebooks
3. **Update paths** - Change base_dir to Drive path
4. **Run notebooks** - Everything works the same!

The choice is yours! Drive is recommended for production work. 🚀

