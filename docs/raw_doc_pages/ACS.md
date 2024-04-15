# Emsi ACS API
#### v1.9.1
##### Information on past releases can be found in the [Changelog](/updates/acs-api-changelog).

## Overview

### Use Case
This is an interface for retrieving American Community Survey (ACS) Census data in a more convenient form which ensures compatability with Emsi areas. Check [/meta](#meta) for the area version.

### About the data
This ACS data is pulled directly from the US Census Data API using ACS 5-year estimates. We have translated ACS variables into representative metrics with descriptive names to make pulling the data more convenient. To find specific information about each metric, such as which underlying ACS variables they use, query the [/meta/metrics](#get-meta-metrics) endpoint. Please note that while this product uses data from the Census Bureau Data API, it is not endorsed or certified by the Census Bureau.

### Content Type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the ACS API, you must request an OAuth bearer token with the scope `acs`.

```har
{
  "method": "POST",
  "url": "https://auth.emsicloud.com/connect/token",
  "show": true,
  "headers": [
    {
      "name": "Content-Type",
      "value": "application/x-www-form-urlencoded"
    }
  ],
  "postData": {
    "mimeType": "application/x-www-form-urlencoded",
    "params": [
      {
          "name": "client_id",
          "value": "CLIENT_ID"
      },
      {
          "name": "client_secret",
          "value": "CLIENT_SECRET"
      },
      {
          "name": "grant_type",
          "value": "client_credentials"
      },
      {
          "name": "scope",
          "value": "acs"
      }
    ]
  }
}
```

**Response**

```json
{
  "access_token":"<ACCESS_TOKEN>",
  "expires_in":3600,
  "token_type":"Bearer"
}
```

Issuing requests with the header `Authorization: Bearer <ACCESS_TOKEN>` will grant you access to this API for the duration of the token. For continued access make sure to fetch a new token before time expires. See our [OAuth 2.0 guide](/guides/oauth-2-0) for additional details.

## /status

Service status (health)

### `GET` <span class="from-raml uri-prefix"></span>/status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/acs/status",
  "show": true,
  "headers": [
    {
      "name": "Authorization",
      "value": "Bearer <ACCESS_TOKEN>"
    }
  ],
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "healthy": true,
    "message": "Service is healthy"
  }
}
```


</div>


</div>



## /meta

Get info on versions, metrics, and attribution.

### `GET` <span class="from-raml uri-prefix"></span>/meta

Get service metadata, including supported taxonomy versions, ACS versions, and attribution text.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/acs/meta",
  "show": true,
  "headers": [
    {
      "name": "Authorization",
      "value": "Bearer <ACCESS_TOKEN>"
    }
  ],
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "acs_version": "2019",
    "area_levels": [
      "nation",
      "state",
      "msa",
      "county",
      "zip",
      "tract"
    ],
    "attribution": {
      "body": "American Community Survey Data. American Community Survey (ACS) data is pulled directly from the Census's API, using the ACS 5-year estimates. While this product uses data from the Census Bureau Data API, it is not endorsed or certified by the Census Bureau.",
      "title": "American Community Survey Data"
    },
    "metrics": [
      "adult_civilian_population",
      "avg_family_size",
      "avg_household_size",
      "carpooling",
      "carpooling_pct",
      "children_poverty_level_pct",
      "civilian_noninstitutionalized_population",
      "cohabiting_couple_households",
      "cohabiting_couple_households_pct",
      "commute_other_means",
      "commute_other_means_pct",
      "disabled_population",
      "disabled_population_pct",
      "driving_alone",
      "driving_alone_pct",
      "employed_with_health_insurance",
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
      "median_house_value",
      "median_household_income",
      "median_monthly_rent",
      "name",
      "non_english_households_pop",
      "occupied_housing_units",
      "occupied_housing_units_pct",
      "per_capita_income",
      "population",
      "poverty_level_pct",
      "public_transport",
      "public_transport_pct",
      "remote_workers",
      "remote_workers_pct",
      "rental_vacancy_rate",
      "seniors_poverty_level_pct",
      "vacant_housing_units",
      "vacant_housing_units_pct",
      "veterans",
      "veterans_pct",
      "walking",
      "walking_pct",
      "workers_16_and_over"
    ],
    "taxonomies": {
      "area": "us_area_2021_1"
    }
  }
}
```


</div>


</div>




### `GET` <span class="from-raml uri-prefix">/meta</span>/metrics

