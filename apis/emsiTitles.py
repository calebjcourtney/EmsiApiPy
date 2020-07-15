"""Summary
"""
import requests

from .base import EmsiBaseConnection


class EmsiTitlesConnection(EmsiBaseConnection):
    """docstring for EmsiTitlesConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://titles.emsicloud.com/"
        self.scope = "titles"

        self.token = self.get_new_token()

    def get_status(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = self.base_url + "status"
        response = requests.request("GET", url)

        return response

    def is_healthy(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = self.base_url + "status"
        response = requests.request("GET", url)

        return response.json()['data']['healthy']

    def get_help(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = self.base_url + "help"
        response = requests.request("GET", url)

        return response.text

    def get_titles(self) -> dict:
        """
        Summary

        Returns:
            dict: Description

        Args:
            metric_name (str, optional): Description
        """
        response = self.download_data("titles")

        return response.json()

    def get_normalize(self, title: str) -> dict:
        """
        Summary

        Args:
            metrics_list (list): Description

        Returns:
            dict: Description
        """
        querystring = {"title": title}
        response = self.querystring_endpoint('normalize', querystring)

        return response.json()

    def post_normalize(self, title: str) -> dict:
        """Summary

        Args:
            payload (dict): Description

        Returns:
            dict: Description
        """
        payload = {"title": title}
        response = self.download_data("normalize", payload)

        return response.json()
