import streamlit as st

from dotenv import load_dotenv
import os
import calendar_chat as cc
import whisper
import speech_recognition as sr

model = whisper.load_model("base")
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

chat = cc.ChatCalendar()

r = sr.Recognizer()

# Funktion zum Abrufen der verfügbaren Mikrofone
def get_available_microphones():
    microphones = sr.Microphone.list_microphone_names()
    return microphones

# Funktion zum Transkribieren des Audios
def transcribe_audio(audio):
    text = r.recognize_google(audio)
    return text

# Funktion zum Abrufen von Chat-Ergebnissen
def retrieve(query):
    result = chat.test(query)
    return result

# Streamlit-App-Konfiguration
st.set_page_config(layout='wide')
st.title("Chat with AI clone")
st.info("Chat Below")

# Texteingabe für die Abfrage
input_text = st.text_area("Enter your query")

# Dropdown-Menü für die Mikrofonauswahl
microphones = get_available_microphones()
selected_microphone = st.selectbox("Select Microphone", microphones)

# Schaltfläche zum Starten/Stoppen der Aufnahme
if st.button(':studio_microphone:'):
    # Verwende das ausgewählte Mikrofon als Audioquelle
    with sr.Microphone(device_index=microphones.index(selected_microphone)) as source:
        if not st.session_state.get('recording', False):
            st.text("Recording... Press again to stop.")
            st.session_state.recording = True

            try:
                # Erhöhe den Timeout auf 30 Sekunden
                audio_data = r.record(source, duration=5)
                st.text("Recording finished! Transcribing...")

                # Transkribiere den Audio-Clips
                result = transcribe_audio(audio_data)

                # Füge das transkribierte Ergebnis zur eigenen Chatbox hinzu
                st.text_area("Chat Box", result, height=100, key="own_chat_box")

                # Führe die Chat-Funktion aus
                chat_result = retrieve(result)

                # Füge das Ergebnis der Chat-Funktion zur allgemeinen Chatbox hinzu
                st.text_area("Chat Box", chat_result, height=100, key="general_chat_box")

                st.success(chat_result)
            except sr.WaitTimeoutError:
                st.text("Recording timed out. Please try again.")
            except sr.UnknownValueError:
                st.text("Could not understand audio. Please try again.")
            except sr.RequestError as e:
                st.text(f"Could not request results from Google Speech Recognition service; {e}")

            st.session_state.recording = False
        else:
            st.text("Recording stopped.")
            st.session_state.recording = False

# Chat mit CSV-Daten
if input_text is not None:
    if st.button("Chat with CSV"):
        st.info("Your Query: " + input_text)
        result = retrieve(input_text)

        # Füge das Ergebnis zur Chatbox hinzu
        st.text_area("Chat Box", result, height=100)

        st.success(result)