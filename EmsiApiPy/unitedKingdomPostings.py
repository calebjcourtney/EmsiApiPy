"""Summary
"""
from __future__ import annotations

from base import JobPostingsConnection


class UKPostingsConnection(JobPostingsConnection):
    """docstring for UKPostingsConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (str): Description
    """

    def __init__(self) -> None:
        """Summary"""
        super().__init__()
        self.base_url = "https://emsiservices.com/uk-jpa/"
        self.scope = "postings:uk"

        self.get_new_token()

        self.name = "UK_Postings"
