# AI Recruiter Assistant

A simple and professional AI-based recruiter tool that indexes candidate CVs and retrieves the most relevant matches based on required skills.

This system uses:

- Local embeddings (SentenceTransformers)
- Qdrant vector database (local persistent storage)
- Semantic similarity search

No external APIs required.

---

## 🚀 Features

- Parse CVs (PDF format)
- Convert CV text into embeddings
- Store embeddings in a local vector database
- Search CVs using natural language skill queries
- Return matching CV IDs sorted by relevance
- Persistent storage (no re-indexing required every run)

---

## 🧠 Architecture
              
<img width="3150" height="367" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/663d0dc5-a844-4426-8e11-aa1cf0ab43b3" />

---

## 📁 Project Structure

ai_recruiter/
│
├── data/ # Store CV PDFs here
├── storage/ # Local vector database (auto-created)
├── src/
│ ├── config.py
│ ├── extract.py
│ ├── embed.py
│ ├── indexer.py
│ └── search.py
│
├── main.py
├── requirements.txt
└── README.md



---

## ⚙️ Installation

### 1️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate


pip install -r requirements.txt

📥 Add CV Files
data/

🗂 Index CVs (Run Once)
python main.py --index
This will:

Extract text from CVs

Generate embeddings

Store vectors in local database (storage/)

🔎 Search for Candidates
python main.py --search
