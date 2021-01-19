"""
Use case
This is an interface for retrieving aggregated Emsi Global Profile data that is filtered, sorted and ranked by various properties of the profiles.

About the data
Profiles are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.
"""
from .base import ProfilesConnection


class GlobalProfilesConnection(ProfilesConnection):
    """
    Use case
    This is an interface for retrieving aggregated Emsi Global Profile data that is filtered, sorted and ranked by various properties of the profiles.

    About the data
    Profiles are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

    Attributes:
        base_url (str): what every url has to start with to query the API
        scope (str): the scope for requesting the proper access token
        token (str): the auth token received from the auth API
    """

    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://emsiservices.com/global-profiles/"
        self.scope = "profiles:global"

        self.get_new_token()
