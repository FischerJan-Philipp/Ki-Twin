import streamlit as st
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import calendar_chat as cc
from elevenlabs import voices, generate, set_api_key, generate, stream
from elevenlabs import Voice, VoiceSettings, generate
from pathlib import Path


#dotenv_path = Path('D:\Kyron\Documents\Python Scripts\Ki-Twin\.env')
#load_dotenv(dotenv_path=dotenv_path)

load_dotenv()

elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
set_api_key(elevenlabs_api_key)
openai_api_key = os.getenv("OPENAI_API_KEY")

chat = cc.ChatCalendar()

st.set_page_config(layout='wide')

st.title("Chat with AI clone")
st.image("Stanley.png", width=200)


st.info("Chat Below")

input_text = st.text_area("Enter your query")

if input_text is not None:
    if st.button("Chat with CSV"):
        st.info("Your Query: " + input_text)
        result = chat.test(input_text)
        st.success(result)
        audio_stream = generate(
            text=result,
            voice=Voice(
                voice_id="2sFP0IlelRrLzaBV9PuJ",
                settings=VoiceSettings(stability=0.3, similarity_boost=0.35, style=0.66, use_speaker_boost=True)
            ),
            stream=True,
            model="eleven_multilingual_v2"
        )
        stream(audio_stream)