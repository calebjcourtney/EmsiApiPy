"""
This service takes text describing a job and normalizes it into a standardized job title from Emsi's job title taxonomy.
https://api.emsidata.com/apis/emsi-job-title-normalization
"""

from .base import EmsiBaseConnection


class JobTitleMappingConnection(EmsiBaseConnection):
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
        self.base_url = "https://emsiservices.com/jtm/"
        self.scope = "jtm"

        self.get_new_token()

    def post_titles(self, titles: list, querystring: dict = None) -> list:
        """
        """
        return self.download_data("titles", payload = {"titles": titles}, querystring = querystring).json()

    def get_title(self, title: str, querystring: dict = None) -> list:
        """
        """
        return self.download_data(f"titles/{title}", querystring = querystring).json()
