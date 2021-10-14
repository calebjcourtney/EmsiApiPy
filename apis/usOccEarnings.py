"""Summary
"""
from .base import EmsiBaseConnection


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
        """Summary
        """

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
        return self.download_data("v1/us/{}/years".format(datarun)).json()

    def post_percentile_wages(self, datarun: str, payload: dict) -> dict:
        """Summary

        Args:
            datarun (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data("v1/us/{}/percentile_wages".format(datarun), payload).json()

    def post_employment_at_wage(self, datarun: str, payload: dict) -> dict:
        """Summary

        Args:
            datarun (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data("v1/us/{}/employment_at_wage".format(datarun), payload).json()

    def postemployment_at_wage_by_occ(self, datarun: str, payload: dict) -> dict:
        """Summary

        Args:
            datarun (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data("v1/us/{}/employment_at_wage_by_occ".format(datarun), payload).json()
