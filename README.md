# 🤖 Dost AI

> An intelligent AI assistant built with LangGraph, LangChain, RAG, FastAPI, and modern LLM technologies.

Dost AI is a ChatGPT-like AI assistant designed to go beyond simple conversations.

It can search the web, understand uploaded documents and YouTube videos, remember important information, perform calculations, and generate images - all through an agentic tool-calling workflow.

Link - ```https://dost-ai-vdxi.onrender.com/```, The app is deployed on Render, it can take some time to open the app.

---

## ✨ Features

### 💬 AI Chat

- Chat with an AI assistant through a simple web interface
- Streaming AI responses
- Multiple conversation threads
- Conversation history
- Context-aware conversations
- Tool-based agent execution

### 🧠 Agentic AI

Dost AI uses **LangGraph** to build an agentic workflow.

Instead of manually deciding which functionality to use, the AI agent can determine which tool is required based on the user's request.

For example:

```text
User: "What are the main points of this YouTube video?"

        ↓

AI Agent
        ↓
YouTube RAG Tool
        ↓
Relevant Content
        ↓
LLM
        ↓
Answer
```


## 🛠️ Tools
Dost AI currently provides the following tools:

| Tool                | Description                                           |
| ------------------- | ----------------------------------------------------- |
| 🧮 Calculator       | Performs mathematical calculations                    |
| 🌐 Web Search       | Searches the web for up-to-date information           |
| 📺 YouTube RAG      | Answers questions about YouTube videos                |
| 📄 Document RAG     | Retrieves information from uploaded documents         |
| 🧠 Memory           | Stores important information for future conversations |
| 🔎 Memory Retrieval | Searches previously stored memories                   |
| 🎨 Image Generation | Generates images from text prompts                    |


# 🏗️ Architecture

High-level architecture of Dost AI:

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Web UI      │
                         │     HTML / JS    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │     Backend      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LangGraph     │
                         │      Agent       │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
       │ Web Search  │     │     RAG     │     │   Memory    │
       └─────────────┘     │   Pipeline  │     │   System    │
                           └──────┬──────┘     └─────────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                   ┌───────────┐     ┌───────────┐
                   │ Documents │     │  YouTube  │
                   └─────┬─────┘     └─────┬─────┘
                         │                 │
                         └────────┬────────┘
                                  │
                                  ▼
                            ┌───────────┐
                            │ ChromaDB  │
                            └───────────┘
```

## 🔄 LangGraph Agent Workflow

The core agent workflow is built using LangGraph.

                    User Message
                         │
                         ▼
                  ┌─────────────┐
                  │  Chat Node  │
                  └──────┬──────┘
                         │
                         ▼
                  Tool Required?
                    /       \
                  Yes        No
                   │          │
                   ▼          ▼
              ┌─────────┐   Response
              │ ToolNode│
              └────┬────┘
                   │
                   ▼
               Chat Node
                   │
                   ▼
                Response


## 🧩 Project Structure

```text
Dost-AI/
│
├── rag/
│   ├── __init__.py
│   ├── loaders.py
│   ├── indexing.py
│   └── retrieval.py
│
├── templates/
│   └── index.html
│
├── data/
├── uploads/
├── generated_images/
├── chroma_db/
│
├── agent.py
├── app.py
├── database.py
├── tools.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── .env.example
├── README.md
└── LICENSE
```


## 📚 What This Project Demonstrates

This project brings together several important concepts in modern AI engineering:

- LLM application development
- Tool calling
- Agentic AI
- LangGraph workflows
- LangChain
- Retrieval-Augmented Generation
- Vector databases
- Embeddings
- YouTube RAG
- Document RAG
- Long-term memory
- Web search
- AI image generation
- Streaming responses
- FastAPI
- Docker

The main goal is to understand how these individual components work together to build a complete AI application rather than treating them as isolated concepts.

## ⭐ If You Like This Project

If you find Dost AI useful or interesting, consider giving the repository a ⭐ on GitHub.

This version is intentionally **only about Dost AI**—no GitHub Actions, no CI/CD pipeline, no Render deployment section.
