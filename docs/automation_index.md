# Automation Index
```python
import EmsiApiPy

conn = EmsiApiPy.AutomationIndexConnection()

# ensure the connection is good
assert conn.is_healthy()

# get the metadata
print(conn.get_countries())
# ['/uk', '/us']


# get the metadata
print(conn.get_metadata())
"""
{
  "taxonomies": {
    "soc": "soc_emsi_2019"
  },
  "attribution": {
    "title": "Automation Index Data",
    "body": "Emsi's US Automation Index analyzes the potential automation risk of occupations based on job task content—derived from ONET work activities. Combining that data with the Frey and Osborne findings at the occupation level, we identify which job tasks are \"at risk\" and which are resilient. We also incorporate data to identify where occupations cluster in industries facing disruption, and where workers' skills mean their nearest job options are also facing automation risk. This is a 100-based index, meaning that occupations with an automation index above 100 have an above average risk of automation, while occupations with an automation index of below 100 have a below average risk of automation."
  }
}
"""

print(conn.get_index())
"""
{
  "11-1011": 82,
  "11-1021": 82.2,
  "11-1031": null,
  "11-2011": 83,
  "11-2021": 76.7,
  ...
}
"""

# automation likelihood for chief execs
conn.filter_soc_index("11-1011")
# {'11-1011': 82}

# automation likelihood for multiple occs
conn.filter_soc_index(["11-1011", "11-1021"])
# {'11-1011': 82, '11-1021': 82.2}

```
