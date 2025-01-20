import streamlit as st

import os

from streamlit_chat import message
from streamlit_mic_recorder import speech_to_text
# from chatbot import gen_chatbot_response
from huggingface_hub import InferenceClient
import random
# import token_temp

client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct",
    token=os.environ["TOKEN_BOT"],
)
def gen_chatbot_response(messages: list):
    arr_err = ["Phi không hiểu ý của bạn", 
               "Bạn có thể hỏi câu khác không?", 
               "Vui lòng thử lại sau", "Hệ thống không hoạt động"]
    text = arr_err[random.randint(0,3)]
    result = client.chat_completion(
        messages=messages,
        max_tokens=500,
        # temperature = 0.4,
        # top_p = 0.5,
       tool_prompt = messages[-1]['content']
    )
    if result:
        text = result.choices[0].message.content
    return text

def flow_response(user_input):
    if not user_input:
        return
    else:
        st.session_state.past.append(user_input)
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input
        })
        with st.spinner(text="Đang trả lời..."):
            response = gen_chatbot_response(st.session_state.messages)
        st.session_state.generated.append(response)
        st.session_state.messages.append({
            "role": "system",
            "content": response
        })
        st.session_state.input_text = None
        st.toast("Tuyệt vời, bạn đánh giá bot được mấy điểm nào?", icon='😍')
        return
# List messages history
if "messages" not in st.session_state:
    st.session_state.messages = []

# First init conversation
st.title("Phi BOT")
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi']
    st.session_state.messages.append({
            "role": "user", 
            "content": 'Hi'
        })
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['Chào bạn, tôi là Phi, trở lý ảo phát triển bởi Microsoft. Tôi có thể giúp gì cho bạn?']
    st.session_state.messages.append({
            "role": "system", 
            "content": 'Chào bạn, tôi là Phi, trở lý ảo phát triển bởi Microsoft. Tôi có thể giúp gì cho bạn?'
        })

response_container = st.container()
input_container = st.container()

linkedin_url = "https://www.linkedin.com/in/meotism/" 
linkedin_icon_url = "https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg"

# Display the LinkedIn icon
st.markdown(
    f'<a href="{linkedin_url}" target="_blank"><img src="{linkedin_icon_url}" /></a>',
    unsafe_allow_html=True
)

# Function for taking user-provided prompt as input

def submit():
    st.session_state.input_text = st.session_state.input
    st.session_state.input = ""

with input_container:
    c1, c2 = st.columns([9,1])
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if 'input' not in st.session_state:
        st.session_state.input = ""
    with c2:
        text = speech_to_text(language='vi', start_prompt="⏺️", stop_prompt="⏹️", key="STT", use_container_width=True, just_once=True)
    if text:
        # st.session_state.input = text
        user_input = text
        flow_response(user_input)
    with c1:
        input_text = st.text_input("You: ", value="", key="input", on_change=submit, label_visibility= "collapsed")
        user_input = st.session_state.input_text
    if user_input:
        flow_response(user_input)
        # st.session_state.past.append(user_input)
        # st.session_state.messages.append({
        #     "role": "user", 
        #     "content": user_input
        # })
        # with st.spinner(text="Đang trả lời..."):
        #     response = gen_chatbot_response(st.session_state.messages)
        # st.session_state.generated.append(response)
        # st.session_state.messages.append({
        #     "role": "system",
        #     "content": response
        # })
        # st.session_state.input_text = None
        # st.toast("Tuyệt vời, bạn đánh giá bot được mấy điểm nào?", icon='😍')
        
# Applying the user input box
with response_container:
    if st.session_state['past']:
        for i in range(len(st.session_state['past'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['generated'][i], key=str(i))