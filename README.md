
# 📚 DocuMind AI

A simple RAG-based PDF Question Answering application that allows users to upload PDF documents and ask questions about their content using Generative AI.

## 🚀 Live Demo

- **Frontend:** [Streamlit App](https://your-app-name.streamlit.app)
- **Backend API:** [FastAPI](https://your-backend-url.onrender.com)

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python, FastAPI
- **LLM:** Groq API
- **Embeddings:** Sentence Transformers
- **Similarity Search:** NumPy, Cosine Similarity
- **PDF Processing:** PyPDF

## ✨ Features

- Upload PDF documents.
- Extract and split document text into chunks.
- Generate embeddings using Sentence Transformers.
- Retrieve relevant chunks using cosine similarity.
- Ask questions about uploaded documents.
- Generate context-aware answers using Groq.

## 🧠 How It Works

1. Upload a PDF document.
2. Extract text and split it into chunks.
3. Convert chunks into vector embeddings.
4. Retrieve relevant chunks based on the user's question.
5. Pass the retrieved context to the Groq LLM.
6. Generate an answer based on the document.