Get metadata on all of the available metrics. This information provides detailed descriptions and titles for each metric and can help map metrics back to their underlying ACS data points.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/acs/meta/metrics",
  "show": true,
  "headers": [
    {
      "name": "Authorization",
      "value": "Bearer <ACCESS_TOKEN>"
    }
  ],
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": [
    {
      "name": "name",
      "title": null,
      "description": "ACS geographic area name.",
      "acs_summary_level": null,
      "acs_concept": null,
      "acs_census_variables": [
        "NAME"
      ],
      "acs_census_variable_links": [
        "https://api.census.gov/data/2017/acs/acs5/profile/variables/NAME.json"
      ],
      "format": "string"
    },
    {
      "name": "median_household_income",
      "title": "Median Household Income",
      "description": "The income of households in the last 12 months which includes the income of the householder and all other individuals 15 years old and over in the household, whether they are related to the householder or not. The median divides the income distribution into two equal parts: one-half of the cases falling below the median income and one-half above the median.",
      "acs_summary_level": "profile",
      "acs_concept": "economic_characteristics",
      "acs_census_variables": [
        "DP03_0062E"
      ],
      "acs_census_variable_links": [
        "https://api.census.gov/data/2017/acs/acs5/profile/variables/DP03_0062E.json"
      ],
      "format": "money"
    }
  ]
}
```


</div>


</div>




### `GET` <span class="from-raml uri-prefix">/meta/metrics</span>/{metric}

Get metadata on a single metric.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>metric</code><div class="type">string</div> | Metric name to look up meta for. See [/meta](#meta) for available metrics.<br>Example: `median_household_income`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/acs/meta/metrics/median_household_income",
  "show": true,
  "headers": [
    {
      "name": "Authorization",
      "value": "Bearer <ACCESS_TOKEN>"
    }
  ],
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "name": "median_household_income",
    "title": "Median Household Income",
    "description": "The income of households in the last 12 months which includes the income of the householder and all other individuals 15 years old and over in the household, whether they are related to the householder or not. The median divides the income distribution into two equal parts: one-half of the cases falling below the median income and one-half above the median.",
    "acs_summary_level": "profile",
    "acs_concept": "economic_characteristics",
    "acs_census_variables": [
      "DP03_0062E"
    ],
    "acs_census_variable_links": [
      "https://api.census.gov/data/2017/acs/acs5/profile/variables/DP03_0062E.json"
    ],
    "format": "money"
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized metric 'foo'"
    }
  ]
}
```


</div>


</div>



## /{level}

Get ACS data for areas at the requested {level}.

### `GET` <span class="from-raml uri-prefix"></span>/{level}

Get ACS data for all available areas at the requested {level}, metrics with insufficient ACS data for a given region are reported as `null`. To fine tune the areas that come back from the API use the POST endpoint documented below with your desired area codes.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>level</code><div class="type">enum</div> | The area level for which to pull ACS data<br>Example: `nation`<br>Must be one of: `nation`, `state`, `msa`, `county`, `zip`, `tract`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>metrics</code><div class="type">string</div> | Specific metrics to return in the response, if no metrics are provided all metrics will be returned. When asking for multiple metrics use a comma separated list of metrics. See [/meta](#meta) for available metrics.<br>This parameter is optional.<br>Example: `name,median_household_income`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/acs/nation",
  "show": true,
  "headers": [
    {
      "name": "Authorization",
      "value": "Bearer <ACCESS_TOKEN>"
    }
  ],
  "queryString": [
    {
      "name": "metrics",
      "value": "name,median_household_income"
    }
  ]
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": [
    {
      "id": 0,
      "median_household_income": 62843,
      "name": "United States"
    }
  ]
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "errors": [
    {
      "status": 400,
      "title": "Invalid request",
      "detail": "Invalid request body"
    }
  ]
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized metric 'foo'"
    }
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix"></span>/{level}

