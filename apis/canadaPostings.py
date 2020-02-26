"""Summary
"""
import unittest

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
class TestCanadaPostingsConnection(unittest.TestCase):
    """
    Our basic test class
    """

    def test_metadata(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        conn = CanadaPostingsConnection()
        response = conn.get_metadata()

        assert response is not None, "No index data returned"
        assert response != [], "No index data returned"


if __name__ == '__main__':
    unittest.main()
