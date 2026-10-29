import streamlit as st
from langgraph_backend_database_sqlite import chatbot , retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid


st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🤖 LangGraph Chatbot")



#***********utility functions***************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = [] 
    add_thread(thread_id)
    

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


#***********Session setup***************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    


if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
    

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = str(generate_thread_id())
    add_thread(st.session_state['thread_id'])




#****sidebar***** 

st.sidebar.title("LangGraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Chats")

for thread_id in st.session_state.get('chat_threads', []):
    if st.sidebar.button(f"Chat {thread_id}"):
        st.session_state['thread_id'] = thread_id
        messages= load_conversation(thread_id)
        
        temp_message_history = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                temp_message_history.append({'role': 'user', 'content': message.content})
            elif isinstance(message, AIMessage):
                temp_message_history.append({'role': 'assistant', 'content': message.content})
        st.session_state['message_history'] = temp_message_history

 # ***********Main Chat Interface  // MAIN UI ***************


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        
user_input = st.chat_input('Type here')
if user_input :
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)


    CONFIG={'configurable': {'thread_id': st.session_state['thread_id']}}


    # bot_message = response['messages'][-1].content
    # st.session_state['message_history'].append({'role': 'assistant', 'content': bot_message})

    with st.chat_message('assistant'):
        bot_message= st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {
                    "messages": [HumanMessage(content=user_input)]
                },
                config=CONFIG,
                stream_mode='messages'
                
            ) 
        )

        st.session_state['message_history'].append({'role': 'assistant', 'content': bot_message})