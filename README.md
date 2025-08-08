# 🤖 Deep-Search-Agent

DeepSearchAgent is an AI-powered, stateful research assistant that uses Google's Gemini (via OpenAI-style interface) and Tavily's web search API to answer complex questions. It remembers previous queries and adapts its behavior across interactions to provide contextual, helpful responses.

🚀 # Features
🔍 Web Search Integration: Uses the Tavily API to fetch real-time search results.

🧠 Stateful Memory: Remembers previous questions to generate better, context-aware responses.

🤝 Dynamic Instructions: Modifies behavior based on the number of user interactions and past topics.

🔧 Powered by Gemini 2.5 Flash: Uses the latest Gemini model through a compatible OpenAI-style API.

📦 Requirements
Make sure you have the following installed:

Python 3.8+
.env file with:

GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
📂 Project Structure

main.py                # Main entry point
agents/                # AI agent and model utilities
.env                   # Your API keys (not included in version control)
▶️ How to Run
bash
Copy
Edit
# Activate your virtual environment
source venv/bin/activate

# Run the agent
uv run main.py
Then simply type your research questions when prompted.

📘 Credits
Built using openai-functions-agents

Search powered by Tavily

AI models via Gemini

