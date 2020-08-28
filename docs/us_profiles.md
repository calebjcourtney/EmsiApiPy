# Aggregate Social Profiles
```python
import EmsiApiPy

conn = EmsiApiPy.AggregateProfilesConnection()

# make sure we have a good connection
assert conn.is_healthy()

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
# {'profiles': 542838}

# the facets that we can rank by
print(conn.get_rankings())
"""
[
    'certifications', 'certifications_name', 'cip2', 'cip2_name', 'cip4', 'cip4_name', 'cip6', 'cip6_name', 
    'city', 'city_name', 'company', 'company_name', 'county', 'edulevels', 'edulevels_name', 'fips', 
    'hard_skills', 'hard_skills_name', 'msa', 'naics2', 'naics3', 'naics4', 'naics5', 'naics6', 'onet', 
    'schools', 'schools_ipeds', 'schools_name', 'skills', 'skills_name', 'soc2', 'soc3', 'soc4', 'soc5', 
    'soft_skills', 'soft_skills_name', 'state', 'title', 'title_name'
]
"""

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
"""
{
    'data': {
        'ranking': {
            'buckets': [...], 
            'facet': 'hard_skills_name', 
            'limit': 10, 
            'rank_by': 'profiles'
        }, 
        'totals': {
            'profiles': 37798
        }
    }
}
"""

# make sure we're using the right id or name for "Data Scientist"
print(conn.get_taxonomies(facet = 'title', q = 'Data Scientist'))
"""
[
    {'id': '15.30650', 'name': 'Data Scientists', 'properties': {'singular_name': 'Data Scientist', 'soc2': '15', 'soc2_name': 'Computer and Mathematical'}, 'score': 7.0462027},
    {'id': '15.1073', 'name': 'Data Specialists', 'properties': {'singular_name': 'Data Specialist', 'soc2': '15', 'soc2_name': 'Computer and Mathematical'}, 'score': 4.670484},
    {'id': '15.1272', 'name': 'Data Developers', 'properties': {'singular_name': 'Data Developer', 'soc2': '15', 'soc2_name': 'Computer and Mathematical'}, 'score': 4.670484},
    ...
]
"""

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
print(df.head())

"""
                hard_skills_name  profiles
0  Python (Programming Language)     21969
1     SQL (Programming Language)     18616
2               Machine Learning     18475
3       R (Programming Language)     17354
4                   Data Science     14308
"""
```
