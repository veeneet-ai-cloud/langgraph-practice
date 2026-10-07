import streamlit as st

from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    # ai_message = response['messages'][-1].content[0]
    messages = response.get('messages', []) if isinstance(response, dict) else getattr(response, 'messages', [])
    last_msg = messages[-1] if messages else None

    ai_message = ""
    if last_msg:
        # 2. Get the 'content' attribute (or dict key)
        content = getattr(last_msg, 'content', None) or (last_msg.get('content') if isinstance(last_msg, dict) else None)
        
        # 3. Handle list of blocks vs string
        if isinstance(content, list) and len(content) > 0:
            first_block = content[0]
            if isinstance(first_block, dict):
                ai_message = first_block.get('text', '')
            else:
                ai_message = getattr(first_block, 'text', '')
        elif isinstance(content, str):
            ai_message = content

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)