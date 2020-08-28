# EmsiApiPy
This library is designed as a helpful resource for connecting to [Emsi's APIs](https://api.emsidata.com/). It is provided as- is under no warranty by Emsi, but rather as an effort by various users to provide a centralized, coordinated way to access the APIs in an effective manner. It is currently under active development, so improvements are being added all the time, and these may include breaking changes.

## Table of Contents
1. [Installation](  #installation)
2. [Setup](  #Setup)
3. [Testing](  #Testing)
4. [Usage](  #Usage)
    - [Core LMI Examples](  #core-lmi-usage-examples)
    - [US Profiles Examples](  #aggregate-social-profiles)
    - [US Job Postings Examples](  #us-job-postings)

## Installation
Clone the repository. Install the required packages in `requirements.txt` into a [python virtual environment](https://www.geeksforgeeks.org/python-virtual-environment/). Here's an example using [virtualenv](https://virtualenv.pypa.io/en/latest/), which is what the source code has been tested in .

```bash
virtualenv - p python3 venv
source venv/bin/activate
pip install - r requirements.txt
```

## Setup
There is a file in the repository named `permissions.py.sample`. When the repo is cloned, it will look like this:

```python
DEFAULT = {
    "username": "foo",
    "password": "bar"
}
```

You will need to change the `foo` and `bar` values to what was provided by the Emsi API support team, and rename the file to `permissions.py`.

Make sure that the EmsiApiPy folder is accessible from your [`PYTHONPATH`](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). You will know you've set it up correctly if you can run `import EmsiApiPy` from within your python environment.

## Testing
Tests can be run with `./tests/run_tests.sh`. Please be aware that this is testing all of the API connections available. If you don't have access to one of the APIs, then the tests will fail. It might be worth editing the `run_tests.sh` file to ensure that you are only running tests for the APIs that you want to access.


## Usage
### Core LMI Usage Examples
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


### Aggregate Social Profiles
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


### US Job Postings
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


### Emsi Skills
```python
import EmsiApiPy

conn = EmsiApiPy.SkillsClassificationConnection()

# make sure we have a good connection
assert conn.is_healthy()

# get a list of all the skills
print(conn.get_list_all_skills()["data"][:])
"""
[
  {
    "id": "KS120P86XDXZJT3B7KVJ",
    "infoUrl": "https://skills.emsidata.com/skills/KS120P86XDXZJT3B7KVJ",
    "name": "(American Society For Quality) ASQ Certified",
    "type": {
      "id": "ST3",
      "name": "Certification"
    }
  },
  {
    "id": "KS126XS6CQCFGC3NG79X",
    "infoUrl": "https://skills.emsidata.com/skills/KS126XS6CQCFGC3NG79X",
    "name": ".NET Assemblies",
    "type": {
      "id": "ST1",
      "name": "Hard Skill"
    }
  },
  ...
]
"""

# search the library for any skills with the name of "python" in them
print(conn.get_list_all_skills(q="python"))
"""
{
  "data": [
    {
      "id": "KS125LS6N7WP4S6SFTCK",
      "infoUrl": "https://skills.emsidata.com/skills/KS125LS6N7WP4S6SFTCK",
      "name": "Python (Programming Language)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      }
    },
    {
      "id": "KSGWPO6DSN70GRY20JFT",
      "infoUrl": "https://skills.emsidata.com/skills/KSGWPO6DSN70GRY20JFT",
      "name": "Pandas (Python Package)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      }
    },
    ...
  ]
}
"""

# extract skills from text
text = """
Full Stack Web Developer

If you're ready to join a high-functioning team of full stack devs working closely with product managers, data engineers, and designers to create interfaces and visualizations that make nuanced data intelligible, we'd love to hear from you.

Candidates must have

    Experience with the front-end basics: HTML5, CSS3, and JS
    Experience using a version control system
    Familiarity with MV* frameworks, e.g. React, Ember, Angular, Vue
    Familiarity with server-side languages like PHP, Python, or Node

Great candidates also have

    Experience with a particular JS MV* framework (we happen to use React)
    Experience working with databases
    Experience with AWS
    Familiarity with microservice architecture
    Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS

People who succeed in this position are

    Team oriented and ready to work closely with other developers
    Determined to produce clean, well-tested code
    Comfortable with working in rapid development cycles
    Skilled oral and written communicators
    Enthusiastic for learning and pushing the envelope
""".encode("utf-8").decode("utf-8", "strict")

print(conn.post_extract(text))
"""
{
  "data": [
    {
      "confidence": 1.0,
      "skill": {
        "id": "KS440H66BML35BBRFCTK",
        "infoUrl": "https://skills.emsidata.com/skills/KS440H66BML35BBRFCTK",
        "name": "Server-Side",
        "tags": [
          {
            "key": "wikipediaExtract",
            "value": "Server-side refers to operations that are performed by the server in a client–server relationship in a computer network."
          },
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/Server-Side"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
      }
    },
    {
      "confidence": 1.0,
      "skill": {
        "id": "KSMNXY6MPS1EDWJ8P6B0",
        "infoUrl": "https://skills.emsidata.com/skills/KSMNXY6MPS1EDWJ8P6B0",
        "name": "Enthusiasm",
        "tags": [],
        "type": {
          "id": "ST2",
          "name": "Soft Skill"
        }
      }
    },
    {
      "confidence": 1.0,
      "skill": {
        "id": "KSDJCA4E89LB98JAZ7LZ",
        "infoUrl": "https://skills.emsidata.com/skills/KSDJCA4E89LB98JAZ7LZ",
        "name": "React.js",
        "tags": [
          {
            "key": "wikipediaExtract",
            "value": "React is an open-source JavaScript library for building user interfaces or UI components. It is maintained by Facebook and a community of individual developers and companies.\nReact can be used as a base in the development of single-page or mobile applications. However, React is only concerned with rendering data to the DOM, and so creating React applications usually requires the use of additional libraries for state management and routing. Redux and React Router are respective examples of such libraries."
          },
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/React.js"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
      }
    },
    ...
  ]
}
"""

```
