# Step 1: Import Libraries
import os
from moviepy.editor import VideoFileClip
import whisper
from transformers import pipeline
import streamlit as st

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

# File upload
uploaded_file = st.file_uploader("Upload Audio/Video File", type=["mp4", "avi", "wav", "mp3"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Button to process the file
    if st.button("Transcribe and Summarize"):
        with st.spinner("Processing..."):
            transcribed_text, summary_text, transcription_file_path, audio_file = transcribe_and_summarize(uploaded_file)

            # Display results
            st.subheader("Transcribed Text")
            st.text_area("", value=transcribed_text, height=200)

            st.subheader("Summary")
            st.text_area("", value=summary_text, height=100)

            # Provide download links
            st.markdown(f"[Download Transcription](./{transcription_file_path})")
            st.markdown(f"[Download Extracted Audio](./{audio_file})")

# Clean up temporary files if needed
if uploaded_file is not None and hasattr(uploaded_file, 'name') and os.path.exists(uploaded_file.name): 
    os.remove(uploaded_file.name)