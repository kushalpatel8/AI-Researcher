# AI-Researcher
AI-Researcher is an autonomous agentic framework designed to assist researchers in identifying, analyzing, and synthesizing academic literature. Built using LangChain and LangGraph, the agent interacts with the arXiv API to find recent papers, reads their content, and generates new research directions or even full research papers rendered in LaTeX PDF format.

Features
Automated Literature Search: Queries the arXiv API to find the most recent papers in fields like Physics, Mathematics, Computer Science, and Economics.

Intelligent Paper Analysis: Uses a ReAct agent graph to read and understand the contents of selected research papers.

Research Synthesis: Identifies promising future research directions based on current findings.

LaTeX Generation: Automatically writes new research papers, including mathematical equations, and renders them as professional PDFs.

Interactive Frontend: Includes a Streamlit-based web interface for real-time interaction with the research agent.

Project Structure
ai_researcher.py: The core logic for setting up the LangGraph ReAct agent and the initial research prompt.

arxiv_tool.py: Custom tool for searching and parsing XML data from the arXiv API.

frontend.py: A Streamlit application providing a chat interface for the agent.

read_pdf.py & write_pdf.py: Utility scripts for processing input papers and generating LaTeX-based research outputs.

pyproject.toml: Project metadata and dependency specifications.

Getting Started
Prerequisites
Python >= 3.14

A Google Gemini API Key (stored in a .env file as GOOGLE_API_KEY)

Installation
Clone the repository:

Bash
git clone <repository-url>
cd ai-researcher
Install dependencies:
The project uses uv or standard pip. Dependencies include langchain, langchain-google-genai, requests, and streamlit.

Bash
pip install langchain langchain-community langchain-core langchain-google-genai requests streamlit
Environment Setup:
Create a .env file in the root directory:

Code snippet
GOOGLE_API_KEY=your_actual_api_key_here
Usage
Running the Terminal Agent
To interact with the researcher directly via the command line:

Bash
python ai_researcher.py
Running the Web Interface
To launch the Streamlit dashboard:

Bash
streamlit run frontend.py
How It Works
Topic Selection: The user provides a research topic.

Discovery: The agent searches arXiv for recent relevant publications.

Deep Dive: The agent reads a selected paper to identify gaps and future work.

Proposal: It suggests new research ideas for the user to approve.

Writing: Once an idea is selected, the agent writes a full paper and exports it to PDF.
