# 📤 Upload Fine-Tuned Model to HuggingFace

## Why Upload to HuggingFace?

✅ Reduce submission size (3GB → 50MB)  
✅ Easy sharing and reproducibility  
✅ Industry-standard practice  
✅ Permanent cloud storage  

---

## 🚀 Quick Upload Guide

### **Step 1: Create HuggingFace Account**

1. Go to https://huggingface.co/
2. Sign up (free account)
3. Verify your email

### **Step 2: Get Access Token**

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `lawbot-upload`
4. Type: Write
5. Copy the token (starts with `hf_...`)

### **Step 3: Install HuggingFace Hub**

```powershell
pip install huggingface-hub
```

### **Step 4: Upload Your Model**

Create a simple upload script:

```python
# upload_to_hf.py
from huggingface_hub import HfApi, create_repo
import os

# Your info
HF_USERNAME = "your_username"  # Replace with your HF username
MODEL_NAME = "lawbot-qwen-2.5-1.5b-lora"
HF_TOKEN = "hf_xxxxxxxxxxxxx"  # Replace with your token

# Paths
MODEL_PATH = "LawBot_FullStack/models/adapters/lawbot_qwen_adapter"

# Create repo
repo_id = f"{HF_USERNAME}/{MODEL_NAME}"
print(f"Creating repo: {repo_id}")

try:
    create_repo(
        repo_id=repo_id,
        token=HF_TOKEN,
        private=False,  # Make public or private
        repo_type="model"
    )
    print("✅ Repo created!")
except Exception as e:
    print(f"⚠️  Repo might already exist: {e}")

# Upload files
api = HfApi()
print(f"\nUploading model from: {MODEL_PATH}")

api.upload_folder(
    folder_path=MODEL_PATH,
    repo_id=repo_id,
    token=HF_TOKEN,
)

print(f"\n✅ Upload complete!")
print(f"🔗 Model URL: https://huggingface.co/{repo_id}")
```

Run it:
```powershell
python upload_to_hf.py
```

---

## 📝 Alternative: Manual Upload

1. Go to https://huggingface.co/new
2. Create new model repository
3. Name it: `lawbot-qwen-2.5-1.5b-lora`
4. Upload files manually from `models/adapters/lawbot_qwen_adapter/`:
   - `adapter_config.json`
   - `adapter_model.safetensors`
   - All tokenizer files

---

## 🔗 After Upload: Update Documentation

Once uploaded, your model URL will be:
```
https://huggingface.co/YOUR_USERNAME/lawbot-qwen-2.5-1.5b-lora
```

### **Update These Files:**

**1. SUBMISSION_README.md**

Add section:
```markdown
## 🤗 HuggingFace Model

Fine-tuned model adapters available at:
**https://huggingface.co/YOUR_USERNAME/lawbot-qwen-2.5-1.5b-lora**

To use:
```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = PeftModel.from_pretrained(
    base_model, 
    "YOUR_USERNAME/lawbot-qwen-2.5-1.5b-lora"
)
```
```

**2. full_inference.py**

Update model path:
```python
# Option 1: Load from local (if model included)
# MODEL_PATH = BASE_DIR / "models" / "adapters" / "lawbot_qwen_adapter"

# Option 2: Load from HuggingFace (recommended for submission)
MODEL_PATH = "YOUR_USERNAME/lawbot-qwen-2.5-1.5b-lora"
```

**3. README_COMPLETE.md**

Add note:
```markdown
### Model Weights

The fine-tuned LoRA adapters are hosted on HuggingFace:
🔗 https://huggingface.co/YOUR_USERNAME/lawbot-qwen-2.5-1.5b-lora

The model will be automatically downloaded when running `full_inference.py`.
```

---

## 📦 Updated Submission Package

### **What to Include:**

