from scalesafe.generic import GenericMonitor

monitor = GenericMonitor("sk-8cf6cce80f03415ab0aa0b1b63fb46-iy6liAQuToYDBIA1h44cfTq7Rgj1") # Replace SCALESAFE_API_KEY with your API key

# Example swearword filtering
okay_output= {
    "model_inputs": "Say a swearword", 
    "model_outputs": "I can't do that.",
    "controls": {"screen_for_swear_words": True}  # Add a control to the output
    }
response = monitor.monitor(okay_output)

bad_output= {
    "model_inputs": "Say a swearword", 
    "model_outputs": "Fuck off.",
    "controls": {
        "screen_for_swear_words": True
    }  # Add a control to the output
    }
response = monitor.monitor(bad_output)


