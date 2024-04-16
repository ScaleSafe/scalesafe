from openai import OpenAI
client = OpenAI()

# We will use the OpenAIChatMonitor to monitor the responses
from scalesafe.openai import OpenAIChatMonitor 
monitor = OpenAIChatMonitor("SCALESAFE_API_KEY") # Replace SCALESAFE_API_KEY with your API key

import numpy as np
for i in range(10):
    messages=[
        {"role": "system", "content": "Make up an education fact for children.Review this loan application and provide a recommendation "},
        {"role": "user", "content": "I am writing to request a business loan of $50,000 to support the growth and inventory expansion of my corner store, Neighborhood Nook, located at 452 Elm Street, Springfield. The funding will be utilized to enhance our product offerings and improve store fixtures, thereby increasing customer satisfaction and sales. Our store has consistently shown a positive cash flow and has a loyal customer base which assures the repayment of this loan. Attached are our financial statements and a detailed business plan for your review. CREDIT RATING:" + str(np.random.randint(300, 850))}
    ]
     
    response_attributes = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages
    )
    attributes = response_attributes.choices[0].message.content.strip()

    # Monitor the responses to keep in compliance, assess ongoing risks, and simplify audits
    monitor.monitor(response_attributes, messages)