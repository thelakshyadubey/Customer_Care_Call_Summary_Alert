import os
import tempfile
import whisper
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_community.utilities.zapier import ZapierNLAWrapper
import streamlit as st

# Load environment variables
load_dotenv()

@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

def email_summary(uploaded_file):
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.getbuffer())
        temp_audio_path = temp_audio.name

    # Transcription
    model = load_model()
    result = model.transcribe(temp_audio_path)
    transcription = result["text"]

    # LLM and Zapier setup
    llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)
    zapier = ZapierNLAWrapper()

    gmail_send_email_tool = Tool(
        name="GmailSendEmail",
        func=lambda instructions: zapier.run(
            instructions=instructions,
            action_id="308a38c1-ae26-4622-8122-805d90a8579f",
            params={
                "To": "lakshya.dubey04@gmail.com",
                "Subject": "Customer Call Summary",
                "Body": instructions
            }
        ),
        description="Send an email using Gmail via Zapier"
    )

    agent = initialize_agent(
        tools=[gmail_send_email_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Run agent
    prompt = (
        f"Use the Gmail: Send Email Zapier action to send an email to lakshya.dubey04@gmail.com "
        f"summarizing the following text:\n\n{transcription}"
    )

    agent.run(prompt)

    os.remove(temp_audio_path)
