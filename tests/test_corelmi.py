# thanks to Paolo Rovelli for this: https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py/27876800#27876800
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


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
