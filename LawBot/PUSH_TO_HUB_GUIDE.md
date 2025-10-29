# How to Push Your Fine-Tuned Model to Hugging Face Hub

## After Saving Locally

After you run:
```python
model.save_pretrained(f"{base_dir}/models/adapters/lawbot_qwen_adapter")
tokenizer.save_pretrained(f"{base_dir}/models/adapters/lawbot_qwen_adapter")
print("✅ Adapter weights saved locally to Drive!")
```

## Step 1: Add Cell to Push to HF Hub

Add this as a new cell after the save cell:

```python
# OPTIONAL: Push to Hugging Face Hub for permanent storage
from huggingface_hub import login

# Login to HF (will ask for token the first time)
login()  # Or use: login(token="your_hf_token")

# Push adapter to your HF Hub
model.push_to_hub("your-username/lawbot-qwen-1.5b-adapter")
tokenizer.push_to_hub("your-username/lawbot-qwen-1.5b-adapter")

print("✅ Pushed to Hugging Face Hub!")
print("Model available at: https://huggingface.co/your-username/lawbot-qwen-1.5b-adapter")
```

## Step 2: Get Your Hugging Face Token

1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it: "Colab LawBot"
4. Select: "Write" permissions
5. Copy the token

## Step 3: Login

**Option A: Interactive (Easiest)**
```python
from huggingface_hub import login
login()
```
A link will appear - click it, authorize, and paste the token.

**Option B: Direct Token**
```python
from huggingface_hub import login
login(token="hf_your_token_here")
```

**Option C: Environment Variable**
```python
import os
os.environ["HF_TOKEN"] = "hf_your_token_here"
```

## Step 4: Create Your Model Name

Choose a name like:
- `your-username/lawbot-qwen-1.5b-adapter`
- `your-username/lawbot-ipc-crpc-constitution`
- `your-username/indian-legal-assistant`

Replace `your-username` with your HF username!

## Step 5: Push

```python
# Create the repository on HF Hub
model.push_to_hub("your-username/lawbot-qwen-1.5b-adapter", private=False)

# Push tokenizer too
tokenizer.push_to_hub("your-username/lawbot-qwen-1.5b-adapter")

print("✅ Upload complete!")
```

## Benefits of Pushing to HF Hub

✅ **Permanent storage** - Won't lose your model!  
✅ **Easy sharing** - Share link with others  
✅ **Use anywhere** - Load from any Colab session  
✅ **Version control** - Keep track of improvements  
✅ **Free** - HF Hub is free to use  

## Loading from HF Hub Later

Once pushed, you can load it anywhere:

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="your-username/lawbot-qwen-1.5b-adapter",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

print("✅ Model loaded from HF Hub!")
```

## Alternative: Just Keep in Drive

**If you don't want to push to HF Hub:**

Your model is already saved in:
```
/content/drive/MyDrive/LawBot/models/adapters/lawbot_qwen_adapter/
```

This is **permanent** too! It's in your Google Drive, so it won't disappear.

**Pros of Drive:**
- ✅ Already there
- ✅ No extra steps
- ✅ Private by default
- ✅ Easy to download

**Pros of HF Hub:**
- ✅ Shareable link
- ✅ Can load from anywhere
- ✅ Better for collaboration
- ✅ Version history

## My Recommendation

**For your assignment:**
1. Model is already saved in Drive ✅
2. That's sufficient for submission ✅
3. Optional: Push to HF Hub if you want to show it off

**The Drive location is permanent and accessible anytime!**

## Quick Decision

- Just want to submit? → Your model in Drive is enough! ✅
- Want to show it off? → Push to HF Hub
- Planning to reuse? → HF Hub is better for accessibility

**Bottom line:** Your model is already safely saved in Drive. The HF Hub push is optional but nice to have!

