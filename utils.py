import os
import tempfile
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_community.utilities.zapier import ZapierNLAWrapper

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ZAPIER_KEY = os.getenv("ZAPIER_NLA_API_KEY")
ASSEMBLYAI_KEY = os.getenv("ASSEMBLYAI_API_KEY")

headers = {
    "authorization": ASSEMBLYAI_KEY,
    "content-type": "application/json"
}

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


def transcribe_audio(file_path):
    # Upload file to AssemblyAI
    with open(file_path, 'rb') as f:
        upload_response = requests.post(upload_endpoint, headers=headers, files={'file': f})
    audio_url = upload_response.json()['upload_url']

    # Request transcription
    transcript_request = {"audio_url": audio_url}
    response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    transcript_id = response.json()['id']

    # Poll for completion
    status = 'processing'
    while status not in ('completed', 'error'):
        poll_response = requests.get(f"{transcript_endpoint}/{transcript_id}", headers=headers)
        status = poll_response.json()['status']

    if status == 'completed':
        return poll_response.json()['text']
    else:
        raise Exception("Transcription failed")


def email_summary(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.getbuffer())
        temp_audio_path = temp_audio.name

    transcription = transcribe_audio(temp_audio_path)

    # Initialize LLM and Zapier tool
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

    prompt = (
        f"Use the Gmail: Send Email Zapier action to send an email to lakshya.dubey04@gmail.com "
        f"summarizing the following customer call transcription:\n\n{transcription}"
    )

    agent.run(prompt)
    os.remove(temp_audio_path)
