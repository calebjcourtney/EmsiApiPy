"""Summary
"""
import requests

from base import EmsiBaseConnection


class AggregateProfilesConnection(EmsiBaseConnection):
    """docstring for AggregateProfilesConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self, username: str, password: str) -> None:
        """Summary

        Args:
            username (str): Description
            password (str): Description
        """
        super().__init__(username, password)
        self.base_url = "https://emsiservices.com/profiles/"
        self.scope = "profiles:us"

        self.token = self.get_new_token()

    def download_data(self, api_endpoint, payload = None):
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

    def querystring_endpoint(self, api_endpoint, querystring):
        """Summary

        Args:
            api_endpoint (TYPE): Description
            querystring (TYPE): Description

        Returns:
            TYPE: Description

        Deleted Parameters:
            payload (None, optional): Description
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

    def get_status(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = self.base_url + "status"
        response = requests.request("GET", url)

        return response.json()['data']['message']

    def is_healthy(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = "https://emsiservices.com/profiles/status"
        response = requests.request("GET", url)

        return response.json()['data']['healthy']

    def get_metadata(self):
        """
        Summary

        Returns:
            TYPE: Description

        Deleted Parameters:
            nation (str, optional): Description
        """
        response = self.download_data("meta")

        return response.json()['data']

    def post_totals(self, payload):
        """Summary

        Args:
            payload (TYPE): Description

        Returns:
            TYPE: Description
        """
        response = self.download_data('totals', payload)

        return response.json()['data']['totals']

    def post_recency(self, payload):
        """Summary

        Args:
            payload (TYPE): Description

        Returns:
            TYPE: Description
        """
        response = self.download_data('recency', payload)

        return response.json()['data']['recency']

    def get_rankings(self):
        """Summary

        Returns:
            TYPE: Description
        """
        response = self.download_data('rankings')

        return response.json()['data']

    def post_rankings(self, facet, payload):
        """Summary

        Args:
            facet (TYPE): Description
            payload (TYPE): Description

        Returns:
            TYPE: Description
        """
        response = self.download_data("rankings/{}".format(facet), payload)

        return response.json()

    def get_taxonomies(self, facet = None, q = None):
        """Summary

        Args:
            facet (None, optional): Description
            q (None, optional): Description

        Returns:
            TYPE: Description
        """
        if facet is None:
            response = self.download_data("taxonomies")
        else:
            api_endpoint = "taxonomies/{}".format(facet)
            querystring = {"q": q}
            response = self.querystring_endpoint(api_endpoint, querystring)

        return response.json()['data']

    def post_taxonomies(self, facet, payload):
        """Summary

        Args:
            facet (TYPE): Description
            payload (TYPE): Description

        Returns:
            TYPE: Description
        """
        response = self.download_data("taxonomies/{}/lookup".format(facet), payload)

        return response.json()['data']


###### TESTS ######
def test_profiles_conn():
    """Summary
    """
    import configparser
    config = configparser.ConfigParser()
    config.read('permissions.ini')

    if 'AggregateProfilesConnection' in config.sections():
        conn = AggregateProfilesConnection(config['AggregateProfilesConnection']['username'], config['AggregateProfilesConnection']['password'])
    else:
        conn = AggregateProfilesConnection(config['DEFAULT']['username'], config['DEFAULT']['password'])

    response = conn.get_metadata()

    assert response is not None, "No index data returned"
    assert response != [], "No index data returned"


if __name__ == '__main__':
    test_profiles_conn()
