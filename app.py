import streamlit as st
from utils import email_summary

def main():
    st.set_page_config(page_title="Customer Call Summarizer")
    st.title("📞 Customer Call Summarizer")
    st.markdown("Upload MP3 call recordings. Summaries will be sent via Gmail.")

    uploaded_files = st.file_uploader("Upload MP3 Files", type=["mp3"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            st.write(f"**{file.name}**")
            if st.button(f"Summarize & Send Email for {file.name}"):
                try:
                    email_summary(file)
                    st.success(f"✅ Email sent for {file.name}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
