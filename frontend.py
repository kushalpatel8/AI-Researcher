import streamlit as st
import uuid
import logging
from ai_researcher2 import INITIAL_PROMPT, graph
from langchain_core.messages import AIMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄")
st.title("📄 Research AI Agent")

# 1. Initialize session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

# Create a unique thread ID per session so LangGraph memory doesn't bleed across page refreshes
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# 2. Render existing chat history so it doesn't disappear on script rerun
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # Log and display user input
    logger.info(f"User input: {user_input}")
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 3. Prepare input: ONLY send the new message (and system prompt on turn 1). 
    # LangGraph's MemorySaver handles the rest!
    messages_to_send = []
    if len(st.session_state.chat_history) == 1: 
        messages_to_send.append({"role": "system", "content": INITIAL_PROMPT})
    messages_to_send.append({"role": "user", "content": user_input})

    chat_input = {"messages": messages_to_send}
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    logger.info("Starting agent processing...")

    # 4. Stream agent response cleanly into a single placeholder
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Use stream_mode="updates" to only get the newest node outputs
        for event in graph.stream(chat_input, config, stream_mode="updates"):
            for node_name, node_state in event.items():
                
                if node_name == "agent":
                    message = node_state["messages"][-1]
                    
                    # Show a nice toast notification if the agent is fetching a tool
                    if getattr(message, "tool_calls", None):
                        for tool_call in message.tool_calls:
                            st.toast(f"🛠️ Agent using tool: {tool_call['name']}")
                    
                    # Append and display text output safely
                    if isinstance(message, AIMessage) and message.content:
                        
                        # Handle standard string content
                        if isinstance(message.content, str):
                            text_content = message.content
                            
                        # Handle list of dictionaries (Gemini's complex block format)
                        elif isinstance(message.content, list):
                            text_content = "".join(
                                block["text"] for block in message.content 
                                if isinstance(block, dict) and "text" in block
                            )
                            
                        # Fallback for anything else
                        else:
                            text_content = str(message.content)
                            
                        full_response += text_content + "\n\n"
                        response_placeholder.markdown(full_response)
                        
                elif node_name == "tools":
                    st.toast("✅ Tool execution complete.")

        # Save final response to history
        if full_response:
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})