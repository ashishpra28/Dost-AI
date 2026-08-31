# Import libraries 
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from .loaders import load_documents_pipeline

# Define embedding model 
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector store 
vector_store = Chroma(
    collection_name="Dost_AI_Collections",
    embedding_function=embedding_model,
    persist_directory="chroma_db"
)

# Split documents 
def split_doc(documents, thread_id: str, source: str):
    """Split documents and add metadata."""

    if not documents:
        raise ValueError(
            "No readable content found in document."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    # Add metadata to every chunk
    for chunk in chunks:
        chunk.metadata["thread_id"] = thread_id
        chunk.metadata["source"] = source

    return chunks

# Add documents to vector store 
def add_docs_to_vector_store(chunks):
    """Add chunks to Chroma."""

    if not chunks:
        raise ValueError(
            "No valid chunks found."
        )

    vector_store.add_documents(chunks)

# Create final indexing pipeline 
def indexing_pipeline(source: str, thread_id: str):
    """Complete document indexing pipeline."""

    # 1. Load document
    documents = load_documents_pipeline(source)

    # 2. Split document + add metadata
    chunks = split_doc(
        documents,
        thread_id,
        source
    )

    # 3. Store chunks in Chroma
    add_docs_to_vector_store(chunks)

    return {
        "source": source,
        "chunks": len(chunks),
        "thread_id": thread_id
    }