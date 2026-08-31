# Import libraries 
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma 
from .indexing import vector_store 

# Define retriever function 
def retriever_pipeline(query:str,thread_id:str, k: int=4): 
    docs = vector_store.similarity_search(query=query, k=k, filter={
        "thread_id":thread_id
    })
    """Retrieve relevant chunks for a conversation."""

    if not docs: 
        return "No relevant uploaded document content found."

    results = []

    for i,docs in enumerate(docs, start=1):
        source = docs.metadata.get(
            "source",
            "uploaded document"
        )

        results.append(
            f"[Source {i}: {source}]\n"
            f"{docs.page_content}"
        )

    return "\n\n".join(results)