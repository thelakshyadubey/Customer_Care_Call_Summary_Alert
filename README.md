# Customer_Care_Call_Summary_Alert
Project Deployed on Render: https://customer-care-call-summary-alert.onrender.com<br>
📞 Customer Call Summary & Email Bot
This is a Streamlit-based AI assistant that takes in customer support call recordings (audio files), transcribes them using AssemblyAI, summarizes the conversation using GROQ's LLaMA-3 via LangChain, and sends the summary via Zapier Gmail Integration — all with a single upload!

🔧 Features
🎙️ Upload audio files (.mp3)
🧠 Transcribe using AssemblyAI
✍️ Summarize with GROQ's LLaMA-3
📧 Auto-send email summaries via Zapier Gmail Integration
✅ Built with Streamlit

📁 Folder Structure
bash
Copy
Edit
├── app.py              # Streamlit frontend
├── utils.py            # Core logic: transcription, LLM, Zapier
├── requirements.txt    # All dependencies
├── .env                # Secret keys (not tracked in Git)
└── README.md           # You're here

🚀 Getting Started
1. Clone the repo
git clone https://github.com/thelakshyadubey/Customer_Care_Call_Summary_Alert.git
cd Customer_Care_Call_Summary_Alert

2. Install dependencies
pip install -r requirements.txt

3. Set up .env
Create a .env file in the root folder and add your credentials:
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GROQ_API_KEY=your_groq_api_key
ZAPIER_NLA_API_KEY=your_zapier_key

▶️ Run the App
streamlit run app.py

📬 How it works
Upload a .mp3 call recording.
The app:
Uploads it to AssemblyAI → gets transcript.
Uses LLaMA-3 via LangChain to summarize.
Sends the summary via Zapier Gmail action.
All magic happens seamlessly in the background.

📌 Tools & Technologies

UI -> Streamlit
Transcription ->	AssemblyAI
Summarization ->	GROQ (LLaMA-3)
Email	Zapier -> (Gmail API)
Agent Chain ->	LangChain

🧠 Author
Lakshya Dubey

PREVIEW
![image](https://github.com/user-attachments/assets/83f4cc63-f1ca-4491-9595-d2c9c5536e55)
![image](https://github.com/user-attachments/assets/e63feecd-ce0f-455d-b29d-028179c5049e)

