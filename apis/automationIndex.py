import requests


class AutomationIndexConnection(object):
    """docstring for AutomationIndexConnection"""

    def __init__(self, username, password):
        super(AutomationIndexConnection, self).__init__()
        self.username = username
        self.password = password

    def get_available_endpoints():
        pass

    def get_status():
        pass

    def get_countries():
        pass

    def get_metadata(nation = 'us'):
        pass

    def get_index(nation = 'us'):
        pass

    def filter_soc_index(soc_code, nation = 'us'):
        if type(soc_code) != list or type(soc_code) != str:
            raise ValueError("input `soc_code` must be one of type `list` or `str`")


# Let's add tests here
