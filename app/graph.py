from app.agents.research import research_agent
from app.agents.financial import financial_agent
from app.agents.strategy import strategy_agent
from app.agents.critic import critic_agent
from app.state import AnalysisState
from langgraph.graph import StateGraph, END
from app.config import settings

def create_graph():
    builder = StateGraph(AnalysisState)
    
    builder.add_node("research", research_agent)
    builder.add_node("financial", financial_agent)
    builder.add_node("strategy", strategy_agent)
    builder.add_node("critic", critic_agent)
    
    builder.set_entry_point("research")
    builder.add_edge("research", "financial")
    builder.add_edge("research", "strategy")

    builder.add_edge(["financial", "strategy"], "critic")
    
    def decided(state):
        # Nếu đã đạt giới hạn retry, kết thúc
        if state.get("retry_count", 0) >= settings.MAX_RETRIES:
            return END
        
        # Nếu critic_feedback là None hoặc đã có final_report, kết thúc
        if state.get("critic_feedback") is None:
            return END
        else:
            # Có feedback cần cải thiện, quay lại research
            return "research"
    
    builder.add_conditional_edges("critic", decided, {
        "research": "research",
        END: END
    })
    
    return builder.compile()
