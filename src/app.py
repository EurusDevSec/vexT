import streamlit as st

from search_core import search_hybrid
from rag_engine import generative_rag_answer


#CONFIG FRONTEND

st.set_page_config(
    page_title="VexT - AI hybrid Search"
    
)