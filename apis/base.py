"""Summary
"""
import requests


class EmsiBaseConnection(object):
    """docstring for EmsiBaseConnection

    Attributes:
        password (TYPE): Description
        token (TYPE): Description
        username (TYPE): Description
    """

    def __init__(self, username, password):
        """Summary

        Args:
            username (TYPE): Description
            password (TYPE): Description
        """
        super(EmsiBaseConnection, self).__init__()
        self.username = username
        self.password = password

        self.token = self.get_new_token()

    def get_new_token(self):
        """Summary

        Returns:
            TYPE: Description

        Raises:
            ValueError: Description
        """
        url = "https://auth.emsicloud.com/connect/token"

        payload = "grant_type=client_credentials&client_id={}&client_secret={}&scope=emsiauth".format(self.username, self.password)
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code != 200:
            print(response.text)
            print(response.status_code)

            raise ValueError("Looks like you don't have access to this dataset with those credentials")

        return response.json()['access_token']

    def get_data(self, url):
        """Summary

        Args:
            url (TYPE): Description

        Returns:
            TYPE: Description
        """
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(self.token)
        }

        response = requests.get(url, headers = headers)
        if response.status_code == 401:
            self.token = self.get_new_token()
            return self.get_data(url)

        return response

    def post_data(self, url, payload):
        """Summary

        Args:
            url (TYPE): Description
            payload (TYPE): Description

        Returns:
            TYPE: Description
        """
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(self.token)
        }

        response = requests.get(url, headers = headers, json = payload)
        if response.status_code == 401:
            self.token = self.get_new_token()
            return self.post_data(url, payload)

        return response

    def download_data(self, url, payload = None):
        """Summary

        Args:
            url (TYPE): Description
            payload (None, optional): Description

        Returns:
            TYPE: Description
        """
        if payload is None:
            return self.get_data(url)

        else:
            return self.post_data(url, payload)
