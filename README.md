# AI-Researcher 📄
AI-Researcher is an autonomous, agentic framework built with LangChain and LangGraph that automates the lifecycle of academic research. The platform allows users to explore specific topics, analyze recent literature from arXiv, and synthesize findings into professional, LaTeX-formatted research papers.

## 🚀 Features
Autonomous Research Agent: A ReAct-based agent that uses reasoning and acting loops to search, read, and write research autonomously.

Literature Discovery: Real-time integration with the arXiv API to find recently published papers in fields like Physics, Computer Science, and Mathematics.

Deep Paper Analysis: Ability to parse XML metadata and read full PDF content to extract key research outcomes and future directions.

AI-Powered Synthesis: Suggests novel research ideas based on identified gaps in existing literature.

LaTeX Document Generation: Automatically writes comprehensive papers including mathematical equations and renders them as professional PDFs.

Interactive Web Interface: A modern Streamlit dashboard with real-time status updates and tool execution tracking.

## 🔄 Application Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Streamlit as Streamlit UI (main.py)
    participant Agent as LangGraph Agent (ai_researcher.py)
    participant Gemini as Google Gemini AI (gemini-2.5-flash)
    participant Arxiv as arXiv API (arxiv_tool.py)
    participant PDFReader as PDF Extractor (read_pdf.py)
    participant PDFEngine as Markdown PDF Engine (write_pdf.py)

    User->>Streamlit: Enter research topic / query in chat
    Streamlit->>Agent: Stream message state to compiled StateGraph (graph.stream)
    Agent->>Gemini: Invoke model with conversation history & bound tools
    
    opt Literature Discovery
        Gemini-->>Agent: Request tool call: arxiv_search(topic)
        Agent->>Arxiv: Query arXiv API & parse XML metadata
        Arxiv-->>Agent: Return paper titles, summaries & PDF URLs
        Agent->>Gemini: Pass arXiv metadata into context
        Gemini-->>Streamlit: Present relevant papers & propose research ideas
        Streamlit-->>User: Display agent response & suggested directions
        User->>Streamlit: Select paper / confirm research topic
        Streamlit->>Agent: Pass selection to Agent
    end

    opt Deep Paper Analysis
        Gemini-->>Agent: Request tool call: read_pdf(url)
        Agent->>PDFReader: Fetch arXiv PDF via HTTP & extract text (PyPDF2)
        PDFReader-->>Agent: Return full extracted text content
        Agent->>Gemini: Provide paper text for analysis & synthesis
    end

    opt Paper Synthesis & PDF Generation
        Gemini->>Gemini: Synthesize findings, formulate novel paper in Markdown
        Gemini-->>Agent: Request tool call: render_markdown_pdf(markdown_content)
        Agent->>PDFEngine: Generate PDF with TOC & styling in /output
        PDFEngine-->>Agent: Return generated PDF file path
        Agent-->>Streamlit: Update session state with PDF path & notify completion
    end

    Streamlit-->>User: Display research summary & activate sidebar download button
    User->>Streamlit: Click "Download Generated Paper (PDF)"
    Streamlit-->>User: Download generated PDF document
```

## 🛠️ Tech Stack
### Framework: LangChain & LangGraph (Stateful Orchestration)

### Core Model: Gemini 2.5 Flash (gemini-2.5-flash)

### Frontend: Streamlit

### Academic Integration: arXiv API

### Document Handling: PyMuPDF & LaTeX

### Configuration: Dotenv & UV (Package Management)

## 📋 Prerequisites
Ensure you have the following installed:

Python (v3.14 or higher)

An active Google Gemini API Key

## ⚙️ Getting Started
Clone the repository:

Bash
git clone <your-repository-url>
cd AI-Researcher
Install dependencies:

Bash
pip install langchain langchain-google-genai streamlit requests python-dotenv
Set up environment variables:
Create a .env file in the root directory and add your API key:

Code snippet
GOOGLE_API_KEY=your_gemini_api_key_here
Run the application:

For Terminal: python ai_researcher.py

For Web Interface: streamlit run main.py

