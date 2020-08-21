"""Summary
"""
import requests
from dateutil import parser
import datetime
import pandas as pd

from .base import EmsiBaseConnection


class CoreLMIConnection(EmsiBaseConnection):
    """Summary

    Attributes:
        base_url (str): Description
        limit_remaining (int): Description
        limit_reset (TYPE): Description
        scope (str): Description
        token (str): Description
    """

    def __init__(self) -> None:
        """Summary
        """

        super().__init__()
        self.base_url = "https://agnitio.emsicloud.com/"
        self.scope = "emsiauth"

        self.token = ""
        self.get_new_token()
        self.limit_remaining = 300
        self.limit_reset = datetime.datetime.now()
        self.limit_reset += datetime.timedelta(0, 300)

    def download_data(self, api_endpoint: str, payload: dict = None, smart_limit: bool = True) -> requests.Response:
        """Summary

        Args:
            api_endpoint (str): Description
            payload (dict, optional): Description

        Returns:
            requests.Response: Description
        """
        # if smart_limit:
        #     try:
        #         time.sleep((self.limit_reset - datetime.datetime.now()).total_seconds() / self.limit_remaining)
        #     except ZeroDivisionError:
        #         time.sleep((self.limit_reset - datetime.datetime.now()).total_seconds())
        #         self.limit_remaining = 300
        #         self.limit_reset = datetime.datetime.now() + datetime.timedelta(0, 300)

        url = self.base_url + api_endpoint
        if payload is None:
            response = self.get_data(url)

        else:
            response = self.post_data(url, payload)

        if response.status_code == 429:
            import time
            time.sleep(300)

            return self.download_data(api_endpoint, payload)

        self.limit_remaining = int(response.headers['X-Rate-Limit-Remaining'])
        self.limit_reset = parser.parse(response.headers['X-Rate-Limit-Reset'])
        self.limit_reset = self.limit_reset.replace(tzinfo = None)

        return response

    def get_meta(self) -> dict:
        """Summary

        Returns:
            dict: Description
        """
        response = self.download_data("meta")

        return response.json()

    def get_meta_dataset(self, dataset: str, datarun: str) -> dict:
        """Summary

        Args:
            dataset (str): Description
            datarun (str, optional): Description

        Returns:
            dict: Description
        """
        response = self.download_data("meta/dataset/{}/{}".format(dataset, datarun))

        return response.json()

    def get_meta_dataset_dimension(self, dataset: str, dimension: str, datarun: str) -> dict:
        """Summary

        Args:
            dataset (str): Description
            dimension (str): Description
            datarun (str, optional): Description

        Returns:
            dict: Description
        """
        response = self.download_data("meta/dataset/{}/{}/{}".format(dataset, datarun, dimension))

        return response.json()

    def post_retrieve_data(self, dataset: str, payload: dict, datarun: str) -> dict:
        """Summary

        Args:
            dataset (str): Description
            payload (dict): Description
            datarun (str, optional): Description

        Returns:
            dict: Description
        """
        response = self.download_data("{}/{}".format(dataset, datarun), payload)

        return response.json()

    def get_dimension_hierarchy_df(self, dataset: str, dimension: str, datarun: str) -> pd.DataFrame:
        """Summary

        Args:
            dataset (str): Description
            dimension (str): Description
            datarun (str, optional): Description

        Returns:
            pd.DataFrame: Description
        """
        data = self.get_meta_dataset_dimension(dataset, dimension, datarun)
        df = pd.DataFrame(data['hierarchy'])

        return df

    def post_retrieve_df(self, dataset: str, payload: dict, datarun: str) -> pd.DataFrame:
        """Summary

        Args:
            dataset (str): Description
            payload (dict): Description
            datarun (str, optional): Description

        Returns:
            pd.DataFrame: Description
        """
        response = self.post_retrieve_data(dataset, payload, datarun)
        df = pd.DataFrame()
        for column in response['data']:
            df[column['name']] = column['rows']

        return df
