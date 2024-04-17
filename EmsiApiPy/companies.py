"""
This service takes text describing a job and normalizes it into a standardized job title from Emsi's job title taxonomy.
https://api.emsidata.com/apis/titles
"""
from __future__ import annotations

from base import EmsiBaseConnection


class CompaniesConnection(EmsiBaseConnection):
    """
    This API exposes the complete collection of Emsi titles which includes curated occupation and skill mappings for each title and normalization functionality to transform raw job titles to Emsi titles.

    Attributes:
        base_url (str): base url for the API
        scope (str): scope used to request access from the OAuth server
    """

    def __init__(self) -> None:
        """Summary"""
        super().__init__()
        self.base_url = "https://emsiservices.com/companies/"
        self.scope = "companies"

        self.get_new_token()

        self.name = "Companies"

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

    def get_list_all_companies(
        self,
        fields=["id", "name"],
        version: str = "latest",
        limit=None,
        after=None,
    ) -> list:
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

        if limit is not None:
            querystring["limit"] = limit

        if after is not None:
            querystring["after"] = after

        response = self.download_data(
            f"versions/{version}/companies",
            querystring=querystring,
        )

        return response.json()

    def post_list_requested_companies(
        self,
        companies: list,
        fields: list = ["id", "name"],
        version: str = "latest",
    ) -> list:
        """
        Usage information.

        Returns:
            list: the raw markdown text from the doc site (https://api.emsidata.com/apis/emsi-job-title-normalization)

        Args:
            companies (list): Description
            fields (list, optional): List of fields to return per title.
            version (str, optional): The companies classification version.
        """
        payload = {"ids": companies, "fields": fields}
        response = self.download_data(
            f"versions/{version}/companies",
            payload=payload,
        )
        return response.json()["data"]

    def get_company_by_id(
        self,
        company_id: str,
        version: str = "latest",
    ) -> str:
        """
        Usage information.

        Returns:
            str: the raw markdown text from the doc site (https://api.emsidata.com/apis/emsi-job-title-normalization)

        Args:
            company_id (str): Description
            version (str, optional): The titles classification version.
        """
        response = self.download_data(
            f"versions/{version}/companies/{company_id}",
        )
        return response.json()["data"]

    def post_normalize_company(
        self,
        title: str,
        version: str = "latest",
        fields=["id", "name"],
    ) -> dict:
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
        payload = {"term": title, "fields": fields}
        response = self.download_data(
            f"versions/{version}/normalize",
            payload=payload,
        )

        return response.json()["data"]

    def post_inspect_company_normalization(
        self,
        title: str,
        version: str = "latest",
        limit: int = 5,
        fields: list = ["id", "name"],
    ) -> dict:
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
        payload = {"term": title, "limit": limit, "fields": fields}
        response = self.download_data(
            f"versions/{version}/normalize/inspect",
            payload,
        )

        return response.json()["data"]

    def post_normalize_companies_in_bulk(
        self,
        titles: list,
        version: str = "latest",
        fields=["id", "name"],
    ) -> list:
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
        payload = {"terms": titles, "fields": fields}
        response = self.download_data(
            f"versions/{version}/normalize/bulk",
            payload=payload,
        )

        return response.json()["data"]
