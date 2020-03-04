
# thanks to Paolo Rovelli for this: https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py/27876800#27876800
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from apis.aggregateProfiles import AggregateProfilesConnection

jpa_conn = AggregateProfilesConnection()


def test_get_status():
    message = jpa_conn.get_status()
    assert message == "Service is healthy", "API is down or message has changed"


def test_is_healthy():
    """
    """
    assert jpa_conn.is_healthy(), "connection is not healthy"


def test_metadata():
    """
    """
    response = jpa_conn.get_metadata()

    for key in ['attribution', 'earliest_year', 'facets', 'filters', 'latest_year', 'metrics', 'supportsAdvancedFilters', 'taxonomies', 'taxonomy_versions']:
        assert key in response, "{} not in metadata".format(key)


def test_post_totals():
    """
    This will likely need to be updated on a regular basis. Should find a more consistent way to test this endpoint
    """
    payload = {
        "filter": {
            "last_updated": {
                "start": "2018",
                "end": "2019"
            },
            "state": [
                16
            ],
            "skills_name": {
                "include": [
                    "SQL (Programming Language)",
                    "C++ (Programming Language)"
                ],
                "exclude": [
                    "Java (Programming Language)",
                    "C Sharp (Programming Language)"
                ],
                "include_op": "and",
                "exclude_op": "or"
            },
            "educations": {
                "schools_name": [
                    "University of Idaho"
                ]
            }
        },
        "metrics": [
            "profiles"
        ]
    }
    response = jpa_conn.post_totals(payload)

    assert response['profiles'] == 62


def test_post_recency():
    payload = {
        "filter": {
            "last_updated": {
                "start": "2001",
                "end": "2019"
            }
        },
        "metrics": [
            "profiles",
            "unique_schools",
            "unique_companies"
        ]
    }
    response = jpa_conn.post_recency(payload)

    for key in ['profiles', 'unique_schools', 'year', 'unique_companies']:
        assert key in response, "{} not in recency".format(key)


def test_get_rankings():
    response = jpa_conn.get_rankings()
    assert len(response) != 0, "No facets to rank by? Seems dubious"


def test_post_rankings():
    payload = {
        "filter": {
            "last_updated": {
                "start": "2001",
                "end": "2019"
            },
            "state": [
                16
            ]
        },
        "rank": {
            "by": "profiles",
            "limit": 2
        }
    }

    facet = 'fips'

    response = jpa_conn.post_rankings(facet, payload)

    assert len(response['data']['ranking']['buckets']) == 2, "buckets data should be length 2, found {}".format(response['ranking']['buckets'])


def test_get_taxonomies():
    response = jpa_conn.get_taxonomies()
    assert len(response) != 0, "No taxonomies? Seems dubious"

    response = jpa_conn.get_taxonomies(facet = 'title', q = 'Data Scientist')
    assert len(response) > 0, "No matches for Data Scientist? Seems dubious"


def test_post_taxonomies():
    payload = {
        "ids": [
            "11-1011"
        ]
    }
    response = jpa_conn.post_taxonomies('soc5', payload)
    assert len(response) == 1, "No exact match for Chief Execs? Seems dubious"


def test_post_rankings_df():
    payload = {
        "filter": {
            "last_updated": {
                "start": "2001",
                "end": "2019"
            },
            "state": [
                16
            ]
        },
        "rank": {
            "by": "profiles",
            "limit": 2
        }
    }

    facet = 'fips'

    df = jpa_conn.post_rankings_df(facet, payload)

    assert not(df.empty), "No data received from the API. Seems dubious."
    assert len(df) == 2, "DataFrame doesn't have exactly two rows, found {} instead".format(len(df))


from apis.coreLmi import CoreLMIConnection

lmi_conn = CoreLMIConnection()


def test_get_meta():
    response = lmi_conn.get_meta()
    assert response != {}


def test_get_meta_dataset():
    response = lmi_conn.get_meta_dataset(dataset = "emsi.us.occupation", datarun = 'latest')
    assert response != {}


def test_get_meta_dataset_dimension():
    response = lmi_conn.get_meta_dataset_dimension("emsi.us.occupation", "Occupation", datarun = 'latest')
    for column in ['name', 'hierarchy']:
        assert column in response


def test_post_retrieve_data():
    payload = {
        "metrics": [
            {
                "name": "Jobs.2019"
            }
        ],
        "constraints": [
            {
                "dimensionName": "Area",
                "map": {"US": [0]}
            }
        ]
    }
    response = lmi_conn.post_retrieve_data("emsi.us.occupation", payload, datarun = 'latest')

    for key in ['data', 'errors', 'timings', 'totalRows']:
        assert key in response

    assert response['totalRows'] == 1


def test_get_dimension_hierarchy_df():
    df = lmi_conn.get_dimension_hierarchy_df('emsi.us.occupation', 'Occupation', datarun = 'latest')

    assert not df.empty
    for column in ['name', 'orderid', 'parent', 'descr', 'child', 'level_name']:
        assert column in df.columns


def test_post_retrieve_df():
    payload = {
        "metrics": [
            {
                "name": "Jobs.2019"
            }
        ],
        "constraints": [
            {
                "dimensionName": "Area",
                "map": {"US": [0]}
            }
        ]
    }

    df = lmi_conn.post_retrieve_df("emsi.us.occupation", payload, datarun = 'latest')

    assert not df.empty
    assert len(df) == 1
    for column in ['Area', 'Jobs.2019']:
        column in df.columns
