from scalesafe.benchmarking import Benchmarker
from openai import OpenAI
client = OpenAI()

def analyze_resume(job_description, resume_text):
    messages=[
        {"role": "system", "content": "The following is a conversation with a hiring manager trying to extract attributes from a resume. Provide 5 attributes that describe the candidate. Write only the words; with no other text."},
        {"role": "user","content": "This is the job description: {job_description}\n\nBased on this resume text: {resume_text}\n\nList 5 attributes that describe the candidate that may be relevant to the job description."},
    ]
    response_attributes = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages
    )
    attributes = response_attributes.choices[0].message.content.strip()
    return attributes



dataset = Benchmarker('nyEmploymentScreeningText', api_key='sk-72cb69c4af4d406c854d235b66b67f-iy6liAQuToYDBIA1h44cfTq7Rgj1') # Example bias screening for employment AI in New York

for item in dataset:
    result = analyze_resume("Software Engineer", item['input'])
    dataset.answer(result, item['id'])  # We add our responses to the buffer

dataset.post_answers() # We send them to our audit team for analysis