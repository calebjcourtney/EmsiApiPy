"""Summary
"""
import requests

from base import EmsiBaseConnection


class CanadaPostingsConnection(EmsiBaseConnection):
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
        self.base_url = "https://emsiservices.com/ca-jpa/"
        self.scope = "postings:ca"

        self.token = self.get_new_token()

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


###### TESTS ######
def test_ca_jpa_conn():
    """Summary
    """
    conn = CanadaPostingsConnection()

    response = conn.get_metadata()

    assert response is not None, "No index data returned"
    assert response != [], "No index data returned"


if __name__ == '__main__':
    test_ca_jpa_conn()
