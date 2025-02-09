import streamlit as st #using streamlit for UI
#Creating the GUI
from streamlit_chat import message
from dotenv import load_dotenv # basically allows your application to use information from the .env file (retrieves your openAi API key)
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
     SystemMessage, # First message you send in any conversation and tells the model what role it will play
     HumanMessage, #message the human will send to the language model
     AIMessage #the actual response from the language model
)


def init():
    load_dotenv()

    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="Your own ChatGPT",
        page_icon="🦾"
    )

def main():
    init()

    chat = ChatOpenAI(temperature = 0)


    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    # sidebar with user input
    with st.sidebar:
        user_input = st.text_input("Your message: ", key="user_input")

        # handle user input
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))
            

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()
