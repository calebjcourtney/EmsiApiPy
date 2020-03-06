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
            TYPE: Description
        """
        return self.download_data("status").json()

    def is_healthy(self) -> bool:
        """
        Summary

        Returns:
            TYPE: Description
        """
        return self.download_data("status").json()['data']['healthy']

    def extract(self, description: str, version: str = 'latest') -> dict:
        """Summary

        Args:
            description (str): Description
            version (str, optional): Description

        Returns:
            dict: Description
        """
        return self.download_data("versions/{}/extract".format(version), {"full_text": description}).json()
