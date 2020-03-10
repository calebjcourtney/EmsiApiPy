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

        self.token = ""
        self.get_new_token()

    def get_status(self):
        return self.download_data("status").status_code

    def get_versions(self):
        return self.download_data("v1/us/").json()

    def get_datarun_years(self, datarun):
        return self.download_data("v1/us/{}/years".format(datarun)).json()

    def post_percentile_wages(self, datarun, payload):
        return self.download_data("v1/us/{}/percentile_wages".format(datarun), payload).json()

    def post_employment_at_wage(self, datarun, payload):
        return self.download_data("v1/us/{}/employment_at_wage".format(datarun), payload).json()

    def postemployment_at_wage_by_occ(self, datarun, payload):
        return self.download_data("v1/us/{}/employment_at_wage_by_occ".format(datarun), payload).json()

    def post_estimate(self, payload):
        """Summary
        """
        response = self.download_data("estimate", payload)
        return response.json()

    def post_estimate_by_experience(self, payload):
        """Summary
        """
        response = self.download_data("estimate_by_experience", payload)
        return response.json()

    def post_by_msa(self, payload):
        """Summary
        """
        response = self.download_data("by_msa", payload)
        return response.json()

    def get_geographies(self):
        """Summary
        """
        response = self.download_data("geographies")
        return response.json()

    def get_edlevels(self):
        """Summary
        """
        response = self.download_data("edlevels")
        return response.json()

    def get_datarun(self):
        """Summary
        """
        response = self.download_data("datarun")
        return response.text

    def get_soc_version(self):
        """Summary
        """
        response = self.download_data("soc_version")
        return response.text
