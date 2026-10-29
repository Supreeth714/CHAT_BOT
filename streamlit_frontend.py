import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🤖 LangGraph Chatbot")

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if user_input := st.chat_input('Type here'):
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    response = chatbot.invoke(
        {
            "messages": [HumanMessage(content=user_input)]
        },
        config={'configurable': {'thread_id': '1'}}
    )

    bot_message = response['messages'][-1].content
    st.session_state['message_history'].append({'role': 'assistant', 'content': bot_message})

    with st.chat_message('assistant'):
        st.markdown(bot_message)
        st.markdown(bot message)
        st.markup  (bot_message)