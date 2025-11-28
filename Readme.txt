# On_Demand_Professor-Q-A-Bot

A context-aware, AI-powered chatbot designed to provide accurate answers to academic queries by leveraging local LLMs, vector search, and document embeddings. This bot integrates lecture notes, PDFs, and course materials to deliver precise and private, on-demand answers.

---

## 📚 Project Overview

This project enables:

- Uploading and organizing lecture notes or knowledge documents  
- Converting documents into embeddings using SentenceTransformers  
- Storing embeddings in Qdrant Vector Database  
- Using GPT4All (local LLM) to generate accurate answers  
- Querying through an interactive Gradio-based web interface  

Built for academic use-cases such as professor Q&A bots, teaching assistants, course support systems, and private document-based question answering.

---

## 🐳 Qdrant Setup Using Docker

### 1. Install Docker Desktop  
Ensure Docker is installed and running.

### 2. Start Qdrant Vector Database  
Run the following commands:

```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant
```

Qdrant UI/API will be available at:
```
http://localhost:6333
```

---

## 📦 Required Python Packages

Install these libraries:

- **sentence-transformers** → Convert text to embeddings  
- **qdrant-client** → Connect to Qdrant DB  
- **gradio** → Chatbot UI  
- **gpt4all** → Local LLM for answering questions  
- **pymupdf (fitz)** → PDF → text conversion  

### Install all dependencies:
```bash
pip install sentence-transformers qdrant-client gradio gpt4all pymupdf
```

---

## 📂 Repository Structure

```
On_Demand_Professor-Q-A-Bot/
│
├── knowledge_base/              # All documents (PDFs, notes) to index
├── Scripts/
│   ├── initialise_qdrant.py     # Creates Qdrant collection
│   ├── Data_insertion_qdrant.py # Loads+indexes documents
│   └── Chatbot_application.py   # Runs chatbot UI + retrieval
├── query_logs.txt
└── README.md
```

---

## ⚙️ How to Run the System

### ▶️ Step 1 — Initialize Qdrant Collection
```bash
python Scripts/initialise_qdrant.py
```

### ▶️ Step 2 — Add Your Documents
Place PDFs inside:
```
knowledge_base/
```

Edit `pdf_path` in `Data_insertion_qdrant.py` if needed.

### ▶️ Step 3 — Index Documents into Qdrant
```bash
python Scripts/Data_insertion_qdrant.py
```

This will:
- Extract text from PDFs
- Generate embeddings (SentenceTransformers)
- Insert each page into Qdrant with metadata

### ▶️ Step 4 — Launch Chatbot Web App
```bash
python Scripts/Chatbot_application.py
```

Visit:
```
http://localhost:7860
```

---

## 🎯 Features

- Fully local pipeline (no cloud dependency)
- Vector-based similarity search for accurate retrieval
- Privacy-preserving document handling
- Modular & extendable
- User-friendly Gradio UI
- Supports PDF materials used in university courses

---

## 🚀 Future Enhancements

- Real-time PDF upload from UI  
- Support for DOCX, PPT, and textbook formats  
- Integration with more LLMs (LLaMA, Mistral, Gemma, etc.)  
- Chat memory & multi-turn context  
- Authentication for multi-user access  

---

## 👨‍💻 Author
**Vamsi Krishna**

GitHub: https://github.com/Vamsi-Krishna63

---

Feel free to contribute or suggest improvements!
