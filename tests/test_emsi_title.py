# thanks to Paolo Rovelli for this: https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py/27876800#27876800
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from apis.emsiTitles import EmsiTitlesConnection

titles_conn = EmsiTitlesConnection()


def test_get_status():
    response = titles_conn.get_status()

    assert response.status_code == 200


def test_get_help():
    response = titles_conn.get_help()
    assert isinstance(response, str)


def test_get_titles():
    response = titles_conn.get_titles()
    assert len(response) > 0


def test_get_normalize():
    response = titles_conn.get_normalize("software engineer iii")

    for key in ['id', 'title', 'similarity']:
        assert key in response


def test_post_normalize():
    response = titles_conn.post_normalize("software engineer iii")

    for key in ['id', 'title', 'similarity']:
        assert key in response
