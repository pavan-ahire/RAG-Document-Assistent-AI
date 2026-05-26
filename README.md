# 📚 Multi-Document RAG AI Assistant

<div align="center">

### 🚀 Production-Grade Generative AI RAG Application

Semantic PDF Question Answering using  
LangChain • Groq • ChromaDB • Streamlit • HuggingFace

</div>

---

# ✨ Features

✅ Multi-PDF Upload  
✅ Advanced RAG Pipeline  
✅ Semantic Search  
✅ Conversational Memory  
✅ MMR Retrieval  
✅ Grounded AI Responses  
✅ Hallucination Reduction  
✅ Source Citations  
✅ Persistent ChromaDB  
✅ Groq Llama 3.1 Integration  
✅ Professional Streamlit UI  
✅ PDF Chat Export  
✅ Modern AI Chat Experience  

---

# 🧠 Tech Stack

| Technology | Purpose |
|---|---|
| Streamlit | Frontend UI |
| LangChain | RAG Framework |
| Groq API | LLM Inference |
| ChromaDB | Vector Database |
| HuggingFace Embeddings | Semantic Embeddings |
| PyMuPDF | PDF Extraction |
| Python | Backend Logic |

---

# 🏗️ Architecture

```text
PDF Upload
    ↓
PyMuPDF Extraction
    ↓
Text Chunking
    ↓
HuggingFace Embeddings
    ↓
ChromaDB Vector Storage
    ↓
MMR Semantic Retrieval
    ↓
Groq Llama 3.1 Response Generation
    ↓
Grounded AI Answer
```

---

# 📂 Project Structure

```bash
rag-document-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── chroma_db/
│
├── data/
│   └── uploads/
│
├── src/
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── retriever.py
│   ├── llm.py
│   ├── rag_chain.py
│   ├── memory.py
│   └── utils.py
```

---

# ⚡ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/rag-document-assistant.git
```

```bash
cd rag-document-assistant
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Setup Groq API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Get API key from:

👉 https://console.groq.com/

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 📄 Supported Features

| Feature | Supported |
|---|---|
| Multi PDF Upload | ✅ |
| Conversational Memory | ✅ |
| Semantic Search | ✅ |
| Persistent Vector DB | ✅ |
| Source Citations | ✅ |
| PDF Chat Export | ✅ |
| Grounded Responses | ✅ |
| Modern Chat UI | ✅ |

---

# 🔍 RAG Pipeline Details

## 📌 PDF Extraction

Uses:

```python
PyMuPDFLoader
```

Provides better extraction quality for:
- research papers
- structured PDFs
- tables
- reports

---

## 📌 Chunking Strategy

```python
chunk_size = 500
chunk_overlap = 100
```

Using:

```python
RecursiveCharacterTextSplitter
```

Improves:
- semantic retrieval
- context understanding
- answer grounding

---

## 📌 Embedding Model

```python
BAAI/bge-base-en-v1.5
```

Benefits:
- better semantic similarity
- improved retrieval quality
- high contextual understanding

---

## 📌 Retrieval Strategy

Using:

```python
MMR Retrieval
```

Benefits:
- diverse retrieval
- reduced duplicate chunks
- better context coverage

---

# 💬 Example Questions

### Ask Questions Like:

- What are the advantages of FastAPI?
- Which validation library is used?
- Explain dependency injection.
- Summarize the uploaded report.
- What are the key concepts discussed?

---

# 🛡️ Hallucination Reduction

The system uses a custom grounded RAG prompt:

✅ Answers ONLY from uploaded documents  
✅ Avoids outside knowledge  
✅ Reduces hallucinations  
✅ Provides source-aware responses  

If answer is not found:

```text
"I could not find the answer in the uploaded documents."
```

---

# 📸 Screenshots

<img width="1919" height="704" alt="image" src="https://github.com/user-attachments/assets/9dc83f94-fbe7-43e9-a763-e212a9c5c064" />

<img width="336" height="827" alt="image" src="https://github.com/user-attachments/assets/7b344898-bebf-4536-ad50-3b4a87e2d2bf" />


---

# 📦 Requirements

```txt
streamlit
langchain==0.1.20
langchain-community==0.0.38
langchain-groq
langchain-huggingface
langchain-text-splitters
chromadb
sentence-transformers
pymupdf
pypdf
python-dotenv
pandas
reportlab
```

---

# 🚀 Future Improvements

- Hybrid Search
- Reranking
- OCR Support
- Streaming Responses
- Docker Deployment
- Authentication System
- Cloud Deployment
- GPU Acceleration

---

# 👨‍💻 Author

### Pavan Ahire

Generative AI • Machine Learning • RAG Systems • Python Development

---

# ⭐ If You Like This Project

Give this repository a ⭐ on GitHub.

---

# 📜 License

This project is licensed under the MIT License.
