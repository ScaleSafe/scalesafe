import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF
import os

client = OpenAI()

# We will use the OpenAIChatMonitor to monitor the responses
from scalesafe.openai import OpenAIChatMonitor 
monitor = OpenAIChatMonitor("SCALESAFE_API_KEY") # Replace SCALESAFE_API_KEY with your API key

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_resume(job_description, resume_text):

    messages=[
        {"role": "system", "content": "The following is a conversation with a hiring manager trying to extract attributes from a resume. Provide 5 attributes that describe the candidate. Write only the words; with no other text."},
        {"role": "user","content": f"This is the job description: {job_description}\n\nBased on this resume text: {resume_text}\n\nList 5 attributes that describe the candidate that may be relevant to the job description."},
    ]
     
    response_attributes = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages
    )
    attributes = response_attributes.choices[0].message.content.strip()

    # Monitor the responses to keep in compliance, assess ongoing risks, and simplify audits
    monitor.monitor(response_attributes, messages)

    return attributes

def main():
    st.title("Resume Screener App")

    with st.form("job_description_form"):
        job_description = st.text_area("Job Description")
        resume_file = st.file_uploader("Upload Resume PDF")
        submit_button = st.form_submit_button("Analyze Resume")

    if submit_button and resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        rating, attributes = analyze_resume(job_description, resume_text)
        st.subheader("Candidate Attributes:")
        st.write(attributes)

if __name__ == "__main__":
    main()
