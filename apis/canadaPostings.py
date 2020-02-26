"""Summary
"""
import requests
import pandas as pd

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

        self.token = self.get_new_token()


###### TESTS ######
def test_ca_jpa_conn():
    """Summary
    """
    conn = CanadaPostingsConnection()

    response = conn.get_metadata()

    assert response is not None, "No index data returned"
    assert response != [], "No index data returned"


if __name__ == '__main__':
    test_ca_jpa_conn()
