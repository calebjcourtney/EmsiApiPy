# EmsiApiPy
This library is designed as a helpful resource for connecting to [Emsi's APIs](https://api.emsidata.com/). It is provided as- is under no warranty by Emsi, but rather as an effort by various users to provide a centralized, coordinated way to access the APIs in an effective manner. It is currently under active development, so improvements are being added all the time, and these may include breaking changes.

# Table of Contents
1. [Installation](  #installation)
2. [Setup](  #Setup)
3. [Testing](  #Testing)
4. [Usage](  #Usage)
    - [Core LMI Examples](  #core-lmi-usage-examples)
    - [US Profiles Examples](  #aggregate-social-profiles)
    - [US Job Postings Examples]( #us-job-postings)

# Installation
Clone the repository. Install the required packages in `requirements.txt` into a [python virtual environment](https://www.geeksforgeeks.org/python-virtual-environment/). Here's an example using [virtualenv](https://virtualenv.pypa.io/en/latest/ ), which is what the source code has been tested in .
```bash
virtualenv - p python3 venv
source venv / bin / activate
pip install - r requirements.txt
```

# Setup
There is a file in the repository named `permissions.py.sample`. When the repo is cloned, it will look like this:
```python
DEFAULT = {
    "username": "foo",
    "password": "bar"
}
```
You will need to change the `foo` and `bar` values to what was provided by the Emsi API support team, and rename the file to `permissions.py`.

Make sure that the EmsiApiPy folder is accessible from your [`PYTHONPATH`](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). You will know you've set it up correctly if you can run `import EmsiApiPy` from within your python environment.


# Testing
Tests can be run with `. / tests / run_tests.sh`. Please be aware that this is testing all of the API connections available. If you don't have access to one of the APIs, then the tests will fail. It might be worth editing the `run_tests.sh` file to ensure that you are only running tests for the APIs that you want to access.


# Usage
# Core LMI Usage Examples
```python
import EmsiApiPy

conn = EmsiApiPy.CoreLMIConnection()

dataset = "emsi.us.grossregionalproduct"

dimension = "Area"

df = conn.get_dimension_hierarchy_df(dataset = dataset, dimension = dimension)

print(df.head())

"""
   child parent           name abbr level_name display_id
0      0      0  United States   US          1          0
1      1      0        Alabama   AL          2          1
2     10      0       Delaware   DE          2         10
3  10001     10           Kent   DE          3      10001
4  10003     10     New Castle   DE          3      10003
"""

# limit only to the states
df = df.loc[df['level_name'] == '2']

# get the 2019 GRP for each state in the US
payload = {
    "metrics": [
        {
            "name": "Dollars.2019"
        }
    ],
    "constraints": [
        {
            "dimensionName": "Area",
            "map": {row[1]['name']: [row[1]["child"]] for row in df.iterrows()}
        }
    ]
}

data_df = conn.post_retrieve_df(dataset = dataset, payload = payload)
print(data_df.head())

"""
         Area  Dollars.2019
0     Alabama  2.234497e+11
1      Alaska  5.222207e+10
2     Arizona  3.504984e+11
3    Arkansas  1.297678e+11
4  California  3.013869e+12
"""

```


# Aggregate Social Profiles
```python
import EmsiApiPy

conn = EmsiApiPy.AggregateProfilesConnection()

# make sure we have a good connection
assert conn.is_healthy()

# metadata for the profiles endpoint
print(conn.get_meta())

# get the total profiles for the state of Idaho
payload = {
    "filter": {
        "last_updated": {
            "start": "2017",
            "end": "2020"
        },
        "state": [
            16
        ]
    },
    "metrics": [
        "profiles"
    ]
}
print(conn.post_totals(payload))

# the facets that we can rank by
print(conn.get_rankings())

# rank the top 10 hard skills for data scientists
payload = {
    "filter": {
        "last_updated": {
            "start": "2017",
            "end": "2020"
        },
        "title_name": [
            "Data Scientist"
        ]
    },
    "rank": {
        "by": "profiles",
        "limit": 10
    }
}

facet = 'hard_skills_name'

print(conn.post_rankings(facet, payload))

# make sure we're using the right id or name for "Data Scientist"
print(conn.get_taxonomies(facet = 'title', q = 'Data Scientist'))

# get the top hard skills for data scientists as a pandas dataframe
payload = {
    "filter": {
        "last_updated": {
            "start": "2017",
            "end": "2020"
        },
        "title_name": [
            "Data Scientist"
        ]
    },
    "rank": {
        "by": "profiles",
        "limit": 10
    }
}

facet = 'hard_skills_name'

df = conn.post_rankings_df(facet, payload)

```


# US Job Postings
```python
import EmsiApiPy

jpa_conn = EmsiApiPy.UnitedStatesPostingsConnection()

# make sure we have a good connection
assert jpa_conn.is_healthy()

# metadata for the jpa endpoint
print(jpa_conn.get_meta())

# get the total job postings in the state of idaho for a year
payload = {
    "filter": {
        "when": {
            "start": "2019-08",
            "end": "2020-07"
        },
        "state": [
            16
        ]
    },
    "metrics": [
        "unique_postings"
    ]
}
print(jpa_conn.post_totals(payload))

# the facets that we can rank by
print(jpa_conn.get_rankings())

# rank the top 10 hard skills for data scientists
payload = {
    "filter": {
        "when": {
            "start": "2019-08",
            "end": "2020-07"
        },
        "title_name": [
            "Data Scientists"
        ]
    },
    "rank": {
        "by": "unique_postings",
        "limit": 10
    }
}

facet = 'hard_skills_name'

print(jpa_conn.post_rankings(facet, payload))

# make sure we're using the right id or name for "Data Scientist"
print(jpa_conn.get_taxonomies(facet = 'title', q = 'Data Scientist'))

# get the top hard skills for data scientists as a pandas dataframe
payload = {
    "filter": {
        "when": {
            "start": "2019-08",
            "end": "2020-07"
        },
        "title_name": [
            "Data Scientists"
        ]
    },
    "rank": {
        "by": "unique_postings",
        "limit": 10
    }
}

facet = 'hard_skills_name'

df = jpa_conn.post_rankings_df(facet, payload)
```
