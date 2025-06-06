import os
import tempfile
import whisper
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_community.utilities.zapier import ZapierNLAWrapper

# Set API keys
os.environ["GROQ_API_KEY"] = "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"
os.environ["ZAPIER_NLA_API_KEY"] = "sk-ak-StRmfCqKCwHLTPfDkIZNy1yCP7"

# ... your imports and setup ...

def email_summary(uploaded_file):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.getbuffer())
        temp_audio_path = temp_audio.name

    model = whisper.load_model("base")
    result = model.transcribe(temp_audio_path)
    transcription = result["text"]

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
        f"summarizing the following text:\n\n{transcription}"
    )

    agent.run(prompt)

    os.remove(temp_audio_path)
