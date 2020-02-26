"""Summary
"""
import unittest

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

        self.token = self.get_new_token()


class TestUSPostingsConnection(unittest.TestCase):
    """
    Our basic test class
    """

    def test_metadata(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        conn = UnitedStatesPostingsConnection()
        response = conn.get_metadata()

        assert response is not None, "No index data returned"
        assert response != [], "No index data returned"
