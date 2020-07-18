"""
Summary
"""
from .base import EmsiBaseConnection
import json


class SkillsClassificationConnection(EmsiBaseConnection):
    """docstring for SkillsClassificationConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://emsiservices.com/skills/"
        self.scope = "emsi_open"

        self.token = self.get_new_token()

    def get_status(self) -> dict:
        """
        Summary

        Returns:
            dict: Description
        """
        return self.download_data("status")

    def is_healthy(self) -> bool:
        """
        Summary

        Returns:
            bool: Description
        """
        return self.download_data("status").json()['data']['healthy']

    def get_versions(self) -> list:
        """Summary

        Returns:
            list: Description
        """
        return self.download_data("versions").json()

    def get_version_metadata(self, version = "latest") -> list:
        """Summary

        Returns:
            list: Description

        Args:
            version (str, optional): Description
        """
        return self.download_data(f"versions/{version}").json()

    def get_list_all_skills(self, version: str = "latest", q: str = None, typeIds: str = None, fields: str = None) -> list:
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
            "fields": fields
        }

        querystring: dict = {}

        for key, value in base_querystring.items():
            if value is None:
                querystring[key] = value

        if len(querystring) > 0:
            return self.download_data("versions/{}/skills".format(version), querystring = querystring).json()

        else:
            return self.download_data("versions/{}/skills".format(version)).json()

    def post_list_requested_skills(self, payload: dict, version: str = "latest", typeIds = None, fields = None) -> dict:
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
            "fields": fields
        }

        querystring: dict = {}
        for key, value in base_querystring.items():
            if value is None:
                querystring[key] = value

        if len(querystring) > 0:
            return self.download_data("versions/{}/skills".format(version), payload = payload, querystring = querystring).json()

        else:
            return self.download_data("versions/{}/skills".format(version), payload = payload).json()

    def get_skill_by_id(self, skill_id: str, version: str = "latest") -> dict:
        """Summary

        Args:
            skill_id (str): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/skills/{}".format(version, skill_id)).json()

    def post_find_related_skills(self, skill_ids: list, version: str = "latest"):
        """Summary

        Args:
            skill_ids (list): Description
            version (str, optional): Description

        Returns:
            TYPE: Description
        """
        payload = json.dumps({"ids":  skill_ids})
        return self.download_data("versions/{}/related".format(version), payload = payload).json()

    def post_extract(self, description: str, version: str = 'latest') -> dict:
        """Summary

        Args:
            description (str): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/extract".format(version), payload = description).json()

    def post_extract_with_source(self, description: str, version: str = 'latest') -> dict:
        """Summary

        Args:
            description (str): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/extract/trace".format(version), payload = description).json()