Get ACS data for the requested set of areas at the requested {level}, metrics with insufficient ACS data for a given region are reported as `null`. Areas that are invalid or don't exist in the data will be returned with the value `null` for their metrics.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>level</code><div class="type">enum</div> | The area level for which to pull ACS data<br>Example: `nation`<br>Must be one of: `nation`, `state`, `msa`, `county`, `zip`, `tract`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    0
  ],
  "metrics": [
    "adult_civilian_population",
    "avg_family_size",
    "avg_household_size",
    "carpooling",
    "carpooling_pct",
    "children_poverty_level_pct",
    "civilian_noninstitutionalized_population",
    "cohabiting_couple_households",
    "cohabiting_couple_households_pct",
    "commute_other_means",
    "commute_other_means_pct",
    "disabled_population",
    "disabled_population_pct",
    "driving_alone",
    "driving_alone_pct",
    "employed_with_health_insurance",
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
    "median_house_value",
    "median_household_income",
    "median_monthly_rent",
    "name",
    "non_english_households_pop",
    "occupied_housing_units",
    "occupied_housing_units_pct",
    "per_capita_income",
    "population",
    "poverty_level_pct",
    "public_transport",
    "public_transport_pct",
    "remote_workers",
    "remote_workers_pct",
    "rental_vacancy_rate",
    "seniors_poverty_level_pct",
    "vacant_housing_units",
    "vacant_housing_units_pct",
    "veterans",
    "veterans_pct",
    "walking",
    "walking_pct",
    "workers_16_and_over"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/data.schema.json",
    "type": "object",
    "properties": {
        "ids": {
            "title": "Area ids to filter to",
            "description": "List of area ids matching the requested level.",
            "example": [
                1
            ],
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ],
                "pattern": "[0-9]+",
                "minLength": 1,
                "minimum": 0
            },
            "minItems": 1
        },
        "metrics": {
            "title": "Metrics included in the response",
            "description": "List of metrics to be returned, if list is empty (or `metrics` parameter isn't provided) all metrics will be returned.",
            "example": [
                "name",
                "median_household_income"
            ],
            "type": "array",
            "items": {
                "__nodocs": true,
                "type": "string",
                "minLength": 0
            }
        }
    },
    "required": [
        "ids"
    ],
    "additionalProperties": false
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/acs/nation",
  "show": true,
  "headers": [
    {
      "name": "Authorization",
      "value": "Bearer <ACCESS_TOKEN>"
    },
    {
      "name": "Content-Type",
      "value": "application/json"
    }
  ],
  "postData": {
    "mimeType": "application/json",
    "text": "{ \"ids\": [ 0 ], \"metrics\": [ \"adult_civilian_population\", \"avg_family_size\", \"avg_household_size\", \"carpooling\", \"carpooling_pct\", \"children_poverty_level_pct\", \"civilian_noninstitutionalized_population\", \"cohabiting_couple_households\", \"cohabiting_couple_households_pct\", \"commute_other_means\", \"commute_other_means_pct\", \"disabled_population\", \"disabled_population_pct\", \"driving_alone\", \"driving_alone_pct\", \"employed_with_health_insurance\", \"female_householder_family_households\", \"female_householder_family_households_pct\", \"foreign_born_population\", \"foreign_born_population_pct\", \"homeowner_vacancy_rate\", \"households\", \"housing_units\", \"male_householder_family_households\", \"male_householder_family_households_pct\", \"married_family_households\", \"married_family_households_pct\", \"mean_commute_time\", \"median_age\", \"median_house_value\", \"median_household_income\", \"median_monthly_rent\", \"name\", \"non_english_households_pop\", \"occupied_housing_units\", \"occupied_housing_units_pct\", \"per_capita_income\", \"population\", \"poverty_level_pct\", \"public_transport\", \"public_transport_pct\", \"remote_workers\", \"remote_workers_pct\", \"rental_vacancy_rate\", \"seniors_poverty_level_pct\", \"vacant_housing_units\", \"vacant_housing_units_pct\", \"veterans\", \"veterans_pct\", \"walking\", \"walking_pct\", \"workers_16_and_over\" ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": [
    {
      "adult_civilian_population": 250195726,
      "avg_family_size": 3.23,
      "avg_household_size": 2.62,
      "carpooling": 13763532,
      "carpooling_pct": 0.09,
      "children_poverty_level_pct": 0.185,
      "civilian_noninstitutionalized_population": 319706872,
      "cohabiting_couple_households": 7572122,
      "cohabiting_couple_households_pct": 0.063,
      "commute_other_means": 2774115,
      "commute_other_means_pct": 0.018,
      "disabled_population": 40335099,
      "disabled_population_pct": 0.126,
      "driving_alone": 116584507,
      "driving_alone_pct": 0.763,
      "employed_with_health_insurance": 126982830,
      "female_householder_family_households": 33458897,
      "female_householder_family_households_pct": 0.277,
      "foreign_born_population": 44011870,
      "foreign_born_population_pct": 0.136,
      "homeowner_vacancy_rate": 0.016,
      "households": 120756048,
      "housing_units": 137428986,
      "id": 0,
      "male_householder_family_households": 21526258,
      "male_householder_family_households_pct": 0.178,
      "married_family_households": 58198771,
      "married_family_households_pct": 0.482,
      "mean_commute_time": 26.9,
      "median_age": 38.1,
      "median_house_value": 217500,
      "median_household_income": 62843,
      "median_monthly_rent": 1062,
      "name": "United States",
      "non_english_households_pop": 65947773,
      "occupied_housing_units": 120756048,
      "occupied_housing_units_pct": 0.879,
      "per_capita_income": 34103,
      "population": 324697795,
      "poverty_level_pct": 0.095,
      "public_transport": 7641160,
      "public_transport_pct": 0.05,
      "remote_workers": 7898576,
      "remote_workers_pct": 0.052,
      "rental_vacancy_rate": 0.06,
      "seniors_poverty_level_pct": 0.093,
      "vacant_housing_units": 16672938,
      "vacant_housing_units_pct": 0.121,
      "veterans": 18230322,
      "veterans_pct": 0.073,
      "walking": 4073891,
      "walking_pct": 0.027,
      "workers_16_and_over": 152735781
    }
  ]
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "errors": [
    {
      "status": 400,
      "title": "Invalid request",
      "detail": "Invalid request body"
    }
  ]
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized metric 'foo'"
    }
  ]
}
```


</div>


</div>
