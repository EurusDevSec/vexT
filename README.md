# vexT - Hybrid Search & RAG System

![Project Banner](image.png)

**vexT** là một hệ thống tìm kiếm thông minh kết hợp giữa **Hybrid Search** (Keyword + Vector) và **RAG** (Retrieval-Augmented Generation) để cung cấp câu trả lời chính xác dựa trên dữ liệu sản phẩm thực tế.

Dự án sử dụng **OpenSearch** làm công cụ tìm kiếm vector, **SentenceTransformers** để tạo embedding, và **Google Gemini** để tổng hợp câu trả lời.

---

## 🚀 Tính năng chính

- **Hybrid Search**: Kết hợp sức mạnh của tìm kiếm từ khóa (BM25) và tìm kiếm ngữ nghĩa (k-NN/Vector) sử dụng thuật toán HNSW + FAISS.
- **RAG Engine**: Tích hợp Google Gemini 2.0 Flash để trả lời câu hỏi tự nhiên dựa trên kết quả tìm kiếm.
- **ETL Pipeline**: Quy trình xử lý dữ liệu tự động từ CSV sang Vector Index.
- **Giao diện Streamlit**: UI thân thiện để tìm kiếm và chat với dữ liệu.

## 🛠️ Công nghệ sử dụng

- **Core**: Python 3.12+
- **Search Engine**: OpenSearch (Docker)
- **LLM**: Google Gemini (via Google GenAI SDK)
- **Embedding**: `all-MiniLM-L6-v2`
- **Frontend**: Streamlit
- **Quản lý gói**: `uv` (hoặc pip)

---

## 📋 Yêu cầu hệ thống

1. **Docker Desktop** (để chạy OpenSearch).
2. **Python 3.12** trở lên.
3. **Google API Key** (để sử dụng Gemini).

---

## ⚙️ Cài đặt

### 1. Clone dự án

```bash
git clone https://github.com/EurusDevSec/vexT.git
cd vexT
```

### 2. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc và thêm API Key của bạn:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Cài đặt thư viện

Dự án sử dụng `uv` để quản lý gói. Nếu chưa có `uv`, bạn có thể cài đặt hoặc dùng `pip`.

**Cách 1: Dùng uv (Khuyên dùng)**

```bash
# Tại thư mục gốc
cd src
uv sync
```

**Cách 2: Dùng pip**

```bash
pip install -r requirements.txt
# Hoặc cài thủ công các thư viện trong pyproject.toml
pip install opensearch-py sentence-transformers pandas streamlit google-generativeai python-dotenv
```

---

## ▶️ Hướng dẫn chạy

### Bước 1: Khởi động OpenSearch

# vexT — Hybrid Search and RAG

![Project Banner](image.png)

vexT is a prototype hybrid search and retrieval-augmented generation (RAG) system that combines keyword search (BM25) with semantic vector search to deliver context-aware answers over product data. The project demonstrates an end-to-end pipeline: ETL, embedding, vector indexing (OpenSearch + FAISS), hybrid retrieval, and answer generation via Google Gemini.

Key components:

- OpenSearch (vector-enabled) as the search backend
- SentenceTransformers (`all-MiniLM-L6-v2`) for embeddings
- Google Gemini (via Google GenAI SDK) for RAG response generation
- Streamlit for a simple web UI

---

## Features

- Hybrid retrieval: BM25 (text) + approximate k-NN (vector) using HNSW + FAISS
- RAG: contextual answer synthesis using retrieved documents
- ETL pipeline to normalize and convert product CSV into indexed documents
- Streamlit demo app for interactive search and question answering

---

## Requirements

- Docker Desktop (to run the OpenSearch cluster)
- Python 3.12+
- A Google Cloud API key with access to the GenAI endpoint (set via `GOOGLE_API_KEY`)

---

## Quickstart

Follow these steps to run the project locally.

1. Clone the repository

```bash
git clone https://github.com/EurusDevSec/vexT.git
cd vexT
```

2. Configure environment variables

Create a `.env` file in the repository root with your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

3. Install Python dependencies

The project uses `uv` for dependency management; you can use it if available, otherwise use `pip`.

Recommended (uv):

```bash
cd src
uv sync
```

Alternative (pip):

```bash
pip install -r requirements.txt
# or install packages manually from src/pyproject.toml
```

4. Start OpenSearch

From the `infra/` directory:

```bash
cd infra
docker-compose up -d
```

Allow 1–2 minutes for OpenSearch to fully initialize.

5. Run the ETL pipeline

Place your `flipkart_data.csv` file inside the `res/` folder, then run:

```bash
# from project root
cd src
uv run etl_pipeline.py   # or: python etl_pipeline.py
```

This will normalize the CSV, generate embeddings, and export a JSON file ready for indexing.

6. Index data into OpenSearch

```bash
cd src
uv run search_core.py    # or: python search_core.py
```

7. Launch the demo UI

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
