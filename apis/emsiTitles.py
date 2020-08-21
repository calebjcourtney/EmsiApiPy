"""
This service takes text describing a job and normalizes it into a standardized job title from Emsi's job title taxonomy.
https://api.emsidata.com/apis/emsi-job-title-normalization
"""
import requests

from .base import EmsiBaseConnection


class EmsiTitlesConnection(EmsiBaseConnection):
    """This service takes text describing a job and normalizes it into a standardized job title from Emsi's job title taxonomy.

    Attributes:
        base_url (str): base url for the API
        scope (str): scope used to request access from the OAuth server
        token (str): auth token received from the OAuth server
    """

    def __init__(self) -> None:
        """Create the connection
        """
        super().__init__()
        self.base_url = "https://titles.emsicloud.com/"
        self.scope = "titles"

        self.token = self.get_new_token()

    def get_status(self) -> dict:
        """
        Returns health status of the service. Same as is_healthy.

        Returns:
            dict: the status of the server
        """
        url = self.base_url + "status"
        response = requests.request("GET", url)

        return response

    def is_healthy(self) -> bool:
        """
        Returns health status of the service. Same as get_status.

        Returns:
            bool: True if service is health; False if it is not
        """
        url = self.base_url + "status"
        response = requests.request("GET", url)

        return response.json()['data']['healthy']

    def get_help(self) -> str:
        """
        Usage information.

        Returns:
            str: the raw markdown text from the doc site (https://api.emsidata.com/apis/emsi-job-title-normalization)
        """
        url = self.base_url + "help"
        response = requests.request("GET", url)

        return response.text

    def get_titles(self) -> list:
        """
        Returns the taxonomy of titles.

        Returns:
            list: a list of all the titles and their ids
        """
        response = self.download_data("titles")

        return response.json()

    def post_normalize(self, title: str) -> dict:
        """Basic title normalization route. Returns normalized title, its ID, and its similarity score.

        Currently only supports the JSON usage ability for the API, no support for plain text

        Args:
            payload (dict): json to be sent to the API (e.g. `{"title" : "software engineer iii"}`)

        Returns:
            dict: dictionary of the top match from the API (id, title, and similarity)
        """
        payload = {"title": title}
        response = self.download_data("normalize", payload)

        return response.json()

    def get_normalize(self, title: str) -> dict:
        """
        Get type must have the raw title in the query string with key title.

        Args:
            title (list): the title to normalize

        Returns:
            dict: dictionary of the top match from the API (id, title, and similarity)
        """
        querystring = {"title": title}
        response = self.querystring_endpoint('normalize', querystring)

        return response.json()
