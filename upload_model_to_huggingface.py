"""
Upload LawBot Fine-Tuned Model to HuggingFace Hub
Run this to upload your model and reduce submission size
"""

import os
from pathlib import Path

print("="*70)
print("📤 LawBot Model Upload to HuggingFace")
print("="*70)

# Configuration
HF_USERNAME = input("\n🔑 Enter your HuggingFace username: ").strip()
HF_TOKEN = input("🔑 Enter your HuggingFace token (starts with 'hf_'): ").strip()

MODEL_NAME = "lawbot-qwen-2.5-1.5b-lora"
MODEL_PATH = Path("LawBot_FullStack/models/adapters/lawbot_qwen_adapter")

# Alternative path if running from LawBot_FullStack
if not MODEL_PATH.exists():
    MODEL_PATH = Path("models/adapters/lawbot_qwen_adapter")

if not MODEL_PATH.exists():
    print(f"\n❌ Model not found at: {MODEL_PATH}")
    print("   Make sure you're running from the project root")
    exit(1)

print(f"\n📁 Model path: {MODEL_PATH}")
print(f"📦 Repository: {HF_USERNAME}/{MODEL_NAME}")

# Check files
files = list(MODEL_PATH.glob("*"))
print(f"\n📋 Files to upload ({len(files)}):")
for f in files:
    size_mb = f.stat().st_size / (1024*1024)
    print(f"   • {f.name} ({size_mb:.2f} MB)")

# Confirm
print("\n" + "="*70)
confirm = input("Continue with upload? (yes/no): ").strip().lower()
if confirm not in ['yes', 'y']:
    print("❌ Upload cancelled")
    exit(0)

# Install huggingface_hub if needed
print("\n📦 Checking dependencies...")
try:
    from huggingface_hub import HfApi, create_repo, login
    print("✅ huggingface_hub installed")
except ImportError:
    print("⚠️  Installing huggingface_hub...")
    import subprocess
    subprocess.check_call(["pip", "install", "huggingface-hub"])
    from huggingface_hub import HfApi, create_repo, login
    print("✅ huggingface_hub installed")

# Login
print("\n🔐 Logging in to HuggingFace...")
try:
    login(token=HF_TOKEN)
    print("✅ Logged in successfully")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit(1)

# Create repository
repo_id = f"{HF_USERNAME}/{MODEL_NAME}"
print(f"\n📝 Creating repository: {repo_id}")

try:
    repo_url = create_repo(
        repo_id=repo_id,
        token=HF_TOKEN,
        private=False,  # Set to True if you want private repo
        repo_type="model",
        exist_ok=True
    )
    print(f"✅ Repository ready: {repo_url}")
except Exception as e:
    print(f"⚠️  Repository might already exist: {e}")
    print(f"   Continuing with upload...")

# Create README for the model
readme_content = f"""---
license: apache-2.0
base_model: Qwen/Qwen2.5-1.5B-Instruct
tags:
  - legal
  - indian-law
  - qlora
  - peft
  - lora
language:
  - en
pipeline_tag: text-generation
---

# LawBot: Fine-Tuned Qwen2.5-1.5B for Indian Legal Q&A

This model is a fine-tuned version of [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) using LoRA adapters.

## Model Description

LawBot is an intelligent legal question-answering assistant specialized in Indian law (IPC, CrPC, and Constitution).

- **Base Model:** Qwen/Qwen2.5-1.5B-Instruct
- **Fine-tuning Method:** QLoRA (4-bit quantization + LoRA)
- **Training Data:** 14,522 Indian legal Q&A pairs
- **Domains:** Indian Penal Code, Criminal Procedure Code, Constitution of India

## Training Details

### Training Data
- Sources: IPC, CrPC, Constitution Q&A datasets
- Training samples: 11,617
- Validation samples: 2,905
- Format: Instruction-following (input-output pairs)

### Training Procedure
- **Method:** QLoRA via Unsloth
- **LoRA Rank:** 16
- **LoRA Alpha:** 16
- **Batch Size:** 2 (effective: 8 with gradient accumulation)
- **Learning Rate:** 2e-4
- **Epochs:** 3
- **Hardware:** Google Colab T4 GPU
- **Training Time:** ~2-3 hours

### LoRA Configuration
- Target modules: q_proj, k_proj, v_proj, o_proj
- Dropout: 0.05
- Quantization: 4-bit

## Usage

### Loading the Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-1.5B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapters
model = PeftModel.from_pretrained(
    base_model,
    "{repo_id}"
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
```

### Inference Example

```python
prompt = \"\"\"<|im_start|>system
You are a legal assistant specializing in Indian law.
<|im_end|>
<|im_start|>user
What is IPC Section 302?
<|im_end|>
<|im_start|>assistant
\"\"\"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.7)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

## Intended Use

This model is designed for:
- Educational purposes in legal studies
- Legal information retrieval
- Research on Indian law
- Building legal AI assistants

## Limitations

- **Not a substitute for professional legal advice**
- Dataset covers common legal topics but not exhaustive
- May not reflect most recent legal amendments
- Responses should be verified by qualified legal professionals

## Ethical Considerations

- This model is for educational and informational purposes only
- Users should not rely solely on this model for legal decisions
- Always consult qualified legal professionals for legal matters
- Be aware of potential biases in training data

## Citation

If you use this model, please cite:

```bibtex
@misc{{lawbot-2025,
  author = {{{HF_USERNAME}}},
  title = {{LawBot: Fine-Tuned Qwen2.5-1.5B for Indian Legal Q&A}},
  year = {{2025}},
  publisher = {{HuggingFace}},
  url = {{https://huggingface.co/{repo_id}}}
}}
```

## Model Card Contact

For questions or feedback, please open an issue on the [GitHub repository](https://github.com/{HF_USERNAME}/lawbot) or contact via HuggingFace.

## License

Apache 2.0 (following base model license)

## Acknowledgments

- Base model: Qwen Team (Alibaba Cloud)
- Fine-tuning framework: Unsloth
- Training platform: Google Colab
"""

# Save README temporarily
readme_path = MODEL_PATH / "README.md"
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme_content)
print("✅ Created README.md")

# Upload
print(f"\n📤 Uploading to HuggingFace...")
print(f"   This may take 2-5 minutes depending on connection...")

try:
    api = HfApi()
    api.upload_folder(
        folder_path=str(MODEL_PATH),
        repo_id=repo_id,
        token=HF_TOKEN,
        commit_message="Upload LawBot fine-tuned model"
    )
    
    print("\n" + "="*70)
    print("✅ UPLOAD SUCCESSFUL!")
    print("="*70)
    print(f"\n🎉 Your model is now available at:")
    print(f"   https://huggingface.co/{repo_id}")
    print(f"\n📝 Next steps:")
    print(f"   1. Update SUBMISSION_README.md with model URL")
    print(f"   2. Update full_inference.py to use: {repo_id}")
    print(f"   3. Remove models/adapters/ from submission ZIP")
    print(f"   4. Test download: python full_inference.py")
    print("\n" + "="*70)

except Exception as e:
    print(f"\n❌ Upload failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Clean up
if readme_path.exists():
    readme_path.unlink()

