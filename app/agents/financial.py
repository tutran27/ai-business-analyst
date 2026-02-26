from langchain_core.prompts import ChatPromptTemplate

from app.agents.base import get_llm
from app.utils import retry_async

import asyncio

@retry_async
async def financial_agent(state):
    if not state.get('research_report'):
        return {"financial_report": "Không có báo cáo nghiên cứu"}
    
    template = """
    Bạn là một nhà phân tích tài chính cấp cao.
    Dựa trên nghiên cứu thị trường sau: {research_report}

    NHIỆM VỤ: Cung cấp chi phí, dự báo doanh thu, điểm hòa vốn và rủi ro.

    YÊU CẦU ĐỊNH DẠNG NGHIÊM NGẶT:
    1. CHỈ TRẢ VỀ PLAIN TEXT (VĂN BẢN THUẦN).
    2. TUYỆT ĐỐI KHÔNG dùng các ký tự: **, #, _, *.
    3. Dùng dấu gạch đầu dòng duy nhất là "-" cho các ý nhỏ.
    4. Tiêu đề mục viết HOA toàn bộ để phân biệt.

    Ví dụ:
    GIỚI THIỆU
    Dựa trên báo cáo...

    1. CHI PHÍ KHỞI NGHIỆP
    - Chi phí ban đầu: 1 tỷ
    ----------
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = get_llm()
    chain = prompt | llm
    financial_report = await chain.ainvoke({"research_report": state.get('research_report', '')})
    financial_report = financial_report.content.strip()
    # xoa ** markdown
    import re
    clean_content = re.sub(r'[*#_]', '', financial_report)
    return {"financial_report": clean_content}

# Test Agent
if __name__ == "__main__":
    async def test_financial_agent():
        result = await financial_agent({
            "research_report": """BÁO CÁO THỊ TRƯỜNG THƯƠNG MẠI ĐIỆN TỬ VIỆT NAM NĂM 2025

            1. TỔNG QUAN THỊ TRƯỜNG
            Thị trường thương mại điện tử (TMĐT) Việt Nam năm 2025 đã đạt kỷ lục doanh thu mới với sự tăng trưởng mạnh mẽ, đặc biệt là sự thống trị của các gian hàng chính hãng và xu hướng sẵn sàng mua sắm sản phẩm giá trị cao.

            2. SỐ LIỆU QUAN TRỌNG
            - Tổng doanh số trên 4 sàn TMĐT lớn nhất Việt Nam ước đạt 429.660 tỉ đồng, tăng 34.75% so với năm 2024.   
            - Doanh thu từ gian hàng chính hãng của Lazada đạt 59,7%, cao nhất thị trường.
            - Giá trị đơn hàng trung bình của Lazada cao nhất, cho thấy vị thế vững chắc trong nhóm khách hàng cao cấp.

            3. XU HƯỚNG CHÍNH
            - Sự thống trị của các thương hiệu công nghệ, đặc biệt là Apple với doanh số cao nhất năm.
            - Sự trỗi dậy của nhóm hàng chính hãng (Shop Mall), cho thấy người Việt ưu tiên chất lượng và giá trị dài hạn.

            4. KẾT LUẬN
            Thị trường TMĐT Việt Nam năm 2025 đã đạt được nhiều thành tựu đáng kể, với sự tăng trưởng mạnh mẽ và sự ưu tiên của người Việt đối với chất lượng và giá trị dài hạn. """})
                    
        return result
    
    # Run the test
    print("============ Testing financial agent... ==========")
    result = asyncio.run(test_financial_agent())
    print(result['financial_report'])
    print("============ Done Test ===============")

