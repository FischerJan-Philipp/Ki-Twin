import pandas
import streamlit as st
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import PandasAI
import calendar_chat as cc

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

chat = cc.ChatCalendar()

st.set_page_config(layout='wide')

st.title("Chat with AI clone")



st.info("Chat Below")

input_text = st.text_area("Enter your query")

if input_text is not None:
    if st.button("Chat with CSV"):
        st.info("Your Query: " + input_text)
        result = chat.test(input_text)
        st.success(result)