# This is the code to make scalesafe seamlessly work with OpenAI API useage of AI models.

from .generic import GenericMonitor


class OpenAIChatMonitor(GenericMonitor):
    """This is a monitor object to help to manage the compliance of OpenAI Chat API useage."""

    def __init__(self, api_key=None, location=None):
        super().__init__(api_key, location)

    def monitor(self, response, messages, api_key=None):
        """
        response: ChatCompletion - This is the response from the OpenAI chat API.
        """

        data = {
            "model_version": response.model,
            "model_start_time": response.created,
            "model_end_time": response.created,
            "model_inputs": messages,
            "model_outputs": response.choices[0].message.content,
            "openai_response_id": response.id,
        }

        return super().monitor(data, api_key)

    def wrapper(client, model, messages, api_key=None, **kwargs):
        """This is a wrapper around the OpenAI chat completions.create method to monitor the useage."""
        monitor = OpenAIChatMonitor()
        response = client.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        monitor.monitor(response, messages, api_key)
        return response


class OpenAIAssistantMonitor(GenericMonitor):
    """This is a monitor object to help to manage the compliance of OpenAI Assistant API useage."""

    def __init__(self, api_key=None, location=None):
        super().__init__(api_key, location)

    def monitor(self, response, api_key=None):
        """
        response: AssistantCompletion - This is the response from the OpenAI assistant API.
        """
        data = {
            "model_version": response.model,
            "model_start_time": response.created,
            "model_end_time": response.created,
            "model_inputs": response.prompt,
            "model_outputs": response.choices[0].message.content,
            "openai_response_id": response.id,
        }

        return super().monitor(data, api_key)
