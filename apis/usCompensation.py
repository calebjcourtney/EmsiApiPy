"""Summary
"""
from __future__ import annotations

from .base import EmsiBaseConnection


class UsCompensationConnection(EmsiBaseConnection):
    """Summary

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (str): Description

    Deleted Attributes:
        limit_remaining (int): Description
        limit_reset (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary"""

        super().__init__()
        self.base_url = "https://comp.emsicloud.com/"
        self.scope = "emsiauth"

        self.get_new_token()

        self.name = "US_Compensation"

    def post_estimate(self, payload: dict) -> dict:
        """Summary

        Args:
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data("estimate", payload).json()

    def post_estimate_by_experience(self, payload: dict) -> dict:
        """Summary

        Args:
            payload (TYPE): Description

        Returns:
            dict: Description
        """
        return self.download_data("estimate_by_experience", payload).json()

    def post_by_msa(self, payload: dict) -> dict:
        """Summary

        Args:
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data("by_msa", payload).json()

    def get_geographies(self) -> dict:
        """Summary

        Returns:
            dict: Description
        """
        return self.download_data("geographies").json()

    def get_edlevels(self) -> dict:
        """Summary

        Returns:
            dict: Description
        """
        return self.download_data("edlevels").json()

    def get_datarun(self) -> str:
        """Summary

        Returns:
            str: Description
        """
        return self.download_data("datarun").text

    def get_soc_version(self) -> str:
        """Summary

        Returns:
            str: Description
        """
        return self.download_data("soc_version").text
