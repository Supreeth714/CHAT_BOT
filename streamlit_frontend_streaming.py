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

   

    # bot_message = response['messages'][-1].content
    # st.session_state['message_history'].append({'role': 'assistant', 'content': bot_message})

    with st.chat_message('assistant'):
       bot_message= st.write_stream(
           message_chunk.content for message_chunk,metadata in chatbot.stream(
               {
                "messages": [HumanMessage(content=user_input)]
               },
               config={'configurable': {'thread_id': '1'}},
               stream_mode='messages'
               
           )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': bot_message})