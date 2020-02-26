"""Summary
"""
import requests
import pandas as pd

from ..permissions import DEFAULT


class EmsiBaseConnection(object):
    """docstring for EmsiBaseConnection

    Attributes:
        password (TYPE): Description
        token (TYPE): Description
        username (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """

        self.username, self.password = DEFAULT['username'], DEFAULT['password']

    def get_new_token(self) -> None:
        """Summary

        Raises:
            ValueError: Description

        No Longer Returned:
            str: Description
        """
        url = "https://auth.emsicloud.com/connect/token"

        payload = "grant_type=client_credentials&client_id={}&client_secret={}&scope={}".format(self.username, self.password, self.scope)
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code != 200:
            print(response.text)
            print(response.status_code)

            raise ValueError("Looks like you don't have access to this dataset with those credentials")

        self.token = response.json()['access_token']

    def get_data(self, url: str) -> requests.Response:
        """Summary

        Args:
            url (str): Description

        Returns:
            requests.Response: Description
        """
        headers = {'content-type': "application/json", 'authorization': "Bearer {}".format(self.token)}

        response = requests.get(url, headers = headers)
        if response.status_code == 401:
            self.get_new_token()
            return self.get_data(url)

        return response

    def post_data(self, url: str, payload: dict) -> requests.Response:
        """Summary

        Args:
            url (str): Description
            payload (dict): Description

        Returns:
            requests.Response: Description
        """
        headers = {'content-type': "application/json", 'authorization': "Bearer {}".format(self.token)}

        response = requests.post(url, headers = headers, json = payload)
        if response.status_code == 401:
            self.get_new_token()
            return self.post_data(url, payload)

        return response

    def download_data(self, api_endpoint, payload = None) -> requests.Response:
        """Summary

        Args:
            api_endpoint (TYPE): Description
            payload (None, optional): Description

        Returns:
            TYPE: Description
        """
        url = self.base_url + api_endpoint
        if payload is None:
            return self.get_data(url)

        else:
            return self.post_data(url, payload)


