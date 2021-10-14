"""
This API will be removed in the future, and is here temporarily.
Since it will be removed, no additional work will be done on this integration to support it.

https://api.emsidata.com/apis/emsi-acs-indicators
"""

from .base import EmsiBaseConnection


class ACSIndicatorsConnection(EmsiBaseConnection):
    """docstring for ACSIndicatorsConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://emsiservices.com/acs/"
        self.scope = "acs"

        self.get_new_token()

        self.name = "ACS"

    def get_metrics(self, metric_name: str = None) -> dict:
        """
        Summary

        Returns:
            dict: Description

        Args:
            metric_name (str, optional): Description
        """
        if metric_name is None:
            response = self.download_data("meta/metrics")
        else:
            response = self.download_data("meta/metrics/{}".format(metric_name))

        return response.json()['data']

    def get_level(self, level: str, metrics_list: list) -> dict:
        """
        Summary

        Args:
            level (str): Description
            metrics_list (list): Description

        Returns:
            dict: Description
        """
        querystring = {"metrics": ",".join(metrics_list)}
        response = self.download_data(level, querystring=querystring)

        return response.json()['data']

    def post_level(self, level: str, payload: dict) -> dict:
        """Summary

        Args:
            level (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        response = self.download_data(level, payload)

        return response.json()['data']
