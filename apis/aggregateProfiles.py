"""Summary
"""
import requests

from base import EmsiBaseConnection


class AggregateProfilesConnection(EmsiBaseConnection):
    """docstring for AggregateProfilesConnection

    Deleted Attributes:
        password (TYPE): Description
        username (TYPE): Description
    """

    def get_new_token(self):
        """Summary

        Returns:
            TYPE: Description

        Raises:
            ValueError: Description
        """
        url = "https://auth.emsicloud.com/connect/token"

        payload = "grant_type=client_credentials&client_id={}&client_secret={}&scope=profiles:us".format(self.username, self.password)
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code != 200:
            print(response.text)
            print(response.status_code)

            raise ValueError("Looks like you don't have access to this dataset with those credentials")

        return response.json()['access_token']

    def download_data(self, api_endpoint, payload = None):
        """Summary

        Args:
            api_endpoint (TYPE): Description
            payload (None, optional): Description

        Returns:
            TYPE: Description
        """
        url = "https://emsiservices.com/profiles/" + api_endpoint
        if payload is None:
            return self.get_data(url)

        else:
            return self.post_data(url, payload)

    def querystring_endpoint(self, api_endpoint, querystring):
        """Summary

        Args:
            api_endpoint (TYPE): Description
            payload (None, optional): Description

        Returns:
            TYPE: Description
        """
        url = "https://emsiservices.com/profiles/" + api_endpoint

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(self.token)
        }

        response = requests.get(url, headers = headers, params = querystring)
        if response.status_code == 401:
            self.token = self.get_new_token()
            return self.querystring_endpoint(api_endpoint, querystring)

        return response

    def get_available_endpoints(self):
        """
        List available endpoints.

        Returns:
            TYPE: Description
        """
        response = self.download_data("")

        return response.json()['data']['endpoints']

    def get_status(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = "https://emsiservices.com/profiles/status"
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

        Args:
            nation (str, optional): Description

        Returns:
            TYPE: Description
        """
        api_endpoint = "/meta"
        response = self.download_data(api_endpoint)

        return response.json()['data']

    def post_totals(self, payload):
        response = self.download_data('totals', payload)

        return response.json()['data']['totals']

    def post_recency(self, payload):
        response = self.download_data('recency', payload)

        return response.json()['data']['recency']

    def get_rankings(self):
        response = self.download_data('rankings')

        return response.json()['data']

    def post_rankings(self, facet, payload):
        response = self.download_data("rankings/{}".format(facet), payload)

        return response.json()

    def get_taxonomies(self, facet = None, q = None):
        if facet is None:
            response = self.download_data("taxonomies")
        else:
            api_endpoint = "taxonomies/{}".format(facet)
            querystring = {"q": q}
            response = self.querystring_endpoint(api_endpoint, querystring)

        return response.json()['data']

    def post_taxonomies(self, facet, payload):
        response = self.download_data("taxonomies/{}/lookup".format(facet), payload)

        return response.json()['data']


###### TESTS ######
def test_profiles_conn():
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
