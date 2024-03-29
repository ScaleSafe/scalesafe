import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF
import os

client = OpenAI()

from scalesafe.openai import OpenAIChatMonitor

# Since this app actually uses two different 'AI systems'
monitor_ = OpenAIChatMonitor("SCALESAFE_API_KEY_1") 

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_resume(job_description, resume_text):
    # Assuming you've designed a prompt for employability rating
    response_rating = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "The following is a conversation with a hiring manager trying to rate a resume. Provide an employability rating for the candidate. **State only a number from 1 to 5. No other text.**"},
            {"role": "user", "content": "Based on this job description: {job_description}\n\nRate the employability of the candidate based on this resume text: {resume_text}. Provide a single number from 1 to 5, where 1 is the lowest and 5 is the highest:"},
        ])
    rating = response_rating.choices[0].message.content.strip()

    # Assuming a separate prompt for extracting candidate attributes

    response_attributes = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "The following is a conversation with a hiring manager trying to extract attributes from a resume. Provide 5 attributes that describe the candidate. Write only the words; with no other text."},
            {"role": "user","content": "Based on this resume text: {resume_text}\n\nList 5 attributes that describe the candidate."}
        ])
    attributes = response_attributes.choices[0].message.content.strip()

    # Monitor the responses to keep 

    return rating, attributes

def main():
    st.title("Resume Screener App")

    with st.form("job_description_form"):
        job_description = st.text_area("Job Description")
        resume_file = st.file_uploader("Upload Resume PDF")
        submit_button = st.form_submit_button("Analyze Resume")

    if submit_button and resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        rating, attributes = analyze_resume(job_description, resume_text)
        st.subheader("Employability Rating:")
        st.write(rating)
        st.subheader("Candidate Attributes:")
        st.write(attributes)

if __name__ == "__main__":
    main()
