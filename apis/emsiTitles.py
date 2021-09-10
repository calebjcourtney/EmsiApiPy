"""
This service takes text describing a job and normalizes it into a standardized job title from Emsi's job title taxonomy.
https://api.emsidata.com/apis/titles
"""

from .base import EmsiBaseConnection


class EmsiTitlesConnection(EmsiBaseConnection):
    """
    This API exposes the complete collection of Emsi titles which includes curated occupation and skill mappings for each title and normalization functionality to transform raw job titles to Emsi titles.

    Attributes:
        base_url (str): base url for the API
        scope (str): scope used to request access from the OAuth server
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://emsiservices.com/titles/"
        self.scope = "emsi_open"

        self.get_new_token()

    def get_status(self) -> dict:
        """
        Get the health of the service. Be sure to check the healthy attribute of the response, not just the status code. Caching not recommended.

        Returns:
            dict: the status of the server
        """
        response = self.download_data("status")

        return response

    def is_healthy(self) -> bool:
        """
        Get the health of the service. Be sure to check the healthy attribute of the response, not just the status code. Caching not recommended.

        Returns:
            bool: True if service is health; False if it is not
        """
        response = self.download_data("status")

        return response.json()['data']['healthy']

    def get_meta(self) -> str:
        """
        Get service metadata, including latest version, and attribution text. Caching is encouraged, but the metadata can change weekly.

        Returns:
            str: service metadata, including latest version, and attribution text
        """
        response = self.download_data("meta")

        return response.json()["data"]

    def get_versions(self) -> list:
        """
        Version latest can be used as an alias to the latest title version. See our titles Changelog for the updates in each version.

        Returns:
            list: A list of available title versions
        """
        response = self.download_data("versions")

        return response.json()["data"]

    def get_version_info(self, version: str = "latest") -> dict:
        """
        Get version specific metadata including available fields, data versions, title counts and removed title counts.

        Returns:
            dict: Version specific metadata

        Args:
            version (str, optional): The titles classification version.
        """
        response = self.download_data(f"versions/{version}")

        return response.json()["data"]

    def get_version_changes(self, version: str = "latest") -> dict:
        """
        Get version specific changes.

        Returns:
            dict: Version specific changes

        Args:
            version (str, optional): The titles classification version.
        """
        response = self.download_data(f"versions/{version}/changes")

        return response.json()["data"]

    def get_list_all_titles(self, q: str = None, fields = ['id', 'name'], version: str = "latest", limit = None) -> list:
        """
        Returns a list of all titles in {version} sorted by title name

        Returns:
            list: Returns a list of all titles in {version} sorted by title name

        Args:
            q (str, optional): A query string of title names to search for.
            fields (list, optional): List of fields to return per title.
            version (str, optional): The titles classification version.
            limit (None, optional): Limit the number of titles returned in the response.
        """
        querystring = {"fields": ",".join(fields)}

        if q is not None:
            querystring["q"] = q

        if limit is not None:
            querystring["limit"] = limit

        response = self.download_data(f"versions/{version}/titles", querystring = querystring)

        return response.json()["data"]

    def post_list_requested_titles(self, titles: list, fields: list = ['id', 'name', 'pluralName'], version: str = "latest") -> list:
        """
        Usage information.

        Returns:
            list: the raw markdown text from the doc site (https://api.emsidata.com/apis/emsi-job-title-normalization)

        Args:
            titles (list): Description
            fields (list, optional): List of fields to return per title.
            version (str, optional): The titles classification version.
        """
        payload = {"ids": titles, "fields": fields}
        response = self.download_data(f"versions/{version}/titles", payload = payload)
        return response.json()["data"]

    def get_title_by_id(self, title_id: str, version: str = "latest") -> str:
        """
        Usage information.

        Returns:
            str: the raw markdown text from the doc site (https://api.emsidata.com/apis/emsi-job-title-normalization)

        Args:
            title_id (str): Description
            version (str, optional): The titles classification version.
        """
        response = self.download_data(f"versions/{version}/titles/{title_id}")
        return response.json()["data"]

    def post_normalize_title(self, title: str, version: str = "latest", confidenceThreshold = 0.5, fields = ['id', 'name', 'pluralName']) -> dict:
        """Normalize a raw job title string to the best matching Emsi title.

        Currently only supports the JSON usage ability for the API, no support for plain text

        Args:
            title (str): Description
            version (str, optional): The titles classification version.
            confidenceThreshold (float, optional): Description
            fields (list, optional): List of fields to return per title.

        Returns:
            dict: dictionary of the top match from the API (id, title, and similarity)
        """
        payload = {
            "term": title,
            "fields": fields,
            "confidenceThreshold": confidenceThreshold
        }
        response = self.download_data(
            f"versions/{version}/normalize",
            payload = payload
        )

        return response.json()["data"]

    def post_inspect_title_normalization(self, title: str, version: str = "latest", confidenceThreshold: float = 0.5, limit: int = 5, fields: list = ['id', 'name', 'pluralName']) -> dict:
        """Normalize a raw job title string to a list of the top matching Emsi titles.

        Currently only supports the JSON usage ability for the API, no support for plain text

        Args:
            title (str): Description
            version (str, optional): The titles classification version.
            confidenceThreshold (float, optional): Description
            limit (int, optional): Description
            fields (list, optional): List of fields to return per title.

        Returns:
            dict: dictionary of the top match from the API (id, title, and similarity)
        """
        payload = {
            "term": title,
            "confidenceThreshold": confidenceThreshold,
            "limit": limit,
            "fields": fields
        }
        response = self.download_data(f"versions/{version}/normalize/inspect", payload)

        return response.json()["data"]

    def post_normalize_titles_in_bulk(self, titles: list, version: str = "latest", confidenceThreshold: float = 0.5, fields = ['id', 'name', 'pluralName']) -> list:
        """
        Normalize multiple raw job title strings to a list of best matching Emsi titles.

        Args:
            titles (list): Description
            version (str, optional): The titles classification version.
            confidenceThreshold (float, optional): Description
            fields (list, optional): List of fields to return per title.

        Returns:
            list: dictionary of the top match from the API (id, title, and similarity)
        """
        payload = {
            "terms": titles,
            "confidenceThreshold": confidenceThreshold,
            "fields": fields
        }
        response = self.download_data(f"versions/{version}/normalize/bulk", payload = payload)

        return response.json()["data"]
