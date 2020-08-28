# US Job Postings
```python
import EmsiApiPy

jpa_conn = EmsiApiPy.UnitedStatesPostingsConnection()

# make sure we have a good connection
assert jpa_conn.is_healthy()

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
# {'unique_postings': 298730}

# the facets that we can rank by
print(jpa_conn.get_rankings())
# ['certifications', 'certifications_name', 'city', 'etc...']


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
"""
{
  "data": {
    "ranking": {
      "buckets": [
        {
          "name": "Python (Programming Language)",
          "unique_postings": 30883
        },
        {
          "name": "Machine Learning",
          "unique_postings": 28525
        },
        {
          "name": "R (Programming Language)",
          "unique_postings": 22111
        }
      ],
      "facet": "hard_skills_name",
      "limit": 10,
      "rank_by": "unique_postings"
    },
    "totals": {
      "unique_postings": 43469
    }
  }
}
"""

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
print(df.head())

"""
                hard_skills_name  unique_postings
0  Python (Programming Language)            30883
1               Machine Learning            28525
2       R (Programming Language)            22111
3                   Data Science            21638
4     SQL (Programming Language)            18928
"""
```
