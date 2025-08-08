from agents import RunContextWrapper, Agent
from context import UserContext

def dynamic_prompt(ctx: RunContextWrapper[UserContext], agent: Agent) -> str:
    return (
        f"You are a research assistant called {agent.name}. "
        f"The user is {ctx.context.username}. "
        "You have access to web search. Use it to answer complex research queries."
    )
