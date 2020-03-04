# thanks to Paolo Rovelli for this: https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py/27876800#27876800
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from apis.acsIndicators import ACSIndicatorsConnection

acs_conn = ACSIndicatorsConnection()


def test_get_status():
    response = acs_conn.get_status()

    assert response == "Service is healthy"


def test_get_meta():
    response = acs_conn.get_meta()

    for key in ['acs_version', 'area_levels', 'attribution', 'metrics', 'taxonomies']:
        assert key in response['data']


def test_get_metrics():
    response = acs_conn.get_metrics()
    assert len(response) > 0

    response = acs_conn.get_metrics("median_age")
    assert response['name'] == 'median_age'


def test_get_level():
    response = acs_conn.get_level("nation", ["name", "median_age"])

    assert len(response) == 1
    assert response[0]['name'] == 'United States'


def test_post_level():
    payload = {
        "ids": [
            0
        ],
        "metrics": [
            "median_age",
            "name"
        ]
    }
    response = acs_conn.post_level("nation", payload)

    assert len(response) == 1
    assert response[0]['name'] == 'United States'
