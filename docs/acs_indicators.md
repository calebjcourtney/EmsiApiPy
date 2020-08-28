# Core LMI
```python
import EmsiApiPy

conn = EmsiApiPy.ACSIndicatorsConnection()

# ensure the connection is good
assert conn.is_healthy()

# get the metadata
print(conn.get_meta())
"""
{
  "data": {
    "acs_version": "2018",
    "area_levels": [
      "nation",
      "state",
      "msa",
      "county"
    ],
    "attribution": {
      "body": "American Community Survey (ACS) data is pulled directly from the Census's API, using the ACS 5-year estimates. While this product uses data from the Census Bureau Data API, it is not endorsed or certified by the Census Bureau.",
      "title": "American Community Survey Data"
    },
    "metrics": [
      "avg_family_size",
      "avg_household_size",
      "children_poverty_level_pct",
      "disabled_population",
      "disabled_population_pct",
      "families",
      "families_pct",
      "female_householder_family_households",
      "female_householder_family_households_pct",
      "foreign_born_population",
      "foreign_born_population_pct",
      "homeowner_vacancy_rate",
      "households",
      "housing_units",
      "male_householder_family_households",
      "male_householder_family_households_pct",
      "married_family_households",
      "married_family_households_pct",
      "mean_commute_time",
      "median_age",
      "median_household_income",
      "name",
      "non_family_households",
      "non_family_households_pct",
      "occupied_housing_units",
      "occupied_housing_units_pct",
      "per_capita_income",
      "poverty_level_pct",
      "remote_workers",
      "remote_workers_pct",
      "rental_vacancy_rate",
      "seniors_poverty_level_pct",
      "vacant_housing_units",
      "vacant_housing_units_pct",
      "veterans",
      "veterans_pct"
    ],
    "taxonomies": {
      "area": "us_area_2018_4"
    }
  }
}
"""

# list of metrics
print(conn.get_metrics())
"""
[
  {
    "acs_census_variable_links": [
      "https://api.census.gov/data/2018/acs/acs5/profile/variables/NAME.json"
    ],
    "acs_census_variables": [
      "NAME"
    ],
    "acs_concept": null,
    "acs_summary_level": "profile",
    "description": "ACS geographic area name.",
    "format": "string",
    "name": "name",
    "title": null
  },
  {
    "acs_census_variable_links": [
      "https://api.census.gov/data/2018/acs/acs5/profile/variables/DP03_0062E.json"
    ],
    "acs_census_variables": [
      "DP03_0062E"
    ],
    "acs_concept": "economic_characteristics",
    "acs_summary_level": "profile",
    "description": "The income of households in the last 12 months which includes the income of the householder and all other individuals 15 years old and over in the household, whether they are related to the householder or not. The median divides the income distribution into two equal parts: one-half of the cases falling below the median income and one-half above the median.",
    "format": "money",
    "name": "median_household_income",
    "title": "Median Household Income"
  },
  ...
]
"""

# get info about a particular metric (median age)
print(conn.get_metrics("median_age"))
"""
{
  "acs_census_variable_links": [
    "https://api.census.gov/data/2018/acs/acs5/profile/variables/DP05_0018E.json"
  ],
  "acs_census_variables": [
    "DP05_0018E"
  ],
  "acs_concept": "economic_characteristics",
  "acs_summary_level": "profile",
  "description": "The age that divides a population into two numerically equal groups - that is, half the people are younger than this age and half are older.",
  "format": "float",
  "name": "median_age",
  "title": "Median Age"
}
"""

# get the median age for the nation
print(conn.get_level("nation", ["median_age"]))
# [{'id': 0, 'median_age': 37.9}]

```
