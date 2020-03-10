"""Summary
"""
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
        """Summary
        """

        super().__init__()
        self.base_url = "https://comp.emsicloud.com/"
        self.scope = "emsiauth"

        self.token = ""
        self.get_new_token()

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
