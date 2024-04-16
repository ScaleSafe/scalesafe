from scalesafe.benchmarking import Benchmarker
dataset = Benchmarker('nyEmploymentScreeningText', api_key='SCALESAFE_API_KEY') # Example bias screening for employment AI in New York

import numpy as np
for item in dataset:
    # Your AI model here
    output = True if np.random.random() > 0.5 else False
    dataset.answer(output, item['id'])  # We add our responses to the buffer

dataset.post_answers() # We send them to our audit team for analysis