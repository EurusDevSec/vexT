import pandas as pd
import numpy as np 
from sentence_transformers import SentenceTransformer
import os

#CONFIG

print("Loading model AI... ")
model = SentenceTransformer('all-MiniLM-L6-v2')


dir_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path= os.path.join(dir_script,"res", "products.csv")

# print(csv_path)
def normalize_data(file_path):
    # df = pd.DataFrame(file_path)
    # print(df.head())
    
    df =pd.read_csv(file_path)
    # print(df)
    df["category"] = df["category"].fillna("Unknown")
    df["title"] = df["title"].fillna("Unknown")

    # Clear garbage

    # print(df["category"])
    # "  electronics   " -> "Electronics"
    df["category"] = df["category"].apply(lambda x: str(x).strip().title())
    # print(df["category"])
    
    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")
    # print(df["publish_date"])

    #filer garbage

    init_count = len(df)
    df = df.dropna(subset=["content_text"])
    print(f"Cleared {init_count - len(df)} lines not have descrip content")

    return df 



def generate_vectors(df):
    print("🧠 Đang tạo Vector Embeddings (Vectorization)...")
    
    # Lấy danh sách text để đưa vào model
    sentences = df['content_text'].tolist()
    
    # Batch Processing: Thư viện này tự động xử lý batch ngầm bên dưới
    embeddings = model.encode(sentences, show_progress_bar=True)
    
    # Gán vector ngược lại vào DataFrame
    # Lưu ý: OpenSearch cần vector dạng List, không phải Numpy Array
    df['embedding'] = list(embeddings)
    
    print(f"✅ Đã tạo vector thành công cho {len(df)} dòng dữ liệu.")
    return df

def main():
    try:
        #1. Ingestion and normalization
        df_clean = normalize_data(file_path)

        #2. Vectorization

        df_final=generate_vectors(df_clean)
        
        #3. Result

        print("\n Result after process")
        print(df_final[['title', 'category', 'publish_date']].head())
        print(f"\nKích thước Vector mẫu: {len(df_final['embedding'].iloc[0])} chiều")

        df_final.to_json('product_ready.json',orient='records')

    except KeyboardInterrupt:
        print("System are stopped")
if __name__ == "__main__":
    main()