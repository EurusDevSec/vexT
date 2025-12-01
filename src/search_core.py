import json  # <--- ĐÃ THÊM VÀO ĐÂY
import os
from opensearchpy import OpenSearch, helpers
from sentence_transformers import SentenceTransformer

# --- CẤU HÌNH ---
# Cập nhật cấu hình kết nối cho OpenSearch Docker (Bảo mật mặc định)
auth = ('admin', 'StrongPassword123!')  # Mật khẩu đã set trong docker-compose.yml

client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True,
    http_auth=auth,         # Thêm xác thực Basic Auth
    use_ssl=True,           # Bật SSL vì OpenSearch mặc định dùng HTTPS
    verify_certs=False,     # Bỏ qua check chứng chỉ (vì dùng self-signed trong Docker)
    ssl_assert_hostname=False,
    ssl_show_warn=False
)

INDEX_NAME = "vext_products"

# Load model AI
print("⏳ Đang tải model AI cho tìm kiếm...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_index():
    print(f"🛠️ Đang thiết lập INDEX_MAPPING cho {INDEX_NAME}...")

    # Define data structure (schema)
    index_body = {
        "settings": {
            "index": {
                "knn": True,                        # Kích hoạt plugin Vector
                "knn.algo_param.ef_search": 100,    # Tinh chỉnh tốc độ tìm kiếm
                "number_of_shards": 1,              # Demo dùng 1 shard cho nhẹ
                "number_of_replicas": 0             # Tắt replica tiết kiệm ổ cứng
            }
        },
        "mappings": {
            "dynamic": "strict", # Quan trọng: Chặn OpenSearch tự đoán kiểu dữ liệu
            "properties": {
                # --- Metadata Chính xác (Keyword) ---
                "id": { "type": "keyword" },        # Lookup nhanh
                "category": { "type": "keyword" },  # Lọc chính xác
                "brand": { "type": "keyword" },
                
                # --- Metadata Phạm vi (Range) ---
                "price": { "type": "float" },       # Lọc giá
                "publish_date": { 
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis"
                },

                # --- Tìm kiếm Toàn văn (Full-Text) ---
                "title": { 
                    "type": "text", 
                    "analyzer": "standard",
                    "fields": {
                        "keyword": { "type": "keyword" } 
                    }
                },
                "content_text": { "type": "text" }, 
                
                # --- Vector Search (k-NN HNSW) ---
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384,               # Khớp model MiniLM
                    "method": {
                        "name": "hnsw",             # Thuật toán SOTA
                        "space_type": "cosinesimil",
                        "engine": "nmslib",
                        "parameters": {
                            "ef_construction": 128,
                            "m": 16
                        }
                    }
                }
            }
        }
    }
    
    # Xóa index cũ
    if client.indices.exists(index=INDEX_NAME):
        client.indices.delete(index=INDEX_NAME)
        print(f"   🗑️ Đã xóa index cũ '{INDEX_NAME}'.")
        
    # Tạo index mới
    try:
        client.indices.create(index=INDEX_NAME, body=index_body)
        print(f"   ✅ Đã tạo Index '{INDEX_NAME}' thành công với HNSW (m=16, ef=128).")
    except Exception as e:
        print(f"   ❌ Lỗi tạo index: {e}")

def ingest_data():
    # Đường dẫn file json
    dir_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(dir_script, "res", "product_ready.json")
    
    print(f"🔄 Đang đọc dữ liệu từ {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        # Chuẩn bị dữ liệu bulk
        actions = []
        for product in products:
            action = {
                "_index": INDEX_NAME,
                "_source": product
            }
            actions.append(action)
        
        # Gửi lên Server
        helpers.bulk(client, actions)
        print(f"🚀 Đã nạp thành công {len(actions)} sản phẩm vào OpenSearch.")
        
        # Refresh để tìm thấy ngay
        client.indices.refresh(index=INDEX_NAME)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {file_path}. Hãy chạy etl_pipeline.py trước!")

def search_hybrid(user_query, min_price=0):
    print(f"\n🔎 Đang tìm kiếm: '{user_query}' (Giá > {min_price})...")
    
    # B1: Vector hóa
    query_vector = model.encode(user_query).tolist()
    
    # B2: Query DSL
    query_body = {
        "size": 3,
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "price": {"gte": min_price}
                    }
                },
                "should": [
                    {
                        "multi_match": {
                            "query": user_query,
                            "fields": ["title^2", "content_text"],
                            "boost": 0.3
                        }
                    },
                    {
                        "knn": {
                            "embedding": {
                                "vector": query_vector,
                                "k": 3,
                                "boost": 0.7
                            }
                        }
                    }
                ]
            }
        }
    }
    
    # B3: Thực thi
    try:
        response = client.search(index=INDEX_NAME, body=query_body)
        print(f"--- KẾT QUẢ TÌM KIẾM CHO: '{user_query}' ---")
        if not response['hits']['hits']:
            print("   (Không tìm thấy kết quả nào)")
        
        for hit in response['hits']['hits']:
            score = hit['_score']
            source = hit['_source']
            print(f"⭐ Score: {score:.4f} | 🏷️ {source['title']} | 💰 {source['price']:,.0f} VNĐ")
            print(f"   ℹ️ {source['content_text'][:100]}...") 
            print("-" * 30)
    except Exception as e:
        print(f"❌ Lỗi tìm kiếm: {e}")

# --- PHẦN CHẠY CHÍNH (MAIN BLOCK) ---
if __name__ == "__main__":
    try:
        # 1. Tạo cấu trúc bảng (Mapping)
        create_index()
        
        # 2. Nạp dữ liệu vào bảng
        ingest_data()
        
        # 3. Chạy thử tìm kiếm
        # Kịch bản 1: Tìm máy tính code (Ngữ nghĩa) + Lọc giá > 10 triệu
        search_hybrid("Máy tính cho dân code", min_price=10000000)
        
        # Kịch bản 2: Tìm chuột (Từ khóa chính xác) + Không lọc giá
        search_hybrid("Chuột Logitech", min_price=0)
        
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng chương trình.")
    except Exception as e:
        print(f"\n❌ Có lỗi xảy ra: {e}")