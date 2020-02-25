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

    def __init__(self, username: str, password: str) -> None:
        """Summary

        Args:
            username (str): Description
            password (str): Description
        """
        super(EmsiBaseConnection, self).__init__()
        self.username = username
        self.password = password

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

        response = requests.get(url, headers = headers, json = payload)
        if response.status_code == 401:
            self.get_new_token()
            return self.post_data(url, payload)

        return response
