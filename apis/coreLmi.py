"""
import EmsiApiPy

conn = EmsiApiPy.CoreLMIConnection()

dataset = "emsi.us.grossregionalproduct"

dimension = "Area"

df = conn.get_dimension_hierarchy_df(dataset = dataset, dimension = dimension)

print(df.head())

#    child parent           name abbr level_name display_id
# 0      0      0  United States   US          1          0
# 1      1      0        Alabama   AL          2          1
# 2     10      0       Delaware   DE          2         10
# 3  10001     10           Kent   DE          3      10001
# 4  10003     10     New Castle   DE          3      10003

# limit only to the states
df = df.loc[df['level_name'] == '2']

# get the 2019 GRP for each state in the US
payload = {
    "metrics": [
        {
            "name": "Dollars.2019"
        }
    ],
    "constraints": [
        {
            "dimensionName": "Area",
            "map": {row[1]['name']: [row[1]["child"]] for row in df.iterrows()}
        }
    ]
}

data_df = conn.post_retrieve_df(dataset = dataset, payload = payload)
print(data_df.head())

#          Area  Dollars.2019
# 0     Alabama  2.234497e+11
# 1      Alaska  5.222207e+10
# 2     Arizona  3.504984e+11
# 3    Arkansas  1.297678e+11
# 4  California  3.013869e+12
"""

import requests
from dateutil import parser
import datetime
import pandas as pd
import time

from .base import EmsiBaseConnection


class CoreLMIConnection(EmsiBaseConnection):
    """Summary

    Attributes:
        base_url (str): the base url used for querying the API
        limit_remaining (int): the number of queries made within the allowed time period
        limit_reset (int): the time the limit will reset on the queries allowed
        scope (str): scope to be passed to the OAuth server
        token (str): token received back from the OAuth server
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

    def download_data(self, api_endpoint: str, payload: dict = None, smart_limit: bool = False) -> requests.Response:
        """Needs more work for downloading the data from Agnitio, since it does not automatically handle the rate liimit from the API

        Args:
            api_endpoint (str): the url endpoint to query
            payload (dict, optional): the payload to pass to the API. if no payload, then a GET request will be made.

        Returns:
            requests.Response: The response from the server
        """
        # possible addition of adding smart_limit
        # for now, if smart_limit is true, then it will simply wait 1 second before returning data
        if smart_limit:
            time.sleep(1)

        # currently in-progress:
        #       - track the limit remaining
        #       - sleep for a longer or shorter amount of time depending on number of requests left
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

        # we've run out of requests
        if response.status_code == 429:
            # wait until the limit has reset then run again
            time.sleep(300)

            return self.download_data(api_endpoint, payload)

        elif response.status_code != 200:
            import json
            print(json.dumps(payload))
            print(url)
            print(response.text)

        # limit information
        self.limit_remaining = int(response.headers['X-Rate-Limit-Remaining'])
        self.limit_reset = parser.parse(response.headers['X-Rate-Limit-Reset'])
        self.limit_reset = self.limit_reset.replace(tzinfo = None)

        return response

    def get_meta(self) -> dict:
        """
        You can use this interface (which uses these data discovery endpoints) to browse available datasets. Your contract with Emsi will determine which datasets you have access to, and you can list these datasets and their versions by querying the /meta endpoint

        Returns:
            dict: json data response from the server
        """
        response = self.download_data("meta")

        return response.json()

    def get_meta_definitions(self) -> dict:
        """
        You can use this interface (which uses these data discovery endpoints) to browse available datasets. Your contract with Emsi will determine which datasets you have access to, and you can list these datasets and their versions by querying the /meta endpoint

        Returns:
            dict: json data response from the server
        """
        response = self.download_data("meta/definitions")

        return response.json()

    def get_meta_dataset(self, dataset: str, datarun: str) -> list:
        """
        Available versions of a specific dataset can be retrieved by adding dataset/<name> to the path

        Args:
            dataset (str): the dataset to query (e.g. `emsi.us.occupation`)
            datarun (str): the data version to use when querying the dataset (e.g. `2020.3`)

        Returns:
            list: list of dataset versions available
        """
        response = self.download_data("meta/dataset/{}/{}".format(dataset, datarun))

        return response.json()

    def get_meta_dataset_dimension(self, dataset: str, dimension: str, datarun: str) -> dict:
        """
        Finally, you can view the hierarchy of a particular dimension of a dataset by adding dataset/<name>/<version>/<dimension> to the path:

        Args:
            dataset (str): the dataset to query (e.g. `emsi.us.occupation`)
            dimension (str): the dimension of the data to get a hierarchy for
            datarun (str): the data version to use when querying the dataset (e.g. `2020.3`)

        Returns:
            dict: hierarchichal representation of the dimension of data for the particular dataset
        """
        response = self.download_data("meta/dataset/{}/{}/{}".format(dataset, datarun, dimension))

        return response.json()

    def post_retrieve_data(self, dataset: str, payload: dict, datarun: str) -> dict:
        """
        Agnitio data queries are performed by assembling a JSON description of the query and POSTing it to the specific dataset you wish to query.

        Args:
            dataset (str): the dataset to query (e.g. `emsi.us.occupation`)
            payload (dict): the json data to be sent to the API
            datarun (str): the data version to use when querying the dataset (e.g. `2020.3`)

        Returns:
            dict: full data returned from the API
        """
        response = self.download_data("{}/{}".format(dataset, datarun), payload)

        return response.json()

    def get_dimension_hierarchy_df(self, dataset: str, dimension: str, datarun: str) -> pd.DataFrame:
        """
        Finally, you can view the hierarchy of a particular dimension of a dataset by adding dataset/<name>/<version>/<dimension> to the path:

        Args:
            dataset (str): the dataset to query (e.g. `emsi.us.occupation`)
            dimension (str): the dimension of the data to get a hierarchy for
            datarun (str): the data version to use when querying the dataset (e.g. `2020.3`)

        Returns:
            pd.DataFrame: Hierarchy data parsed into a pd.DataFrame
        """
        data = self.get_meta_dataset_dimension(dataset, dimension, datarun)
        df = pd.DataFrame(data['hierarchy'])

        return df

    def post_retrieve_df(self, dataset: str, payload: dict, datarun: str) -> pd.DataFrame:
        """
        Agnitio data queries are performed by assembling a JSON description of the query and POSTing it to the specific dataset you wish to query.

        Args:
            dataset (str): the dataset to query (e.g. `emsi.us.occupation`)
            payload (dict): the json data to be sent to the API
            datarun (str): the data version to use when querying the dataset (e.g. `2020.3`)

        Returns:
            pd.DataFrame: Data from the API in a pd.DataFrame
        """
        response = self.post_retrieve_data(dataset, payload, datarun)
        df = pd.DataFrame()
        for column in response['data']:
            df[column['name']] = column['rows']

        return df
