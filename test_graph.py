from app.graph import create_graph
import asyncio

graph = create_graph()

state = {
    "user_query": "Kinh doanh cà phê ở Việt Nam",
    "research_report": None,
    "financial_report": None,
    "strategy_report": None,
    "critic_feedback": None,
    "final_output": None,
    "retry_count": 0
}

result = asyncio.run(graph.ainvoke(state))

for key, value in result.items():
    if key.lower()=="final_report":
        print(f"\n\n========== FINAL REPORT =========")
        for k, v in result[key].items():
            print(f"\n\n========== {k.upper()} =========")
            print(v)
        
            if k == 'swot':
                print(f"\n\n========== SWOT ANALYSIS =========")
                for kk, vv in result[key][k].items():
                    print(f"\n\n{kk.upper()} : {vv}")
                    
    else:
        print(f"\n\n========== {key.upper()} =========")
        print(value)


