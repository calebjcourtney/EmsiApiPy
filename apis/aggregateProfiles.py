"""Summary
"""
import unittest

import requests
import pandas as pd


from .base import EmsiBaseConnection


class AggregateProfilesConnection(EmsiBaseConnection):
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
        self.base_url = "https://emsiservices.com/profiles/"
        self.scope = "profiles:us"

        self.token = self.get_new_token()

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


class TestAggregateProfilesConnection(unittest.TestCase):
    """
    Our basic test class
    """

    conn = AggregateProfilesConnection()

    def test_metadata(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        conn = AggregateProfilesConnection()
        response = conn.get_metadata()

        assert response is not None, "No index data returned"
        assert response != [], "No index data returned"


if __name__ == '__main__':
    unittest.main()
