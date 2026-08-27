# import libraries 
from langchain_core.tools import tool 
from langchain_tavily import TavilySearch 
from dotenv import load_dotenv 

import math 
import os 

load_dotenv()

# define calculator tool 
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

# define web search tool 
web_search = TavilySearch(
    max_results = 5, 
    topic = "general",
    search_depth = "advance"
)