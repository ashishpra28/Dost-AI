# Import libraries 
from langchain_groq import ChatGroq 
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState 
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

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
DEFAULT_MODEL = os.getenv("GROQ_MODEL","openai/gpt-oss-120b")

ALLOWED_MODEL = {
    "openai/gpt-oss-20b",
    "qwen/qwen3.6-27b"
}

# System prompt
SYSTEM_PROMPT = """
You are a helpful Agentic AI assistant named Dost AI similar to ChatGPT, Claude, Gemini, etc....

You can:
1. Answer normal questions.
2. Use tools when needed.
3. Search uploaded documents using the RAG tool.
4. Search the web for latest/current information using Tavily Search.
5. Remember important user information using the memory tool.
6. Recall memory when useful.
7. Use calculator for math.

Rules:
- If the user provides his/her name start the conversation with his/her name or with a word 'Bro'.
- If the user asks about latest news, current events, recent updates, today's information, current prices, current people, current versions, new releases, or anything time-sensitive, use Tavily Search.
- If the user asks about an uploaded document, use search_uploaded_documents.
- If the user asks you to remember something, use remember_this.
- If the user asks about previous preferences or saved facts, use recall_memory.
- Use calculator for math questions.
- When using web search, summarize clearly and mention that the answer is based on web search results.
- Be clear, helpful, and concise.
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
    def chat_node(state:MessagesState): 
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        response = llm_with_tool.invoke(messages)
        return {"messages":[response]}

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