import streamlit as st

import time

from streamlit_chat import message
from streamlit_mic_recorder import speech_to_text
# from chatbot import gen_chatbot_response
from huggingface_hub import InferenceClient
import random
import token_temp

client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct",
    token=token_temp.TOKEN,
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
        st.session_state.input = text
    with c1:
        input_text = st.text_input("You: ", value="", key="input", on_change=submit, label_visibility= "collapsed")
    user_input = st.session_state.input_text
    if user_input:
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
        
# Applying the user input box
with response_container:
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['generated'][i], key=str(i))