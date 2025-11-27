import json
import os
from opensearchpy import OpenSearch, helpers
from sentence_transformers import SentenceTransformer


client = OpenSearch(
    hosts=[{'host':'localhost','port':9200}],
    http_compress=True,
    use_ssl=False
)

I