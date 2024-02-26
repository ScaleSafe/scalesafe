# This is the code to make scalesafe seamlessly work with OpenAI API useage of AI models.

from generic import GenericMonitor

class OpenAIChatMonitor(GenericMonitor):
    """This is a monitor object to help to manage the compliance of OpenAI Chat API useage."""
    def __init__(self, api_key):
        super().__init__(api_key)