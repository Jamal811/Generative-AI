import streamlit as st
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Load the BlenderBot model and tokenizer
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

# Set Streamlit page layout
st.set_page_config(page_title="Life Event Bot", layout="centered", initial_sidebar_state="collapsed")

# Define the title of the app
st.title("🤖 Life Event Bot - Your Personalized Milestone Tracker")

# Add a nice description
st.markdown("""
### Welcome to Life Event Bot!
This chatbot helps you predict and track life milestones by analyzing your responses. 
Set your goals, and the bot will guide you towards achieving them.
""")

# Sidebar for user input on goals and traits
st.sidebar.title("Set Your Milestones")
milestone = st.sidebar.text_input("Your next milestone (e.g., promotion, fitness goal)", "Get promoted")
goal_date = st.sidebar.date_input("Target Date")

# Display in sidebar
st.sidebar.markdown(f"**Milestone:** {milestone}")
st.sidebar.markdown(f"**Target Date:** {goal_date}")

# Main interaction
user_input = st.text_area("Tell me about your day or your current thoughts.", placeholder="Start typing here...")

if st.button("Talk to Life Event Bot"):
    if user_input:
        # Tokenize the user input
        inputs = tokenizer([user_input], return_tensors="pt")
        
        # Generate a long response using Blenderbot
        response_ids = model.generate(inputs['input_ids'], max_length=200)
        bot_response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
        
        # Display the bot response
        st.markdown(f"**Life Event Bot says:** {bot_response}")
    else:
        st.error("Please write something to continue the conversation!")

# Add a cool footer
st.markdown("""
---
**Note**: This chatbot is designed to give personalized life advice based on your interactions. Keep chatting to receive tailored suggestions!
""")
