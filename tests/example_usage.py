from scalesafe.openai import OpenAIChatMonitor
from openai import OpenAI

client = OpenAI()
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
