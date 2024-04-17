from EmsiApiPy.base import Token

def test_token():
    token = Token("super-secret-token")

    assert token.token == "super-secret-token"
    assert not token.is_expired()
