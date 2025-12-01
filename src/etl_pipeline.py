import pandas as pd
import numpy as np 
# Chú ý: Thư viện tên là sentence_transformers (có chữ s ở cuối)
from sentence_transformers import SentenceTransformer 
import os

# --- CẤU HÌNH ---
print("Loading model AI... ")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Xác định đường dẫn file
dir_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Tạo thư mục res nếu chưa có
os.makedirs(os.path.join(dir_script, "res"), exist_ok=True)
file_path = os.path.join(dir_script, "res", "products.csv")

# --- HÀM TẠO DỮ LIỆU MẪU (Fix lỗi CSV của bạn) ---
def create_dummy_data():
    print("🛠️ Đang tạo file dữ liệu mẫu chuẩn (products.csv)...")
    data = [
        {
            "id": 1,
            "title": "Laptop Dell XPS 13",
            "category": "Electronics",
            "publish_date": "2023-10-01",
            "price": 25000000,
            "content_text": "Máy tính xách tay Dell XPS 13 màn hình vô cực, chip Intel Core i7, RAM 16GB, SSD 512GB. Thiết kế mỏng nhẹ doanh nhân."
        },
        {
            "id": 2,
            "title": "iPhone 15 Pro Max",
            "category": "Mobile",
            "publish_date": "2023-09-15",
            "price": 30000000,
            "content_text": "Điện thoại iPhone 15 Pro Max vỏ titan, chip A17 Pro, camera 48MP zoom quang học 5x. Màu xanh titan tự nhiên."
        },
        {
            "id": 3,
            "title": "Chuột Logitech MX Master 3",
            "category": "Accessories",
            "publish_date": "2023-01-20",
            "price": 2500000,
            "content_text": "Chuột không dây Logitech MX Master 3S, thiết kế công thái học, cuộn siêu nhanh MagSpeed, pin sạc USB-C."
        },
        {
            "id": 4,
            "title": "Sách Clean Code",
            "category": "Books",
            "publish_date": None, # Test dữ liệu thiếu ngày
            "price": 500000,
            "content_text": "Cuốn sách Clean Code của Robert C. Martin hướng dẫn cách viết mã sạch, dễ bảo trì và tối ưu cho lập trình viên."
        },
        {
            "id": 5,
            "title": None, # Test thiếu tiêu đề
            "category": "Unknown",
            "publish_date": "2022-12-12",
            "price": 0,
            "content_text": "Dữ liệu bị lỗi tiêu đề nhưng vẫn có nội dung mô tả để test vector."
        }
    ]
    # Tạo DataFrame và lưu ra CSV chuẩn
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding='utf-8')
    print("✅ Đã tạo file products.csv thành công!")

# --- CÁC HÀM XỬ LÝ (ETL) ---
def normalize_data(file_path):
    print(f"🔄 Đang đọc dữ liệu từ: {file_path}")
    df = pd.read_csv(file_path)
    
    # Xử lý giá trị thiếu (Fill NA)
    df["category"] = df["category"].fillna("Unknown")
    df["title"] = df["title"].fillna("Unknown Product")

    # Chuẩn hóa chuỗi (String Cleaning)
    df["category"] = df["category"].apply(lambda x: str(x).strip().title())
    
    # Chuẩn hóa ngày tháng (Date Parsing)
    # errors='coerce' nghĩa là: nếu lỗi thì biến thành NaT (trống) chứ không báo lỗi dừng chương trình
    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")

    # Lọc rác (Filter Garbage)
    # Chỉ xóa những dòng KHÔNG CÓ nội dung mô tả (vì không tạo vector được)
    init_count = len(df)
    df = df.dropna(subset=["content_text"])
    
    if init_count - len(df) > 0:
        print(f"⚠️ Đã lọc bỏ {init_count - len(df)} dòng thiếu nội dung mô tả.")

    return df 

def generate_vectors(df):
    print("🧠 Đang tạo Vector Embeddings (Vectorization)...")
    
    # Lấy danh sách text
    sentences = df['content_text'].tolist()
    
    # Tạo vector (Batch process)
    embeddings = model.encode(sentences, show_progress_bar=True)
    
    # Chuyển về dạng List để OpenSearch hiểu
    df['embedding'] = list(embeddings)
    
    print(f"✅ Đã tạo vector thành công cho {len(df)} dòng dữ liệu.")
    return df

def main():
    try:
        # BƯỚC 0: TỰ ĐỘNG TẠO DATA CHUẨN
        create_dummy_data()

        # BƯỚC 1: ETL
        df_clean = normalize_data(file_path)

        # BƯỚC 2: VECTOR HÓA
        df_final = generate_vectors(df_clean)
        
        # BƯỚC 3: KẾT QUẢ
        print("\n--- KẾT QUẢ KIỂM TRA (SAMPLE) ---")
        # In ra 3 cột quan trọng để check xem còn bị lệch không
        print(df_final[['title', 'category', 'price', 'publish_date']].head())
        
        # Kiểm tra kích thước vector dòng đầu tiên
        vector_dim = len(df_final['embedding'].iloc[0])
        print(f"\n📏 Kích thước Vector: {vector_dim} chiều (Chuẩn SOTA)")

        # Lưu kết quả ra JSON để dùng cho bước sau
        output_path = os.path.join(dir_script, "res", "product_ready.json")
        df_final.to_json(output_path, orient='records', date_format='iso')
        print(f"💾 Đã lưu kết quả vào: {output_path}")

    except KeyboardInterrupt:
        print("System stopped by user")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()