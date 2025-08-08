from agents import function_tool, RunContextWrapper
from context import UserContext
import time

@function_tool()
async def search(ctx: RunContextWrapper[UserContext], query: str) -> str:
    time.sleep(1)  # Simulate delay
    return f"Search results for '{query}' :"
