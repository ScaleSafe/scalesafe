# ScaleSafe Monitoring Engine

This codebase is the open-source toolkit for integrating monitoring into an AI system, for use generally with [scalesafe.ai](scalesafe.ai). The goal is to help you log AI usage, screen responses for safety and compliance, allow convenient human-in-the-loop control and request-for-manual-review handling, support continued risk monitoring, and provide risk and compliance audits. 

This supports the EU AI Act, New York Bill 144, and other AI regulations.


## How this works?
You can assess the safety and compliance obligations and limitations of AI system use according to your model, its properties, and where it's being used. Go to [assess.scalesafe.ai](assess.scalesafe.ai) to see the requirements. This will create an account and allow you to begin monitoring. You can find your [API key](app.scalesafe.ai/keys) in the app.

To integrate with your app, choose the appropriate monitoring class and include it with your AI system / model usage. Some examples of this are below.

```bash
pip install scalesafe
```

### For OpenAI Chat
When a synchronous AI model is being used, you just need to monitor the input and output of the model. This can be done with the `OpenAIChatMonitor` class.

```python

```



### For OpenAI Assistants
This can be a little more complicated, as we're not longer working synchronously.








