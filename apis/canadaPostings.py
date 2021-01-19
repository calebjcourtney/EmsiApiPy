"""
https://api.emsidata.com/apis/canada-job-postings
"""
from .base import JobPostingsConnection


class CanadaPostingsConnection(JobPostingsConnection):
    """
    Use case
    This is an interface for retrieving Canada job posting data that is filtered, sorted and ranked by various properties of the job postings.

    About the data
    Job postings are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

    Attributes:
        base_url (str): what every url has to start with to query the API
        scope (str): the scope for requesting the proper access token
        token (str): the auth token received from the auth API
    """

    def __init__(self) -> None:
        """
        Inherits from the base postings connection, that is all it needs.
        """
        super().__init__()
        self.base_url = "https://emsiservices.com/ca-jpa/"
        self.scope = "postings:ca"

        self.get_new_token()
