# Import libraries 
from langchain_groq import ChatGroq 
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState 
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import trim_messages
from tools import all_tools

import os 
import sqlite3
import certifi 
from pathlib import Path 
from dotenv import load_dotenv 
load_dotenv() 

# Use Certifi's trusted CA certificates for secure HTTPS connections
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

Path("data").mkdir(exist_ok=True)

# Define models 
DEFAULT_MODEL = os.getenv("GROQ_MODEL","openai/gpt-oss-20b")

ALLOWED_MODEL = {
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b"
}

# Define system prompt
SYSTEM_PROMPT = """
You are a helpful Agentic AI assistant named Dost AI, similar to ChatGPT, Claude, Gemini, etc.

You can:
1. Answer normal questions.
2. Use tools when needed.
3. Search uploaded documents using the retrieve_docs tool.
4. Search the web for latest/current information using Tavily Search.
5. Remember important user information using the remember_chats tool.
6. Recall memory when useful.
7. Use calculator for math.
8. Search and answer questions about YouTube videos using search_youtube_video.

Rules:

- If the user provides his/her name, start the conversation with his/her name or with the word "Bro".

- If the user asks about latest news, current events, recent updates,
  today's information, current prices, current people, current versions,
  new releases, or anything time-sensitive, use Tavily Search.

- If the user asks about an uploaded PDF, DOCX, TXT, Markdown,
  notes, or other uploaded document, use retrieve_docs.

- If the user asks you to remember something, use remember_chats.

- If the user asks about previous preferences or saved facts,
  use recall_memory.

- Use calculator for math questions.

- When using web search, summarize clearly and mention that the answer
  is based on web search results.

YOUTUBE RULE:

- If the user's message contains a YouTube URL and the user asks
  ANYTHING about that video, ALWAYS use search_youtube_video.

- Do NOT answer YouTube questions from your own knowledge.

- Extract the YouTube URL from the user's message and pass it as
  the youtube_url argument.

- Pass the user's actual question about the video as the question argument.

- Do NOT use retrieve_docs for YouTube URLs.

Examples:

User:
"https://www.youtube.com/watch?v=QDLIQ5IL2Bk
What is this video about?"

Action:
Call search_youtube_video with:
youtube_url = "https://www.youtube.com/watch?v=QDLIQ5IL2Bk"
question = "What is this video about?"

User:
"https://www.youtube.com/watch?v=QDLIQ5IL2Bk
Explain the main concept."

Action:
Call search_youtube_video.

User:
"https://www.youtube.com/watch?v=QDLIQ5IL2Bk
What does the speaker say about RAG?"

Action:
Call search_youtube_video.

Be clear, helpful, and concise.
"""

# Check if user provides model is matching or not 
def check_model_name(model_name: str | None) -> str: 
    """ It checks selected model name from frontend.
    If model name is missing or not provided, use DEFAULT_MODEL"""

    if not model_name: 
        return DEFAULT_MODEL 
    
    model_name = model_name.strip()

    if model_name not in ALLOWED_MODEL: 
        return DEFAULT_MODEL 

    return model_name 

# Build agent workflow 
def build_agent(model_name: str):
    """Build a LangGraph agent for a selected Groq model"""

    selected_model = check_model_name(model_name=model_name)

    # define model 
    llm = ChatGroq(model=selected_model, temperature=0.3, streaming=True)

    # define llm tool 
    llm_with_tool = llm.bind_tools(all_tools) 


    # define chat node
    def chat_node(state: MessagesState):
        trimmed_messages = trim_messages(
            state["messages"],
            max_tokens=4000,
            strategy="last",
            token_counter=llm,
            include_system=False,
            start_on="human",
        )
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + trimmed_messages
        response = llm_with_tool.invoke(messages)
        return {"messages": [response]}

    # define tool node
    tool_node = ToolNode(all_tools)

    # define graph 
    graph = StateGraph(MessagesState)

    # add nodes
    graph.add_node("chat_node",chat_node)
    graph.add_node("tools",tool_node)

    # add edges 
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge("tools","chat_node")

    # define sqlite3 connection 
    conn = sqlite3.connect("data/chatbot_checkpoints.sqlite",check_same_thread=False)

    # define checkpoint 
    checkpoint = SqliteSaver(conn)

    # compile graph 
    workflow = graph.compile(checkpointer=checkpoint) 

    # return workflow 
    return workflow


# Create agent cache to reuse agent 
_AGENT_CACHE = {}

def get_agent(model_name:str | None = None): 
    """
    Return cached LangGraph agent for selected model.
    If not created yet, create it once and reuse it.
    """

    selected_model = check_model_name(model_name=model_name)

    if selected_model not in _AGENT_CACHE: 
        _AGENT_CACHE[selected_model] = build_agent(selected_model)

    return _AGENT_CACHE[selected_model]