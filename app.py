import streamlit as st
from utils import email_summary

def main():
    st.title("Customer Care Call Summarization")

    uploaded_files = st.file_uploader(
        "Upload recorded .mp3 files",
        type=["mp3"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.write("Uploaded Files:")

        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name

            if uploaded_file.size > 5 * 1024 * 1024:
                st.warning(f"{file_name} is too large. Please upload files under 5MB.")
                continue

            col1, col2, col3 = st.columns([0.1, 1, 2])
            with col1:
                st.write("-")
            with col2:
                st.write(file_name)
            with col3:
                if st.button(f"Send Email for {file_name}"):
                    with st.spinner("Processing..."):
                        email_summary(uploaded_file)
                    st.success(f"Email sent for: {file_name}")

if __name__ == "__main__":
    main()
