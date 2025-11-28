import json
import os
from opensearchpy import OpenSearch, helpers
from sentence_transformers import SentenceTransformer


client = OpenSearch(
    hosts=[{'host':'localhost','port':9200}],
    http_compress=True,
    use_ssl=False
)

INDEX_NAME = "vext_products"

# Load model để tạo vector cho câu truy vấn của người dùng
print("⏳ Đang tải model AI cho tìm kiếm...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_index():
    print(f"Dang thiet lap INDEX_MAPPING cho {INDEX_NAME}")

    # define data structure (schema)
    index_body = {
        "settings": {
            "index": {
                "knn": True,                        # Kích hoạt plugin Vector [cite: 357]
                "knn.algo_param.ef_search": 100,    # Tinh chỉnh tốc độ tìm kiếm
                "number_of_shards": 1,              # Demo dùng 1 shard cho nhẹ (Tài liệu gốc là 2)
                "number_of_replicas": 0             # Tắt replica để tiết kiệm ổ cứng dev
            }
        },
        "mappings": {
            "dynamic": "strict", # Quan trọng: Chặn OpenSearch tự đoán kiểu dữ liệu bừa bãi 
            "properties": {
                # --- Metadata Chính xác (Keyword) ---
                "id": { "type": "keyword" },        # ID dùng keyword để lookup nhanh [cite: 324]
                "category": { "type": "keyword" },  # Lọc danh mục chính xác [cite: 274]
                "brand": { "type": "keyword" },
                
                # --- Metadata Phạm vi (Range) ---
                "price": { "type": "float" },       # Để lọc giá (ví dụ: < 10 triệu) [cite: 277]
                "publish_date": { 
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis" # Định dạng chuẩn ISO-8601
                },

                # --- Tìm kiếm Toàn văn (Full-Text) ---
                "title": { 
                    "type": "text", 
                    "analyzer": "standard",         # Tách từ chuẩn [cite: 286]
                    "fields": {
                        "keyword": { "type": "keyword" } # Giữ lại bản sao keyword để sort/aggs [cite: 329]
                    }
                },
                "content_text": { "type": "text" }, # Nội dung chính để tìm từ khóa [cite: 338]
                
                # --- Vector Search (k-NN HNSW) ---
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384,               # Khớp với model all-MiniLM-L6-v2 [cite: 294]
                    "method": {
                        "name": "hnsw",             # Thuật toán đồ thị SOTA [cite: 347]
                        "space_type": "cosinesimil",# Dùng Cosine Similarity cho NLP [cite: 307]
                        "engine": "nmslib",
                        "parameters": {
                            "ef_construction": 128, # Kích thước danh sách động khi xây đồ thị [cite: 352]
                            "m": 16                 # Số kết nối tối đa mỗi nút [cite: 353]
                        }
                    }
                }
            }
        }
    }
    
    # Xóa index cũ để áp dụng mapping mới
    if client.indices.exists(index=INDEX_NAME):
        client.indices.delete(index=INDEX_NAME)
        print(f"   🗑️ Đã xóa index cũ '{INDEX_NAME}'.")
        
    # Gửi lệnh tạo index
    try:
        client.indices.create(index=INDEX_NAME, body=index_body)
        print(f"   ✅ Đã tạo Index '{INDEX_NAME}' thành công với HNSW (m=16, ef=128).")
    except Exception as e:
        print(f"   ❌ Lỗi tạo index: {e}")