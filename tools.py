# Import libraries 
from langchain_core.tools import tool 
from langchain_tavily import TavilySearch 
from dotenv import load_dotenv 
from database import save_memory, search_memory 
from rag.retrieval import retriever_pipeline 

import math 
import os 

load_dotenv()

# Define current thread id 
CURRENT_THREAD_ID = "default"

def set_current_thread_id(thread_id:str): 
    global CURRENT_THREAD_ID 
    CURRENT_THREAD_ID = thread_id 

# Define calculator tool 
@tool 
def calculator(expression:str): 
    """
    This tool perform mathematical calculations by taking the expression from the user. 
    Useful for simple and intermediate mathematical calculations. 
    Input should be a valid math expression. 
    Example: 2+2, math.sqrt(16), 10*5
    """

    try:
        allowed = {
            "math": math,
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum
        }

        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)

    except Exception as e:
        return f"Calculation error: {str(e)}"

# Define web search tool 
web_search = TavilySearch(
    max_results = 5, 
    topic = "general",
    search_depth = "fast"
)

# Define tool for remembering chats
@tool
def remember_chats(memory: str) -> str:
    """
    Save an important user preference or fact into long-term memory.
    Use this when the user asks you to remember something.
    """

    return save_memory(
        thread_id=CURRENT_THREAD_ID,
        memory=memory
    )


# Define tool for recalling memory
@tool
def recall_memory(query: str) -> str:
    """
    Recall saved long-term memories about the user or this conversation.
    """

    return search_memory(
        thread_id=CURRENT_THREAD_ID,
        query=query
    )

# Define retriever tool 
@tool 
def retrieve_docs(query:str): 
    """
    Search uploaded documents for relevant information.
    Use this when the user asks about uploaded YouTube links, PDFs, DOCX, TXT, notes, files, or documents.
    """

    return retriever_pipeline(
        query=query,
        thread_id=CURRENT_THREAD_ID
    )

# Create all tools list 
all_tools = [
    calculator,
    web_search,
    remember_chats,
    recall_memory,
    retrieve_docs
]