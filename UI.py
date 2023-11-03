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

st.title("ChatCSV powered by LLM")

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

    with col2:

        st.info("Chat Below")

        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Chat with CSV"):
                st.info("Your Query: " + input_text)
                result = chat.test(input_text)
                st.success(result)