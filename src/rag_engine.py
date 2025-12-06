import os
import google.generativeai as genai
from dotenv import load_dotenv

# config api

project_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

#config model
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in environment(.env)")

genai.configure(api_key =GOOGLE_API_KEY)
model=genai.GenerativeModel('gemini-2.5-flash')

def build_prompt(user_query, search_results):
    """
    prompt Engineering: Context Injection
    json -> easy text for AI
    """

    context_text=""
    for i, item in enumerate(search_results):
        source=item['_source']
        price_str=f"₹{source['price']:,.0f}"
        context_text +=f"""
        --- san pham {i+1}
        Ten: {source['title']}
        Gia: {price_str}
        Danh Muc: {source['category']}
        Mo ta: {source['content_text']}
        """


    # Prompt Template
    final_prompt= f"""
    Bạn là VexT - Trợ lý tư vấn bán hàng thông minh của công ty Eurus.

    Nhiệm vụ:
    Trả lời câu hỏi của khách hàng dựa trên DANH SÁCH SẢN PHẨM bên dưới.

    QUY TẮT BẮT BUỘC:
    1. Chỉ được dùng thông tin trong danh sách cung cấp. Không bịa đặt và hallucination
    2. Nếu không tìm thấy sản phẩm phù hợp trong danh sách, hãy nói "hiện tại kho hàng chưa có sản phẩm này".
    3. Trả lời ngắn gọn, súc tích, chuyên nghiệp
    4. Luôn kèm theo giá tiền khi nhắc đến sản phẩm.
    
    DANH SÁCH SẢN PHẨM TÌM THẤY (CONTEXT):
    {context_text}

    CÂU HỎI CỦA KHÁCH HÀNG:

    {user_query}

    CÂU TRẢ LỜI CỦA BẠN:

    """
    return final_prompt


def generative_rag_answer(user_query, search_results):
    """
    receive Question + search result -> return AI answer
    """

    print("Dang gui du lieu sang Gemini de suy luan")

    if not search_results:
        return "Xin loi, toi khong tim thay san pham nao phu hop voi yeu cau cua ban"
    

    #1. create prompt
    prompt=build_prompt(user_query, search_results)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Loi ket noi AI: {str(e)}"
    
# TEST MODULE
if __name__ == "__main__":
    mock_results = [
        {
            "_source":{
                "title": "Laptop Dell XPS 13",
                "price": 25000000,
                "category": "Electronics",
                "content_text":"Máy tính xách tay Dell XPS 13 màn hình vô cực, chip i7, RAM 16GB"
            }
        }
    ]
    query = "Máy này có code được không em?"
    print(f"User: {query}")
    print("-"*20)
    print(generative_rag_answer(query, mock_results))