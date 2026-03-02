from fastapi import FastAPI
from app import services
from app.services import BusinessAIService
from pydantic import BaseModel

app = FastAPI(
    title="Business Analyst API",
    description="API cho hệ thống Multi-Agent phân tích kinh doanh",
    version="1.0.0"
)

analyzer_service = BusinessAIService()

class AnalysisRequest(BaseModel):
    query: str

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    if not request.query:
        return {"status": "error", "message": "Query is required"}
    result = await analyzer_service.analyze(request.query)
    if result["status"] == "success":
        return result
    elif result["status"] == "failed":
        raise HTTPException(status_code=422, detail=result["error"])
    else:
        raise HTTPException(status_code=500, detail="Unknown error")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
