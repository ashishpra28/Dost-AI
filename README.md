# 🤖 Dost AI

> An intelligent AI assistant built with LangGraph, LangChain, RAG, FastAPI, and modern LLM technologies.

Dost AI is a ChatGPT-like AI assistant designed to go beyond simple conversations.

It can search the web, understand uploaded documents and YouTube videos, remember important information, perform calculations, and generate images — all through an agentic tool-calling workflow.

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
User: "What is 25 × 48?"

        ↓

AI Agent
        ↓
Calculator Tool
        ↓
Result