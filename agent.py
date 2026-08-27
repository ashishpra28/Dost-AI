# import libraries 
from langchain_groq import ChatGroq 
from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from langchain_core.tools import tool 

from langgraph.graph import StateGraph, START, END, MessagesState 
from typing import TypedDict, Annotated 
from langgraph.graph.message import add_messages 
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
defualt_model = os.getenv("GROQ_MODEL","openai/gpt-oss-120b")

allowed_models = {
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "qwen/qwen3.6-27b"
}

