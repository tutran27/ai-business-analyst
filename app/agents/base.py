from app.config import settings
from langchain_groq import ChatGroq

def get_llm():
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_retries=settings.MAX_RETRIES,
        timeout=settings.AGENT_TIMEOUT
    )
    return llm

# Initialize LLM
llm = get_llm()
print(f"================= LLM Calling =================")
print(f"Model: {settings.MODEL_NAME}")
print(f"Temperature: {settings.TEMPERATURE}")
print(f"================= LLM initialized successfully =================")

# Test LLM
if __name__=="__main__":
    print("Testing LLM...")
    llm = get_llm()
    test = llm.invoke("Xin chao, ban co the giup toi khong?")
    print("LLM Response:")
    print(test.content)
    print("============= Testing completed! =============")

