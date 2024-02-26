from exceptions import *

class GenericMonitor():
    """This is a base class from which we can build any kind of monitoring for AI models."""
    def __init__(self, api_key= ""):
        self.api_key = api_key

    def send(self, data):
        """This method is used to send data to the scalesafe endpoints."""
        raise NotImplementedError("send method is not implemented")
    
    def checkExceptions(self, ss_response):
        """This method is used to check for exceptions in the returned data."""
        raise NotImplementedError("checkExceptions method is not implemented")

    def monitor(self, data):
        """This method is used to send the useage data to the server and process any exceptions."""
        ss_response = self.send(data)
        self.checkExceptions(ss_response)