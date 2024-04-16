# We will use the OpenAIChatMonitor to monitor the responses
from scalesafe.generic import GenericMonitor 
monitor = GenericMonitor("SCALESAFE_API_KEY") # Replace SCALESAFE_API_KEY with your API key

import numpy as np
for input in range(100):
    ai_output = True if np.random.random() > 0.5 else False
    # Monitor the responses to keep in compliance, assess ongoing risks, and simplify audits
    monitor.monitor({"model_inputs": input, "model_outputs": ai_output})