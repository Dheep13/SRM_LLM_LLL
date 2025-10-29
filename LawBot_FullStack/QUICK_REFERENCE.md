# LawBot Quick Reference Card

## 🚀 Start LawBot (One Command)

```bash
cd LawBot_FullStack
python run_inference.py
```

**What happens:**
1. Checks dependencies ✓
2. Verifies model ✓
3. Creates vectorstore (if needed) ✓
4. Launches Gradio at http://localhost:7860 ✓

---

## 📝 Manual Commands

### Install Dependencies
```bash
pip install -r requirements-minimal.txt
```

### Create Vectorstore Only
```bash
python scripts/create_vectorstore_simple.py
```

### Launch Gradio Only
```bash
python run_gradio.py
```

---

## 🧪 Test Queries

```
"What is IPC Section 302?"
"How do I file a criminal complaint?"
"What is the procedure for bail?"
"Explain arrest under CrPC"
"What are fundamental rights?"
```

---

## 📊 What You Get

| Component | Status | Location |
|-----------|--------|----------|
| Fine-tuned Model | ✅ | `models/adapters/lawbot_qwen_adapter/` |
| Vectorstore | ✅ | `data/vectorstore/faiss_index/` |
| Legal Tools | ✅ | Built-in dictionary, calculator |
| Gradio UI | ✅ | http://localhost:7860 |

---

## 🔧 Troubleshooting

### Torch Error?
```bash
pip uninstall torchvision -y
pip install torch<2.5.0
```

### Vectorstore Missing?
```bash
python scripts/create_vectorstore_simple.py
```

### Model Not Found?
- Base model will be used automatically
- Ensure adapters in `models/adapters/lawbot_qwen_adapter/`

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `run_inference.py` | One-command startup |
| `run_gradio.py` | Gradio interface |
| `scripts/create_vectorstore_simple.py` | Create FAISS index |
| `requirements-minimal.txt` | Dependencies |
| `INFERENCE_GUIDE.md` | Detailed guide |

---

## ⏱️ Time Required

- **First Run**: 5-10 min (creates vectorstore)
- **Later Runs**: <30 sec
- **Per Query**: 1-5 sec

---

## ✅ Checklist for Testing

- [ ] Run `python run_inference.py`
- [ ] Wait for http://localhost:7860 to open
- [ ] Test with example questions
- [ ] Verify RAG citations appear
- [ ] Check tool usage displays
- [ ] Take screenshots
- [ ] Record demo video

---

## 🎯 Assignment Deliverables

1. ✅ Notebooks (Phases 1-6 completed)
2. ✅ Fine-tuned model (in `models/adapters/`)
3. ✅ Vectorstore (in `data/vectorstore/`)
4. ✅ Inference system (Gradio working)
5. ✅ Screenshots (capture UI)
6. ✅ Report (document observations)

---

## 💡 Pro Tips

- Use example questions for quick testing
- Check "System Status" in Gradio UI
- RAG citations prove retrieval works
- Tool usage shows dictionary integration
- Conversation history tests context handling

---

## 🆘 Need Help?

See `INFERENCE_GUIDE.md` for detailed instructions
See `IMPLEMENTATION_COMPLETE.md` for architecture
See `QUICK_START.md` for deployment options

---

**Ready to test your LawBot! 🎉**

