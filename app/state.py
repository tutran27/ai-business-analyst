from typing import TypedDict, Optional, Dict, Any

class AnalysisState(TypedDict):
    user_query: str

    research_report: Optional[str]
    financial_report: Optional[str]
    strategy_report: Optional[str]

    critic_feedback: Optional[str]

    retry_count: int

    final_report: Optional[Dict[str, Any]]