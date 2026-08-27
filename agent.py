# import libraries 
from langchain_groq import ChatGroq 
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool 

from langgraph.graph import StateGraph, START, END, MessagesState 
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

import os 
import sqlite3
import certifi 
from pathlib import Path 
from dotenv import load_dotenv 
load_dotenv() 

# Use Certifi's trusted CA certificates for secure HTTPS connections
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# define state 
class ChatState(MessagesState): 
    messages : Annotated[list[BaseMessage],add_messages]

Path("data").mkdir(exist_ok=True)

# define models 
DEFAULT_MODEL = os.getenv("GROQ_MODEL","openai/gpt-oss-120b")

ALLOWED_MODEL = {
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "qwen/qwen3.6-27b"
}

# system prompt
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

# check if user provides model is matching or not 
def check_model_name(model_name: str | None) -> str: 
    """ It checks selected model name from frontend.
    If model name is missing or not provided, use DEFAULT_MODEL"""

    if not model_name: 
        return DEFAULT_MODEL 
    
    model_name = model_name.strip()

    if model_name not in ALLOWED_MODEL: 
        return DEFAULT_MODEL 

    return model_name 

# build agent workflow 
def build_agent(model_name: str); 
    """Build a LangGraph agent for a selected Groq model"""

    selected_model = check_model_name(model_name=model_name)

    # define model 
    llm = ChatGroq(model=model_name, temperature=0.3, streaming=True)

    # define llm tool 
    llm_with_tool = llm.bind_tools(tools) 

    # define chat node 
    def chat_node(state:MessagesState): 
        messages : Annotated[list[BaseMessage],add_messages]