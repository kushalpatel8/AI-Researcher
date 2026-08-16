import os
from ai_researcher import graph, INITIAL_PROMPT

config = {"configurable": {"thread_id": 333333}}

user_prompt = """I would like to write a research paper on the topic of "Dynamic Resource Provisioning and Cold Start Mitigation in Event-Driven Serverless Functions". 

Please search arXiv for recent papers regarding serverless computing cold starts and dynamic resource provisioning. Based on the recent literature, propose a novel angle for a new paper, write the full research paper (including an abstract, introduction,research gap, methodology, conclusion and Referance), and finally render it into a PDF for me."""

messages_to_send = [
    {"role": "system", "content": INITIAL_PROMPT},
    {"role": "user", "content": user_prompt}
]
chat_input = {"messages": messages_to_send}

print("Running research agent...")
for s in graph.stream(chat_input, config, stream_mode="values"):
    message = s["messages"][-1]
    
    if getattr(message, "tool_calls", None):
        for tool_call in message.tool_calls:
            print(f"\n[Tool call: {tool_call['name']}]")
            print(tool_call)
    else:
        content = message.content
        if isinstance(content, list):
            text_content = "".join([
                block.get("text", "") 
                for block in content 
                if isinstance(block, dict) and block.get("type") == "text"
            ])
        else:
            text_content = str(content) 
            
        if text_content:
            print(f"\n[Assistant Message Length: {len(text_content)} chars]")
            print(text_content[:200] + ("..." if len(text_content) > 200 else ""))
            
print("\nFinished execution. The PDF should be in the output/ directory.")
