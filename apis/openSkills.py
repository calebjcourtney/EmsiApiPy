"""
Summary
"""
from .base import EmsiBaseConnection


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
        self.base_url = "https://skills.emsicloud.com/"
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

    def get_documentation(self) -> str:
        """Summary

        Returns:
            str: Description
        """
        return self.download_data("docs").text

    def get_changelog(self) -> str:
        """Summary

        Returns:
            str: Description
        """
        return self.download_data("docs/changelog").text

    def get_versions(self) -> list:
        """Summary

        Returns:
            list: Description
        """
        return self.download_data("versions").json()

    def get_list_all_skills(self, version = "latest") -> list:
        """Summary

        Args:
            version (str, optional): Description

        Returns:
            list: Description
        """
        return self.download_data("versions/{}/skills".format(version)).json()

    def post_list_requested_skills(self, payload: dict = None, querystring: dict = None, version: str = "latest") -> dict:
        """Summary

        Args:
            payload (dict): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/skills".format(version), payload, querystring).json()

    def get_search_skills(self, skill_name: str, version: str = "latest") -> dict:
        """Summary

        Args:
            skill_name (str): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        query = {"q": skill_name}
        return self.download_data("versions/{}/skills".format(version), querystring = query).json()

    def get_skills_fields(self, fields: list, version: str = "latest") -> dict:
        """Summary

        Args:
            fields (list): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        query = {"fields": ",".join(fields)}
        return self.download_data("versions/{}/skills".format(version), querystring = query).json()

    def get_skill_by_id(self, skill_id: str, version: str = "latest") -> dict:
        """Summary

        Args:
            skill_id (str): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/skills/{}".format(version, skill_id)).json()

    def get_fields(self, version: str = "latest") -> dict:
        """Summary

        Args:
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/fields".format(version)).json()

    def get_skill_types(self, version: str = "latest") -> dict:
        """Summary

        Args:
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/types".format(version)).json()

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
        return self.download_data("versions/{}/extract".format(version), payload = description, querystring = {"trace":"true"}).json()
