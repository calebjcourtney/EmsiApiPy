# Emsi Titles
```python
import EmsiApiPy

conn = EmsiApiPy.EmsiTitlesConnection()

# make sure we have a good connection
assert conn.is_healthy()

# get a list of all the skills
print(conn.get_list_all_skills())
"""
[
  {'id': 'ET4A446A1A5F6142AD', 'name': '.NET Application Architect'},
  {'id': 'ET2636514E20FBBF10', 'name': '.NET Application Developer'},
  {'id': 'ETB5E3860B8B9A9755', 'name': '.NET Architect'},
  {'id': 'ET00CAA8CEEDAA95C1', 'name': '.NET Azure Developer'},
  {'id': 'ET0230746480ACE6B7', 'name': '.NET Back End Developer'},
  {'id': 'ET306D9060C7305DEF', 'name': '.NET Consultant'},
  {'id': 'ETEB3BB8E555C79368', 'name': '.NET Developer'},
  ...
]
"""

# Get the mapping to skills and occupations for .NET Developers
print(conn.get_title_by_id("ETEB3BB8E555C79368"))
"""
{
  'pluralName': '.NET Developers', 
  'mapping': {
    'skills': [
      {
        'id': 'KS1200B62W5ZF38RJ7TD',
        'name': '.NET Framework'
      }
    ], 
    'socs': [
      {
        'id': '15-1256', 
        'name': 'Software Developers and Software Quality Assurance Analysts and Testers'
      }, 
      {
        'id': '15-1251', 
        'name': 'Computer Programmers'
      }
    ]
  },
  'id': 'ETEB3BB8E555C79368',
  'name': '.NET Developer'
}

"""

# normalize a job title
print(conn.post_normalize_title("data engineer"))
"""
{
  'confidence': 1.0,
  'title': {
    'id': 'ETD326FE202B769CD9',
    'name': 'Data Engineer',
    'pluralName': 'Data Engineers'
  }
}
"""

# inspect the normalization for what other options are available (only get the top 3 results)
print(conn.post_inspect_title_normalization("data engineer"))
"""
[
  {
    'confidence': 1.0,
    'title': {
      'id': 'ETD326FE202B769CD9',
      'name': 'Data Engineer',
      'pluralName': 'Data Engineers'
    }
  },
  {
    'confidence': 0.874889075756073,
    'title': {
      'id': 'ET5A7EE2114C1AE58B',
      'name': 'Manager/Data Engineer',
      'pluralName': 'Manager/Data Engineers'
    }
  },
  {
    'confidence': 0.8418798446655273,
    'title': {
      'id': 'ET40B76C2B31035EDF',
      'name': 'Data Engineer Intern',
      'pluralName': 'Data Engineer Interns'
    }
  }
]
"""

# normalize multiple titles at once
print(conn.post_normalize_titles_in_bulk(['data engineer', 'data scientist', 'data analyst']))

"""
[
  {
    'confidence': 1.0,
    'term': 'data engineer',
    'title': {
      'id': 'ETD326FE202B769CD9',
      'name': 'Data Engineer',
      'pluralName': 'Data Engineers'
    }
  },
  {
    'confidence': 1.0,
    'term': 'data scientist',
    'title': {
      'id': 'ET3B93055220D592C8',
      'name': 'Data Scientist',
      'pluralName': 'Data Scientists'
    }
  },
  {
    'confidence': 1.0,
    'term': 'data analyst',
    'title': {
      'id': 'ET3037E0C947A02404',
      'name': 'Data Analyst',
      'pluralName': 'Data Analysts'
    }
  }
]
"""
```
