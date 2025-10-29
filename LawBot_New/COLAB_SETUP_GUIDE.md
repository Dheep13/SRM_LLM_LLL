# Google Colab Setup Guide for LawBot

## Directory Structure in Colab

When you upload files to Colab, here's where everything goes:

```
/content/
├── your_workspace/               # Your main folder
│   ├── notebooks/               # Upload all 6 notebooks here
│   │   ├── phase1_data_prep.ipynb
│   │   ├── phase2_finetune_lawbot.ipynb
│   │   ├── phase3_rag_lawbot.ipynb
│   │   ├── phase4_reward_model_lawbot.ipynb
│   │   ├── phase5_lawbot_agent.ipynb
│   │   └── phase6_gradio_app.ipynb
│   │
│   └── datasets/                # Upload your 3 JSON files here
│       ├── constitution_qa.json
│       ├── crpc_qa.json
│       └── ipc_qa.json
```

## Step-by-Step Setup

### 1. Create Uploads Folder
In your first Colab notebook, run:

```python
import os
os.makedirs('/content/LawBot/datasets', exist_ok=True)
os.makedirs('/content/LawBot/data/processed', exist_ok=True)
os.makedirs('/content/LawBot/models/adapters', exist_ok=True)
os.makedirs('/content/LawBot/vectorstore/faiss_index', exist_ok=True)
print("Folders created!")
```

### 2. Upload Dataset Files

**Option A: Using Colab's UI (Easiest)**
1. Click the 📁 folder icon on left sidebar
2. Click "Upload to session storage" button
3. Select your 3 JSON files:
   - `constitution_qa.json`
   - `crpc_qa.json`
   - `ipc_qa.json`
4. Upload them to `/content/LawBot/datasets/`

**Option B: Upload via Code**
```python
from google.colab import files
uploaded = files.upload()  # Click the "Choose Files" button

# Then move them to the right location
import shutil
for filename in uploaded.keys():
    shutil.move(filename, f'/content/LawBot/datasets/{filename}')
    print(f"Moved {filename} to datasets folder")
```

### 3. Adjust Paths in Notebooks

Update the paths in `phase1_data_prep.ipynb`:

**Find this code (around line 44-51):**
```python
# Load all three datasets
with open('../Indian_Legal_Dataset_Lawbot_Assignment/Indian_Legal_Dataset_Lawbot_Assignment/constitution_qa.json', 'r', encoding='utf-8') as f:
    constitution_data = json.load(f)
```

**Change to:**
```python
# Load all three datasets
with open('/content/LawBot/datasets/constitution_qa.json', 'r', encoding='utf-8') as f:
    constitution_data = json.load(f)
    
with open('/content/LawBot/datasets/crpc_qa.json', 'r', encoding='utf-8') as f:
    crpc_data = json.load(f)
    
with open('/content/LawBot/datasets/ipc_qa.json', 'r', encoding='utf-8') as f:
    ipc_data = json.load(f)
```

Also update the output paths:
```python
# OLD:
save_jsonl(cleaned_data, '../data/processed/lawbot_cleaned.jsonl')

# NEW:
save_jsonl(cleaned_data, '/content/LawBot/data/processed/lawbot_cleaned.jsonl')
```

### 4. Quick Setup Script

**Create a setup cell at the start of Phase 1:**

```python
# Cell 1: Setup Environment
import os
import json

# Create directory structure
base_dir = '/content/LawBot'
dirs = [
    f'{base_dir}/datasets',
    f'{base_dir}/data/processed',
    f'{base_dir}/models/adapters',
    f'{base_dir}/vectorstore/faiss_index'
]

for dir_path in dirs:
    os.makedirs(dir_path, exist_ok=True)

print("Directory structure created!")
print(f"Upload your 3 JSON files to: {base_dir}/datasets/")

# Verify dataset files exist
required_files = ['constitution_qa.json', 'crpc_qa.json', 'ipc_qa.json']
print("\nChecking for dataset files:")
for file in required_files:
    file_path = f'{base_dir}/datasets/{file}'
    exists = os.path.exists(file_path)
    status = "✅ Found" if exists else "❌ Missing"
    print(f"{status}: {file}")
```

## Visual Guide

### Upload Files (Step 1)
```
Colab Interface:
├── 📁 File browser (left sidebar)
│   └── Content
│       └── LawBot (you'll create this)
│           └── datasets/
│               ├── Upload constitution_qa.json here
│               ├── Upload crpc_qa.json here
│               └── Upload ipc_qa.json here
```

### Run Phase 1 (Step 2)
```
Notebook → phase1_data_prep.ipynb
Run all cells → Creates:
├── /content/LawBot/data/processed/
│   ├── lawbot_cleaned.jsonl
│   ├── train.jsonl
│   └── val.jsonl
```

### Run Phase 2 (Step 3)
```
Notebook → phase2_finetune_lawbot.ipynb
Update paths to use /content/LawBot/
Runs training → Creates:
└── /content/LawBot/models/adapters/
    └── lawbot_qwen_adapter/
```

## Quick Reference: Path Mapping

| Local Path | Colab Path |
|------------|------------|
| `../Indian_Legal_Dataset.../constitution_qa.json` | `/content/LawBot/datasets/constitution_qa.json` |
| `../data/processed/train.jsonl` | `/content/LawBot/data/processed/train.jsonl` |
| `../models/adapters/` | `/content/LawBot/models/adapters/` |
| `../vectorstore/` | `/content/LawBot/vectorstore/` |

## Alternative: Use Your Actual Folder Structure

If you want to keep the local structure, upload:

```
/content/
└── Indian_Legal_Dataset_Lawbot_Assignment/
    └── Indian_Legal_Dataset_Lawbot_Assignment/
        ├── constitution_qa.json  ← Upload here
        ├── crpc_qa.json          ← Upload here
        └── ipc_qa.json           ← Upload here
```

Then use the original paths in notebooks (no changes needed).

## Recommendation

**Use the first approach** (`/content/LawBot/`) because:
- ✅ Cleaner structure
- ✅ Easier to manage
- ✅ Clear separation of notebooks and data
- ✅ Easier to download outputs later

## Pro Tips

1. **Verify upload:** Run the setup script to check files are in place
2. **Save outputs:** After each phase, download outputs as backup
3. **Use Drive:** Mount Drive and save important files there
4. **GPU RAM:** Free tier has ~15GB RAM - may need to reduce batch size

## Troubleshooting

**"File not found" error?**
- Check the exact path using: `os.listdir('/content/LawBot/datasets')`
- Verify filename spelling (case-sensitive!)

**"No module named X" error?**
- Run the pip install cells at the start of each notebook

**"CUDA out of memory" error?**
- Restart runtime: Runtime → Restart
- Reduce batch_size in training config
- Use smaller max_seq_length

## Quick Start Commands

```python
# Copy-paste this into Phase 1 as first cell:

import os
os.makedirs('/content/LawBot/datasets', exist_ok=True)

# Then upload files via UI to /content/LawBot/datasets/
# Then verify:
import os
files = os.listdir('/content/LawBot/datasets')
print("Uploaded files:", files)
```

That's it! Your files are ready. Now just update the paths in the notebooks and run them! 🚀

