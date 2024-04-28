"""This is a helper to assist with the admin interface for the scalesafe app. Ideally, developers never need to visit the website and everything can be done via the admin command interface."""

from .exceptions import *
import os
import requests

def _get_api_key(api_key_passed=None):
    if api_key_passed:
        return api_key_passed
    os_api_key = os.environ.get("SCALESAFE_API_KEY")
    if os_api_key:
        return os_api_key
    raise ScaleSafeTokenError(
        "Scalesafe API Key not found in local environment. Please set the environment variable SCALESAFE_API_KEY or pass the api_key as an argument. You can find an api key in the scalesafe dashboard."
    )

def get_requirements(api_key=None):
    """This method is used to get the requirements for the AI system. The API key will uniquely identify the model and user to return the requirements and their status."""
    api_key = _get_api_key(api_key)
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.scalesafe.com/v1/get_model_requirements"
    ss_response = requests.get(url, headers=headers)
    ss_response.raise_for_status()
    return ss_response.json()



