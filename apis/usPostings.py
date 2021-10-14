"""Summary
"""
from .base import JobPostingsConnection


class UnitedStatesPostingsConnection(JobPostingsConnection):
    """docstring for CanadaPostingsConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (str): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://emsiservices.com/jpa/"
        self.scope = "postings:us"

        self.get_new_token()

        self.name = "US_Postings"
