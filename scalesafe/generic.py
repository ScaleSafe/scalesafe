from .exceptions import *
import os, requests


class GenericMonitor:
    """This is a base class from which we can build any kind of monitoring and safety checks for AI models."""

    def __init__(self, api_key=None, location=None):
        """
        api_key: str - This is the API key for the scalesafe server. If not provided, it will look for the environment variable SCALESAFE_API_KEY. The API key uniquely identifies the AI model and the user ID.

        location: str - This is the location of the AI model, since compliance depends on location. Set to 'everywhere' if you want to maximal compliance checks, or a location string matching the location of the AI model in the web app. Otherwise it will use the IP to determine the location.

        """
        self.init_api_key = api_key
        self.location = location

    def _checkExceptions(self, ss_response):
        """This method checks for exceptions in the returned data and raises the appropriate custom exceptions."""

        if not ss_response:
            raise ValueError("The response is empty or None.")

        if "error" not in ss_response:
            return  # No error in the response, so just return

        error_message = ss_response.get("error", "").lower()

        if "invalid api key" in error_message:
            raise ScaleSafeTokenError("Invalid API Key provided.")
        elif "api key not found" in error_message or "not active" in error_message:
            raise ScaleSafeTokenError("API Key not found or not active.")
        elif "rate limit exceeded" in error_message:
            raise APIRateLimitExceededError("API rate limit has been exceeded.")
        elif "missing fields" in error_message or "data validation" in error_message:
            raise DataValidationError(
                "Data validation error: missing or incorrect fields."
            )
        elif "unauthorized" in error_message:
            raise UnauthorizedAccessError("Unauthorized access attempt detected.")
        elif (
            "model not found" in error_message or "resource not found" in error_message
        ):
            raise ResourceNotFoundError("The requested resource was not found.")
        elif "database operation" in error_message:
            raise DatabaseOperationError("Database operation failed.")
        else:
            raise ScaleSafeException("An unspecified error occurred.")

    def _get_api_key(self, api_key_passed=None):
        if api_key_passed:
            return api_key_passed
        if self.init_api_key:
            return self.init_api_key
        os_api_key = os.environ.get("SCALESAFE_API_KEY")
        if os_api_key:
            return os_api_key
        raise ScaleSafeTokenError(
            "Scalesafe API Key not found in local environment. Please set the environment variable SCALESAFE_API_KEY or pass the api_key as an argument to the monitor method."
        )

    def monitor(self, data, api_key=None):
        """This method is used to send the usage data to the server and process any exceptions.
        By default it will return the status of the AI system and raise an exception.
        Data is a flexible packet of information that can be used to monitor the AI system."""
        ss_response = self._sendMonitor(data, api_key)
        self._checkExceptions(ss_response)
        return ss_response

    def _sendMonitor(self, data, api_key=None):
        """This method is used to send data to the scalesafe monitoring endpoint."""

        api_key = self._get_api_key(api_key)

        headers = {"Authorization": f"Bearer {api_key}"}

        url = "https://log-model-data-zc6tu6qxxa-uc.a.run.app"
        ss_response = requests.post(url, headers=headers, json=data)
        ss_response.text
        ss_response.raise_for_status()
        return ss_response

    def status(self, api_key=None):
        """This method is used to check the status of the AI system."""
        status = self._sendStatus(api_key)
        if status.get("status") == "Out of Compliance":
            raise OutOfComplianceError(
                status.get(
                    "message",
                    "Scalesafe server is showing system is out of compliance.",
                )
            )
        return status

    def _sendStatus(self, api_key=None):
        """This method is used to get a status request from the scalesafe monitoring endpoint."""
        api_key = self._get_api_key(api_key)
        headers = {"Authorization": f"Bearer {api_key}"}
        url = "https://get-model-status-zc6tu6qxxa-uc.a.run.app"
        ss_response = requests.get(url, headers=headers)
        ss_response.raise_for_status()
        return ss_response.json()
