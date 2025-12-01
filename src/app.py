import streamlit as st

from search_core import search_hybrid
from rag_engine import generative_rag_answer


#CONFIG FRONTEND

st.set_page_config(
    page_title="VexT - AI hybrid Search",
    page_icon="🔍",
    layout="wide"
)

# custom css
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
    }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .price-tag {
        color: #d63031;
        font-weight: bold;
        font-size: 1.2em;
    }
</style>
""", unsafe_allow_html=True)


# SIDEBAR: FILER METADATA

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1265/1265775.png", width=80)
    st.title("vexT Control")
    st.markdown("---")
    st.header("Bộ lọc Metadata")
    st.info("Metadata giúp thu hẹp phạm vi tìm kiếm trước khi Vector quét dữ liệu.")

    # Filter 1: Gia tien
    min_price_input = st.slider(
        "Ngân sách tối thiểu (VNĐ)",
        min_value=0,
        max_value=50000000,
        step=500000,
        value=0
    )

    # Filter 2: Debug Mode
    show_debug = st.checkbox("hien thi Debug(JSON)", value = False)
    st.markdown("---")
    st.caption("Powered by OpenSearch & gemini")

