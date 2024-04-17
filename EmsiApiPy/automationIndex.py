"""
This API is deprecated and will be removed in the future.
No new features will be added here.

https://api.emsidata.com/apis/automation-index
"""
from __future__ import annotations

from base import EmsiBaseConnection


class AutomationIndexConnection(EmsiBaseConnection):
    """docstring for AutomationIndexConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary"""
        super().__init__()
        self.base_url = "https://emsiservices.com/automation-index/"
        self.scope = "automation-index"

        self.get_new_token()

        self.name = "Automation_Index"

    def get_meta(self):
        # redefine the meta schema that was used in Emsi Base
        return self.get_metadata()

    def get_available_endpoints(self):
        """
        List available endpoints.

        Returns:
            TYPE: Description
        """
        response = self.download_data("")

        return response.json()["data"]["endpoints"]

    def get_countries(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        endpoints = self.get_available_endpoints()
        endpoints.remove("/status")

        return endpoints

    def get_metadata(self, nation="us"):
        """
        Summary

        Args:
            nation (str, optional): Description

        Returns:
            TYPE: Description
        """
        api_endpoint = f"/{nation}/meta"
        response = self.download_data(api_endpoint)

        return response.json()["data"]

    def get_index(self, nation="us"):
        """Summary

        Args:
            nation (str, optional): Description

        Returns:
            TYPE: Description
        """
        api_endpoint = f"/{nation}/data"
        response = self.download_data(api_endpoint)

        return response.json()["data"]

    def filter_soc_index(self, soc_code, nation="us"):
        """Summary

        Args:
            soc_code (TYPE): Description
            nation (str, optional): Description

        Raises:
            ValueError: Description

        Returns:
            TYPE: Description
        """
        if type(soc_code) != list and type(soc_code) != str:
            raise ValueError(
                "input `soc_code` must be one of type `list` or `str`",
            )

        if type(soc_code) == list:
            payload = soc_code
        elif "," in soc_code:
            payload = soc_code.split(",")
        else:
            payload = [soc_code]

        index = self.get_index(nation)

        output = {}
        for soc in payload:
            try:
                output[soc] = index[soc]
            except ValueError:
                raise ValueError(f"`soc_code` '{soc}' is invalid")

        return output
