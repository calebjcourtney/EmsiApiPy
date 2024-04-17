"""Summary
"""
from __future__ import annotations

from base import EmsiBaseConnection


class UsOccupationEarningsConnection(EmsiBaseConnection):
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
        self.base_url = "https://earnings.emsicloud.com/"
        self.scope = "occearn"

        self.get_new_token()

        self.name = "US_OccupationEarnings"

    def get_versions(self) -> list:
        """Summary

        Returns:
            list: Description
        """
        return self.download_data("v1/us/").json()

    def get_datarun_years(self, datarun: str) -> list:
        """Summary

        Args:
            datarun (str): Description

        Returns:
            list: Description
        """
        return self.download_data(f"v1/us/{datarun}/years").json()

    def post_percentile_wages(self, datarun: str, payload: dict) -> dict:
        """Summary

        Args:
            datarun (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data(
            f"v1/us/{datarun}/percentile_wages",
            payload,
        ).json()

    def post_employment_at_wage(self, datarun: str, payload: dict) -> dict:
        """Summary

        Args:
            datarun (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data(
            f"v1/us/{datarun}/employment_at_wage",
            payload,
        ).json()

    def postemployment_at_wage_by_occ(
        self,
        datarun: str,
        payload: dict,
    ) -> dict:
        """Summary

        Args:
            datarun (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data(
            f"v1/us/{datarun}/employment_at_wage_by_occ",
            payload,
        ).json()
