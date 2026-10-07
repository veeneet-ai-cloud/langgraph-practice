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


def parse_stream_chunk(stream):
    for message_chunk, metadata in stream:
        content = message_chunk.content
        
        # If content is a list of blocks/dictionaries
        if isinstance(content, list) and len(content) > 0:
            block = content[0]
            if isinstance(block, dict):
                yield block.get('text', '')
            else:
                yield getattr(block, 'text', '')
        # If content is already a plain string
        elif isinstance(content, str):
            yield content

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    
    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            parse_stream_chunk(
                chatbot.stream(
                    {'messages': [HumanMessage(content=user_input)]},
                    config=CONFIG,
                    stream_mode='messages'
                )
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})