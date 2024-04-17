import pytest
import responses
from responses import matchers

from permissions import DEFAULT
DEFAULT["username"] = "test-user"
DEFAULT["password"] = "test-password"

@pytest.fixture
def token():
    from EmsiApiPy.base import Token
    return Token("super-secret-token")
