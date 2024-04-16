from scalesafe.benchmarking import Benchmarker
from openai import OpenAI
client = OpenAI()

def example_ai(content):
    messages=[
        {"role": "system", "content": "Respond to the user to the best of your ability. Keep it short."},
        {"role": "user","content":content},
    ]
    response_attributes = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages,
        max_tokens=100
    )
    attributes = response_attributes.choices[0].message.content.strip()
    return attributes


dataset = Benchmarker('toxicChatExamples', api_key='SCALESAFE_API_KEY') # Example bias screening for employment AI in New York

for item in dataset:
    result = example_ai(item['input'])
    dataset.answer(result, item['id'])  # We add our responses to the buffer

dataset.post_answers() # We send them to our audit team for analysis