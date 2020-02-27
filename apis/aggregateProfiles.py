"""
The following is taken from Emsi's documentation, available here: https://api.emsidata.com/apis/aggregate-profile-data
"""
from .base import ProfilesConnection


class AggregateProfilesConnection(ProfilesConnection):
    """
    Use case
    This is an interface for retrieving aggregated Emsi profile data that is filtered, sorted and ranked by various properties of the profiles.

    About the data
    Profiles are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

    Usage:


    Attributes:
        base_url (str): what every url has to start with to query the API
        scope (str): the scope for requesting the proper access token
        token (str): the auth token received from the auth API
    """

    def __init__(self) -> None:
        """Summary

        """
        super().__init__()
        self.base_url = "https://emsiservices.com/profiles/"
        self.scope = "profiles:us"

        self.token = self.get_new_token()
