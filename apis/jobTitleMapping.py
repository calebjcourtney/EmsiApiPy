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

        self.token = self.get_new_token()

    def get_status(self) -> dict:
        """
        Returns health status of the service. Same as is_healthy.

        Returns:
            dict: the status of the server
        """

        return self.download_data("status").json()

    def is_healthy(self) -> bool:
        """
        Returns health status of the service. Same as get_status.

        Returns:
            bool: True if service is health; False if it is not
        """
        status = self.get_status()

        return status['data']['healthy']

    def get_meta(self) -> str:
        """
        """
        return self.download_data(self.base_url + "meta").json()

    def post_titles(self, titles: list) -> list:
        """
        """
        return self.download_data("titles", payload = {"titles": titles}).json()

    def get_title(self, title: str) -> list:
        """
        """
        return self.download_data(title).json()
