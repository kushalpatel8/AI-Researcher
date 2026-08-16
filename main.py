import streamlit as st
from ai_researcher import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄")
st.title("📄 Research AI Agent")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

with st.sidebar:
    st.header("Downloads")
    if st.session_state.pdf_path and Path(st.session_state.pdf_path).exists():
        with open(st.session_state.pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Generated Paper (PDF)",
                data=pdf_file,
                file_name=Path(st.session_state.pdf_path).name,
                mime="application/pdf"
            )
    else:
        st.write("No PDF generated yet.")

# --- FIX 1: Render existing chat history on every Streamlit rerun ---
for message in st.session_state.chat_history:
    st.chat_message(message["role"]).write(message["content"])

# Chat interface
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # Log and display user input
    logger.info(f"User input: {user_input}")
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # --- FIX 2: Prevent LangGraph memory duplication ---
    # Since MemorySaver tracks the thread, we only pass the SYSTEM prompt 
    # on the very first turn, and then only pass the NEW user input.
    messages_to_send = []
    if len(st.session_state.chat_history) == 1:
        messages_to_send.append({"role": "system", "content": INITIAL_PROMPT})
    messages_to_send.append({"role": "user", "content": user_input})
    
    chat_input = {"messages": messages_to_send}
    logger.info("Starting agent processing...")

    full_response = ""
    
    # Use a placeholder to cleanly update the agent's text 
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        for s in graph.stream(chat_input, config, stream_mode="values"):
            message = s["messages"][-1]
            
            # Handle tool calls (log only)
            if getattr(message, "tool_calls", None):
                for tool_call in message.tool_calls:
                    logger.info(f"Tool call: {tool_call['name']}")
                    
            # Capture the PDF output path
            if getattr(message, "type", None) == "tool" and message.name == "render_markdown_pdf":
                st.session_state.pdf_path = message.content
                st.session_state.chat_history.append({"role": "assistant", "content": "Your Research paper Generated in proffessional way"})
                # Trigger a rerun to show the download button in the sidebar immediately
                st.rerun()
            
            # Handle assistant response
            if isinstance(message, AIMessage) and message.content:
                
                # --- FIX 3: Parse Gemini's list/dict output format ---
                if isinstance(message.content, list):
                    # Extract the actual text from the list of blocks
                    text_content = "".join([
                        block.get("text", "") 
                        for block in message.content 
                        if isinstance(block, dict) and block.get("type") == "text"
                    ])
                else:
                    text_content = str(message.content) 
                
                # stream_mode="values" outputs the whole state per node execution.
                # Update the placeholder with the current text rather than concatenating it.
                if text_content:
                    full_response = text_content
                    response_placeholder.write(full_response)
                
    # Add final response to history
    if full_response:
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})