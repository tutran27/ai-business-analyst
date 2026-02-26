from langchain_core.prompts import ChatPromptTemplate
from app.agents.base import get_llm
from app.utils import retry_async
import asyncio

llm = get_llm()


@retry_async
async def strategy_agent(state):
    if not state.get("research_report"):
        return {"strategy_report": "Không có báo cáo nghiên cứu"}

    prompt = ChatPromptTemplate.from_template(
        """
        BẠN LÀ CHUYÊN GIA TƯ VẤN CHIẾN LƯỢC KINH DOANH.
        Dựa trên nghiên cứu thị trường sau:
        {research}

        NHIỆM VỤ: Đề xuất chiến lược kinh doanh với 5 mục:
        1. ĐỊNH VỊ THƯƠNG HIỆU
        2. PHÂN KHÚC KHÁCH HÀNG MỤC TIÊU
        3. LỢI THẾ CẠNH TRANH
        4. CHIẾN LƯỢC KHÁC BIỆT HÓA
        5. PHÂN TÍCH SWOT (Trình bày rõ: Điểm mạnh, Điểm yếu, Cơ hội, Thách thức)

        QUY TẮC ĐỊNH DẠNG BẮT BUỘC:
        - TUYỆT ĐỐI KHÔNG DÙNG KÝ TỰ MARKDOWN NHƯ: **, #, _, *, [].
        - CHỈ DÙNG CHỮ IN HOA ĐỂ LÀM TIÊU ĐỀ.
        - DÙNG DẤU GẠCH NGANG "-" ĐỂ LIỆT KÊ CÁC Ý.
        - TRẢ VỀ KẾT QUẢ DƯỚI DẠNG VĂN BẢN THUẦN (PLAIN TEXT).
        - ĐÁNH SỐ THỨ TỰ CHO TỪNG MỤC

        MẪU TRÌNH BÀY MONG MUỐN:
        1. ĐỊNH VỊ THƯƠNG HIỆU
        Nội dung viết tại đây...
        ----------
        2. PHÂN KHÚC KHÁCH HÀNG
        - Ý thứ nhất
        - Ý thứ hai
        ----------
        3. PHÂN TÍCH SWOT
        ĐIỂM MẠNH:
        - Liệt kê tại đây...
        ĐIỂM YẾU:
        - Liệt kê tại đây...
        """
    )

    chain = prompt | llm

    result = await chain.ainvoke({
        "research": state["research_report"]
    })

    # xoa ** markdown
    import re
    clean_content = re.sub(r'[*#_]', '', result.content)
    return {
        "strategy_report": clean_content
    }

# Test Agent
if __name__ == "__main__":
    async def test_strategy_agent():
        result = await strategy_agent({
            "research_report": """
            BÁO CÁO THỊ TRƯỜNG THƯƠNG MẠI ĐIỆN TỬ VIỆT NAM NĂM 2025

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
            Thị trường TMĐT Việt Nam năm 2025 đã đạt được nhiều thành tựu đáng kể, với sự tăng trưởng mạnh mẽ và sự ưu tiên của người Việt đối với chất lượng và giá trị dài hạn."""
        })
        return result
    
    # Run the test
    print("============ Testing strategy agent... ==========")
    result = asyncio.run(test_strategy_agent())
    print(result['strategy_report'])
    print("============ Done Test ===============")
