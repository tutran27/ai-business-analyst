from langchain_core.prompts import ChatPromptTemplate
from app.agents.base import get_llm
from app.agents.base import get_llm
from app.utils import retry_async
from app.schemas import BusinessReport

@retry_async
async def critic_agent(state):

    llm = get_llm()
    
    if state.get("research_report") is None:
        return {"critic_feedback": "Research report is missing"}
    if state.get("financial_report") is None:
        return {"critic_feedback": "Financial report is missing"}
    if state.get("strategy_report") is None:
        return {"critic_feedback": "Strategy report is missing"}
    
    template = """
    Bạn là một chuyên gia đánh giá chiến lược kinh doanh.

    Dưới đây là báo cáo:

    ===== RESEARCH =====
    {research}

    ===== FINANCIAL =====
    {financial}

    ===== STRATEGY =====
    {strategy}

    Nhiệm vụ của bạn:

    1. Kiểm tra tính logic và sự nhất quán.
    2. Nếu thiếu thông tin quan trọng hoặc không hợp lý → trả về:
       IMPROVE: <lý do cụ thể>

    3. Nếu đầy đủ và hợp lý → trả về JSON hợp lệ theo format:

    {{
      "market_summary": "...",
      "financial_projection": "...",
      "strategy": "...",
      "swot": {{
        "strengths": ["..."],
        "weaknesses": ["..."],
        "opportunities": ["..."],
        "threats": ["..."]
      }}
    }}

    LƯU Ý QUAN TRỌNG VỀ ĐỊNH DẠNG (BẮT BUỘC):
    - Trường "strategy" và "financial_projection" BẮT BUỘC phải là MỘT CHUỖI STRING (String) gom toàn bộ nội dung. TUYỆT ĐỐI KHÔNG chia nhỏ thành các Dictionary/Object lồng nhau (như {{"positioning": "..."}}).
    - Sử dụng ký tự \\n để xuống dòng bên trong chuỗi string nếu cần.
    - Escape (sử dụng dấu \\) cho các dấu ngoặc kép bên trong nội dung văn bản để đảm bảo JSON có thể được parse.
    
    Chỉ trả về:
    - Hoặc "IMPROVE: ..."
    - Hoặc JSON hợp lệ
    Không thêm giải thích ngoài JSON.
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    try:
        result = await chain.ainvoke({
            "research": state["research_report"],
            "financial": state["financial_report"],
            "strategy": state["strategy_report"]
        })
    except Exception as e:
        print(f"====== Vong lap thu {state.get('retry_count')+1} =====")
        return {"critic_feedback": f"Error: {str(e)}",
                "retry_count": state.get("retry_count", 0) + 1}
    
    result = result.content.strip()
    
    print("Critic result:")
    print("=" * 50)
    print(result)
    print("=" * 50)
    if result.upper().startswith("IMPROVE:"):
        print(f"====== Vong lap thu {state.get('retry_count')+1} =====")
        return {"critic_feedback": result,
                "retry_count": state.get("retry_count", 0) + 1}
    
    
    try:
        report = BusinessReport.model_validate_json(result)
        return {"final_report": report.model_dump(),
                "critic_feedback": None}
    except Exception as e:
        print(f"====== Vong lap thu {state.get('retry_count')+1} =====")
        return {"critic_feedback": f"Error: {str(e)}",
                "retry_count": state.get("retry_count", 0) + 1}