# Step 1: Import Libraries
import os
import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
from transformers import pipeline

# Step 2: Define the Function for Transcription and Summarization
def transcribe_and_summarize(file):
    audio_file = None
    if file.name.endswith('.mp4') or file.name.endswith('.avi'):
        # Extract audio from video
        video = VideoFileClip(file.name)
        audio_file = "extracted_audio.wav"
        video.audio.write_audiofile(audio_file)
    else:
        audio_file = file.name  # Assume it's an audio file

    # Transcribe Audio using Whisper
    model = whisper.load_model("base")  # You can use "small", "medium", or "large" for better accuracy
    result = model.transcribe(audio_file)
    transcribed_text = result['text']

    # Summarize the Transcribed Text
    summarizer = pipeline("summarization")
    summary = summarizer(transcribed_text, max_length=130, min_length=30, do_sample=False)

    # Save the transcribed text to a .txt file
    transcription_file_path = "transcription.txt"
    with open(transcription_file_path, "w") as f:
        f.write(transcribed_text)

    return transcribed_text, summary[0]['summary_text'], transcription_file_path, audio_file

# Step 3: Create Streamlit Interface
st.title("Audio/Video Transcription and Summarization")
st.write("Upload an audio or video file to transcribe its audio, generate a summary, and download the extracted audio.")

uploaded_file = st.file_uploader("Upload Audio/Video File", type=["mp3", "wav", "mp4", "avi"])

if uploaded_file is not None:
    # Run transcription and summarization
    transcribed_text, summary_text, transcription_file_path, audio_file_path = transcribe_and_summarize(uploaded_file)

    # Display Transcribed Text
    st.subheader("Transcribed Text")
    st.text_area("Transcribed Text", transcribed_text, height=200)

    # Display Summary
    st.subheader("Summary")
    st.text_area("Summary", summary_text, height=100)

    # Download Links
    st.subheader("Downloads")
    with open(transcription_file_path, "rb") as f:
        st.download_button("Download Transcription", f, file_name="transcription.txt")
    if audio_file_path:
        with open(audio_file_path, "rb") as f:
            st.download_button("Download Extracted Audio", f, file_name="extracted_audio.wav")
