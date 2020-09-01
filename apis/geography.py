"""
This service takes text describing a job and normalizes it into a standardized job title from Emsi's job title taxonomy.
https://api.emsidata.com/apis/emsi-job-title-normalization
"""

from .base import EmsiBaseConnection


class GeographyConnection(EmsiBaseConnection):
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
        self.base_url = "https://emsiservices.com/gis/v1/"
        self.scope = "gis"

        self.get_new_token()

    def get_status(self) -> dict:
        """
        Returns health status of the service. Same as is_healthy.

        Returns:
            dict: the status of the server
        """
        response = self.download_data("status")

        return response

    def is_healthy(self) -> bool:
        """
        Returns health status of the service. Same as get_status.

        Returns:
            bool: True if service is health; False if it is not
        """
        response = self.download_data("status")

        return response.json()['data']['healthy']

    def get_countries(self) -> str:
        """
        """
        return self.download_data(self.base_url).json()

    def get_country_meta(self, country: str) -> list:
        """
        """
        return self.download_data(country).json()

    def post_withinproximity(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/withinproximity"
        return self.download_data(url, payload).json()

    def post_closest(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/closest"
        return self.download_data(url, payload).json()

    def post_contains(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/contains"
        return self.download_data(url, payload).json()

    def post_centroid(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/centroid"
        return self.download_data(url, payload).json()

    def post_mbr(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/mbr"
        return self.download_data(url, payload).json()

    def post_mbc(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/mbc"
        return self.download_data(url, payload).json()

    def post_geojson(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/geojson"
        return self.download_data(url, payload).json()

    def post_svg(self, country: str, version: str, level: str, payload: dict) -> dict:
        url = f"{self.base_url}{country}/{version}/{level}/svg"
        return self.download_data(url, payload).json()
