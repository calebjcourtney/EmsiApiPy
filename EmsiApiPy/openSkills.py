"""
Summary
"""
from __future__ import annotations

from base import EmsiBaseConnection


class SkillsClassificationConnection(EmsiBaseConnection):
    """docstring for SkillsClassificationConnection

    Attributes:
        base_url (str): Description
        scope (str): Description

    Deleted Attributes:
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary"""
        super().__init__()
        self.base_url = "https://emsiservices.com/skills/"
        self.scope = "emsi_open"

        self.get_new_token()

        self.name = "Skills"

    def get_meta(self):
        return self.get_versions()

    def get_versions(self) -> list:
        """Summary

        Returns:
            list: Description
        """
        return self.download_data("versions").json()

    def get_version_metadata(self, version="latest") -> list:
        """Summary

        Returns:
            list: Description

        Args:
            version (str, optional): Description
        """
        return self.download_data(f"versions/{version}").json()

    def get_version_changes(self, version="latest") -> dict:
        """Summary

        Args:
            version (str, optional): Description

        Returns:
            dict: Description
        """
        response = self.download_data(f"versions/{version}/changes")
        data = response.json()["data"]

        return data

    def get_list_all_skills(
        self,
        version: str = "latest",
        q: str | None = None,
        typeIds: str | None = None,
        fields: str | None = None,
    ) -> dict:
        """Summary

        Args:
            version (str, optional): Description
            q (str, optional): Description
            typeIds (str, optional): Description
            fields (str, optional): Description

        Returns:
            list: Description
        """

        base_querystring = {
            "q": q,
            "typeIds": typeIds,
            "fields": fields,
        }

        querystring = {}

        for key, value in base_querystring.items():
            if value is not None:
                querystring[key] = value

        if len(querystring) > 0:
            return self.download_data(
                f"versions/{version}/skills",
                querystring=querystring,
            ).json()

        else:
            return self.download_data(f"versions/{version}/skills").json()

    def post_list_requested_skills(
        self,
        payload: dict,
        version: str = "latest",
        typeIds=None,
        fields=None,
    ) -> dict:
        """Summary

        Args:
            payload (dict): Description
            version (str, optional): Description
            typeIds (None, optional): Description
            fields (None, optional): Description

        Returns:
            dict: Description
        """

        base_querystring = {
            "typeIds": typeIds,
            "fields": fields,
        }

        querystring: dict = {}
        for key, value in base_querystring.items():
            if value is None:
                querystring[key] = value

        if len(querystring) > 0:
            return self.download_data(
                f"versions/{version}/skills",
                payload=payload,
                querystring=querystring,
            ).json()

        else:
            return self.download_data(
                f"versions/{version}/skills",
                payload=payload,
            ).json()

    def get_skill_by_id(self, skill_id: str, version: str = "latest") -> dict:
        """Summary

        Args:
            skill_id (str): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data(
            f"versions/{version}/skills/{skill_id}",
        ).json()

    def post_find_related_skills(
        self,
        skill_ids: list,
        limit=10,
        fields=["id", "name", "type", "infoUrl"],
        version: str = "latest",
    ):
        """Summary

        Args:
            skill_ids (list): Description
            limit (int, optional): Description
            fields (list, optional): Description
            version (str, optional): Description

        Returns:
            TYPE: Description
        """
        payload = {
            "ids": skill_ids,
            "limit": limit,
            "fields": fields,
        }
        return self.download_data(
            f"versions/{version}/related",
            payload=payload,
        ).json()

    def post_extract(
        self,
        description: str,
        version: str = "latest",
        confidenceThreshold: float = 0.5,
    ) -> dict:
        """Summary

        Args:
            description (str): Description
            version (str, optional): Description
            confidenceThreshold (float, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data(
            f"versions/{version}/extract",
            payload={"text": description},
            querystring={"confidenceThreshold": confidenceThreshold},
        ).json()

    def post_extract_with_source(
        self,
        description: str,
        version: str = "latest",
        includeNormalizedText: bool = False,
    ) -> dict:
        """Summary

        Args:
            description (str): Description
            version (str, optional): Description
            includeNormalizedText (bool, optional): Description

        Returns:
            dict: Description

        Deleted Parameters:
            confidenceThreshold (float, optional): Description
        """
        return self.download_data(
            f"versions/{version}/extract/trace",
            payload={
                "text": description,
                "includeNormalizedText": includeNormalizedText,
            },
        ).json()
