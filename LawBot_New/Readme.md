SRM INSTITUTE OF SCIENCE AND TECHNOLOGY
21CSE658T LARGE LANGUAGE MODELS

LIFE LONG LEARNING ASSESSMENT - LLT

Program Offered: M. Tech 					                                Max. Marks: 30
						                       


Assignment Title: "LawBot: Building an Intelligent Legal Q&A Assistant using Fine-Tuning, RAG, and Reinforcement Learning"

OBJECTIVE: 

Students will build a domain-specific legal question-answering assistant (“LawBot”) that can:
1. Learn legal terminology and reasoning via fine-tuning.
2. Retrieve law-specific context using RAG (Retrieval-Augmented Generation).
3. Improve factual accuracy and tone using Reinforcement Learning (RLHF/GRPO).
4. Integrate external legal or judiciary APIs for live lookups.


DATASET: Indian Legal Q&A Dataset

Source Files:
❖	constitution_qa.json
❖	crpc_qa.json
❖	ipc_qa.json

Description:
➢	Combined dataset of Indian Penal Code (IPC), Criminal Procedure Code (CrPC), and Constitution of India Q&A pairs.
➢	Each record contains: {"instruction": "Question", "output": "Answer", "source": "IPC/CrPC/Constitution"}


PROJECT PHASES


Phase 1: Dataset Preparation (IPC/CrPC/Constitution)
➔	Load and merge constitution_qa.json, crpc_qa.json, and ipc_qa.json.
➔	Normalize to instruction format: {"instruction": <question>, "output": <answer>, "source": ["IPC" | "CrPC" | "Constitution"]}.
➔	Clean and deduplicate; retain section references where available (e.g., IPC Sections 60–81).
➔	Split 80:20 into train/validation sets.

Deliverable: lawbot_cleaned.jsonl + short preprocessing report


Phase 2: Fine-Tuning
➔	Use Qwen2.5-1.5B, Mistral-7B, Phi-3-mini, or any other LLM of your choice with LoRA/QLoRA fine-tuning.
➔	Frameworks: Unsloth or Hugging Face PEFT.
➔	Evaluate the tuned model performance with the appropriate metric.

Deliverable: finetune_lawbot.ipynb + adapter weights + evaluation results


Phase 3: RAG with History-Aware Retrieval
➔	Collect open Indian legal texts (Bare Acts, Case Summaries, Court Judgments, or Govt PDFs).
➔	Convert documents to plain text and split into semantic chunks (~600–1000 tokens with overlap).
➔	Embed chunks using a sentence-transformer model (e.g., all-MiniLM-L6-v2 or legal domain embeddings).
➔	Store vectors in FAISS / Chroma / Pinecone index using LangChain or LlamaIndex.
➔	Retrieve the most relevant chunks based on user query + conversation history for context-aware answers.
➔	Generate grounded responses with section citations; abstain if evidence is insufficient.

Deliverable: rag_lawbot.ipynb + screenshots showing chunking, retrieval, and grounded answers


Phase 4: RLHF / GRPO Fine-Tuning (OPTIONAL)
➔	Collect ~30 examples of good vs bad responses (accuracy, clarity, citation correctness).
➔	Train a reward model using TRL (Hugging Face) or Unsloth GRPOTrainer.
➔	Compare pre- and post-RLHF model performance.

Deliverable: reward_model_lawbot.ipynb


Phase 5: Tool Calling Integration (OPTIONAL)
➔	Integrate APIs or tools for legal reference:
◆	Indian Kanoon / Court Listener for case lookup
◆	Legal dictionary for term explanations
◆	Date calculator for limitation or filing deadlines

Deliverable: lawbot_agent.ipynb / app.py with screenshots of tool calls


Phase 6: Final Report + Demo
➔	Deploy using Streamlit or Gradio.
➔	Include chat UI, retrieved citations, tool traces, and disclaimers (“LawBot is for educational use only”).

Deliverables:
●	app.py / gradio_app.ipynb
●	Demo video / screenshots
●	4–5 page project report


LEARNING OUTCOMES

❖	Understand fine-tuning of LLMs on legal domain text.
❖	Apply RAG for grounded, explainable legal responses.
❖	Use reinforcement learning to improve factual accuracy.
❖	Integrate real-time tools for dynamic data retrieval.
❖	Build an ethical and transparent AI assistant for Indian law.

