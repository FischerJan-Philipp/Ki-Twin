import os
import tempfile
from pydub import AudioSegment
import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Open the audio file
audio_file_path = "./Data/Prof/GMT20231023-060453_Recording.m4a"
audio = AudioSegment.from_file(audio_file_path)

# Define the length of each segment in milliseconds (10 minutes = 600000 ms)
segment_length_ms = 600000

# Calculate the number of segments
num_segments = len(audio) // segment_length_ms

with open("./Data/Prof/transcript.txt", "w") as f:
    # Loop over each segment
    for i in range(num_segments):
        # Extract the segment
        start_time = i * segment_length_ms
        end_time = start_time + segment_length_ms
        segment = audio[start_time:end_time]

        # Save the segment to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            segment.export(temp_audio.name, format="wav")
            temp_audio_path = os.path.abspath(temp_audio.name)

        # Transcribe the segment
        transcription = model.transcribe(temp_audio_path)
        print(f"Segment {i+1}: {transcription['text']}")
        f.write(f"{transcription['text']} ")