class JobPostingsConnection(EmsiBaseConnection):
    """docstring for CanadaPostingsConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (str): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()

    def querystring_endpoint(self, api_endpoint: str, querystring: str) -> requests.Response:
        """Summary

        Args:
            api_endpoint (str): Description
            querystring (str): Description

        Returns:
            requests.Response: Description

        Deleted Parameters:
            payload (None, optional): Description
        """
        url = self.base_url + api_endpoint

        headers = {'content-type': "application/json", 'authorization': "Bearer {}".format(self.token)}

        response = requests.get(url, headers = headers, params = querystring)
        if response.status_code == 401:
            self.token = self.get_new_token()
            return self.querystring_endpoint(api_endpoint, querystring)

        return response

    def get_status(self) -> str:
        """
        Summary

        Returns:
            str: Description
        """
        response = self.download_data("status")

        return response.json()['data']['message']

    def is_healthy(self) -> bool:
        """
        Summary

        Returns:
            bool: Description
        """
        response = self.download_data("status")

        return response.json()['data']['healthy']

    def get_metadata(self) -> dict:
        """
        Summary

        Returns:
            dict: Description

        Deleted Parameters:
            nation (str, optional): Description
        """
        response = self.download_data("meta")

        return response.json()['data']

    def post_totals(self, payload: dict) -> dict:
        """Summary

        Args:
            payload (TYPE): Description

        Returns:
            dict: Description
        """
        response = self.download_data('totals', payload)

        return response.json()['data']['totals']

    def post_timeseries(self, payload: dict) -> dict:
        """Summary

        Args:
            payload (TYPE): Description

        Returns:
            dict: Description
        """
        response = self.download_data('timeseries', payload)

        return response.json()['data']

    def get_rankings(self) -> dict:
        """Summary

        Returns:
            dict: Description
        """
        response = self.download_data('rankings')

        return response.json()['data']

    def post_rankings_timeseries(self, facet: str, payload: dict) -> dict:
        """Summary

        Args:
            facet (TYPE): Description
            payload (TYPE): Description

        Returns:
            dict: Description
        """
        response = self.download_data('rankings/{}/timeseries'.format(facet), payload)

        return response.json()['data']

    def post_rankings(self, facet: str, payload: dict) -> dict:
        """Summary

        Args:
            facet (TYPE): Description
            payload (TYPE): Description

        Returns:
            dict: Description
        """
        response = self.download_data("rankings/{}".format(facet), payload)

        return response.json()

    def post_nested_rankings(self, facet: str, nested_facet: str, payload: dict) -> dict:
        """Summary

        Args:
            facet (TYPE): Description
            nested_facet (TYPE): Description
            payload (TYPE): Description

        Returns:
            dict: Description
        """
        response = self.download_data("rankings/{}/rankings/{}".format(facet, nested_facet), payload)

        return response.json()

    def post_samples(self, payload: dict) -> dict:
        """Summary

        Args:
            payload (TYPE): Description

        Returns:
            dict: Description
        """
        response = self.download_data('samples', payload)

        return response.json()['data']

    def get_taxonomies(self, facet: str = None, q: str = None) -> dict:
        """Summary

        Args:
            facet (None, optional): Description
            q (None, optional): Description

        Returns:
            dict: Description
        """
        if facet is None:
            response = self.download_data("taxonomies")
        else:
            api_endpoint = "taxonomies/{}".format(facet)
            querystring = {"q": q}
            response = self.querystring_endpoint(api_endpoint, querystring)

        return response.json()['data']

    def post_taxonomies(self, facet: str, payload: dict) -> dict:
        """Summary

        Args:
            facet (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        response = self.download_data("taxonomies/{}/lookup".format(facet), payload)

        return response.json()['data']

    def post_rankings_df(self, facet: str, payload: dict) -> pd.DataFrame:
        response = self.post_rankings(facet, payload)

        df = pd.DataFrame(response['data']['ranking']['buckets'])
        df.rename(columns = {'name': facet}, inplace = True)

        return df

    def post_nested_rankings_df(self, facet: str, nested_facet: str, payload: dict) -> pd.DataFrame:
        response = self.post_nested_rankings(facet, nested_facet, payload)

        df = pd.DataFrame()
        for bucket in response['data']['ranking']['buckets']:
            temp_df = pd.DataFrame(bucket['ranking']['buckets'])
            temp_df['facet'] = bucket['name']

            df = df.append(temp_df, ignore_index = True)

        df.rename(columns = {'facet': facet, 'name': nested_facet}, inplace = True)

        return df


class ProfilesConnection(EmsiBaseConnection):
    """
    Use case
    This is an interface for retrieving aggregated Emsi profile data that is filtered, sorted and ranked by various properties of the profiles.

    About the data
    Profiles are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary

        """
        super().__init__()

    def querystring_endpoint(self, api_endpoint: str, querystring: str) -> requests.Response:
        """Summary

        Args:
            api_endpoint (str): Description
            querystring (str): Description

        Returns:
            requests.Response: Description
        """
        url = self.base_url + api_endpoint

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(self.token)
        }

        response = requests.get(url, headers = headers, params = querystring)
        if response.status_code == 401:
            self.token = self.get_new_token()
            return self.querystring_endpoint(api_endpoint, querystring)

        return response

    def get_status(self) -> str:
        """
        Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.

        Returns:
            str: Description
        """
        response = self.download_data("status")
        return response.json()['data']['message']

    def is_healthy(self) -> bool:
        """
        Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.

        Returns:
            bool: Description
        """
        response = self.download_data("status")
        return response.json()['data']['healthy']

    def get_metadata(self) -> dict:
        """
        Get service metadata, including taxonomies, available years of data (first and last year in which any available profiles were updated), and attribution text. Caching is encouraged, but the metadata may change weekly.

        Returns:
            dict: Description

        Deleted Parameters:
            nation (str, optional): Description
        """
        response = self.download_data("meta")
        return response.json()['data']

    def post_totals(self, payload: dict) -> dict:
        """Get summary metrics on all profiles matching the filters.

        Args:
            payload (dict): Description

        Returns:
            dict: Description
        """
        response = self.download_data('totals', payload)

        return response.json()['data']['totals']

    def post_recency(self, payload: dict) -> dict:
        """Group filtered profile metrics by year, based on profile recency (when they were last updated).

        Args:
            payload (dict): Description

        Returns:
            dict: Description
        """
        response = self.download_data('recency', payload)

        return response.json()['data']['recency']

    def get_rankings(self) -> dict:
        """Get a list of current available ranking facets.

        Returns:
            dict: Description
        """
        response = self.download_data('rankings')

        return response.json()['data']

    def post_rankings(self, facet: str, payload: dict) -> dict:
        """Rank profiles by a given facet

        Args:
            facet (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        response = self.download_data("rankings/{}".format(facet), payload)

        return response.json()

    def get_taxonomies(self, facet: str = None, q: str = None) -> dict:
        """
        Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete), or list taxonomy items.
        Get a list of current available taxonomy facets.
        Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete).

        Args:
            facet (str, optional): Description
            q (str, optional): Description

        Returns:
            dict: Description
        """
        if facet is None:
            response = self.download_data("taxonomies")
        else:
            api_endpoint = "taxonomies/{}".format(facet)
            querystring = {"q": q}
            response = self.querystring_endpoint(api_endpoint, querystring)

        return response.json()['data']

    def post_taxonomies(self, facet: str, payload: dict) -> dict:
        """Lookup taxonomy items by ID.

        Args:
            facet (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        response = self.download_data("taxonomies/{}/lookup".format(facet), payload)

        return response.json()['data']

    def post_rankings_df(self, facet: str, payload: dict) -> pd.DataFrame:
        """Summary

        Args:
            facet (str): Description
            payload (dict): Description

        Returns:
            pd.DataFrame: Description
        """
        response = self.post_rankings(facet, payload)
        df = pd.DataFrame(response['ranking']['buckets'])

        return df
