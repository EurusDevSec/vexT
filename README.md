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

Chạy OpenSearch bằng Docker Compose từ thư mục `infra`:

```bash
cd infra
docker-compose up -d
```

_Đợi khoảng 1-2 phút để OpenSearch khởi động hoàn tất._

### Bước 2: Chuẩn bị dữ liệu (ETL)

Đảm bảo bạn đã có file dữ liệu `flipkart_data.csv` trong thư mục `res/`.
Sau đó chạy pipeline để xử lý dữ liệu và tạo file JSON trung gian:

```bash
# Từ thư mục gốc
cd src
uv run etl_pipeline.py
# Hoặc: python etl_pipeline.py
```

### Bước 3: Đánh chỉ mục (Indexing)

Nạp dữ liệu đã xử lý vào OpenSearch:

```bash
# Từ thư mục src
uv run search_core.py
# Hoặc: python search_core.py
```

### Bước 4: Khởi chạy ứng dụng

Mở giao diện web Streamlit:

```bash
# Từ thư mục src
uv run streamlit run app.py
# Hoặc: streamlit run app.py
```

Truy cập vào địa chỉ hiển thị trên terminal (thường là `http://localhost:8501`).

---

## 📂 Cấu trúc dự án

```
vexT/
├── docs/                   # Tài liệu kỹ thuật
├── infra/                  # Cấu hình Docker
│   └── docker-compose.yml
├── res/                    # Thư mục chứa dữ liệu (CSV)
├── src/                    # Mã nguồn chính
│   ├── app.py              # Giao diện Streamlit
│   ├── etl_pipeline.py     # Xử lý dữ liệu & Vector hóa
│   ├── search_core.py      # Tương tác OpenSearch (Index & Search)
│   ├── rag_engine.py       # Logic RAG & Gemini
│   └── pyproject.toml      # Quản lý dependencies
├── .env                    # Biến môi trường (API Key)
└── README.md               # Hướng dẫn sử dụng
```

## 📝 Ghi chú

- **Tài khoản OpenSearch mặc định**: `admin` / `StrongPassword123!` (được cấu hình trong `docker-compose.yml`).
- **Dữ liệu**: Dự án sử dụng tập dữ liệu mẫu Flipkart. Bạn có thể thay đổi mapping trong `etl_pipeline.py` để dùng dữ liệu khác.
