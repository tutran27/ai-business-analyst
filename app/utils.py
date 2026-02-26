import asyncio
from app.config import settings

def retry_async(agent_function):
    async def wrapper(state):
        for attempt in range(settings.MAX_RETRIES):
            try:
                result = await asyncio.wait_for(agent_function(state), 
                                              timeout=settings.AGENT_TIMEOUT)
                return result
            except Exception as e:
                state['retry_count'] +=1
                if state['retry_count'] == settings.MAX_RETRIES -1:
                    raise e
    return wrapper

