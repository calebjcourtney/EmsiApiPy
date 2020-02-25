"""Summary
"""
import requests

from base import EmsiBaseConnection


class AutomationIndexConnection(EmsiBaseConnection):
    """docstring for AutomationIndexConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://emsiservices.com/automation-index/"
        self.scope = "automation-index"

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
        url = "https://emsiservices.com/automation-index/status"
        response = requests.request("GET", url)

        return response.json()['data']['message']

    def is_healthy(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = "https://emsiservices.com/automation-index/status"
        response = requests.request("GET", url)

        return response.json()['data']['healthy']

    def get_countries(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        endpoints = self.get_available_endpoints()
        endpoints.remove('/status')

        return endpoints

    def get_metadata(self, nation = 'us'):
        """
        Summary

        Args:
            nation (str, optional): Description

        Returns:
            TYPE: Description
        """
        api_endpoint = "/{}/meta".format(nation)
        response = self.download_data(api_endpoint)

        return response.json()['data']

    def get_index(self, nation = 'us'):
        """Summary

        Args:
            nation (str, optional): Description

        Returns:
            TYPE: Description
        """
        api_endpoint = "/{}/data".format(nation)
        response = self.download_data(api_endpoint)

        return response.json()['data']

    def filter_soc_index(self, soc_code, nation = 'us'):
        """Summary

        Args:
            soc_code (TYPE): Description
            nation (str, optional): Description

        Raises:
            ValueError: Description

        Returns:
            TYPE: Description
        """
        if type(soc_code) != list or type(soc_code) != str:
            raise ValueError("input `soc_code` must be one of type `list` or `str`")

        if type(soc_code) == list:
            payload = soc_code
        elif "," in soc_code:
            payload = soc_code.split(",")
        else:
            payload = [soc_code]

        index = self.get_index(nation)

        output = {}
        for soc in payload:
            try:
                output[soc] = index[soc]
            except ValueError:
                raise ValueError("`soc_code` '{}' is invalid".format(soc))

        return output


###### TESTS ######
def test_automation_conn():
    """Summary
    """
    conn = AutomationIndexConnection()

    response = conn.get_index()

    assert response is not None, "No index data returned"
    assert response != [], "No index data returned"


if __name__ == '__main__':
    test_automation_conn()
