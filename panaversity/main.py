# State-less Bot

# import os
# import asyncio
# from dotenv import load_dotenv
# from agents import (
#     Agent, Runner,
#     OpenAIChatCompletionsModel, AsyncOpenAI,
#     set_tracing_disabled, ModelSettings,
#     ItemHelpers, function_tool
# )
# from tavily import TavilyClient

# # 🌱 Load .env and setup
# load_dotenv()
# set_tracing_disabled(True)

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# # Initialize Tavily client
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# print(f"TAVILY_API_KEY loaded? {bool(os.getenv('TAVILY_API_KEY'))}")
# tavily = TavilyClient(api_key=TAVILY_API_KEY)


# # 🔌 Gemini client
# external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
# model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# # 🧰 Tools
# # @function_tool
# # async def search(query: str) -> str:
# #     """Simulated deep search tool"""
# #     return f"🔍 Results for '{query}' :"

# @function_tool
# async def search(query: str) -> str:
#     """Use Tavily to get web search results for the query."""
#     results = tavily.search(query=query, max_results=5)

#     if not results or not results.get("results"):
#         return "No relevant results found."

#     output = "🔍 Top search results:\n"
#     for idx, r in enumerate(results["results"], start=1):
#         output += f"{idx}. [{r['title']}]({r['url']})\n"

#     return output

# # 🧠 Base Agent Setup
# base_agent = Agent(
#     name="DeepSearchAgent",
#     instructions="You are an advanced research assistant. Use the 'search' tool to answer complex technical questions.",
#     tools=[search],
#     model=model,
#     model_settings=ModelSettings(temperature=0.4)
# )

# async def main():
#     print("🤖 DeepSearchAgent is ready! Type 'exit' to quit.\n")
    
#     while True:
#         try:
#             question = input("❓ Ask your research question: ").strip()
#             if question.lower() in ("exit", "quit"):
#                 print("👋 Goodbye!")
#                 break

#             print("\n💬 DeepSearchAgent is thinking...\n")
#             result = Runner.run_streamed(starting_agent=base_agent, input=question)

#             async for event in result.stream_events():
#                 if hasattr(event, "item") and event.item is not None:
#                     if event.item.type == "tool_call_output_item":
#                         print(f"🔧 Tool output:\n{event.item.output}\n")
#                     elif event.item.type == "message_output_item":
#                         print(f"🧠 Agent says:\n{ItemHelpers.text_message_output(event.item)}\n")

#         except (KeyboardInterrupt, EOFError):
#             print("\n👋 Session ended.")
#             break

# # 🏁 Entry
# if __name__ == "__main__":
#     asyncio.run(main())

# Statefull Bot
import os
import asyncio
from dotenv import load_dotenv
from agents import (
    Agent, Runner,
    OpenAIChatCompletionsModel, AsyncOpenAI,
    set_tracing_disabled, ModelSettings,
    ItemHelpers, function_tool, RunContextWrapper
)
from tavily import TavilyClient

# 🌱 Load .env and setup
load_dotenv()
set_tracing_disabled(True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Initialize Tavily client
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
print(f"TAVILY_API_KEY loaded? {bool(os.getenv('TAVILY_API_KEY'))}")
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# 🔌 Gemini client
external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# 🧰 Tools
@function_tool
async def search(query: str) -> str:
    """Use Tavily to get web search results for the query."""
    results = tavily.search(query=query, max_results=5)

    if not results or not results.get("results"):
        return "No relevant results found."

    output = "🔍 Top search results:\n"
    for idx, r in enumerate(results["results"], start=1):
        output += f"{idx}. [{r['title']}]({r['url']})\n"

    return output

# 🧠 Stateful Agent Setup
class StatefulAgent:
    def __init__(self):
        self.interaction_count = 0
        self.previous_queries = []
        
    def get_instructions(self, context: RunContextWrapper, agent: Agent) -> str:
        self.interaction_count += 1
        messages = getattr(context, 'messages', [])
        
        # Basic instruction
        instruction = f"""You are {agent.name}, an advanced research assistant. 
        This is interaction #{self.interaction_count}."""
        
        # Add context if we have previous queries
        if len(self.previous_queries) > 0:
            instruction += "\n\nPrevious topics we've discussed:\n"
            for idx, query in enumerate(self.previous_queries, 1):
                instruction += f"{idx}. {query}\n"
            instruction += "\nBuild on our previous conversations when relevant."
        
        # First interaction special case
        if self.interaction_count == 1:
            instruction = "You are a research assistant. This is our first interaction - be welcoming and explain how you can help!"
        
        return instruction

# Create stateful instruction generator
stateful_instructions = StatefulAgent()

# 🧠 Base Agent Setup
base_agent = Agent(
    name="DeepSearchAgent",
    instructions=lambda context, agent: stateful_instructions.get_instructions(context, agent),
    tools=[search],
    model=model,
    model_settings=ModelSettings(temperature=0.4)
)

async def main():
    print("🤖 DeepSearchAgent is ready! Type 'exit' to quit.\n")
    
    while True:
        try:
            question = input("❓ Ask your research question: ").strip()
            if question.lower() in ("exit", "quit"):
                print("👋 Goodbye!")
                break

            # Store the question before processing
            if question.lower() not in ("", "hi", "hello"):
                stateful_instructions.previous_queries.append(question)

            print("\n💬 DeepSearchAgent is thinking...\n")
            result = Runner.run_streamed(starting_agent=base_agent, input=question)

            async for event in result.stream_events():
                if hasattr(event, "item") and event.item is not None:
                    if event.item.type == "tool_call_output_item":
                        print(f"🔧 Tool output:\n{event.item.output}\n")
                    elif event.item.type == "message_output_item":
                        print(f"🧠 Agent says:\n{ItemHelpers.text_message_output(event.item)}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n👋 Session ended.")
            break

# 🏁 Entry
if __name__ == "__main__":
    asyncio.run(main())
