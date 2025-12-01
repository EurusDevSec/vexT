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

# MAIN AREA: CHAT & SEARCH
st.title("🔍 VexT: Hệ thống Tìm kiếm Lai & RAG")
st.markdown("simple question, pro answer")

# input text
user_query = st.text_input("Bạn đang tìm kiếm sản phẩm gì?", placeholder="Ví dụ máy tính chạy Docker giá rẻ...")

if st.button("Search"):
    if not user_query:
        st.warning("Vui long nhap cau hoi!")
    else:
        # buoc1: Hybrid Search
        with st.spinner("Đang quét dữ liệu Vector & Metadata..."):
            raw_results = search_hybrid(user_query, min_price_input)

        if not raw_results:  # [] hoặc lỗi
            st.warning("Không tìm thấy sản phẩm nào hoặc xảy ra lỗi tìm kiếm.")
        else:
            # buoc2: suy luan (RAG)
            with st.spinner("AI đang đọc tài liệu và tổng hợp câu trả lời..."):
                ai_answer = generative_rag_answer(user_query, raw_results)

            # DISPLAY RESULT
            st.success("Tư vấn từ vexT")
            st.write(ai_answer)
            st.markdown("---")

            # 2. Dẫn chứng (Evidence) - Danh sách sản phẩm tìm thấy
            st.subheader(f"📦 Tìm thấy {len(raw_results)} sản phẩm phù hợp:")

            # Chia cột để hiển thị thẻ sản phẩm
            cols = st.columns(3)

            for i, hit in enumerate(raw_results):
                source = hit.get('_source', {})
                score = hit.get('_score', 0.0)
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="product-card">
                        <h3>{source.get('title','N/A')}</h3>
                        <p class="price-tag">{source.get('price',0):,.0f} VNĐ</p>
                        <p><b>Danh mục:</b> {source.get('category','N/A')}</p>
                        <p style="font-size:0.9em; color:gray">{source.get('content_text','')[:100]}...</p>
                        <hr>
                        <small>Độ phù hợp (Score): {score:.4f}</small>
                    </div>
                    """, unsafe_allow_html=True)

            # 3. Debug (Nếu bật)
            if show_debug:
                with st.expander("🛠️ Xem dữ liệu JSON thô (Dành cho Dev)"):
                    st.json(raw_results)