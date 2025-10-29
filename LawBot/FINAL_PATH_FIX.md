# Final Path Fixes Needed

## Phase 2: Two More Paths to Fix

In `phase2_finetune_lawbot.ipynb`, change these two lines:

### Line 1: Output Directory (Cell 6)
```python
# OLD:
output_dir="../models/adapters",

# NEW:
output_dir=f"{base_dir}/models/adapters",
```

### Line 2: Evaluation Results (Cell 12)
```python
# OLD:
with open('../data/processed/evaluation_results.json', 'w') as f:

# NEW:
with open(f'{base_dir}/data/processed/evaluation_results.json', 'w') as f:
```

## All Notebooks Summary

✅ **Phase 1**: All paths use `f'{base_dir}/...'` - COMPLETE!

✅ **Phase 2**: 
- Cell 1: Mounts Drive ✅
- Cell 3: Load data paths ✅
- Cell 10: Save model paths ✅
- Needs: Cell 6 output_dir ✅
- Needs: Cell 12 eval results ✅

✅ **Phase 3**: Mounts Drive ✅

## Pattern to Follow

**All notebooks should use:**
```python
base_dir = '/content/drive/MyDrive/LawBot'
```

**For all file operations:**
- ✅ `f'{base_dir}/data/processed/train.jsonl'`
- ✅ `f'{base_dir}/models/adapters/...'`
- ✅ `f'{base_dir}/vectorstore/...'`

**Never use:**
- ❌ `'../data/...'`
- ❌ `'../models/...'`

## Quick Fix

In Phase 2 Colab notebook, find these two lines:
1. `output_dir="../models/adapters"` → Change to `output_dir=f"{base_dir}/models/adapters"`
2. `with open('../data/processed/evaluation_results.json'` → Change to `with open(f'{base_dir}/data/processed/evaluation_results.json'`

That's it! All notebooks will be in sync!

