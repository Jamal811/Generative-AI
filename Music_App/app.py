import gradio as gr
from transformers import AutoTokenizer, AutoModelForTextToWaveform
import torch
import numpy as np
import scipy.io.wavfile as wav

# Initialize music generation model
tokenizer = AutoTokenizer.from_pretrained("facebook/musicgen-small")
model = AutoModelForTextToWaveform.from_pretrained("facebook/musicgen-small", attn_implementation="eager")

# Function to generate music based on a prompt
def generate_music(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    waveform = model.generate(**inputs, max_length=500)  # Adjust max_length as needed
    waveform_np = waveform.squeeze().cpu().numpy()

    # Save the waveform as a .wav file for playback and download
    file_path = '/tmp/generated_music.wav'
    wav.write(file_path, 22050, waveform_np.astype(np.float32))
    return file_path

# Gradio interface for music generation
with gr.Blocks() as app:
    gr.Markdown("## AI Music Generation")

    # Music Generation Section
    with gr.Row():
        prompt_music = gr.Textbox(label="Enter Music Prompt", placeholder="e.g., Upbeat electronic music with deep bass")
        generate_button_music = gr.Button("Generate Music")
    output_music = gr.Audio(label="Generated Music", type="filepath")

    generate_button_music.click(fn=generate_music, inputs=[prompt_music], outputs=[output_music])

app.launch()