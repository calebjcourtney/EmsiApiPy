import pytest
import responses
from responses import matchers

from EmsiApiPy.base import Token
from EmsiApiPy.base import EmsiBaseConnection


def test_token():
    token = Token("super-secret-token")

    assert token.token == "super-secret-token"
    assert not token.is_expired()


@responses.activate
def test_emsi_base_connection():
    responses.add(
        responses.POST,
        "https://auth.emsicloud.com/connect/token",
        json={
            "access_token": "super-secret-token",
            "expires_in": 3600,
            "token_type": "Bearer",
        },
    )

    conn = EmsiBaseConnection()
    assert conn._username == "test-user"
    assert conn._password == "test-password"
    assert conn.scope == ""
    assert conn.base_url == ""
    assert conn.name == ""

    # with dummy username and password, token should not be created
    conn.get_new_token()
    assert conn.token.token == "super-secret-token"

    # set the base url for future requests
    conn.base_url = "https://example.com/"

    # test the download_data method - GET request
    responses.add(
        responses.GET,
        f"{conn.base_url}meta/metrics",
        json={"message": "GET was a success"},
    )

    assert conn.download_data("meta/metrics").json() == {"message": "GET was a success"}

    # test the download_data method - POST request
    responses.add(
        responses.POST,
        f"{conn.base_url}meta/metrics",
        json={"message": "POST was a success"},
    )

    assert conn.download_data(
        "meta/metrics", payload={"filters": "some filtering"}
    ).json() == {"message": "POST was a success"}

    # test the get_data method
    assert conn.get_data(f"{conn.base_url}meta/metrics").json() == {
        "message": "GET was a success"
    }

    # test the post_data method
    assert conn.post_data(
        f"{conn.base_url}meta/metrics", payload={"filters": "some filtering"}
    ).json() == {"message": "POST was a success"}

    # test the status endpoint
    responses.add(
        responses.GET,
        f"{conn.base_url}status",
        json={"data": {"message": "Service is healthy", "healthy": True}},
    )

    assert conn.get_status() == "Service is healthy"

    # test the is_healthy method
    assert conn.is_healthy()

    # test the get_meta method
    responses.add(
        responses.GET,
        f"{conn.base_url}meta",
        json={"data": "some meta info"},
    )
    assert conn.get_meta() == "some meta info"
