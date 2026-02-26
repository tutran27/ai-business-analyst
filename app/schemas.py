from pydantic import BaseModel
from typing import List

class SWOT(BaseModel):
    strengths: List[str]       # Điểm mạnh
    weaknesses: List[str]      # Điểm yếu
    opportunities: List[str]   # Cơ hội
    threats: List[str]         # Thách thức

class BusinessReport(BaseModel):
    market_summary: str         # Tóm tắt thị trường
    financial_projection: str   # Dự báo tài chính
    swot: SWOT                  # SWOT analysis
    strategy: str               # Đề xuất chiến lược

# Test class
if __name__=="__main__":
    print("============= Testing BusinessReport =============")
    sample= {
        "market_summary": "Thị trường đang phát triển mạnh với nhu cầu tăng cao",
        "financial_projection": "Dự báo doanh thu tăng 20% trong 5 năm tới",
        "swot": {
            "strengths": ["Địa điểm thuận lợi", "Đội ngũ nhân sự chuyên nghiệp"],
            "weaknesses": ["Chi phí vận hành cao", "Thiếu kinh nghiệm quốc tế"],
            "opportunities": ["Mở rộng thị trường châu Á", "Hợp tác với đối tác nước ngoài"],
            "threats": ["Cạnh tranh gay gắt", "Biến động thị trường"]
        },
        "strategy": "Tập trung phát triển thị trường châu Á và tăng cường hợp tác quốc tế"
    }
    try:
        report = BusinessReport.model_validate_json(sample)
        print("Report created successfully!")
        print(report)
    except Exception as e:
        print(f"Error: {e}")

   
