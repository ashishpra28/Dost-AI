# Import libraries
from pathlib import Path 
from urllib.parse import urlparse, parse_qs 
from langchain_community.document_loaders import PyPDFLoader, TextLoader,WebBaseLoader,Docx2txtLoader
from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from langchain_core.documents import Document


# Create detect source type function
def detect_source_type(source):
    """Detect whether the source is YouTube, website, or file."""

    # for youtube 
    if ("youtube.com" in source):
        return "Youtube"
    
    # for website 
    elif source.startswith("http"):
        return "Website"
    else:
        suffix = Path(source).suffix.lower()

    # for pdf 
    if suffix == ".pdf":
        return "pdf"
    
    # for txt 
    elif suffix == ".txt":
        return "txt"

    # for md 
    elif suffix == ".md":
        return "markdown"
    
    # for csv
    elif suffix == ".csv":
        return "csv"
    
    # for unsupported 
    else:
        raise ValueError("Unsupported source type")

# Extract video id
def extract_video_id(url):
    """Extract YouTube video ID"""

    if "youtu.be" in url:
        return url.split("/")[-1]
    return parse_qs(urlparse(url).query)["v"][0]
    
# Create youtube transcript loader 
def load_youtube(source):
    """Load youtube transcript"""

    # video id 
    video_id = extract_video_id(source)
    try:
        # fetch transcript 
        api = YouTubeTranscriptApi()
        transcript_chunks = api.fetch(video_id=video_id,languages=["en-IN", "en", "hi"])
        transcript = " ".join(chunk.text for chunk in transcript_chunks)
        
        # convert transcript to documents
        documents = [Document(page_content=transcript,metadata={"source":source})]
        return documents
    
    except TranscriptsDisabled:
        raise ValueError("No captions available for this video")

# Create website loader 
def load_website(source):
    """Load website content"""
    loader = WebBaseLoader(source)
    documents = loader.load()
    return documents

# Create pdf loader 
def load_pdf(source):
    """Load pdf documents"""
    loader = PyPDFLoader(source)
    documents = loader.load()
    return documents

# Create docs loader
def load_docx(source: str):
    """Load DOCX document."""
    loader = Docx2txtLoader(source)
    return loader.load()

# Create text loader 
def load_text(source):
    """Load text based files"""
    loader = TextLoader(source,encoding="utf-8")
    documents = loader.load()
    return documents

# Create final load documents pipeline 
def load_documents_pipeline(source):
    """Load documents from any supported source."""

    source_type = detect_source_type(source)
    if source_type == "Youtube":
        return load_youtube(source)
    elif source_type == "Website":
        return load_website(source)
    elif source_type == "pdf":
        return load_pdf(source)
    elif source_type == "docx":
        return load_docx(source)
    elif source_type in ["txt","markdown","csv"]:
        return load_text(source)
    else:
        raise ValueError("Unsupported source")