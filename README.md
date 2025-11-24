# 🔍 PUR Auditor RAG

> **Intelligent R&D Project Analysis with Retrieval-Augmented Generation**

This project is a sophisticated **RAG (Retrieval-Augmented Generation)** application designed to audit and analyze technical documents (PURs - Planos de Utilização de Recursos). It leverages the power of **AWS Bedrock**, **LangChain**, and **Vector Search** to extract insights, validate compliance, and summarize complex project data dynamically.

---

## 🛠️ Tech Stack & Architecture

This project is built on a modern AI stack, ensuring scalability, accuracy, and performance.

### 🦜🔗 **LangChain**

We use **LangChain** as the orchestration framework to build our RAG pipeline. It manages:

- **Document Loading & Splitting**: Efficiently processing PDF documents.
- **Retrieval**: Connecting to our vector store to find the most relevant context.
- **Chain Management**: Linking the retrieval step with the LLM generation to produce accurate answers.

### 🧠 **RAG (Retrieval-Augmented Generation)**

Our core engine is based on **RAG**, which allows the LLM to "see" your specific documents before answering.

1. **Ingestion**: Documents are chunked and embedded into vectors.
2. **Storage**: Vectors are stored in a **FAISS** index for millisecond-latency similarity search.
3. **Retrieval**: When a user asks a question, we fetch the most relevant chunks.
4. **Generation**: The LLM generates an answer based *only* on the retrieved context, reducing hallucinations.

### ☁️ **AWS Bedrock**

We utilize **AWS Bedrock** to access high-performance Foundation Models (FMs).

- **Model**: Amazon Titan Text Express (or similar).
- **Benefit**: Secure, scalable, and fully managed serverless inference.

### ⚡ **FastAPI & Next.js**

- **Backend**: **FastAPI** serves the RAG engine via a high-performance REST API.
- **Frontend**: **Next.js 16** provides a reactive, modern UI with "Quick Tags" for instant analysis.

---

## ✨ Key Features

- **📄 PDF Ingestion**: Drag-and-drop PDF processing with automatic text extraction.
- **🔍 Semantic Search**: Finds relevant information even if keywords don't match exactly.
- **🏷️ Dynamic Quick Tags**: Instantly extract **Budget**, **Timeline**, **Risks**, and **Summary** with one click.
- **💬 Interactive Chat**: Ask follow-up questions to dive deeper into specific sections.
- **📜 History Tracking**: Keeps a sidebar history of all your analyses.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- AWS Credentials (with Bedrock access)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pur-auditor-rag
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Run the Application

We have a handy script to start both servers:

```bash
./start_app.sh
```

*Backend runs on `http://localhost:8000`*
*Frontend runs on `http://localhost:3000`*

---

## 📂 Project Structure

```text
pur-auditor-rag/
├── 📂 src/                 # Core Python Logic
│   ├── auditor.py          # RAG Chain & Prompt Logic
│   ├── rag_engine.py       # Vector Store & Retrieval
│   ├── ingest.py           # PDF Processing
│   └── api.py              # FastAPI Endpoints
├── 📂 frontend/            # Next.js Application
│   ├── app/                # React Components & Pages
│   └── lib/                # API Clients
├── 📂 notebooks/           # Jupyter Notebooks for Experiments
├── 📂 data/                # Raw PDF Storage
└── 📄 start_app.sh         # Startup Script
```

---

## 🔗 Useful Links

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [AWS Bedrock Guide](https://aws.amazon.com/bedrock/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)

---

*Built with ❤️ by the R&D Team*
