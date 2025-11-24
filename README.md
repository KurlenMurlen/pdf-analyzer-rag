# PUR Auditor RAG

![Project Banner](https://capsule-render.vercel.app/api?type=waving&color=0:000000,100:333333&height=200&section=header&text=PDF%20Auditor%20RAG&fontSize=80&fontColor=ffffff)

> **Intelligent R&D Project Analysis with Retrieval-Augmented Generation**

This project is a sophisticated **RAG (Retrieval-Augmented Generation)** application designed to audit and analyze technical documents (PURs - Planos de Utilização de Recursos). It leverages the power of **AWS Bedrock**, **LangChain**, and **Vector Search** to extract insights, validate compliance, and summarize complex project data dynamically.

---

## Tech Stack & Architecture

| Component | Technology | Description |
|-----------|------------|-------------|
| **Orchestration** | ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white) | Manages document splitting, retrieval, and chain execution. |
| **LLM Provider** | ![AWS](https://img.shields.io/badge/AWS_Bedrock-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white) | Amazon Titan Text Express for secure, serverless inference. |
| **Vector Store** | ![FAISS](https://img.shields.io/badge/FAISS-005A9C?style=for-the-badge&logo=meta&logoColor=white) | Efficient similarity search for document chunks. |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | High-performance REST API serving the RAG engine. |
| **Frontend** | ![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white) | Reactive UI with "Quick Tags" for instant analysis. |

---

## Key Features

### Core Capabilities

* **PDF Ingestion**
  Drag-and-drop PDF processing with automatic text extraction and semantic chunking.

* **Semantic Search**
  Finds relevant information based on meaning rather than just keyword matching.

* **Dynamic Quick Tags**
  Instantly extract specific data points with one click:
  * `Budget`
  * `Timeline`
  * `Risks`
  * `Summary`

* **Interactive Chat**
  Ask follow-up questions to dive deeper into specific sections of the document.

* **History Tracking**
  Keeps a sidebar history of all your previous analyses for easy reference.

---

## Getting Started

### Prerequisites

* **Python 3.9+**
* **Node.js 18+**
* **AWS Credentials** (with Bedrock access)

### Installation & Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd pur-auditor-rag
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Set up environment variables
cp .env.example .env
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
```

#### 4. Run the Application

We have a handy script to start both servers:

```bash
./start_app.sh
```

| Service | URL |
|---------|-----|
| **Backend** | `http://localhost:8000` |
| **Frontend** | `http://localhost:3000` |

---

## Project Structure

```text
pur-auditor-rag/
├── src/                 # Core Python Logic
│   ├── auditor.py       # RAG Chain & Prompt Logic
│   ├── rag_engine.py    # Vector Store & Retrieval
│   ├── ingest.py        # PDF Processing
│   └── api.py           # FastAPI Endpoints
├── frontend/            # Next.js Application
│   ├── app/             # React Components & Pages
│   └── lib/             # API Clients
├── notebooks/           # Jupyter Notebooks for Experiments
├── data/                # Raw PDF Storage
└── start_app.sh         # Startup Script
```

---

## Useful Links

* [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
* [AWS Bedrock Guide](https://aws.amazon.com/bedrock/)
* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [Next.js Documentation](https://nextjs.org/docs)

---

<div align="center">
  <sub>Built by the R&D Team</sub>
</div>


