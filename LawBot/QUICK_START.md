# LawBot Quick Start Guide

## 🚀 Running the Project - ZERO Setup Required!

### Step 1: Open Google Colab
1. Go to https://colab.research.google.com/
2. Sign in with your Google account

### Step 2: Upload Notebooks
1. Upload all 6 phase notebooks from the `notebooks/` folder
2. Upload the 3 dataset files from `Indian_Legal_Dataset_Lawbot_Assignment/Indian_Legal_Dataset_Lawbot_Assignment/`

### Step 3: Run Phase 1
1. Open `phase1_data_prep.ipynb`
2. Enable GPU if prompted (Runtime → Change runtime type → GPU)
3. Run all cells
4. Wait for dataset processing to complete

### Step 4: Run Phase 2
1. Open `phase2_finetune_lawbot.ipynb`
2. Run all cells
3. Training will take 1-2 hours (let it run!)
4. Adapter weights will be saved automatically

### Step 5: Run Phase 3
1. Open `phase3_rag_lawbot.ipynb`
2. Run all cells
3. FAISS index will be created (~30-60 mins)

### Step 6: Skip Phases 4 & 5 (Optional)
These are for advanced features - you can skip them if you want.

### Step 7: Run Phase 6
1. Open `phase6_gradio_app.ipynb`
2. Run all cells
3. Gradio will create a public link
4. Share the link to demo!

## That's it! ✅

No API keys, no environment variables, no configuration needed!

## What You DON'T Need

❌ Google Drive API keys  
❌ Client ID/Secret  
❌ HuggingFace token (public models work fine)  
❌ Pinecone account  
❌ OpenAI API  
❌ .env file  
❌ Any credentials!  

## What You DO Need

✅ Google Colab account (free)  
✅ GPU runtime (free tier works)  
✅ Internet connection  
✅ That's literally it!  

## Common Questions

**Q: Do I need Google Drive?**  
A: No! Everything runs locally in Colab.

**Q: Do I need API keys?**  
A: No! All models are public.

**Q: Do I need to configure anything?**  
A: No! Just run the notebooks.

**Q: What if I want to save outputs to Drive?**  
A: Optional! Just mount drive in the notebook with `drive.mount('/content/drive')`

**Q: The credentials.json file - do I need it?**  
A: No! Not needed for this project. Only if you want programmatic Google Drive access.

## Troubleshooting

**Issue:** "CUDA out of memory"  
**Fix:** Use smaller batch size in Phase 2, or reduce sequence length

**Issue:** "Module not found"  
**Fix:** Run the pip install cell in the notebook

**Issue:** "File not found"  
**Fix:** Make sure dataset files are in the correct location

**Issue:** Training takes forever  
**Fix:** That's normal! Phase 2 takes 1-2 hours minimum

## Project Status

✅ All 6 phase notebooks ready  
✅ No configuration needed  
✅ Works in Google Colab  
✅ Free GPU tier sufficient  
✅ Complete architecture documentation  
✅ Setup guide included  

**You're ready to start!** Just open Colab and run Phase 1! 🎉

