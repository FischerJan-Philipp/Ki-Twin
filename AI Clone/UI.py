import io

import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import calendar_chat as cc
from elevenlabs import voices, generate, set_api_key, generate, stream
from elevenlabs import Voice, VoiceSettings, generate
from pathlib import Path
from audio_recorder_streamlit import audio_recorder
import whisper
import openai
import speech_recognition as sr

model = whisper.load_model("base")
#dotenv_path = Path('D:\Kyron\Documents\Python Scripts\Ki-Twin\.env')
#load_dotenv(dotenv_path=dotenv_path)

load_dotenv()

elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
set_api_key(elevenlabs_api_key)
openai_api_key = os.getenv("OPENAI_API_KEY")

chat = cc.ChatCalendar()

r = sr.Recognizer()

def transcribe_audio(audio):
    text = r.recognize_whisper(audio)
    return text

def retrieve(query):
    result = chat.test(query)
    return result

def generate_audio(query):
    print("generating audio...")
    audio_stream = generate(
        text=query,
        voice=Voice(
            voice_id="2sFP0IlelRrLzaBV9PuJ",
            settings=VoiceSettings(stability=0.3, similarity_boost=0.35, style=0.66, use_speaker_boost=True)
        ),
        stream=True,
        model="eleven_multilingual_v2"
    )
    if audio_stream:
        audio_bytes = b"".join(audio_stream)
        st.audio(audio_bytes)
        stream(audio_stream)

st.set_page_config(layout='wide')

st.title("Chat with AI clone")
st.image("Stanley.png", width=200)

input_text = st.text_area("Gib deine Nachricht ein")

if st.button(':studio_microphone:'):
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        st.text("Recording for 10 seconds...")
        # Read the audio data from the default microphone
        audio_data = r.record(source, duration=10)
        st.text("Recording finished! Transcribing...")

    # Transcribe the audio to text
    result = transcribe_audio(audio_data)
    st.text(result)
    finalResult = retrieve(result)
    st.success(finalResult)
    audio_stream = generate_audio(finalResult)

if input_text is not None:
    if st.button('Senden'):
        st.info("Your Query: " + input_text)
        result = retrieve(input_text)
        st.success(result)
        audio_stream = generate_audio(result)


