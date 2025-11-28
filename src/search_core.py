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