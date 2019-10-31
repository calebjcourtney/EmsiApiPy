import requests


class AutomationIndexConnection(object):
    """docstring for AutomationIndexConnection
    
    Attributes:
        password (TYPE): Description
        username (TYPE): Description
    """
    def __init__(self, username, password):
        """Summary
        
        Args:
            username (TYPE): Description
            password (TYPE): Description
        """
        super(AutomationIndexConnection, self).__init__()
        self.username = username
        self.password = password


    def get_available_endpoints():
        """List available endpoints.
        """
    url = "https://emsiservices.com/automation-index/"
    response = requests.request("GET", url, headers=headers, auth = (self.username, self.password))

    return response.json()['data']['endpoints']


    def get_status():
        """Summary
        """
        url = "https://emsiservices.com/automation-index/status"
        response = requests.request("GET", url)

        return response.json()['data']['message']


    def is_healthy():
        """Summary
        """
        url = "https://emsiservices.com/automation-index/status"
        response = requests.request("GET", url)

        return response.json()['data']['healthy']


    def get_countries():
        """Summary
        """
        endpoints = self.get_available_endpoints()
        endpoints.remove('/status')

        return endpoints


    def get_metadata(nation = '/us'):
        """Summary
        
        Args:
            nation (str, optional): Description
        """
        url = "https://emsiservices.com/automation-index{}/meta".format(nation)
        response = requests.request("GET", url, auth = (self.username, self.password))

        return response.json()['data']


    def get_index(nation = '/us'):
        """Summary
        
        Args:
            nation (str, optional): Description
        """
        url = "https://emsiservices.com/automation-index{}/data".format(nation)
        response = requests.request("GET", url, auth = (self.username, self.password))

        return response.json()['data']



    def filter_soc_index(soc_code, nation = '/us'):
        """Summary
        
        Args:
            soc_code (TYPE): Description
            nation (str, optional): Description
        
        Raises:
            ValueError: Description
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


# Let's add tests here