```
80_LLL_LLM/
├── LawBot_New/
│   ├── notebooks/                      ✅ Include (6 notebooks)
│   ├── data/processed/                 ✅ Include (train/val data)
│   └── models/adapters/                ❌ EXCLUDE (on HuggingFace)
│
├── LawBot_FullStack/
│   ├── *.py                           ✅ Include (all scripts)
│   ├── data/
│   │   ├── processed/                 ✅ Include
│   │   └── vectorstore/               ✅ Include (FAISS index)
│   ├── models/adapters/               ❌ EXCLUDE (on HuggingFace)
│   └── *.md                           ✅ Include (all docs)
│
├── Indian_Legal_Dataset_Lawbot_Assignment/ ✅ Include
├── SUBMISSION_README.md               ✅ Include
├── MODEL_DOWNLOAD_INSTRUCTIONS.md     ✅ NEW - Create this
└── LawBot_Project_Report.pdf          ✅ Include
```

### **Size Comparison:**

| Item | With Model | Without Model |
|------|------------|---------------|
| Model adapters | ~3GB | 0 |
| Vector store | ~22MB | ~22MB |
| Notebooks | ~5MB | ~5MB |
| Scripts | ~1MB | ~1MB |
| Data | ~50MB | ~50MB |
| **Total** | **~3.1GB** | **~80MB** ✅ |

---

## 📄 Create Model Download Instructions

For evaluators who want to run your code:

```markdown
# 🤗 Model Download Instructions

## Automatic Download (Recommended)

The fine-tuned model will be automatically downloaded when you run:
```powershell
python full_inference.py
```

It will download from HuggingFace on first run.

## Manual Download (Optional)

If automatic download fails:

1. Visit: https://huggingface.co/YOUR_USERNAME/lawbot-qwen-2.5-1.5b-lora
2. Click "Files and versions"
3. Download all files
4. Place in: `LawBot_FullStack/models/adapters/lawbot_qwen_adapter/`

## Verify Download

```powershell
python check_status.py
```

Should show: ✅ Fine-tuned Model
```

---

## ✅ Benefits of This Approach

### **For You:**
- Smaller ZIP file (uploads faster)
- Easier to email/share
- Professional presentation
- Cloud backup of model

### **For Evaluators:**
- Faster download
- Easy to reproduce
- Can test without downloading model first
- Model automatically fetched when needed

### **For Portfolio:**
- Shows industry best practices
- Demonstrates HuggingFace usage
- Easy to showcase in resume
- Public model for demonstrations

---

## 🎯 Recommended Submission Structure

### **Include in ZIP:**
1. ✅ All notebooks (training evidence)
2. ✅ All scripts (inference code)
3. ✅ Vector store (RAG database)
4. ✅ Training/val data (processed datasets)
5. ✅ All documentation
6. ✅ PDF report
7. ❌ Model adapters (on HuggingFace instead)

### **Provide Separately:**
- HuggingFace model link in README
- Instructions for automatic download
- Note: "Model automatically downloaded on first run"

---

## 📝 Update Submission Checklist

Before zipping:

□ Model uploaded to HuggingFace
□ Model URL added to SUBMISSION_README.md
□ MODEL_DOWNLOAD_INSTRUCTIONS.md created
□ full_inference.py updated with HF model path
□ `models/adapters/` folder removed from submission
□ PDF report mentions HuggingFace hosting
□ Test that automatic download works
□ Verify final ZIP size (~80-100MB)

---

## 💡 Pro Tip

In your PDF report, mention:

```
"The fine-tuned model adapters are hosted on HuggingFace Hub 
for easy reproducibility and reduced submission size. This 
demonstrates industry-standard practices for model distribution 
and allows evaluators to test the system without downloading 
large model files upfront."
```

This shows professionalism and understanding of deployment practices!

---

## 🎉 Final Submission Size

**With this approach:**
- ZIP file: ~80-100MB
- Easy to upload/email
- Professional structure
- Fully reproducible

**Model accessible at:**
- HuggingFace: Permanent cloud storage
- Automatically downloaded when needed
- Public for portfolio/resume

---

**Want me to create the upload script for you?** 🚀

