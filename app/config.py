from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = "llama-3.1-8b-instant"
    TEMPERATURE: float = 0.7
    MAX_RETRIES: int = 3
    AGENT_TIMEOUT: int = 30
    
settings = Settings()

# Test LLM
if __name__=="__main__":
    print("============= Testing LLM =============")
    print(f"Model: {settings.MODEL_NAME}")
    print(f"Temperature: {settings.TEMPERATURE}")
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_retries=settings.MAX_RETRIES,
        timeout=settings.AGENT_TIMEOUT
    )
    print("============= LLM Response =============")
    test=llm.invoke("Xin chao, ban co the giup toi khong?")
    print(test.content)
    print("============= Testing completed! =============")
