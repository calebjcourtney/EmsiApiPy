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
        super().__init__()
        self.base_url = "https://emsiservices.com/gis/v1/"
        self.scope = "gis"

        self.get_new_token()

        self.name = "Geography"

    def get_countries(self) -> str:
        # https://api.emsidata.com/apis/geography#get
        return self.download_data(self.base_url).json()

    def get_country_meta(self, country: str) -> list:
        # https://api.emsidata.com/apis/geography#get-country
        return self.download_data(country).json()

    def post_withinproximity(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-withinproximity
        url = f"{country}/{version}/{level}/withinproximity"
        return self.download_data(url, payload).json()

    def post_closest(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-closest
        url = f"{country}/{version}/{level}/closest"
        return self.download_data(url, payload).json()

    def post_contains(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-contains
        url = f"{country}/{version}/{level}/contains"
        return self.download_data(url, payload).json()

    def post_centroid(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-centroid
        url = f"{country}/{version}/{level}/centroid"
        return self.download_data(url, payload = payload).json()

    def post_mbr(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-mbr
        url = f"{country}/{version}/{level}/mbr"
        return self.download_data(url, payload).json()

    def post_mbc(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-mbc
        url = f"{country}/{version}/{level}/mbc"
        return self.download_data(url, payload).json()

    def post_geojson(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-geojson
        url = f"{country}/{version}/{level}/geojson"
        return self.download_data(url, payload).json()

    def post_svg(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://api.emsidata.com/apis/geography#post-country-version-level-svg
        url = f"{country}/{version}/{level}/svg"
        return self.download_data(url, payload).json()

    def post_traveltime(self, country: str, version: str, level: str, payload: dict) -> dict:
        # https://emsiapi-internal.surge.sh/apis/geography#post-country-version-level-traveltime
        url = f"{country}/{version}/{level}/traveltime"
        return self.download_data(url, payload).json()
