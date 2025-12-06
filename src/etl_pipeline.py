import pandas as pd
from sentence_transformers import SentenceTransformer
import os

# --- CẤU HÌNH DỮ LIỆU THỰC (REAL WORLD CONFIG) ---
# 1. Đường dẫn file CSV tải từ Kaggle (Đặt file này vào thư mục res/)
# Ví dụ bạn tải file tên là 'flipkart_com-ecommerce_sample.csv'
CSV_FILENAME = "flipkart_data.csv" 

# 2. BẢN ĐỒ ÁNH XẠ CỘT (MAPPING SCHEMA)
# Bên Trái: Tên cột trong hệ thống VexT (CỐ ĐỊNH)
# Bên Phải: Tên cột trong file CSV tải về (THAY ĐỔI TÙY FILE)
COLUMN_MAPPING = {
    "title": "product_name",        # Trong CSV Kaggle cột tên là product_name
    "price": "retail_price",        # Trong CSV Kaggle cột tên là retail_price
    "category": "product_category_tree", 
    "content_text": "description",  # Cột mô tả dùng để tạo vector
    "publish_date": "crawl_timestamp" # Ngày tháng (nếu có)
}

# 3. GIỚI HẠN DỮ LIỆU (QUAN TRỌNG)
# Vector hóa tốn nhiều CPU. Để demo mượt, hãy giới hạn 2000-5000 dòng.
# Đừng tham load cả 100k dòng nếu không có GPU.
DATA_LIMIT = 5000 

print("⏳ Loading model AI...")
# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') # Dùng model đa ngôn ngữ để khớp với search_core

def load_and_map_data(file_path):
    print(f"🔄 Đang đọc file Big Data: {file_path}")
    
    # Đọc CSV
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy file CSV. Hãy tải từ Kaggle và bỏ vào thư mục res/")
        return None

    # Đổi tên cột theo Mapping
    # Đảo ngược dict để dùng hàm rename: {Tên_Cũ: Tên_Mới}
    rename_dict = {v: k for k, v in COLUMN_MAPPING.items()}
    df = df.rename(columns=rename_dict)
    
    # Kiểm tra xem có đủ cột quan trọng không
    required_cols = ["title", "content_text"]
    for col in required_cols:
        if col not in df.columns:
            print(f"❌ File CSV thiếu cột quan trọng map vào '{col}'. Kiểm tra lại COLUMN_MAPPING!")
            return None

    # Chỉ lấy các cột cần thiết cho VexT
    available_cols = [c for c in COLUMN_MAPPING.keys() if c in df.columns]
    df = df[available_cols]

    return df

def clean_data(df):
    print(f"🧹 Đang làm sạch {len(df)} dòng dữ liệu...")
    
    # 1. Giới hạn số lượng (Sampling) nhưng GIỮ LẠI DEMO DATA
    if len(df) > DATA_LIMIT:
        print(f"⚠️ Dữ liệu quá lớn ({len(df)} dòng).")
        
        # Danh sách từ khóa quan trọng cho Demo
        demo_keywords = [
            "Alisha Solid Women's Cycling Shorts",
            "FabHomeDecor Fabric Double Sofa Bed",
            "Sicons All Purpose Arnica Dog Shampoo",
            "AW Bellies",
            "Eternal Gandhi Super Series Crystal Paper Weights"
        ]
        
        # Lọc ra các dòng chứa từ khóa demo (Case insensitive)
        # Tạo mask: Nếu title chứa bất kỳ keyword nào -> True
        mask = df['title'].astype(str).apply(lambda x: any(k.lower() in x.lower() for k in demo_keywords))
        df_demo = df[mask]
        print(f"   👉 Đã tìm thấy {len(df_demo)} sản phẩm Demo quan trọng.")
        
        # Lấy phần còn lại để fill cho đủ DATA_LIMIT
        df_rest = df[~mask]
        remaining_count = DATA_LIMIT - len(df_demo)
        
        if remaining_count > 0:
            df_sample = df_rest.sample(n=remaining_count, random_state=42)
            df = pd.concat([df_demo, df_sample])
        else:
            df = df_demo.head(DATA_LIMIT)
            
        print(f"   ✅ Đã chốt danh sách {len(df)} dòng (Bao gồm Demo Data).")
    
    # 2. Xử lý Giá tiền (Lọc bỏ chữ, chỉ lấy số)
    # Ví dụ Kaggle hay ghi giá là "20,000 USD" -> cần chuyển thành số
    if 'price' in df.columns:
        # Ép kiểu số, lỗi thành NaN
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df['price'].fillna(0) # Giá rỗng thì cho bằng 0
    
    # 3. Xử lý Category (Làm sạch chuỗi)
    if 'category' in df.columns:
        # Lấy danh mục cha đầu tiên, loại bỏ ký tự thừa
        df['category'] = df['category'].astype(str).apply(lambda x: x.replace('["', '').replace('"]', '').split(">>")[0].strip())
    else:
        df['category'] = "General"

    # 4. Xử lý Null ở Description
    df = df.dropna(subset=['content_text'])
    df['content_text'] = df['content_text'].astype(str)
    
    # 5. Xử lý Ngày tháng (Nếu có)
    if 'publish_date' in df.columns:
         df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
    
    return df

def generate_vectors(df):
    print(f"🧠 Đang Vector hóa {len(df)} sản phẩm (Việc này có thể mất vài phút)...")
    
    sentences = df['content_text'].tolist()
    
    # Batch size = 64 giúp chạy nhanh hơn
    embeddings = model.encode(sentences, batch_size=64, show_progress_bar=True)
    
    df['embedding'] = list(embeddings)
    return df

def main():
    # Setup đường dẫn
    dir_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(dir_script, "res", CSV_FILENAME)
    output_path = os.path.join(dir_script, "res", "flipkart_data_ready.json")

    # Pipeline
    df = load_and_map_data(input_path)
    if df is not None:
        df_clean = clean_data(df)
        df_final = generate_vectors(df_clean)
        
        # Lưu kết quả
        df_final.to_json(output_path, orient='records', date_format='iso')
        print(f"\n✅ XONG! Đã lưu {len(df_final)} sản phẩm vector hóa vào: {output_path}")
        print("👉 Bây giờ hãy chạy lại 'uv run search_core.py' để nạp dữ liệu mới này vào OpenSearch!")

if __name__ == "__main__":
    main()