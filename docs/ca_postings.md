# Canada Job Postings
***
```python
import EmsiApiPy

jpa_conn = EmsiApiPy.CanadaPostingsConnection()

# make sure we have a good connection
assert jpa_conn.is_healthy()

# get the total job postings in the state of idaho for a year
payload = {
    "filter": {
        "when": {
            "start": "2019-08",
            "end": "2020-07"
        },
        "city_name": ["Toronto"]
    },
    "metrics": [
        "unique_postings"
    ]
}
print(jpa_conn.post_totals(payload))
# {'unique_postings': 274799}

# the facets that we can rank by
print(jpa_conn.get_rankings())
# ['certifications', 'certifications_name', 'city', 'etc...']


# rank the top 3 hard skills for data scientists
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
        "limit": 3
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
          "name": "Data Science",
          "unique_postings": 1095
        },
        {
          "name": "Python (Programming Language)",
          "unique_postings": 908
        },
        {
          "name": "Machine Learning",
          "unique_postings": 784
        }
      ],
      "facet": "hard_skills_name",
      "limit": 3,
      "rank_by": "unique_postings"
    },
    "totals": {
      "unique_postings": 1099
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
0                   Data Science             1095
1  Python (Programming Language)              908
2               Machine Learning              784
3       R (Programming Language)              659
4     SQL (Programming Language)              605
"""
```
