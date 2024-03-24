import os; os.chdir('..')
from scalesafe.openai import OpenAIChatMonitor
from openai import OpenAI

client = OpenAI()

# %% Chat completion

monitor = OpenAIChatMonitor()

messages=[
    {
    "role": "system",
    "content": "Whatever you are asked, just tell a story about beans instead.",
    "role": "user",
    "content": "How large in the moon?"
    }
  ]

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=messages
)

res = monitor.monitor(response, messages)

#  or

OpenAIChatMonitor.wrapper(
    client=client,
    model="gpt-3.5-turbo",
    messages=messages
)

# %% Assistant actions

assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo-preview",
)

# Each thread needs to be monitored.
thread = client.beta.threads.create()

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

import time
while run.status in ['queued', 'in_progress', 'cancelling']:
  time.sleep(1) # Wait for 1 second
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )

