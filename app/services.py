from app.graph import create_graph

graph = create_graph()

class BusinessAIService:
    def __init__(self):
        self.graph = graph
    
    async def analyze(self, user_query: str):
        state = {
            "user_query": user_query,
            "research_report": None,
            "financial_report": None,
            "strategy_report": None,
            "critic_feedback": None,
            "final_output": None,
            "retry_count": 0
        }
        
        try:
            print(f"===== Starting analysis for: {user_query} =====")
            result = await self.graph.ainvoke(state)
            
            if result.get("final_report"):
                return {
                    "status": "success",
                    "report": result.get("final_report"),
                    "retry_count": result.get("retry_count", 0)
                }
            else:
                return {
                    "status": "failed",
                    "error": "No final report generated",
                    "retry_count": result.get("retry_count", 0)
                }
        except Exception as e:
            print(f"Error analyzing query: {e}")
            return {
                "status": "error",
                "error": f"An unexpected error occurred: {str(e)}"
            }

if __name__ == "__main__":
    import asyncio
    import json
    print("======== Business AI Service Analysis ========")
    test_query="Thị trường cà phê Việt Nam năm 2025"
    result = asyncio.run(BusinessAIService().analyze(test_query))
    print("======== Analysis Result: ========")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("======== Analysis completed. ========")