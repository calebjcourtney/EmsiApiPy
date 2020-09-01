"""Summary
"""
from .base import JobPostingsConnection


class CanadaPostingsConnection(JobPostingsConnection):
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
        self.base_url = "https://emsiservices.com/ca-jpa/"
        self.scope = "postings:ca"

        self.get_new_token()
