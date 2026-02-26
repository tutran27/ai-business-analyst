from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch

from app.agents.base import get_llm
from app.utils import retry_async

import asyncio
from dotenv import load_dotenv

load_dotenv()

tavily_search = TavilySearch(max_results=3)

@retry_async
async def research_agent(state):
    feedback=state.get("critic_feedback", None)

    search_context=""
    if feedback:
        print(f"--- RESEARCH RE-TRYING WITH FEEDBACK: {feedback} ---")
        search_context = f"LƯU Ý QUAN TRỌNG: Lần trước báo cáo bị từ chối vì: {feedback}. Hãy tìm kiếm kỹ hơn về vấn đề này."
    try:
        search_results = await tavily_search.ainvoke(state["user_query"])
    except Exception as e:
        print(f"Error in research agent: {e}")
        return {"research_report": "Không có kết quả tìm kiếm"}
    
    result = search_results.get("results", [])
    if not result:
        print("No search results found")
        return {"research_report": "Không có kết quả tìm kiếm"}
    # Convert search results to string for the prompt
    search_results_str = "\n\n".join([res["content"] for res in result])
    
    template = """
    Bạn là chuyên gia nghiên cứu thị trường.
    {search_context}
    Dựa trên các nguồn sau:
    {search_results_str}

    Hãy tạo báo cáo thật NGẮN GỌN, chỉ tập trung vào những thông tin quan trọng và có giá trị quyết định kinh doanh theo cấu trúc:

    1. TỔNG QUAN THỊ TRƯỜNG 
    2. SỐ LIỆU QUAN TRỌNG
    3. XU HƯỚNG CHÍNH 
    4. KẾT LUẬN

    Yêu cầu:
    - Không lan man
    - Không dùng markdown
    - Không lặp lại thông tin
    - Chỉ giữ thông tin có giá trị quyết định kinh doanh
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = get_llm()
    chain = prompt | llm
    result = await chain.ainvoke({"search_context": search_context,
                                  "search_results_str": search_results_str})
    # xoa ** markdown
    import re
    clean_content = re.sub(r'[*#_]', '', result.content)
    return {"research_report": clean_content}

# Kiem tra
if __name__ == "__main__":

    async def test_research_agent():
        state = {
            "user_query": "Xu hướng sử dụng AI trong kinh doanh năm 2025 tại Việt Nam",
            "research_report": None,
            "financial_report": None,
            "strategy_report": None,
            "critic_feedback": None,
            "retry_count": 0,
            "final_output": None,
        }

        result = await research_agent(state)
        return result

    output = asyncio.run(test_research_agent())
    print("\n============= Testing research_agent =============")
    print(output["research_report"])
    print("\n============= Testing completed! =============")
