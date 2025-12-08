# vexT — Next-Gen Hybrid Search & RAG Engine

![Project Banner](image.png)

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenSearch](https://img.shields.io/badge/OpenSearch-2.11-005EB8?style=for-the-badge&logo=opensearch&logoColor=white)](https://opensearch.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

**vexT** is a state-of-the-art (SOTA) prototype for **Hybrid Search** and **Retrieval-Augmented Generation (RAG)**. It bridges the gap between traditional keyword search and modern semantic understanding, delivering precise, context-aware answers for e-commerce product data.

---

## 🚀 Key Features

- **🧠 Hybrid Retrieval Engine**: Combines the precision of **BM25** (Keyword Search) with the semantic understanding of **k-NN HNSW** (Vector Search) using OpenSearch.
- **🤖 Generative AI (RAG)**: Integrates **Google Gemini 2.5 Flash** to synthesize natural language answers based on retrieved product context.
- **🌍 Multilingual Support**: Powered by `paraphrase-multilingual-MiniLM-L12-v2`, enabling seamless search in English, Vietnamese, and more.
- **⚡ High-Performance Infrastructure**: Dockerized OpenSearch cluster with optimized HNSW settings (`m=16`, `ef_construction=128`).
- **🛠️ Automated ETL Pipeline**: Robust data processing pipeline that handles cleaning, sampling, and vectorization of large datasets.
- **📊 Interactive UI**: A clean, responsive Streamlit interface for real-time testing and demonstration.

---

## 🏗️ Architecture

The system follows a modular architecture:

1.  **Data Ingestion (Offline)**: Raw CSV data is processed, vectorized, and indexed into OpenSearch.
2.  **Search Runtime (Online)**: User queries are vectorized and sent to OpenSearch via a Hybrid Query DSL.
3.  **RAG Inference**: Top results are injected into a prompt context for Gemini to generate the final response.

_(See `docs/system_workflow_detailed.md` for a deep dive into the internal workflow)_

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop**: For running the OpenSearch cluster.
- **Python 3.12+**: The core programming language.
- **uv** (Recommended): An extremely fast Python package installer and resolver.
- **Google Cloud API Key**: Access to Gemini models.

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/EurusDevSec/vexT.git
cd vexT
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Install Dependencies

We recommend using `uv` for lightning-fast setup:

```bash
cd src
uv sync
```

_(Alternatively, use `pip install -r requirements.txt` if you prefer standard pip)_

### 4. Start Infrastructure

Launch the OpenSearch cluster using Docker Compose. Note that we use custom ports (`10200`, `10600`) to avoid conflicts on Windows.

```bash
# From project root
docker-compose -f infra/docker-compose.yml up -d
```

_Wait ~30 seconds for the cluster to initialize._

### 5. Run ETL Pipeline

Process the data and generate vectors. This step includes smart sampling to preserve demo scenarios.

```bash
# From src/ directory
uv run etl_pipeline.py
```

### 6. Index Data

Create the index mapping and ingest data into OpenSearch.

```bash
uv run search_core.py
```

### 7. Launch Application

Start the Streamlit frontend.

```bash
uv run streamlit run app.py
```

Access the app at: `http://localhost:8501`

---

## 📂 Project Structure

```
vexT/
├── docs/                   # Documentation & Architecture plans
├── infra/                  # Infrastructure (Docker Compose)
│   └── docker-compose.yml
├── res/                    # Resources (Data files)
│   ├── flipkart_data.csv
│   └── flipkart_data_ready.json
├── src/                    # Source Code
│   ├── app.py              # Streamlit Frontend
│   ├── etl_pipeline.py     # Data Processing & Vectorization
│   ├── rag_engine.py       # Gemini AI Integration
│   └── search_core.py      # OpenSearch Logic
├── .env                    # Environment Variables
├── CODE_OF_CONDUCT.md      # Community Standards
├── CONTRIBUTING.md         # Contribution Guidelines
└── README.md               # Project Documentation
```

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

---

## 📜 Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Contact

**EurusDevSec** - [GitHub Profile](https://github.com/EurusDevSec)

Project Link: [https://github.com/EurusDevSec/vexT](https://github.com/EurusDevSec/vexT)

```bash
cd src
uv run streamlit run app.py   # or: streamlit run app.py
```

Open the URL shown by Streamlit (usually http://localhost:8501).

---

## Project layout

```
vexT/
├── docs/            # Technical documentation
├── infra/           # Docker compose for OpenSearch
├── res/             # Input datasets (e.g. flipkart_data.csv)
├── src/             # Application source code
│   ├── app.py       # Streamlit demo
│   ├── etl_pipeline.py
│   ├── search_core.py
│   ├── rag_engine.py
│   └── pyproject.toml
├── .env
└── README.md
```

---

## Notes and tips

- Default OpenSearch credentials (configured in `infra/docker-compose.yml`): `admin` / `StrongPassword123!`.
- The ETL mapping (column names) is configurable in `src/etl_pipeline.py` to accommodate other datasets.
- For development, the heap settings in `infra/docker-compose.yml` are conservative; increase them for larger datasets or production use.

If you want, I can also: add a `requirements.txt`, create a small `Makefile` for the common commands, or add unit tests for the ETL and search modules.
