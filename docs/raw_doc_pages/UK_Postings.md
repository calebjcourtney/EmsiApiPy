# UK Job Postings 
#### v2.18.0
##### Information on past releases can be found in the [Changelog](/updates/uk-job-postings-changelog).

## Overview

### Use case
This is an interface for retrieving aggregate job posting data that is filtered, sorted and ranked by various properties of the job postings.

### About the data
Job postings are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

### Content type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the UK Job Postings API, you must request an OAuth bearer token with the scope `postings:uk`.

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
          "value": "postings:uk"
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

### Filtering
All data endpoints have an extensive filter request property allowing you to filter job postings down to specific subsets for analysis. The only required property of a filter is the `when` field, which can either filter job posting results to currently active postings (defined by the string `active`), or a specified range of months/days (defined by an object with `start` and `end` dates). Available months and the latest available day can be found in the [/meta](#meta) endpoint, along with a list of all of the available facets, filters, and metrics.

Most filters are associated with a particular taxonomy and have both id filters and name filters. For instance, to filter by job title you may use the
`title` filter with job title codes or the `title_name` filter with job title names. These filters require exact matches, including capitalization, punctuation, and
whitespace, in order to work as expected. Supported codes and/or names can be found by performing a ranking along the filter's facet (see [/rankings](#rankings) for more
details) or by searching in one of the taxonomy endpoints (see [/taxonomies](#taxonomies)).

Each taxonomy filter has both a shorthand and a verbose syntax.

1. **Shorthand**: a list of items.
  ```json
  {
    "when": {"start": "2018-01", "end": "2018-06"},
    "title_name": ["Data Scientist", "Computer Scientist"]
  }
  ```
  These filters match all job postings in the first 6 months of 2018 that include either one of the job titles "Data Scientist" or "Computer Scientist".

  This shorthand filter syntax is equivalent to the following in the verbose form:
  ```json
  {
    "when": {"start": "2018-01", "end": "2018-06"},
    "title_name": {
      "include": ["Data Scientist", "Computer Scientist"],
      "include_op": "or"
    }
  }
  ```

2. **Verbose**: an object defining inclusive/exclusive items and optional operators defining how to match those items in a posting.
  ```json
  {
    "when": {"start": "2018-01-01", "end": "2018-04-01"},
    "skills_name": {
      "include": ["SQL (Programming Lanague)", "C++ (Programming Language)"],
      "include_op": "and",
      "exclude": ["Java (Programming Language)", "C Sharp (Programming Language)"],
      "exclude_op": "or"
    }
  }
  ```
  These filters match all job postings in the first 90 days of 2018 that mention both SQL and C++ skills while not mention Java or C# skills.

  **Note:** The `include_op` and `exclude_op` fields apply to `include` and `exclude` fields respectively, they default to `or` if unspecified.
  * `and` – match job postings that include/exclude all items in the list
  * `or` – match job postings that include/exclude any of the items in the list

  Combining multiple values in the `include`/`exclude` fields of a filter with an `and` operator currently is only useful for filters that have multiple values per job posting
  (e.g., skills and education levels). Using this approach on filters that only have a single value per posting (i.e., company, occupation, job title, etc.) would always result
  in `0` matching postings.

All filters applied to a request must be true for a job posting to be included in the response. See the "Full Reference" tab under each
endpoint for the full listing of filters and metrics that can be applied to your requests.

### Glossary
The job posting metrics available in this API are listed below.

| Metric | Definition |
|------|------------|
|`unique_postings`|The number of unique (de-duplicated) monthly active job postings that match your filters. A posting is counted once for each month it is active.|
|`duplicate_postings`|Job postings are often posted multiple times and in multiple places online. Emsi de-duplicates these postings to get the "unique_postings" (see above) but also provides "duplicate_postings", which is the number of duplicate monthly active job postings for a given query.|
|`total_postings`|The sum of "unique_postings" and "duplicate_postings" is the total number of postings found online.|
|`posting_intensity`|The number of total job postings divided by the number of unique (de-duplicated) job postings.|
|`significance`|_This metric can only be used to rank `by` a facet in a ranking request, it cannot be used as a totals metric, or an extra ranking metric._<br>The relative concentration of each ranked item based on your filters as compared to all available postings in the filtered timeframe. Larger scores mean these ranked items occur more frequently in your filtered job postings than in all other postings in the filtered timeframe.|
|`unique_companies`|The number of unique companies represented in your filtered set of postings.|
|`median_posting_duration`|The median duration of closed job postings that match your filters. Duration is measured in days.|
|`median_salary`|The median annual salary advertised on job postings.|
|`min_salary`|The minimum annual salary advertised on job postings.|
|`max_salary`|The maximum annual salary advertised on job postings.|

> **Note:** Salary is defined as the average of all advertised salaries listed in a job posting.

Information about facet limitations in this API are listed below.

| Facet | Definition |
|------|------------|
|`sources`|_This facet can only be ranked_ `by` "unique_postings" _in a ranking, nested ranking, or ranking timeseries query._ <br>The job boards that the postings were found on.|

<div class="internal-only">

**Arachnid access claims**

The following scopes allow access to arachnid job posting data:

* `postings:early_feed_access` – The `/postings` endpoint will return arachnid job postings.
* `postings:early_analytics_access` - All analytics endpoints will return arachnid job posting data.

</div>

## /status

Service status (health)

### `GET` <span class="from-raml uri-prefix"></span>/status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/uk-jpa/status",
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
    "message": "Service is healthy",
    "healthy": true
  }
}
```


</div>


</div>



## /meta

Get info on taxonomies, versioning, available months of data, etc.

### `GET` <span class="from-raml uri-prefix"></span>/meta

Get service metadata, including taxonomies, version, available months of data, facets, metrics, and attribution text. Caching is encouraged, but the metadata does change monthly.



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/uk-jpa/meta",
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
    "attribution": {
      "body": "Job postings are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.",
      "title": "Emsi Job Postings"
    },
    "available_months": [
      "2016-01",
      "2016-02",
      "2016-03",
      "2016-04",
      "2016-05",
      "2016-06",
      "2016-07",
      "2016-08",
      "2016-09",
      "2016-10",
      "2016-11",
      "2016-12",
      "2017-01",
      "2017-02",
      "2017-03",
      "2017-04",
      "2017-05",
      "2017-06",
      "2017-07",
      "2017-08",
      "2017-09",
      "2017-10",
      "2017-11",
      "2017-12",
      "2018-01",
      "2018-02",
      "2018-03",
      "2018-04",
      "2018-05",
      "2018-06",
      "2018-07",
      "2018-08",
      "2018-09",
      "2018-10",
      "2018-11",
      "2018-12",
      "2019-01",
      "2019-02",
      "2019-03",
      "2019-04",
      "2019-05",
      "2019-06",
      "2019-07",
      "2019-08",
      "2019-09",
      "2019-10",
      "2019-11",
      "2019-12",
      "2020-01",
      "2020-02",
      "2020-03",
      "2020-04",
      "2020-05",
      "2020-06",
      "2020-07",
      "2020-08",
      "2020-09",
      "2020-10",
      "2020-11",
      "2020-12",
      "2021-01"
    ],
    "facets": [
      "certifications",
      "certifications_name",
      "city",
      "city_name",
      "company",
      "company_name",
      "contract_type",
      "contract_type_name",
      "country",
      "country_name",
      "employment_type",
      "employment_type_name",
      "hard_skills",
      "hard_skills_name",
      "lau1",
      "lau1_name",
      "max_years_experience",
      "min_years_experience",
      "nuts1",
      "nuts1_name",
      "nuts3",
      "nuts3_name",
      "skill_cluster",
      "skills",
      "skills_name",
      "soc1",
      "soc1_name",
      "soc2",
      "soc2_name",
      "soc3",
      "soc3_name",
      "soc4",
      "soc4_name",
      "soft_skills",
      "soft_skills_name",
      "sources",
      "title",
      "title_name"
    ],
    "filters": [
      "city",
      "city_name",
      "company",
      "company_is_staffing",
      "company_name",
      "contract_type",
      "contract_type_name",
      "country",
      "country_name",
      "employment_type",
      "employment_type_name",
      "is_internship",
      "is_remote",
      "keywords",
      "keywords.query",
      "keywords.type",
      "lau1",
      "lau1_name",
      "max_years_experience",
      "max_years_experience.lower_bound",
      "max_years_experience.upper_bound",
      "min_years_experience",
      "min_years_experience.lower_bound",
      "min_years_experience.upper_bound",
      "nuts1",
      "nuts1_name",
      "nuts3",
      "nuts3_name",
      "posting_duration",
      "posting_duration.lower_bound",
      "posting_duration.upper_bound",
      "salary",
      "salary.lower_bound",
      "salary.upper_bound",
      "skill_cluster",
      "skills",
      "skills_name",
      "soc1",
      "soc1_name",
      "soc2",
      "soc2_name",
      "soc3",
      "soc3_name",
      "soc4",
      "soc4_name",
      "sources",
      "title",
      "title_name",
      "when",
      "when.end",
      "when.start",
      "when.type"
    ],
    "latest_day": "2021-02-25",
    "metrics": [
      "duplicate_postings",
      "max_salary",
      "median_posting_duration",
      "median_salary",
      "min_salary",
      "posting_intensity",
      "significance",
      "total_postings",
      "unique_companies",
      "unique_postings"
    ],
    "postingFields": [
      "body",
      "city",
      "city_name",
      "company",
      "company_is_staffing",
      "company_name",
      "company_raw",
      "country",
      "country_name",
      "duplicates",
      "duration",
      "employment_type",
      "employment_type_name",
      "expired",
      "id",
      "is_internship",
      "is_remote",
      "lau1",
      "lau1_name",
      "location",
      "max_years_experience",
      "min_years_experience",
      "nuts1",
      "nuts1_name",
      "nuts3",
      "nuts3_name",
      "posted",
      "salary",
      "score",
      "skills",
      "skills_name",
      "soc1",
      "soc1_name",
      "soc2",
      "soc2_name",
      "soc3",
      "soc3_name",
      "soc4",
      "soc4_name",
      "sources",
      "title",
      "title_name",
      "title_raw",
      "url"
    ],
    "supportsAdvancedFilters": true,
    "taxonomies": {
      "area": "uk_area_2015",
      "skills": "skillsv7.35",
      "soc": "uk_soc2010emsi",
      "title": "emsi_title_v4.8",
      "company": "company"
    },
    "taxonomy_versions": {
      "area": [
        "uk_area_2015",
        "uk_area_2013_1"
      ],
      "soc": [
        "soc_emsi_2010"
      ],
      "title": [
        "emsi"
      ],
      "company": [
        "company",
        "emsi_company"
      ]
    }
  }
}
```


</div>


</div>



## /totals

Get summary metrics on all postings matching the filters.

### `POST` <span class="from-raml uri-prefix"></span>/totals





#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2020-01",
      "end": "2020-03"
    },
    "city_name": [
      "London, England"
    ],
    "title_name": [
      "Staff Nurses"
    ]
  },
  "metrics": [
    "unique_companies",
    "unique_postings",
    "median_posting_duration"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/totals.schema.json",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your postings query",
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting timeframe filter, can be the string `active` (except for the timeseries endpoints) to match all currently active postings, or a more granular timeframe `when` object detailed below.",
                    "type": [
                        "string",
                        "object"
                    ],
                    "properties": {
                        "start": {
                            "title": "Filter to postings after this date (inclusive)",
                            "description": "The start of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2015-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2016-06"
                        },
                        "type": {
                            "title": "Choose which date on a posting to filter by",
                            "description": "Determines how posting dates are evaluated.\n* `posted` - Match postings that were posted in your date range.\n* `active` - Match postings that were active within your date range.\n* `expired` - Match postings that expired in your date range.",
                            "type": "string",
                            "enum": [
                                "posted",
                                "active",
                                "expired"
                            ],
                            "default": "active"
                        }
                    },
                    "required": [
                        "start",
                        "end"
                    ],
                    "additionalProperties": false
                },
                "keywords": {
                    "title": "Filter postings by keyword",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter postings",
                            "description": "Keyword(s) to match in the original title and body of the job postings.",
                            "example": "work/life balance",
                            "type": "string",
                            "minLength": 1
                        },
                        "type": {
                            "title": "Type of keyword search to run",
                            "description": "How the keyword(s) are matched in a job posting.\n* `or` - Match postings with any of the keywords.\n* `and` - Match postings with all the keywords.\n* `phrase` - Match postings with the keywords as a phrase.\n* `expression` - Match postings using a complex boolean expression; e.g. `\"(uav OR drone) AND agriculture NOT surveillance\"`.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match postings that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "default": "or",
                            "type": "string",
                            "enum": [
                                "or",
                                "and",
                                "phrase",
                                "expression"
                            ]
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "TG9uZG9u"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "city_name": {
                    "title": "Filter by city names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "London"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1": {
                    "title": "Filter by Emsi LAU1 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "00FY"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1_name": {
                    "title": "Filter by Emsi LAU1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3": {
                    "title": "Filter by standard level 3 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF14"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3_name": {
                    "title": "Filter by standard level 3 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1": {
                    "title": "Filter by standard level 1 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1_name": {
                    "title": "Filter by standard level 1 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "East Midlands"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country": {
                    "title": "Filter by abbreviated country codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "ENG"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country_name": {
                    "title": "Filter by country names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "England"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "53.30837"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title_name": {
                    "title": "Filter by job title names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Web Developer"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1": {
                    "title": "Filter by Emsi 1-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1_name": {
                    "title": "Filter by Emsi UK SOC1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Associate Professional and Technical Occupations"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2": {
                    "title": "Filter by Emsi 2-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "35"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2_name": {
                    "title": "Filter by Emsi UK SOC2 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Business and Public Service Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3": {
                    "title": "Filter by Emsi 3-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "354"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3_name": {
                    "title": "Filter by Emsi UK SOC3 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales, Marketing and Related Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4": {
                    "title": "Filter by Emsi 4-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3545"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4_name": {
                    "title": "Filter by Emsi UK SOC4 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales accounts and business development managers"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company": {
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "NC95f2bd68-11c7-4140-92ab-7b82fd2d9f7e"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_name": {
                    "title": "Filter by company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_is_staffing": {
                    "title": "Filter to or exclude postings from staffing companies",
                    "description": "Passing `false` filters out postings from companies that have been identified as staffing companies or recruiting agencies; `true` limits results to _only_ those from staffing or recruiting companies. By default both staffing and non-staffing companies are included in the results.",
                    "example": true,
                    "type": "boolean"
                },
                "skill_cluster": {
                    "__internal": true,
                    "title": "**Experimental** Emsi-curated skill cluster Ids",
                    "description": "A list of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "406"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "KS7G2FY662ZPN6H4DZND"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills_name": {
                    "title": "Filter by skill names (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "SQL (Programming Language)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "sources": {
                    "title": "Filter by job posting source websites",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "monster.co.uk"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type": {
                    "title": "Filter by normalized contract type codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "10"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type_name": {
                    "title": "Filter by normalized contract type names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Apprenticeship"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type": {
                    "title": "Filter by employment type (Full/Part time) codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        1
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type_name": {
                    "title": "Filter by employment type (Full/Part time) names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Full-time (> 32 hours)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "min_years_experience": {
                    "title": "Filter on the minimum years of experience requested in a posting",
                    "description": "This filter operates on the advertised minimum years of experience found in a job posting. Not all postings advertise minimum years of experience, when using this filter only postings with a minimum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for minimum years of experience",
                            "description": "Lower bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 1
                        },
                        "upper_bound": {
                            "title": "Upper bound for minimum years of experience",
                            "description": "Upper bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 3
                        }
                    },
                    "additionalProperties": false
                },
                "max_years_experience": {
                    "title": "Filter on the maximum years of experience requested in a posting",
                    "description": "This filter operates on the advertised maximum years of experience found in a job posting. Not all postings advertise maximum years of experience, when using this filter only postings with a maximum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for maximum years of experience",
                            "description": "Lower bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 4
                        },
                        "upper_bound": {
                            "title": "Upper bound for maximum years of experience",
                            "description": "Upper bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 6
                        }
                    },
                    "additionalProperties": false
                },
                "salary": {
                    "title": "Filter by average advertised annual salary",
                    "description": "This filter operates on the average advertised annual salary found in a job posting. Not all postings advertise salaries, when using this filter only postings with advertised salaries will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for salary range",
                            "description": "Lower bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 45000
                        },
                        "upper_bound": {
                            "title": "Upper bound for salary range",
                            "description": "Upper bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 60000
                        }
                    },
                    "additionalProperties": false
                },
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 30
                        }
                    },
                    "additionalProperties": false
                },
                "is_remote": {
                    "title": "Filter by remote job postings",
                    "description": "Job postings that are described as remote or partially remote positions.",
                    "type": "boolean",
                    "example": true
                },
                "is_internship": {
                    "title": "Filter by internship job postings",
                    "description": "Job postings that are described as internship positions.",
                    "type": "boolean",
                    "example": true
                }
            },
            "required": [
                "when"
            ],
            "additionalProperties": false
        },
        "metrics": {
            "title": "Metrics to include in the summary",
            "description": "The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
            "default": [
                "unique_postings"
            ],
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "unique_postings",
                    "duplicate_postings",
                    "total_postings",
                    "posting_intensity",
                    "unique_companies",
                    "median_posting_duration",
                    "min_salary",
                    "median_salary",
                    "max_salary"
                ]
            },
            "minItems": 1
        }
    },
    "required": [
        "filter"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/uk-jpa/totals",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2020-01\", \"end\": \"2020-03\" }, \"city_name\": [ \"London, England\" ], \"title_name\": [ \"Staff Nurses\" ] }, \"metrics\": [ \"unique_companies\", \"unique_postings\", \"median_posting_duration\" ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "totals": {
      "median_posting_duration": 36,
      "unique_companies": 335,
      "unique_postings": 1350
    }
  }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="422">

Your request wasn't valid (bad keyword expression).


```json
{
  "errors": [
    {
      "status": 422,
      "title": "Invalid request content",
      "detail": "Invalid keyword search expression syntax:\n\t\"general merchandise\" OR \"apparel\" OR \"grocery\" OR\n\t                                                  ^"
    }
  ]
}
```


</div>


</div>



## /timeseries

Get summary metrics just like the [/totals](#totals) endpoint but broken out by month or day. Use `YYYY-MM` date format in the time-frame filter, `when`, to get monthly summary, or use `YYYY-MM-DD` date format for daily summary data. When requesting a daily timeseries only up to 90 days may be requested at a time. Months or days with 0 postings will be included in the response.

`median_posting_duration` metric is not available by timeseries to avoid biased results.


### `POST` <span class="from-raml uri-prefix"></span>/timeseries





#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2020-01",
      "end": "2020-03"
    },
    "title_name": [
      "Web Developers"
    ]
  },
  "metrics": [
    "unique_companies",
    "unique_postings"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/timeseries.schema.json",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your postings query",
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting timeframe filter, can be the string `active` (except for the timeseries endpoints) to match all currently active postings, or a more granular timeframe `when` object detailed below.",
                    "type": [
                        "string",
                        "object"
                    ],
                    "properties": {
                        "start": {
                            "title": "Filter to postings after this date (inclusive)",
                            "description": "The start of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2015-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2016-06"
                        },
                        "type": {
                            "title": "Choose which date on a posting to filter by",
                            "description": "Determines how posting dates are evaluated.\n* `posted` - Match postings that were posted in your date range.\n* `active` - Match postings that were active within your date range.\n* `expired` - Match postings that expired in your date range.",
                            "type": "string",
                            "enum": [
                                "posted",
                                "active",
                                "expired"
                            ],
                            "default": "active"
                        }
                    },
                    "required": [
                        "start",
                        "end"
                    ],
                    "additionalProperties": false
                },
                "keywords": {
                    "title": "Filter postings by keyword",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter postings",
                            "description": "Keyword(s) to match in the original title and body of the job postings.",
                            "example": "work/life balance",
                            "type": "string",
                            "minLength": 1
                        },
                        "type": {
                            "title": "Type of keyword search to run",
                            "description": "How the keyword(s) are matched in a job posting.\n* `or` - Match postings with any of the keywords.\n* `and` - Match postings with all the keywords.\n* `phrase` - Match postings with the keywords as a phrase.\n* `expression` - Match postings using a complex boolean expression; e.g. `\"(uav OR drone) AND agriculture NOT surveillance\"`.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match postings that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "default": "or",
                            "type": "string",
                            "enum": [
                                "or",
                                "and",
                                "phrase",
                                "expression"
                            ]
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "TG9uZG9u"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "city_name": {
                    "title": "Filter by city names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "London"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1": {
                    "title": "Filter by Emsi LAU1 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "00FY"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1_name": {
                    "title": "Filter by Emsi LAU1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3": {
                    "title": "Filter by standard level 3 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF14"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3_name": {
                    "title": "Filter by standard level 3 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1": {
                    "title": "Filter by standard level 1 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1_name": {
                    "title": "Filter by standard level 1 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "East Midlands"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country": {
                    "title": "Filter by abbreviated country codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "ENG"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country_name": {
                    "title": "Filter by country names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "England"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "53.30837"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title_name": {
                    "title": "Filter by job title names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Web Developer"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1": {
                    "title": "Filter by Emsi 1-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1_name": {
                    "title": "Filter by Emsi UK SOC1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Associate Professional and Technical Occupations"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2": {
                    "title": "Filter by Emsi 2-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "35"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2_name": {
                    "title": "Filter by Emsi UK SOC2 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Business and Public Service Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3": {
                    "title": "Filter by Emsi 3-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "354"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3_name": {
                    "title": "Filter by Emsi UK SOC3 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales, Marketing and Related Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4": {
                    "title": "Filter by Emsi 4-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3545"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4_name": {
                    "title": "Filter by Emsi UK SOC4 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales accounts and business development managers"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company": {
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "NC95f2bd68-11c7-4140-92ab-7b82fd2d9f7e"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_name": {
                    "title": "Filter by company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_is_staffing": {
                    "title": "Filter to or exclude postings from staffing companies",
                    "description": "Passing `false` filters out postings from companies that have been identified as staffing companies or recruiting agencies; `true` limits results to _only_ those from staffing or recruiting companies. By default both staffing and non-staffing companies are included in the results.",
                    "example": true,
                    "type": "boolean"
                },
                "skill_cluster": {
                    "__internal": true,
                    "title": "**Experimental** Emsi-curated skill cluster Ids",
                    "description": "A list of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "406"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "KS7G2FY662ZPN6H4DZND"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills_name": {
                    "title": "Filter by skill names (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "SQL (Programming Language)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "sources": {
                    "title": "Filter by job posting source websites",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "monster.co.uk"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type": {
                    "title": "Filter by normalized contract type codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "10"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type_name": {
                    "title": "Filter by normalized contract type names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Apprenticeship"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type": {
                    "title": "Filter by employment type (Full/Part time) codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        1
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type_name": {
                    "title": "Filter by employment type (Full/Part time) names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Full-time (> 32 hours)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "min_years_experience": {
                    "title": "Filter on the minimum years of experience requested in a posting",
                    "description": "This filter operates on the advertised minimum years of experience found in a job posting. Not all postings advertise minimum years of experience, when using this filter only postings with a minimum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for minimum years of experience",
                            "description": "Lower bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 1
                        },
                        "upper_bound": {
                            "title": "Upper bound for minimum years of experience",
                            "description": "Upper bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 3
                        }
                    },
                    "additionalProperties": false
                },
                "max_years_experience": {
                    "title": "Filter on the maximum years of experience requested in a posting",
                    "description": "This filter operates on the advertised maximum years of experience found in a job posting. Not all postings advertise maximum years of experience, when using this filter only postings with a maximum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for maximum years of experience",
                            "description": "Lower bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 4
                        },
                        "upper_bound": {
                            "title": "Upper bound for maximum years of experience",
                            "description": "Upper bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 6
                        }
                    },
                    "additionalProperties": false
                },
                "salary": {
                    "title": "Filter by average advertised annual salary",
                    "description": "This filter operates on the average advertised annual salary found in a job posting. Not all postings advertise salaries, when using this filter only postings with advertised salaries will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for salary range",
                            "description": "Lower bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 45000
                        },
                        "upper_bound": {
                            "title": "Upper bound for salary range",
                            "description": "Upper bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 60000
                        }
                    },
                    "additionalProperties": false
                },
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 30
                        }
                    },
                    "additionalProperties": false
                },
                "is_remote": {
                    "title": "Filter by remote job postings",
                    "description": "Job postings that are described as remote or partially remote positions.",
                    "type": "boolean",
                    "example": true
                },
                "is_internship": {
                    "title": "Filter by internship job postings",
                    "description": "Job postings that are described as internship positions.",
                    "type": "boolean",
                    "example": true
                }
            },
            "required": [
                "when"
            ],
            "additionalProperties": false
        },
        "metrics": {
            "title": "Metrics to calculate per month or day",
            "default": [
                "unique_postings"
            ],
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "unique_postings",
                    "duplicate_postings",
                    "total_postings",
                    "posting_intensity",
                    "unique_companies",
                    "min_salary",
                    "median_salary",
                    "max_salary"
                ]
            },
            "minItems": 1
        }
    },
    "required": [
        "filter"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/uk-jpa/timeseries",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2020-01\", \"end\": \"2020-03\" }, \"title_name\": [ \"Web Developers\" ] }, \"metrics\": [ \"unique_companies\", \"unique_postings\" ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "timeseries": {
      "month": [
        "2020-01",
        "2020-02",
        "2020-03"
      ],
      "unique_companies": [
        1578,
        1606,
        1522
      ],
      "unique_postings": [
        2767,
        2944,
        2901
      ]
    },
    "totals": {
      "unique_companies": 1917,
      "unique_postings": 3956
    }
  }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="422">

Your request wasn't valid (bad keyword expression).


```json
{
  "errors": [
    {
      "status": 422,
      "title": "Invalid request content",
      "detail": "Invalid keyword search expression syntax:\n\t\"general merchandise\" OR \"apparel\" OR \"grocery\" OR\n\t                                                  ^"
    }
  ]
}
```


</div>


</div>



## /rankings

Group and rank postings by available facets.

### `GET` <span class="from-raml uri-prefix"></span>/rankings

Get a list of current available ranking facets.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/uk-jpa/rankings",
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
    "certifications",
    "certifications_name",
    "city",
    "city_name",
    "company",
    "company_name",
    "contract_type",
    "contract_type_name",
    "country",
    "country_name",
    "employment_type",
    "employment_type_name",
    "hard_skills",
    "hard_skills_name",
    "lau1",
    "lau1_name",
    "max_years_experience",
    "min_years_experience",
    "nuts1",
    "nuts1_name",
    "nuts3",
    "nuts3_name",
    "skill_cluster",
    "skills",
    "skills_name",
    "soc1",
    "soc1_name",
    "soc2",
    "soc2_name",
    "soc3",
    "soc3_name",
    "soc4",
    "soc4_name",
    "soft_skills",
    "soft_skills_name",
    "sources",
    "title",
    "title_name"
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/rankings</span>/{rankingFacet}

Group and rank postings by {rankingFacet}.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>rankingFacet</code><div class="type">enum</div> | Example: `title_name`<br>Must be one of: `certifications`, `certifications_name`, `city`, `city_name`, `company`, `company_name`, `country`, `employment_type`, `employment_type_name`, `hard_skills`, `hard_skills_name`, `lau1`, `lau1_name`, `nuts1`, `nuts1_name`, `nuts3`, `nuts3_name`, `skill_cluster`, `skills`, `skills_name`, `soc1`, `soc1_name`, `soc2`, `soc2_name`, `soc3`, `soc3_name`, `soc4`, `soc4_name`, `soft_skills`, `soft_skills_name`, `sources`, `title`, `title_name`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2020-01",
      "end": "2020-03"
    },
    "skills_name": [
      "SQL (Programming Language)"
    ],
    "keywords": {
      "query": "work/life balance",
      "type": "phrase"
    }
  },
  "rank": {
    "by": "unique_postings",
    "limit": 5,
    "extra_metrics": [
      "unique_companies",
      "median_posting_duration"
    ]
  }
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/ranking.schema.json",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your postings query",
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting timeframe filter, can be the string `active` (except for the timeseries endpoints) to match all currently active postings, or a more granular timeframe `when` object detailed below.",
                    "type": [
                        "string",
                        "object"
                    ],
                    "properties": {
                        "start": {
                            "title": "Filter to postings after this date (inclusive)",
                            "description": "The start of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2015-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2016-06"
                        },
                        "type": {
                            "title": "Choose which date on a posting to filter by",
                            "description": "Determines how posting dates are evaluated.\n* `posted` - Match postings that were posted in your date range.\n* `active` - Match postings that were active within your date range.\n* `expired` - Match postings that expired in your date range.",
                            "type": "string",
                            "enum": [
                                "posted",
                                "active",
                                "expired"
                            ],
                            "default": "active"
                        }
                    },
                    "required": [
                        "start",
                        "end"
                    ],
                    "additionalProperties": false
                },
                "keywords": {
                    "title": "Filter postings by keyword",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter postings",
                            "description": "Keyword(s) to match in the original title and body of the job postings.",
                            "example": "work/life balance",
                            "type": "string",
                            "minLength": 1
                        },
                        "type": {
                            "title": "Type of keyword search to run",
                            "description": "How the keyword(s) are matched in a job posting.\n* `or` - Match postings with any of the keywords.\n* `and` - Match postings with all the keywords.\n* `phrase` - Match postings with the keywords as a phrase.\n* `expression` - Match postings using a complex boolean expression; e.g. `\"(uav OR drone) AND agriculture NOT surveillance\"`.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match postings that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "default": "or",
                            "type": "string",
                            "enum": [
                                "or",
                                "and",
                                "phrase",
                                "expression"
                            ]
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "TG9uZG9u"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "city_name": {
                    "title": "Filter by city names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "London"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1": {
                    "title": "Filter by Emsi LAU1 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "00FY"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1_name": {
                    "title": "Filter by Emsi LAU1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3": {
                    "title": "Filter by standard level 3 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF14"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3_name": {
                    "title": "Filter by standard level 3 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1": {
                    "title": "Filter by standard level 1 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1_name": {
                    "title": "Filter by standard level 1 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "East Midlands"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country": {
                    "title": "Filter by abbreviated country codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "ENG"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country_name": {
                    "title": "Filter by country names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "England"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "53.30837"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title_name": {
                    "title": "Filter by job title names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Web Developer"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1": {
                    "title": "Filter by Emsi 1-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1_name": {
                    "title": "Filter by Emsi UK SOC1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Associate Professional and Technical Occupations"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2": {
                    "title": "Filter by Emsi 2-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "35"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2_name": {
                    "title": "Filter by Emsi UK SOC2 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Business and Public Service Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3": {
                    "title": "Filter by Emsi 3-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "354"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3_name": {
                    "title": "Filter by Emsi UK SOC3 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales, Marketing and Related Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4": {
                    "title": "Filter by Emsi 4-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3545"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4_name": {
                    "title": "Filter by Emsi UK SOC4 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales accounts and business development managers"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company": {
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "NC95f2bd68-11c7-4140-92ab-7b82fd2d9f7e"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_name": {
                    "title": "Filter by company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_is_staffing": {
                    "title": "Filter to or exclude postings from staffing companies",
                    "description": "Passing `false` filters out postings from companies that have been identified as staffing companies or recruiting agencies; `true` limits results to _only_ those from staffing or recruiting companies. By default both staffing and non-staffing companies are included in the results.",
                    "example": true,
                    "type": "boolean"
                },
                "skill_cluster": {
                    "__internal": true,
                    "title": "**Experimental** Emsi-curated skill cluster Ids",
                    "description": "A list of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "406"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "KS7G2FY662ZPN6H4DZND"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills_name": {
                    "title": "Filter by skill names (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "SQL (Programming Language)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "sources": {
                    "title": "Filter by job posting source websites",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "monster.co.uk"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type": {
                    "title": "Filter by normalized contract type codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "10"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type_name": {
                    "title": "Filter by normalized contract type names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Apprenticeship"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type": {
                    "title": "Filter by employment type (Full/Part time) codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        1
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type_name": {
                    "title": "Filter by employment type (Full/Part time) names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Full-time (> 32 hours)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "min_years_experience": {
                    "title": "Filter on the minimum years of experience requested in a posting",
                    "description": "This filter operates on the advertised minimum years of experience found in a job posting. Not all postings advertise minimum years of experience, when using this filter only postings with a minimum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for minimum years of experience",
                            "description": "Lower bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 1
                        },
                        "upper_bound": {
                            "title": "Upper bound for minimum years of experience",
                            "description": "Upper bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 3
                        }
                    },
                    "additionalProperties": false
                },
                "max_years_experience": {
                    "title": "Filter on the maximum years of experience requested in a posting",
                    "description": "This filter operates on the advertised maximum years of experience found in a job posting. Not all postings advertise maximum years of experience, when using this filter only postings with a maximum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for maximum years of experience",
                            "description": "Lower bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 4
                        },
                        "upper_bound": {
                            "title": "Upper bound for maximum years of experience",
                            "description": "Upper bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 6
                        }
                    },
                    "additionalProperties": false
                },
                "salary": {
                    "title": "Filter by average advertised annual salary",
                    "description": "This filter operates on the average advertised annual salary found in a job posting. Not all postings advertise salaries, when using this filter only postings with advertised salaries will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for salary range",
                            "description": "Lower bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 45000
                        },
                        "upper_bound": {
                            "title": "Upper bound for salary range",
                            "description": "Upper bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 60000
                        }
                    },
                    "additionalProperties": false
                },
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 30
                        }
                    },
                    "additionalProperties": false
                },
                "is_remote": {
                    "title": "Filter by remote job postings",
                    "description": "Job postings that are described as remote or partially remote positions.",
                    "type": "boolean",
                    "example": true
                },
                "is_internship": {
                    "title": "Filter by internship job postings",
                    "description": "Job postings that are described as internship positions.",
                    "type": "boolean",
                    "example": true
                }
            },
            "required": [
                "when"
            ],
            "additionalProperties": false
        },
        "rank": {
            "title": "Choose how to rank your results",
            "type": "object",
            "properties": {
                "by": {
                    "title": "What metric to use to rank the ranking facet",
                    "description": "Some metrics may be approximations for performance reasons.",
                    "default": "unique_postings",
                    "type": "string",
                    "enum": [
                        "unique_postings",
                        "duplicate_postings",
                        "total_postings",
                        "posting_intensity",
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job titles, cities, companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`\n* Skills or certifications timeseries ranking when requesting a `unique_companies` metric: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "duplicate_postings",
                            "total_postings",
                            "posting_intensity",
                            "unique_companies",
                            "median_posting_duration",
                            "min_salary",
                            "median_salary",
                            "max_salary"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by number of unique postings for the item",
                    "description": "Require ranked items to have at least this many unique postings matching the filter.\nDefault: `3` when ranking by `significance`",
                    "default": 1,
                    "type": "integer",
                    "minimum": 1
                },
                "include": {
                    "title": "Filter ranked items to only those provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                },
                "exclude": {
                    "title": "Filter ranked items to only those not provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                }
            },
            "additionalProperties": false
        }
    },
    "required": [
        "filter",
        "rank"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/uk-jpa/rankings/title_name",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2020-01\", \"end\": \"2020-03\" }, \"skills_name\": [ \"SQL (Programming Language)\" ], \"keywords\": { \"query\": \"work/life balance\", \"type\": \"phrase\" } }, \"rank\": { \"by\": \"unique_postings\", \"limit\": 5, \"extra_metrics\": [ \"unique_companies\", \"median_posting_duration\" ] } }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "ranking": {
      "buckets": [
        {
          "median_posting_duration": 44,
          "name": "Software Developers",
          "unique_companies": 52,
          "unique_postings": 76
        },
        {
          "median_posting_duration": 46,
          "name": ".NET Developers",
          "unique_companies": 48,
          "unique_postings": 75
        },
        {
          "median_posting_duration": 43,
          "name": "Software Engineers",
          "unique_companies": 34,
          "unique_postings": 62
        },
        {
          "median_posting_duration": 32,
          "name": "Unclassified",
          "unique_companies": 41,
          "unique_postings": 52
        },
        {
          "median_posting_duration": 38,
          "name": "C# .NET Developers",
          "unique_companies": 33,
          "unique_postings": 51
        }
      ],
      "facet": "title_name",
      "limit": 5,
      "rank_by": "unique_postings"
    },
    "totals": {
      "median_posting_duration": 36,
      "unique_companies": 992,
      "unique_postings": 2431
    }
  }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="404">

The facet you requested wasn't found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized facet 'foo'"
    }
  ]
}
```


</div>


<div data-tab="422">

Your request wasn't valid (bad keyword expression).


```json
{
  "errors": [
    {
      "status": 422,
      "title": "Invalid request content",
      "detail": "Invalid keyword search expression syntax:\n\t\"general merchandise\" OR \"apparel\" OR \"grocery\" OR\n\t                                                  ^"
    }
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/rankings/{rankingFacet}</span>/timeseries

Group and rank postings by {ranking_facet} with a monthly or daily timeseries for each ranked group. Use `YYYY-MM` date format in the timeseries time-frame filter, `timeseries.when`, to get monthly summary of each ranked group, or use `YYYY-MM-DD` date format for daily summary.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>rankingFacet</code><div class="type">enum</div> | Example: `title_name`<br>Must be one of: `certifications`, `certifications_name`, `city`, `city_name`, `company`, `company_name`, `country`, `employment_type`, `employment_type_name`, `hard_skills`, `hard_skills_name`, `lau1`, `lau1_name`, `nuts1`, `nuts1_name`, `nuts3`, `nuts3_name`, `skill_cluster`, `skills`, `skills_name`, `soc1`, `soc1_name`, `soc2`, `soc2_name`, `soc3`, `soc3_name`, `soc4`, `soc4_name`, `soft_skills`, `soft_skills_name`, `sources`, `title`, `title_name`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2020-01",
      "end": "2020-06"
    },
    "company_name": [
      "Sainsbury’s Group"
    ]
  },
  "rank": {
    "by": "unique_postings",
    "limit": 5
  },
  "timeseries": {
    "when": {
      "start": "2019-01",
      "end": "2019-06"
    },
    "metrics": [
      "unique_postings",
      "total_postings"
    ]
  }
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/ranking-timeseries.schema.json",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your postings query",
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting timeframe filter, can be the string `active` (except for the timeseries endpoints) to match all currently active postings, or a more granular timeframe `when` object detailed below.",
                    "type": [
                        "string",
                        "object"
                    ],
                    "properties": {
                        "start": {
                            "title": "Filter to postings after this date (inclusive)",
                            "description": "The start of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2015-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2016-06"
                        },
                        "type": {
                            "title": "Choose which date on a posting to filter by",
                            "description": "Determines how posting dates are evaluated.\n* `posted` - Match postings that were posted in your date range.\n* `active` - Match postings that were active within your date range.\n* `expired` - Match postings that expired in your date range.",
                            "type": "string",
                            "enum": [
                                "posted",
                                "active",
                                "expired"
                            ],
                            "default": "active"
                        }
                    },
                    "required": [
                        "start",
                        "end"
                    ],
                    "additionalProperties": false
                },
                "keywords": {
                    "title": "Filter postings by keyword",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter postings",
                            "description": "Keyword(s) to match in the original title and body of the job postings.",
                            "example": "work/life balance",
                            "type": "string",
                            "minLength": 1
                        },
                        "type": {
                            "title": "Type of keyword search to run",
                            "description": "How the keyword(s) are matched in a job posting.\n* `or` - Match postings with any of the keywords.\n* `and` - Match postings with all the keywords.\n* `phrase` - Match postings with the keywords as a phrase.\n* `expression` - Match postings using a complex boolean expression; e.g. `\"(uav OR drone) AND agriculture NOT surveillance\"`.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match postings that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "default": "or",
                            "type": "string",
                            "enum": [
                                "or",
                                "and",
                                "phrase",
                                "expression"
                            ]
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "TG9uZG9u"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "city_name": {
                    "title": "Filter by city names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "London"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1": {
                    "title": "Filter by Emsi LAU1 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "00FY"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1_name": {
                    "title": "Filter by Emsi LAU1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3": {
                    "title": "Filter by standard level 3 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF14"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3_name": {
                    "title": "Filter by standard level 3 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1": {
                    "title": "Filter by standard level 1 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1_name": {
                    "title": "Filter by standard level 1 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "East Midlands"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country": {
                    "title": "Filter by abbreviated country codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "ENG"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country_name": {
                    "title": "Filter by country names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "England"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "53.30837"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title_name": {
                    "title": "Filter by job title names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Web Developer"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1": {
                    "title": "Filter by Emsi 1-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1_name": {
                    "title": "Filter by Emsi UK SOC1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Associate Professional and Technical Occupations"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2": {
                    "title": "Filter by Emsi 2-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "35"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2_name": {
                    "title": "Filter by Emsi UK SOC2 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Business and Public Service Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3": {
                    "title": "Filter by Emsi 3-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "354"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3_name": {
                    "title": "Filter by Emsi UK SOC3 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales, Marketing and Related Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4": {
                    "title": "Filter by Emsi 4-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3545"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4_name": {
                    "title": "Filter by Emsi UK SOC4 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales accounts and business development managers"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company": {
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "NC95f2bd68-11c7-4140-92ab-7b82fd2d9f7e"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_name": {
                    "title": "Filter by company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_is_staffing": {
                    "title": "Filter to or exclude postings from staffing companies",
                    "description": "Passing `false` filters out postings from companies that have been identified as staffing companies or recruiting agencies; `true` limits results to _only_ those from staffing or recruiting companies. By default both staffing and non-staffing companies are included in the results.",
                    "example": true,
                    "type": "boolean"
                },
                "skill_cluster": {
                    "__internal": true,
                    "title": "**Experimental** Emsi-curated skill cluster Ids",
                    "description": "A list of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "406"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "KS7G2FY662ZPN6H4DZND"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills_name": {
                    "title": "Filter by skill names (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "SQL (Programming Language)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "sources": {
                    "title": "Filter by job posting source websites",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "monster.co.uk"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type": {
                    "title": "Filter by normalized contract type codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "10"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type_name": {
                    "title": "Filter by normalized contract type names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Apprenticeship"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type": {
                    "title": "Filter by employment type (Full/Part time) codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        1
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type_name": {
                    "title": "Filter by employment type (Full/Part time) names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Full-time (> 32 hours)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "min_years_experience": {
                    "title": "Filter on the minimum years of experience requested in a posting",
                    "description": "This filter operates on the advertised minimum years of experience found in a job posting. Not all postings advertise minimum years of experience, when using this filter only postings with a minimum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for minimum years of experience",
                            "description": "Lower bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 1
                        },
                        "upper_bound": {
                            "title": "Upper bound for minimum years of experience",
                            "description": "Upper bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 3
                        }
                    },
                    "additionalProperties": false
                },
                "max_years_experience": {
                    "title": "Filter on the maximum years of experience requested in a posting",
                    "description": "This filter operates on the advertised maximum years of experience found in a job posting. Not all postings advertise maximum years of experience, when using this filter only postings with a maximum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for maximum years of experience",
                            "description": "Lower bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 4
                        },
                        "upper_bound": {
                            "title": "Upper bound for maximum years of experience",
                            "description": "Upper bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 6
                        }
                    },
                    "additionalProperties": false
                },
                "salary": {
                    "title": "Filter by average advertised annual salary",
                    "description": "This filter operates on the average advertised annual salary found in a job posting. Not all postings advertise salaries, when using this filter only postings with advertised salaries will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for salary range",
                            "description": "Lower bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 45000
                        },
                        "upper_bound": {
                            "title": "Upper bound for salary range",
                            "description": "Upper bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 60000
                        }
                    },
                    "additionalProperties": false
                },
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 30
                        }
                    },
                    "additionalProperties": false
                },
                "is_remote": {
                    "title": "Filter by remote job postings",
                    "description": "Job postings that are described as remote or partially remote positions.",
                    "type": "boolean",
                    "example": true
                },
                "is_internship": {
                    "title": "Filter by internship job postings",
                    "description": "Job postings that are described as internship positions.",
                    "type": "boolean",
                    "example": true
                }
            },
            "required": [
                "when"
            ],
            "additionalProperties": false
        },
        "rank": {
            "title": "Choose how to rank your results",
            "type": "object",
            "properties": {
                "by": {
                    "title": "What metric to use to rank the ranking facet",
                    "description": "Some metrics may be approximations for performance reasons.",
                    "default": "unique_postings",
                    "type": "string",
                    "enum": [
                        "unique_postings",
                        "duplicate_postings",
                        "total_postings",
                        "posting_intensity",
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job titles, cities, companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`\n* Skills or certifications timeseries ranking when requesting a `unique_companies` metric: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "duplicate_postings",
                            "total_postings",
                            "posting_intensity",
                            "unique_companies",
                            "median_posting_duration",
                            "min_salary",
                            "median_salary",
                            "max_salary"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by number of unique postings for the item",
                    "description": "Require ranked items to have at least this many unique postings matching the filter.\nDefault: `3` when ranking by `significance`",
                    "default": 1,
                    "type": "integer",
                    "minimum": 1
                },
                "include": {
                    "title": "Filter ranked items to only those provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                },
                "exclude": {
                    "title": "Filter ranked items to only those not provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                }
            },
            "additionalProperties": false
        },
        "timeseries": {
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting timeframe filter, can be the string `active` (except for the timeseries endpoints) to match all currently active postings, or a more granular timeframe `when` object detailed below.",
                    "type": [
                        "string",
                        "object"
                    ],
                    "properties": {
                        "start": {
                            "title": "Filter to postings after this date (inclusive)",
                            "description": "The start of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2015-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2016-06"
                        },
                        "type": {
                            "title": "Choose which date on a posting to filter by",
                            "description": "Determines how posting dates are evaluated.\n* `posted` - Match postings that were posted in your date range.\n* `active` - Match postings that were active within your date range.\n* `expired` - Match postings that expired in your date range.",
                            "type": "string",
                            "enum": [
                                "posted",
                                "active",
                                "expired"
                            ],
                            "default": "active"
                        }
                    },
                    "required": [
                        "start",
                        "end"
                    ],
                    "additionalProperties": false
                },
                "metrics": {
                    "title": "Metrics to calculate per month or day",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "duplicate_postings",
                            "total_postings",
                            "posting_intensity",
                            "unique_companies",
                            "min_salary",
                            "median_salary",
                            "max_salary"
                        ]
                    },
                    "minItems": 1
                }
            },
            "additionalProperties": false
        }
    },
    "required": [
        "filter",
        "rank",
        "timeseries"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/uk-jpa/rankings/title_name/timeseries",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2020-01\", \"end\": \"2020-06\" }, \"company_name\": [ \"Sainsbury’s Group\" ] }, \"rank\": { \"by\": \"unique_postings\", \"limit\": 5 }, \"timeseries\": { \"when\": { \"start\": \"2019-01\", \"end\": \"2019-06\" }, \"metrics\": [ \"unique_postings\", \"total_postings\" ] } }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "ranking": {
      "buckets": [
        {
          "name": "Home Delivery Drivers",
          "timeseries": {
            "month": [
              "2019-01",
              "2019-02",
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "total_postings": [
              0,
              0,
              0,
              136,
              198,
              445
            ],
            "unique_postings": [
              0,
              0,
              0,
              10,
              26,
              29
            ]
          },
          "unique_postings": 114
        },
        {
          "name": "Customer Service and Training Managers",
          "timeseries": {
            "month": [
              "2019-01",
              "2019-02",
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "total_postings": [
              0,
              0,
              0,
              42,
              311,
              433
            ],
            "unique_postings": [
              0,
              0,
              0,
              22,
              75,
              87
            ]
          },
          "unique_postings": 105
        },
        {
          "name": "Trading Assistants",
          "timeseries": {
            "month": [
              "2019-01",
              "2019-02",
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "total_postings": [
              0,
              0,
              0,
              41,
              427,
              1098
            ],
            "unique_postings": [
              0,
              0,
              0,
              6,
              48,
              73
            ]
          },
          "unique_postings": 83
        },
        {
          "name": "Convenience Store Managers",
          "timeseries": {
            "month": [
              "2019-01",
              "2019-02",
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "total_postings": [
              0,
              0,
              0,
              189,
              242,
              268
            ],
            "unique_postings": [
              0,
              0,
              0,
              8,
              20,
              25
            ]
          },
          "unique_postings": 63
        },
        {
          "name": "Online Marketing Assistants",
          "timeseries": {
            "month": [
              "2019-01",
              "2019-02",
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "total_postings": [
              0,
              0,
              0,
              130,
              182,
              327
            ],
            "unique_postings": [
              0,
              0,
              0,
              4,
              19,
              25
            ]
          },
          "unique_postings": 62
        }
      ],
      "facet": "title_name",
      "limit": 5,
      "rank_by": "unique_postings"
    },
    "totals": {
      "unique_postings": 667
    }
  }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="404">

The facet you requested wasn't found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized facet 'foo'"
    }
  ]
}
```


</div>


<div data-tab="422">

Your request wasn't valid (bad keyword expression).


```json
{
  "errors": [
    {
      "status": 422,
      "title": "Invalid request content",
      "detail": "Invalid keyword search expression syntax:\n\t\"general merchandise\" OR \"apparel\" OR \"grocery\" OR\n\t                                                  ^"
    }
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/rankings/{rankingFacet}</span>/rankings/{nestedRankingFacet}

Get a nested ranking (e.g. top companies, then top skills per company).


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>rankingFacet</code><div class="type">enum</div> | Example: `title_name`<br>Must be one of: `certifications`, `certifications_name`, `city`, `city_name`, `company`, `company_name`, `country`, `employment_type`, `employment_type_name`, `hard_skills`, `hard_skills_name`, `lau1`, `lau1_name`, `nuts1`, `nuts1_name`, `nuts3`, `nuts3_name`, `skill_cluster`, `skills`, `skills_name`, `soc1`, `soc1_name`, `soc2`, `soc2_name`, `soc3`, `soc3_name`, `soc4`, `soc4_name`, `soft_skills`, `soft_skills_name`, `sources`, `title`, `title_name`
<code>nestedRankingFacet</code><div class="type">enum</div> | Example: `city_name`<br>Must be one of: `certifications`, `certifications_name`, `city`, `city_name`, `company`, `company_name`, `country`, `employment_type`, `employment_type_name`, `hard_skills`, `hard_skills_name`, `lau1`, `lau1_name`, `nuts1`, `nuts1_name`, `nuts3`, `nuts3_name`, `skill_cluster`, `skills`, `skills_name`, `soc1`, `soc1_name`, `soc2`, `soc2_name`, `soc3`, `soc3_name`, `soc4`, `soc4_name`, `soft_skills`, `soft_skills_name`, `sources`, `title`, `title_name`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2020-01",
      "end": "2020-03"
    }
  },
  "rank": {
    "by": "unique_postings",
    "limit": 5
  },
  "nested_rank": {
    "by": "significance",
    "limit": 5
  }
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/nested-ranking.schema.json",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your postings query",
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting timeframe filter, can be the string `active` (except for the timeseries endpoints) to match all currently active postings, or a more granular timeframe `when` object detailed below.",
                    "type": [
                        "string",
                        "object"
                    ],
                    "properties": {
                        "start": {
                            "title": "Filter to postings after this date (inclusive)",
                            "description": "The start of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2015-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2016-06"
                        },
                        "type": {
                            "title": "Choose which date on a posting to filter by",
                            "description": "Determines how posting dates are evaluated.\n* `posted` - Match postings that were posted in your date range.\n* `active` - Match postings that were active within your date range.\n* `expired` - Match postings that expired in your date range.",
                            "type": "string",
                            "enum": [
                                "posted",
                                "active",
                                "expired"
                            ],
                            "default": "active"
                        }
                    },
                    "required": [
                        "start",
                        "end"
                    ],
                    "additionalProperties": false
                },
                "keywords": {
                    "title": "Filter postings by keyword",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter postings",
                            "description": "Keyword(s) to match in the original title and body of the job postings.",
                            "example": "work/life balance",
                            "type": "string",
                            "minLength": 1
                        },
                        "type": {
                            "title": "Type of keyword search to run",
                            "description": "How the keyword(s) are matched in a job posting.\n* `or` - Match postings with any of the keywords.\n* `and` - Match postings with all the keywords.\n* `phrase` - Match postings with the keywords as a phrase.\n* `expression` - Match postings using a complex boolean expression; e.g. `\"(uav OR drone) AND agriculture NOT surveillance\"`.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match postings that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "default": "or",
                            "type": "string",
                            "enum": [
                                "or",
                                "and",
                                "phrase",
                                "expression"
                            ]
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "TG9uZG9u"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "city_name": {
                    "title": "Filter by city names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "London"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1": {
                    "title": "Filter by Emsi LAU1 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "00FY"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1_name": {
                    "title": "Filter by Emsi LAU1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3": {
                    "title": "Filter by standard level 3 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF14"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3_name": {
                    "title": "Filter by standard level 3 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1": {
                    "title": "Filter by standard level 1 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1_name": {
                    "title": "Filter by standard level 1 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "East Midlands"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country": {
                    "title": "Filter by abbreviated country codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "ENG"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country_name": {
                    "title": "Filter by country names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "England"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "53.30837"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title_name": {
                    "title": "Filter by job title names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Web Developer"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1": {
                    "title": "Filter by Emsi 1-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1_name": {
                    "title": "Filter by Emsi UK SOC1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Associate Professional and Technical Occupations"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2": {
                    "title": "Filter by Emsi 2-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "35"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2_name": {
                    "title": "Filter by Emsi UK SOC2 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Business and Public Service Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3": {
                    "title": "Filter by Emsi 3-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "354"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3_name": {
                    "title": "Filter by Emsi UK SOC3 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales, Marketing and Related Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4": {
                    "title": "Filter by Emsi 4-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3545"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4_name": {
                    "title": "Filter by Emsi UK SOC4 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales accounts and business development managers"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company": {
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "NC95f2bd68-11c7-4140-92ab-7b82fd2d9f7e"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_name": {
                    "title": "Filter by company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_is_staffing": {
                    "title": "Filter to or exclude postings from staffing companies",
                    "description": "Passing `false` filters out postings from companies that have been identified as staffing companies or recruiting agencies; `true` limits results to _only_ those from staffing or recruiting companies. By default both staffing and non-staffing companies are included in the results.",
                    "example": true,
                    "type": "boolean"
                },
                "skill_cluster": {
                    "__internal": true,
                    "title": "**Experimental** Emsi-curated skill cluster Ids",
                    "description": "A list of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "406"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "KS7G2FY662ZPN6H4DZND"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills_name": {
                    "title": "Filter by skill names (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "SQL (Programming Language)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "sources": {
                    "title": "Filter by job posting source websites",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "monster.co.uk"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type": {
                    "title": "Filter by normalized contract type codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "10"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type_name": {
                    "title": "Filter by normalized contract type names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Apprenticeship"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type": {
                    "title": "Filter by employment type (Full/Part time) codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        1
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type_name": {
                    "title": "Filter by employment type (Full/Part time) names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Full-time (> 32 hours)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "min_years_experience": {
                    "title": "Filter on the minimum years of experience requested in a posting",
                    "description": "This filter operates on the advertised minimum years of experience found in a job posting. Not all postings advertise minimum years of experience, when using this filter only postings with a minimum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for minimum years of experience",
                            "description": "Lower bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 1
                        },
                        "upper_bound": {
                            "title": "Upper bound for minimum years of experience",
                            "description": "Upper bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 3
                        }
                    },
                    "additionalProperties": false
                },
                "max_years_experience": {
                    "title": "Filter on the maximum years of experience requested in a posting",
                    "description": "This filter operates on the advertised maximum years of experience found in a job posting. Not all postings advertise maximum years of experience, when using this filter only postings with a maximum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for maximum years of experience",
                            "description": "Lower bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 4
                        },
                        "upper_bound": {
                            "title": "Upper bound for maximum years of experience",
                            "description": "Upper bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 6
                        }
                    },
                    "additionalProperties": false
                },
                "salary": {
                    "title": "Filter by average advertised annual salary",
                    "description": "This filter operates on the average advertised annual salary found in a job posting. Not all postings advertise salaries, when using this filter only postings with advertised salaries will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for salary range",
                            "description": "Lower bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 45000
                        },
                        "upper_bound": {
                            "title": "Upper bound for salary range",
                            "description": "Upper bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 60000
                        }
                    },
                    "additionalProperties": false
                },
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 30
                        }
                    },
                    "additionalProperties": false
                },
                "is_remote": {
                    "title": "Filter by remote job postings",
                    "description": "Job postings that are described as remote or partially remote positions.",
                    "type": "boolean",
                    "example": true
                },
                "is_internship": {
                    "title": "Filter by internship job postings",
                    "description": "Job postings that are described as internship positions.",
                    "type": "boolean",
                    "example": true
                }
            },
            "required": [
                "when"
            ],
            "additionalProperties": false
        },
        "rank": {
            "title": "Choose how to rank your results",
            "type": "object",
            "properties": {
                "by": {
                    "title": "What metric to use to rank the ranking facet",
                    "description": "Some metrics may be approximations for performance reasons.",
                    "default": "unique_postings",
                    "type": "string",
                    "enum": [
                        "unique_postings",
                        "duplicate_postings",
                        "total_postings",
                        "posting_intensity",
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job titles, cities, companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`\n* Skills or certifications timeseries ranking when requesting a `unique_companies` metric: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "duplicate_postings",
                            "total_postings",
                            "posting_intensity",
                            "unique_companies",
                            "median_posting_duration",
                            "min_salary",
                            "median_salary",
                            "max_salary"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by number of unique postings for the item",
                    "description": "Require ranked items to have at least this many unique postings matching the filter.\nDefault: `3` when ranking by `significance`",
                    "default": 1,
                    "type": "integer",
                    "minimum": 1
                },
                "include": {
                    "title": "Filter ranked items to only those provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                },
                "exclude": {
                    "title": "Filter ranked items to only those not provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                }
            },
            "additionalProperties": false
        },
        "nested_rank": {
            "title": "Choose how to rank your results",
            "type": "object",
            "properties": {
                "by": {
                    "title": "What metric to use to rank the ranking facet",
                    "description": "Some metrics may be approximations for performance reasons.",
                    "default": "unique_postings",
                    "type": "string",
                    "enum": [
                        "unique_postings",
                        "duplicate_postings",
                        "total_postings",
                        "posting_intensity",
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job titles, cities, companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`\n* Skills or certifications timeseries ranking when requesting a `unique_companies` metric: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "duplicate_postings",
                            "total_postings",
                            "posting_intensity",
                            "unique_companies",
                            "median_posting_duration",
                            "min_salary",
                            "median_salary",
                            "max_salary"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by number of unique postings for the item",
                    "description": "Require ranked items to have at least this many unique postings matching the filter.\nDefault: `3` when ranking by `significance`",
                    "default": 1,
                    "type": "integer",
                    "minimum": 1
                },
                "include": {
                    "title": "Filter ranked items to only those provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                },
                "exclude": {
                    "title": "Filter ranked items to only those not provided in this field",
                    "description": "This field does not affect totals matched by the request query, it only filters the items returned in the ranking.",
                    "type": "array",
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1
                    },
                    "minItems": 1
                }
            },
            "additionalProperties": false
        }
    },
    "required": [
        "filter",
        "rank",
        "nested_rank"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/uk-jpa/rankings/title_name/rankings/city_name",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2020-01\", \"end\": \"2020-03\" } }, \"rank\": { \"by\": \"unique_postings\", \"limit\": 5 }, \"nested_rank\": { \"by\": \"significance\", \"limit\": 5 } }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "ranking": {
      "buckets": [
        {
          "name": "Unclassified",
          "ranking": {
            "buckets": [
              {
                "name": "Unknown",
                "significance": 0.09041988007642093,
                "unique_postings": 29595
              },
              {
                "name": "[Unknown city]",
                "significance": 0.0032306684663184143,
                "unique_postings": 5966
              },
              {
                "name": "Bangor, Wales",
                "significance": 0.0025301665385741023,
                "unique_postings": 124
              },
              {
                "name": "Framwellgate Moor, England",
                "significance": 0.002196137666081308,
                "unique_postings": 30
              },
              {
                "name": "Whitefield, England",
                "significance": 0.0016130319477460574,
                "unique_postings": 34
              }
            ],
            "facet": "city_name",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 208686
        },
        {
          "name": "Support Workers",
          "ranking": {
            "buckets": [
              {
                "name": "Burnham-on-Sea, England",
                "significance": 0.032190876547826784,
                "unique_postings": 68
              },
              {
                "name": "Meldreth, England",
                "significance": 0.030697150376695164,
                "unique_postings": 29
              },
              {
                "name": "Bidford-on-avon, England",
                "significance": 0.02652134113710322,
                "unique_postings": 23
              },
              {
                "name": "Coleford, England",
                "significance": 0.021951551380772302,
                "unique_postings": 31
              },
              {
                "name": "Brant Broughton, England",
                "significance": 0.02118253099848286,
                "unique_postings": 12
              }
            ],
            "facet": "city_name",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 49733
        },
        {
          "name": "Staff Nurses",
          "ranking": {
            "buckets": [
              {
                "name": "Beaumaris, Wales",
                "significance": 0.08534674186536924,
                "unique_postings": 16
              },
              {
                "name": "Kington, England",
                "significance": 0.0820394201498593,
                "unique_postings": 22
              },
              {
                "name": "Heswall, England",
                "significance": 0.0750217837947537,
                "unique_postings": 25
              },
              {
                "name": "Hoylake, England",
                "significance": 0.07500646928973592,
                "unique_postings": 19
              },
              {
                "name": "Criccieth, Wales",
                "significance": 0.07043659212535752,
                "unique_postings": 13
              }
            ],
            "facet": "city_name",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 22924
        },
        {
          "name": "Care Assistants",
          "ranking": {
            "buckets": [
              {
                "name": "Hathersage, England",
                "significance": 0.07027713631625232,
                "unique_postings": 9
              },
              {
                "name": "East Preston, England",
                "significance": 0.055488100682100076,
                "unique_postings": 8
              },
              {
                "name": "Knebworth, England",
                "significance": 0.05316539815991765,
                "unique_postings": 22
              },
              {
                "name": "Haxby, England",
                "significance": 0.04460770333972354,
                "unique_postings": 6
              },
              {
                "name": "St Minver, England",
                "significance": 0.04460770333972354,
                "unique_postings": 6
              }
            ],
            "facet": "city_name",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 22496
        },
        {
          "name": "Quantity Surveyors",
          "ranking": {
            "buckets": [
              {
                "name": "Belfast, Northern Ireland",
                "significance": 0.07816286766669407,
                "unique_postings": 485
              },
              {
                "name": "Antrim, Northern Ireland",
                "significance": 0.07656845896082769,
                "unique_postings": 170
              },
              {
                "name": "Stretham, England",
                "significance": 0.04242168147233004,
                "unique_postings": 4
              },
              {
                "name": "[Unknown city]",
                "significance": 0.03849093059242479,
                "unique_postings": 1323
              },
              {
                "name": "East Down, England",
                "significance": 0.037806328830614806,
                "unique_postings": 5
              }
            ],
            "facet": "city_name",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 20358
        }
      ],
      "facet": "title_name",
      "limit": 5,
      "rank_by": "unique_postings"
    },
    "totals": {
      "unique_postings": 4415755
    }
  }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="404">

The facet you requested wasn't found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized facet 'foo'"
    }
  ]
}
```


</div>


<div data-tab="422">

Your request wasn't valid (bad keyword expression).


```json
{
  "errors": [
    {
      "status": 422,
      "title": "Invalid request content",
      "detail": "Invalid keyword search expression syntax:\n\t\"general merchandise\" OR \"apparel\" OR \"grocery\" OR\n\t                                                  ^"
    }
  ]
}
```


</div>


</div>



## /postings

List individual postings that match a set of filters.


### `POST` <span class="from-raml uri-prefix"></span>/postings

Get data for individual postings that match your requested filters. Note that not all fields are present for all postings, and some may be `null` or "Unknown".
The `url` field is only available for currently active postings, and the destination website is not guaranteed to be secure or functional.

To request more postings please contact us [here](mailto:api-support@emsibg.com).

<div class="internal-only">

**Posting Data Source Access and Limits**

There are two types of posting data that clients can have access to; Emsi-source posting data, and non-Emsi-source. Give `postings:early_feed_access` claim of type scope to a client to grant access to Emsi-source posting data.

To restrict their access to only expired posting data, give `postings:only_expired_samples` claim.

By default all clients can view up to a total of 10 postings. The limit can be changed through a `postings:samples_full_access` claim. The claim `postings:samples_full_access` alone increases the total limit to 100 postings. To increase the limit to 1000, grant `postings:samples_full_access:1000`.

</div>




#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2020-01",
      "end": "2020-03"
    },
    "skills_name": [
      "Java (Programming Language)"
    ],
    "keywords": {
      "query": "work/life balance",
      "type": "phrase"
    }
  },
  "fields": [
    "id",
    "posted",
    "expired",
    "body",
    "city_name",
    "company_name",
    "title_raw",
    "url",
    "score"
  ],
  "order": [
    "score"
  ],
  "limit": 5
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/postings.schema.json",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your postings query",
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting timeframe filter, can be the string `active` (except for the timeseries endpoints) to match all currently active postings, or a more granular timeframe `when` object detailed below.",
                    "type": [
                        "string",
                        "object"
                    ],
                    "properties": {
                        "start": {
                            "title": "Filter to postings after this date (inclusive)",
                            "description": "The start of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2015-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2016-06"
                        },
                        "type": {
                            "title": "Choose which date on a posting to filter by",
                            "description": "Determines how posting dates are evaluated.\n* `posted` - Match postings that were posted in your date range.\n* `active` - Match postings that were active within your date range.\n* `expired` - Match postings that expired in your date range.",
                            "type": "string",
                            "enum": [
                                "posted",
                                "active",
                                "expired"
                            ],
                            "default": "active"
                        }
                    },
                    "required": [
                        "start",
                        "end"
                    ],
                    "additionalProperties": false
                },
                "keywords": {
                    "title": "Filter postings by keyword",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter postings",
                            "description": "Keyword(s) to match in the original title and body of the job postings.",
                            "example": "work/life balance",
                            "type": "string",
                            "minLength": 1
                        },
                        "type": {
                            "title": "Type of keyword search to run",
                            "description": "How the keyword(s) are matched in a job posting.\n* `or` - Match postings with any of the keywords.\n* `and` - Match postings with all the keywords.\n* `phrase` - Match postings with the keywords as a phrase.\n* `expression` - Match postings using a complex boolean expression; e.g. `\"(uav OR drone) AND agriculture NOT surveillance\"`.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match postings that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "default": "or",
                            "type": "string",
                            "enum": [
                                "or",
                                "and",
                                "phrase",
                                "expression"
                            ]
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "TG9uZG9u"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "city_name": {
                    "title": "Filter by city names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "London"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1": {
                    "title": "Filter by Emsi LAU1 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "00FY"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "lau1_name": {
                    "title": "Filter by Emsi LAU1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3": {
                    "title": "Filter by standard level 3 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF14"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts3_name": {
                    "title": "Filter by standard level 3 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Nottingham"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1": {
                    "title": "Filter by standard level 1 NUTS codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "UKF"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "nuts1_name": {
                    "title": "Filter by standard level 1 NUTS names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "East Midlands"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country": {
                    "title": "Filter by abbreviated country codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "ENG"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "country_name": {
                    "title": "Filter by country names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "England"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "53.30837"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "title_name": {
                    "title": "Filter by job title names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Web Developer"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1": {
                    "title": "Filter by Emsi 1-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc1_name": {
                    "title": "Filter by Emsi UK SOC1 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Associate Professional and Technical Occupations"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2": {
                    "title": "Filter by Emsi 2-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "35"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc2_name": {
                    "title": "Filter by Emsi UK SOC2 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Business and Public Service Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3": {
                    "title": "Filter by Emsi 3-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "354"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc3_name": {
                    "title": "Filter by Emsi UK SOC3 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales, Marketing and Related Associate Professionals"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4": {
                    "title": "Filter by Emsi 4-digit UK SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "3545"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "soc4_name": {
                    "title": "Filter by Emsi UK SOC4 names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Sales accounts and business development managers"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company": {
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "NC95f2bd68-11c7-4140-92ab-7b82fd2d9f7e"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_name": {
                    "title": "Filter by company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "company_is_staffing": {
                    "title": "Filter to or exclude postings from staffing companies",
                    "description": "Passing `false` filters out postings from companies that have been identified as staffing companies or recruiting agencies; `true` limits results to _only_ those from staffing or recruiting companies. By default both staffing and non-staffing companies are included in the results.",
                    "example": true,
                    "type": "boolean"
                },
                "skill_cluster": {
                    "__internal": true,
                    "title": "**Experimental** Emsi-curated skill cluster Ids",
                    "description": "A list of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "406"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "KS7G2FY662ZPN6H4DZND"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "skills_name": {
                    "title": "Filter by skill names (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor skills version see [/meta](#meta).",
                    "example": [
                        "SQL (Programming Language)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "sources": {
                    "title": "Filter by job posting source websites",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "monster.co.uk"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type": {
                    "title": "Filter by normalized contract type codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "10"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "contract_type_name": {
                    "title": "Filter by normalized contract type names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Apprenticeship"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type": {
                    "title": "Filter by employment type (Full/Part time) codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        1
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": [
                            "string",
                            "integer"
                        ],
                        "minLength": 1,
                        "minimum": 0,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": [
                                    "string",
                                    "integer"
                                ],
                                "minLength": 1,
                                "minimum": 0,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "employment_type_name": {
                    "title": "Filter by employment type (Full/Part time) names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Full-time (> 32 hours)"
                    ],
                    "type": [
                        "array",
                        "object"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "include_op": {
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        },
                        "exclude_op": {
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).",
                            "type": "string",
                            "enum": [
                                "and",
                                "or",
                                "AND",
                                "OR"
                            ],
                            "default": "or",
                            "__nodocs": true
                        }
                    },
                    "additionalProperties": false
                },
                "min_years_experience": {
                    "title": "Filter on the minimum years of experience requested in a posting",
                    "description": "This filter operates on the advertised minimum years of experience found in a job posting. Not all postings advertise minimum years of experience, when using this filter only postings with a minimum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for minimum years of experience",
                            "description": "Lower bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 1
                        },
                        "upper_bound": {
                            "title": "Upper bound for minimum years of experience",
                            "description": "Upper bound for the minimum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 3
                        }
                    },
                    "additionalProperties": false
                },
                "max_years_experience": {
                    "title": "Filter on the maximum years of experience requested in a posting",
                    "description": "This filter operates on the advertised maximum years of experience found in a job posting. Not all postings advertise maximum years of experience, when using this filter only postings with a maximum years of experience will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for maximum years of experience",
                            "description": "Lower bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 4
                        },
                        "upper_bound": {
                            "title": "Upper bound for maximum years of experience",
                            "description": "Upper bound for the maximum years of experience required by a job posting (years are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 6
                        }
                    },
                    "additionalProperties": false
                },
                "salary": {
                    "title": "Filter by average advertised annual salary",
                    "description": "This filter operates on the average advertised annual salary found in a job posting. Not all postings advertise salaries, when using this filter only postings with advertised salaries will be included in your results.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for salary range",
                            "description": "Lower bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 45000
                        },
                        "upper_bound": {
                            "title": "Upper bound for salary range",
                            "description": "Upper bound for average advertised salary (inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 60000
                        }
                    },
                    "additionalProperties": false
                },
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "type": "integer",
                            "minimum": 0,
                            "example": 30
                        }
                    },
                    "additionalProperties": false
                },
                "is_remote": {
                    "title": "Filter by remote job postings",
                    "description": "Job postings that are described as remote or partially remote positions.",
                    "type": "boolean",
                    "example": true
                },
                "is_internship": {
                    "title": "Filter by internship job postings",
                    "description": "Job postings that are described as internship positions.",
                    "type": "boolean",
                    "example": true
                }
            },
            "required": [
                "when"
            ],
            "additionalProperties": false
        },
        "fields": {
            "title": "Posting fields returned in the response",
            "description": "See [/meta](#meta) `postingsFields` for available fields.",
            "default": [
                "id",
                "posted",
                "expired",
                "body",
                "city_name",
                "company_name",
                "title_raw",
                "url",
                "score"
            ],
            "type": "array",
            "items": {
                "__nodocs": true,
                "type": "string"
            },
            "minItems": 1
        },
        "limit": {
            "title": "Limit the number of postings returned per page",
            "description": "Maximum: `10` (or more for authorized consumers)",
            "default": 10,
            "type": "integer",
            "minimum": 1
        },
        "order": {
            "title": "The order in which to sort the search results",
            "description": "Postings are sorted with respect to the order of the provided keys.\n* `score` - sort postings according to their relevance to the request filter.\n* `posted` - sort postings by their posted dates.\n\nI.e. using an order of `[\"score\", \"posted\"]` will sort postings first by their score then sort the ones with the same score by posted dates.",
            "default": [
                "score",
                "posted"
            ],
            "type": "array",
            "items": {
                "__nodocs": true,
                "type": "string",
                "enum": [
                    "score",
                    "posted"
                ]
            },
            "minItems": 1
        },
        "page": {
            "title": "Page number",
            "default": 1,
            "type": "integer",
            "minimum": 1
        }
    },
    "required": [
        "filter"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/uk-jpa/postings",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2020-01\", \"end\": \"2020-03\" }, \"skills_name\": [ \"Java (Programming Language)\" ], \"keywords\": { \"query\": \"work/life balance\", \"type\": \"phrase\" } }, \"fields\": [ \"id\", \"posted\", \"expired\", \"body\", \"city_name\", \"company_name\", \"title_raw\", \"url\", \"score\" ], \"order\": [ \"score\" ], \"limit\": 5 }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "data": {
    "limit": 5,
    "page": 1,
    "pages_available": 2,
    "postings": [
      {
        "body": "<!--id: 4cdafdf1c7614f37a202bf1aa1668d15-->The form is incomplete, see above Thanks, your Job Alert has been set-up successfully. Keep an eye on your inbox for the latest jobs that match your search on Harnham.com Harnham-SR-01 <h5>Wimbledon, London Salary:</h5> Competitive 1. Job type Permanent 2. <h5>Sector:</h5> Internal Emma Way Internal Recruitment Consultant <ul><li> UK & European Internal Recruitment </li><li> Global Operations Emailemmaway@harnham.com Similar Jobs Senior Data Science Engineer Salary US$160000</li><li>US$180000 per year + Benefits Location San Francisco, California Description This is organization based in Downtown San Francisco that is looking to help its users extract data driven insights to help with strategic decisions.</li></ul> <h5>ADD TO SHORTLIST</h5> Data UAT Analyst Salary £30000<ul><li>£45000 per annum + bonus, pension, benefits Location West London, London Description A great opportunity performing User Acceptance Testing for a global retail leader on a flagship data warehouse project.</li></ul> <h5>ADD TO SHORTLIST</h5> Data Governance Director Salary £80000<ul><li>£100000 per annum + bonus, pension, benefits Location City of London, London Description An opportunity to develop and implement the data governance framework for global, billion-pound company.</li></ul> <h5>ADD TO SHORTLIST</h5> Java Developer Salary £400<ul><li>£500 per day Location City of London, London Description Java Developer London 6 month contract £400-500 ADD </li></ul><h5>TO SHORTLIST</h5> Director of Algorithms Salary US$180000<ul><li>US$210000 per year + Benefits Location San Francisco, California Description This is the opportunity to work with cutting-edge data and build out a team while helping individuals live healthier, longer lives.</li></ul> <h5>ADD TO SHORTLIST UPLOAD YOUR CV</h5> We help the best talent in the Digital analytics market to find rewarding careers. Simply upload your CV and select your areas of interest and our expert recruitment consultants will be in touch Upload Now Harnham blog & news With over 10 years experience working solely in the Data & Analytics sector our consultants are able to offer detailed insights into the industry. Visit our Blogs & News portal or check out our recent posts below. Harnham's Brush with Fame Harnham have partnered with The Charter School North Dulwich as corporate sponsors of their 'Secret Charter' event. The event sees the south London state school selling over 500 postcard-sized original pieces of art to raise funds for their Art, Drama and Music departments. Conceived by local parent Laura Stephens, the original concept was to auction art from both pupils and contributing parents. Whilst designs from 30 of the school's best art students remain, the scope of contributors has rapidly expanded and now includes the work of local artists alongside celebrated greats including Tracey Emin, Sir Anthony Gormley, Julian Opie, and Gary Hume. In addition to famous artists, several well-known names have contributed their own designs including James Corden, David Mitchell, Miranda Hart, Jo Brand, Jeremy Corbyn, and Hugh Grant. The event itself, sponsored by Harnham and others, will be hosted by James Nesbitt, and will take place at Dulwich Picture Gallery on the 15th October 2018. You can find out how to purchase a postcard and more information about the event here. by Simon Clarke 17. September 2018 News Why A Good <span class=\"jpa-keyword-highlight\">Work</span><ul><li>span class=\"jpa-keyword-highlight\">Life</li></ul></span> <span class=\"jpa-keyword-highlight\">Balance</span> Is Better for Business Contrary to American sitcoms, <span class=\"jpa-keyword-highlight\">work</span> <span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span> isn't about sitting in coffee shops contemplating life and complaining about work. However, there are plenty of jobs where you can work from or in a coffee shop. The rise of virtual, remote, and contractual roles has contributed to the demand for <span class=\"jpa-keyword-highlight\">work</span> <span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. But, sometimes, in our tech-led world, where business can follow us anywhere, the balance becomes more about setting boundaries. It's about putting down our mobile phones, closing our laptops, and dipping our toes into other waters. Where Does Your Country Fit on the <span class=\"jpa-keyword-highlight\">Work</span><ul><li>span class=\"jpa-keyword-highlight\">Life</span> <span class=\"jpa-keyword-highlight\">Balance</span> Scale? European countries have been leading the way with <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> for some time, with the Netherlands topping the list at number one. With the UK sitting at number 29 out of the 38 countries in the Organisation for Economic Co-operation and Development (OECD), what's tipping the scales? 13% of British employees work 50 or more hours per week versus 0.5% of people in the Netherlands work those long hours. The average Brit is therefore only setting aside 14.9 hours for leisure and personal care (including eating and sleeping) a day versus those in the Netherlands who dedicate 15.9 hours. Countries in the Nordics work a maximum of 48-hours per week. However, the reality is significantly lower, with the Finnish working an average of 36.2 hours a week, the Swedes 35.9 hours, Norwegians at 34 hours, and the Danes just 32 hours.<br><br>Denmark, Finland, Sweden, Norway, and Iceland have become renowned for fostering optimal <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. But, though the Netherlands sits at the number one spot on the OECD, the Danes top the list as the happiest in the world. The Danish welfare model, characterised by quality of life and a good <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span> offers: Flexible working conditions and social support networks, including maternity leave and childcare facilities. A high degree of flexibility at work</li><li>often including adaptable start times and the ability to work from home. Lunch breaks are often at a designated time each day, enabling colleagues to interact, eat together, and get away from their desks. There is a minimum 5 weeks' paid holiday for all wage earners. The Danish welfare society is characterised by quality of life and a good <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. <span class=\"jpa-keyword-highlight\">Work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> for the Danes is a healthy balance of priorities. As important as career and ambition is, are is just as important to balance life outside work (pleasure, leisure, family, and health). This understanding of balance not only puts Denmark at the top of the international equality table, it also contributes to a generally high standard of living. Further research shows 33% of working American adults work over the weekend and on holidays. This, in turn, has led 66% to say they don't feel they have a good <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span>. One of the main drivers contributing to the need to always be \"on\" and available is 24/7 technology. For example, if an employer emails, texts, or rings an employee at dinnertime, the employee often feels compelled to answer straightaway. While 57% of those surveyed feel technology has ruined the family dinner, 40% believe it is okay to answer an urgent call or email at the dinner table. So, it comes back to boundaries and not feeling guilty about 'switching off' for a few hours or a few days to 'recharge'. What Companies are Doing to Improve <span class=\"jpa-keyword-highlight\">Work</span><ul><li>span class=\"jpa-keyword-highlight\">Life</span> <span class=\"jpa-keyword-highlight\">Balance</span> Nordic businesses remain at the top of the list for best <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span>. Though much of it is dictated by strict Nordic Labour laws, companies outside the Nordics are beginning to take pages from their playbook. At a business in Helsinki, Finland, employees are encouraged to go home on time at the end of their day. Often this falls around 5:00pm, though leaving earlier to say, go to a child's sports activity, is always a guilt-free option. Like many European businesses, employees also receive five weeks of paid vacation each year. Everyone gets stock options and teams are small with the ability to make autonomous decisions. <h5>The theory:</h5> this team is closest to the project, they know what is best for it. No management approval required, but only to help share in lessons learned. Many Nordic businesses have shortened hours and a focus on family. By putting family first, businesses report improved productivity and innovation, less absenteeism, and reductions in staff turnover. <h5>Other benefits can include:</h5> Ability to leave work 30-minutes early to pick up kids from school or take them to sports practice Ability to use sick days to take care of sick children Businesses regularly offer gym memberships, event discounts, leadership classes, and team-building exercises as well as opportunities for employees to take courses and further their education. At one business, in Sweden, for example, employees have access to a leisure centre and recreational activities such as fishing, tennis, and swimming. Though everyone has their own definition of what <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> means to them, it can be difficult to follow without government mandates, like in some European countries, or if you're a small business. Our UK and Europe Salary Guide showed that, with over 98% of respondents working full time, at least some flexibility is now expected. We found that 53% of respondents work at home at least one day a week, and 56% have flexible working hours, highlighting that these 'benefits' are now becoming the norm. Harnham Life As a business, we try to both reflect, and the lead the way with, developments that we see across the Data & Analytics industry. From ensuring our consultants leave on time two days per week to participate in pursuits outside work, to offering one fully-paid Charity Day per year, we place emphasis on creating an environment where our teams feel like they have a good <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. By building a culture where a consultant can set up a book club or arrange a night out on the town, we have formed a business where employee welfare is prioritised. Though everyone has their own definition of what <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> means to them, it can be difficult to follow without government mandates like in some European countries or if you're a small business. The important thing is to do what's right for you and sometimes turn off your phone, close your laptop, and meet up with some family or friends in that coffee shop. Whether you're looking for a permanent position with more benefits, or the freedom of a contract role, we're here to help with your job search. by Emma Way 15. August 2018 News Giving Back Read about Harnham's corporate social responsibility initiatives Find our more about the causes we support. <h5>READ MORE</h5> Recently Viewed jobs Credit Risk Analyst Salary £40000<ul><li>£55000 per annum + Competitive Benefits Location London Description Work with a major banking client to drive portfolio growth through the use of Data, Analytics and Modelling Read more </li></ul><h5>ADD TO SHORTLIST</h5> Credit Risk Analyst Salary £41000<ul><li>£55000 per annum + Competitive Benefits Location London Description A major retail credit provider is adding to its Strategic Analytics function, where you will be offered flexible working, training in R and leading benefits Read more </li></ul><h5>ADD TO SHORTLIST</h5> Senior Data Analyst Salary US$100000<ul><li>US$120000 per year Location San Francisco, California Description A well-funded startup in the transportation space is expanding their analytics team.</li></ul> This is an excellent opportunity to join a start up at the perfect time! Read more <h5>ADD TO SHORTLIST</h5> Lead Pricing Strategist Salary US$120000<ul><li>US$140000 per year Location San Francisco, California Description A series D SaaS company in SF is looking for a Lead Pricing Strategist to own all things pricing and promo related!</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Marketing Analyst<ul><li>Customer Segmentation</li><li>Innovative Brand Salary £35000</li><li>£45000 per annum + benefits + bonus Location London Description A start up brand with a newly restructured and growing analytics team are looking for a Marketing-Channel Insight Analyst to join their team in London.</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Java Developer Salary £450<ul><li>£500 per day Location Manchester, Greater Manchester Description As a Java Developer, you will be developing a core trading platform for a niche, start-up who specialise in the Hedge Fund sector.</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Java Developer Salary £400<ul><li>£500 per day Location Manchester, Greater Manchester Description A new opportunity to work on the back-end development of a new software product for an online comparison site.</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Insight Executive Salary Up to £35000 per annum + bonus and benefits Location Oxfordshire Description Insight Executive working for a very well known retailer in Milton Keynes. Read more <h5>ADD TO SHORTLIST</h5> Insight Executive Salary Up to £35000 per annum + bonus and benefits Location Milton Keynes, Buckinghamshire Description Insight Executive working for a very well known retailer in Milton Keynes. Read more <h5>ADD TO SHORTLIST</h5> Digital Analytics Technology Manager Salary £65000<ul><li>£75000 per annum Location London Description Join one of the UK's leading retailers and head up the technology and implementation team.</li></ul> Read more <h5>ADD TO SHORTLIST</h5> <ul></ul><h5>RECRUITMENT</h5> + Advice + News & Blog + Salary Guide + Quick Send CV + Refer a Friend <ul></ul><h5>ABOUT US</h5> + About Us + Contract Services + Join Us <ul><li> CONTACT + New York + San Francisco + Berlin + Wimbledon </li><li> OTHER + Privacy Notice + Site & Cookie Policy + Associations + Charity </li><li>© 2018 Harnham Search and Selection Ltd.</li></ul> <h5>All rights reserved Registered office:</h5> 3rd Floor, Melbury House, 51 Wimbledon Hill Road, Wimbledon, SW19 7QW. Harnham Search and Selection is a registered company in England and Wales. <h5>Company registration number:</h5>Â 05723485Â Website by 4MAT / Designed by <h5>Brand Nu Keyword:</h5> <h5>No Keyword Options:</h5> 652 <h5>Location:</h5> Job Details",
        "city_name": "London, England",
        "company_name": "Harnham",
        "expired": "2020-02-25",
        "id": "4cdafdf1c7614f37a202bf1aa1668d15",
        "posted": "2018-11-16",
        "score": 15.217209,
        "title_raw": "Credit Risk Analyst",
        "url": []
      },
      {
        "body": "<!--id: d7106ca4ba1541328e7c5a5184426d9b--><h5>CUSTOMER INSIGHT ANALYST</h5> (M/W) Mein Kunde, ein marktführender Energiekonzern, sucht Unterstützung für sein innovatives und wachsendes Data Analytics Team. Durch deine Analysefähigkeiten trägst du zu einem ganzheitlichen Kundenverständnis bei. <h5>DEINE AUFGABEN</h5> <ul><li> Als Data Analyst generierst du Customer Insights (z.</li></ul>B. Kundenwertanalyse, Kundensegmentierung) zur Optimierung von Direktmarketingaktivitäten über alle Kommunikationskanäle <ul><li> Du entwickelst und führst Potenzial</li><li>und Zielgruppenanalysen durch </li><li> Unterstützung der Kundenrückgewinnung im Rahmen von Churn-Analysen </li><li> Enge Zusammenarbeit mit dem Vertriebs</li><li>und Marketing-Team </li><li> Auf deinen Analyseergebnissen basierend erstellst du Entscheidungsvorlagen und präsentierst diese </li></ul><h5>DAS BRINGST DU MIT</h5> <ul><li> Abgeschlossenes Studium mit statistischem Schwerpunkt </li><li> Du hast mindestens 2 Jahre einschlägige Berufserfahrung im analytischen CRM oder in der Datenanalyse </li><li> Deine SQL Kenntnisse sind sehr gut </li><li> Du hast bereits Erfahrung mit dem Umgang von gängigen Analyse</li><li>und Statistiktools (idealerweise R und/oder SAS) </li><li> Tableau Kenntnisse sind von Vorteil </li><li> Kommunikations</li><li>und Präsentationsstärke und Spaß an der Arbeit im Team </li><li> Sichere Deutsch</li><li>und Englischkenntnisse in Wort und Schrift </li></ul><h5>BENEFITS</h5> <ul><li> Attraktives Gehalt und sehr gute Weiterentwicklungsmöglichkeiten </li><li> Weiterbildung durch Trainings und Workshops </li><li> Frisches Obst und Snacks </li><li> Ansprechende Büroräume im Herzen der Stadt </li></ul><h5>INTERESSE?</h5> Du hast Interesse? Bewirb dich direkt auf dieser Website! Apply Save job Send similar jobs by email Sign-up for Job Alerts Enter your email below to receive alerts to your inbox when similar jobs become available. By clicking \"Yes, send me jobs\" below you are consenting to receive jobs to your inbox, based on the search criteria you have selected, as per our privacy policy. Email address The form is incomplete, see above Thanks, your Job Alert has been set-up successfully. Keep an eye on your inbox for the latest jobs that match your search on Harnham.com <h5>VAC 3097</h5>_1530262138 Düsseldorf, <h5>Nordrhein-Westfalen Salary:</h5> €50000<ul><li>€60000 per annum 1.</li></ul> Job type Permanent 2. <h5>Sector:</h5> Marketing Analyst Linda Stadler Senior Recruitment Consultant Emaillindastadler@harnham.com Similar Jobs Senior Data Science Engineer Salary US$160000<ul><li>US$180000 per year + Benefits Location San Francisco, California Description This is organization based in Downtown San Francisco that is looking to help its users extract data driven insights to help with strategic decisions.</li></ul> <h5>ADD TO SHORTLIST</h5> Data UAT Analyst Salary £30000<ul><li>£45000 per annum + bonus, pension, benefits Location West London, London Description A great opportunity performing User Acceptance Testing for a global retail leader on a flagship data warehouse project.</li></ul> <h5>ADD TO SHORTLIST</h5> Data Governance Director Salary £80000<ul><li>£100000 per annum + bonus, pension, benefits Location City of London, London Description An opportunity to develop and implement the data governance framework for global, billion-pound company.</li></ul> <h5>ADD TO SHORTLIST</h5> Java Developer Salary £400<ul><li>£500 per day Location City of London, London Description Java Developer London 6 month contract £400-500 ADD </li></ul><h5>TO SHORTLIST</h5> Director of Algorithms Salary US$180000<ul><li>US$210000 per year + Benefits Location San Francisco, California Description This is the opportunity to work with cutting-edge data and build out a team while helping individuals live healthier, longer lives.</li></ul> <h5>ADD TO SHORTLIST UPLOAD YOUR CV</h5> We help the best talent in the Digital analytics market to find rewarding careers. Simply upload your CV and select your areas of interest and our expert recruitment consultants will be in touch Upload Now Harnham blog & news With over 10 years experience working solely in the Data & Analytics sector our consultants are able to offer detailed insights into the industry. Visit our Blogs & News portal or check out our recent posts below. Harnham's Brush with Fame Harnham have partnered with The Charter School North Dulwich as corporate sponsors of their 'Secret Charter' event. The event sees the south London state school selling over 500 postcard-sized original pieces of art to raise funds for their Art, Drama and Music departments. Conceived by local parent Laura Stephens, the original concept was to auction art from both pupils and contributing parents. Whilst designs from 30 of the school's best art students remain, the scope of contributors has rapidly expanded and now includes the work of local artists alongside celebrated greats including Tracey Emin, Sir Anthony Gormley, Julian Opie, and Gary Hume. In addition to famous artists, several well-known names have contributed their own designs including James Corden, David Mitchell, Miranda Hart, Jo Brand, Jeremy Corbyn, and Hugh Grant. The event itself, sponsored by Harnham and others, will be hosted by James Nesbitt, and will take place at Dulwich Picture Gallery on the 15th October 2018. You can find out how to purchase a postcard and more information about the event here. by Simon Clarke 17. September 2018 News Why A Good <span class=\"jpa-keyword-highlight\">Work</span><ul><li>span class=\"jpa-keyword-highlight\">Life</li></ul></span> <span class=\"jpa-keyword-highlight\">Balance</span> Is Better for Business Contrary to American sitcoms, <span class=\"jpa-keyword-highlight\">work</span> <span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span> isn't about sitting in coffee shops contemplating life and complaining about work. However, there are plenty of jobs where you can work from or in a coffee shop. The rise of virtual, remote, and contractual roles has contributed to the demand for <span class=\"jpa-keyword-highlight\">work</span> <span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. But, sometimes, in our tech-led world, where business can follow us anywhere, the balance becomes more about setting boundaries. It's about putting down our mobile phones, closing our laptops, and dipping our toes into other waters. Where Does Your Country Fit on the <span class=\"jpa-keyword-highlight\">Work</span><ul><li>span class=\"jpa-keyword-highlight\">Life</span> <span class=\"jpa-keyword-highlight\">Balance</span> Scale? European countries have been leading the way with <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> for some time, with the Netherlands topping the list at number one. With the UK sitting at number 29 out of the 38 countries in the Organisation for Economic Co-operation and Development (OECD), what's tipping the scales? 13% of British employees work 50 or more hours per week versus 0.5% of people in the Netherlands work those long hours. The average Brit is therefore only setting aside 14.9 hours for leisure and personal care (including eating and sleeping) a day versus those in the Netherlands who dedicate 15.9 hours. Countries in the Nordics work a maximum of 48-hours per week. However, the reality is significantly lower, with the Finnish working an average of 36.2 hours a week, the Swedes 35.9 hours, Norwegians at 34 hours, and the Danes just 32 hours.<br><br>Denmark, Finland, Sweden, Norway, and Iceland have become renowned for fostering optimal <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. But, though the Netherlands sits at the number one spot on the OECD, the Danes top the list as the happiest in the world. The Danish welfare model, characterised by quality of life and a good <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span> offers: Flexible working conditions and social support networks, including maternity leave and childcare facilities. A high degree of flexibility at work</li><li>often including adaptable start times and the ability to work from home. Lunch breaks are often at a designated time each day, enabling colleagues to interact, eat together, and get away from their desks. There is a minimum 5 weeks' paid holiday for all wage earners. The Danish welfare society is characterised by quality of life and a good <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. <span class=\"jpa-keyword-highlight\">Work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> for the Danes is a healthy balance of priorities. As important as career and ambition is, are is just as important to balance life outside work (pleasure, leisure, family, and health). This understanding of balance not only puts Denmark at the top of the international equality table, it also contributes to a generally high standard of living. Further research shows 33% of working American adults work over the weekend and on holidays. This, in turn, has led 66% to say they don't feel they have a good <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span>. One of the main drivers contributing to the need to always be \"on\" and available is 24/7 technology. For example, if an employer emails, texts, or rings an employee at dinnertime, the employee often feels compelled to answer straightaway. While 57% of those surveyed feel technology has ruined the family dinner, 40% believe it is okay to answer an urgent call or email at the dinner table. So, it comes back to boundaries and not feeling guilty about 'switching off' for a few hours or a few days to 'recharge'. What Companies are Doing to Improve <span class=\"jpa-keyword-highlight\">Work</span><ul><li>span class=\"jpa-keyword-highlight\">Life</span> <span class=\"jpa-keyword-highlight\">Balance</span> Nordic businesses remain at the top of the list for best <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span>. Though much of it is dictated by strict Nordic Labour laws, companies outside the Nordics are beginning to take pages from their playbook. At a business in Helsinki, Finland, employees are encouraged to go home on time at the end of their day. Often this falls around 5:00pm, though leaving earlier to say, go to a child's sports activity, is always a guilt-free option. Like many European businesses, employees also receive five weeks of paid vacation each year. Everyone gets stock options and teams are small with the ability to make autonomous decisions. <h5>The theory:</h5> this team is closest to the project, they know what is best for it. No management approval required, but only to help share in lessons learned. Many Nordic businesses have shortened hours and a focus on family. By putting family first, businesses report improved productivity and innovation, less absenteeism, and reductions in staff turnover. <h5>Other benefits can include:</h5> Ability to leave work 30-minutes early to pick up kids from school or take them to sports practice Ability to use sick days to take care of sick children Businesses regularly offer gym memberships, event discounts, leadership classes, and team-building exercises as well as opportunities for employees to take courses and further their education. At one business, in Sweden, for example, employees have access to a leisure centre and recreational activities such as fishing, tennis, and swimming. Though everyone has their own definition of what <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> means to them, it can be difficult to follow without government mandates, like in some European countries, or if you're a small business. Our UK and Europe Salary Guide showed that, with over 98% of respondents working full time, at least some flexibility is now expected. We found that 53% of respondents work at home at least one day a week, and 56% have flexible working hours, highlighting that these 'benefits' are now becoming the norm. Harnham Life As a business, we try to both reflect, and the lead the way with, developments that we see across the Data & Analytics industry. From ensuring our consultants leave on time two days per week to participate in pursuits outside work, to offering one fully-paid Charity Day per year, we place emphasis on creating an environment where our teams feel like they have a good <span class=\"jpa-keyword-highlight\">work</span><ul><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. By building a culture where a consultant can set up a book club or arrange a night out on the town, we have formed a business where employee welfare is prioritised. Though everyone has their own definition of what <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</li></ul></span> <span class=\"jpa-keyword-highlight\">balance</span> means to them, it can be difficult to follow without government mandates like in some European countries or if you're a small business. The important thing is to do what's right for you and sometimes turn off your phone, close your laptop, and meet up with some family or friends in that coffee shop. Whether you're looking for a permanent position with more benefits, or the freedom of a contract role, we're here to help with your job search. by Emma Way 15. August 2018 News Giving Back Read about Harnham's corporate social responsibility initiatives Find our more about the causes we support. <h5>READ MORE</h5> Recently Viewed jobs Senior Recruiter Salary Competitive Location Wimbledon, London Description Work at Harnham in Wimbledon as a Senior Recruitment Consultant! Read more <h5>ADD TO SHORTLIST</h5> Credit Risk Analyst Salary £40000<ul><li>£55000 per annum + Competitive Benefits Location London Description Work with a major banking client to drive portfolio growth through the use of Data, Analytics and Modelling Read more </li></ul><h5>ADD TO SHORTLIST</h5> Credit Risk Analyst Salary £41000<ul><li>£55000 per annum + Competitive Benefits Location London Description A major retail credit provider is adding to its Strategic Analytics function, where you will be offered flexible working, training in R and leading benefits Read more </li></ul><h5>ADD TO SHORTLIST</h5> Senior Data Analyst Salary US$100000<ul><li>US$120000 per year Location San Francisco, California Description A well-funded startup in the transportation space is expanding their analytics team.</li></ul> This is an excellent opportunity to join a start up at the perfect time! Read more <h5>ADD TO SHORTLIST</h5> Lead Pricing Strategist Salary US$120000<ul><li>US$140000 per year Location San Francisco, California Description A series D SaaS company in SF is looking for a Lead Pricing Strategist to own all things pricing and promo related!</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Marketing Analyst<ul><li>Customer Segmentation</li><li>Innovative Brand Salary £35000</li><li>£45000 per annum + benefits + bonus Location London Description A start up brand with a newly restructured and growing analytics team are looking for a Marketing-Channel Insight Analyst to join their team in London.</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Java Developer Salary £450<ul><li>£500 per day Location Manchester, Greater Manchester Description As a Java Developer, you will be developing a core trading platform for a niche, start-up who specialise in the Hedge Fund sector.</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Java Developer Salary £400<ul><li>£500 per day Location Manchester, Greater Manchester Description A new opportunity to work on the back-end development of a new software product for an online comparison site.</li></ul> Read more <h5>ADD TO SHORTLIST</h5> Insight Executive Salary Up to £35000 per annum + bonus and benefits Location Oxfordshire Description Insight Executive working for a very well known retailer in Milton Keynes. Read more <h5>ADD TO SHORTLIST</h5> Insight Executive Salary Up to £35000 per annum + bonus and benefits Location Milton Keynes, Buckinghamshire Description Insight Executive working for a very well known retailer in Milton Keynes. Read more <h5>ADD TO SHORTLIST</h5> <ul></ul><h5>RECRUITMENT</h5> + Advice + News & Blog + Salary Guide + Quick Send CV + Refer a Friend <ul></ul><h5>ABOUT US</h5> + About Us + Contract Services + Join Us <ul><li> CONTACT + New York + San Francisco + Berlin + Wimbledon </li><li> OTHER + Privacy Notice + Site & Cookie Policy + Associations + Charity </li><li>© 2018 Harnham Search and Selection Ltd.</li></ul> <h5>All rights reserved Registered office:</h5> 3rd Floor, Melbury House, 51 Wimbledon Hill Road, Wimbledon, SW19 7QW. Harnham Search and Selection is a registered company in England and Wales. <h5>Company registration number:</h5>Â 05723485Â Website by 4MAT / Designed by <h5>Brand Nu Keyword:</h5> <h5>No Keyword Options:</h5> 606 <h5>Location:</h5> Job Details",
        "city_name": "London, England",
        "company_name": "Harnham",
        "expired": "2020-02-25",
        "id": "d7106ca4ba1541328e7c5a5184426d9b",
        "posted": "2018-11-16",
        "score": 15.054247,
        "title_raw": "CUSTOMER INSIGHT ANALYST",
        "url": []
      },
      {
        "body": "<!--id: 280e6623d0134c3fb890010cb8f6edcd-->Full Stack Developer / Software Engineer Posted about 1 hour ago 2318 London, England, £70000 - £80000 per annum + benefits <h5>Job Type:</h5> Permanent Managed by: Java Team Full Stack Developer / Software Engineer (Java JavaScript). Would you like to work on complex and interesting systems, gain valuable knowledge of financial trading systems and enjoy a good <span class=\"jpa-keyword-highlight\">work</span> <span class=\"jpa-keyword-highlight\">life</span> / <span class=\"jpa-keyword-highlight\">balance</span> with flexible working? You could be joining a City based trading firm on a 12 month fixed term contract. As a Full Stack Developer you will work fairly independently on a wide range of Java and JavaScript projects to support every aspect of the highly scalable real-time trading platform; from complex serverside components to JavaScript React on the frontend working across the full development lifecycle. You'll be based in an informal atmosphere in the City with a good <span class=\"jpa-keyword-highlight\">work</span> <span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>, casual dress code, bright and spacious offices with a peaceful work environment. <h5>Requirements:</h5> <ul><li>Strong object orientated Java 8 development experience </li><li>Strong JavaScript frontend experience including frameworks such as React and Redux </li><li>Good knowledge of Oracle databases, PL/SQL </li><li>Full lifecycle development experience </li><li>Collaborative with excellent communication skills As a Full Stack Developer / Software Engineer you will earn a competitive salary (to £80k; on a 12 month fixed term contract) plus benefits.</li></ul>",
        "city_name": "London, England",
        "company_name": "Client Server Limited",
        "expired": "2020-03-09",
        "id": "280e6623d0134c3fb890010cb8f6edcd",
        "posted": "2019-11-28",
        "score": 14.9483595,
        "title_raw": "Full Stack Developer / Software Engineer",
        "url": []
      },
      {
        "body": "<!--id: b13ac43575314315ba27521270602e68-->Senior Java Engineer (Consultancy <h5>WITHOUT THE TRAVEL</h5>)<ul><li>£55k RealTime Recruitment </li><li> Belfast </li><li> £45000</li><li>55000 </li><li> Permanent full-time </li><li> Updated 17/12/2019 </li><li> Conor Mullan this job is expired Apply Now Share this job × __________________________________________________ </li><li> Facebook Twitter Google Plus Email Description Senior Java Developer (Consultancy</li><li>No TRAVEL)</li><li>£55k Senior Java Developer | Free Onsite Parking | Medical Insurance | Excellent <span class=\"jpa-keyword-highlight\">Work</span></li><li>span class=\"jpa-keyword-highlight\">Life</li></ul></span> <span class=\"jpa-keyword-highlight\">Balance</span> | Training Orientated Culture | Modern Office Environment | <h5>NO TRAVEL</h5> Get to work in a consultancy environment on various projects with ZERO travel involved. They promise technically challenging work with the guarantee that you will grow and progress in your career. They boast modern office facilities, a market<ul><li>leading package and an unparalleled <span class=\"jpa-keyword-highlight\">work</span> <span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>. Why should I be interested in this Senior Java Developer role? </li><li> Market Leading Pension scheme (9%) </li><li> Free Onsite Parking </li><li> 33 days holiday </li><li> Zero Travel </li><li> Medical Insurance </li><li> Continuous social events (including family events) which run throughout the year </li><li> Microsoft discounts </li><li> Life assurance </li><li> Extraordinary <span class=\"jpa-keyword-highlight\">work</span></li><li>span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span> </li><li> Lead a team made up of incredible people </li><li> Usher a thriving native business to its next stage of growth What will I be doing as a Senior Java Developer? </li><li> Innovate & optimise existing systems for scalability, performance & reliability </li><li> Collaborate with a highly skilled team spanning architects, engineers and business owners to deliver the best results </li><li> Experiment with the latest technologies</li><li>continue to have a passion and spot the latest trends What do I need for this Senior Java Developer role? </li><li> 5+ years of hands-on Java experience </li><li> Solid design & architecture knowledge Sound interesting?</li></ul> Drop me a message or give me a call to find out more! <h5>Skills:</h5> Java 8, Spring Framework, Java Development, Java technology, Hibernate, Core Java, RESTful WebServices, Spring MVC, consultancy, senior java, belfast <h5>Benefits:</h5> Annual Bonus / 13th <h5>Cheque, Flexitime, Group Life Assurance, Performance Bonus, Pension Fund, Parking, Paid Holidays Ref:</h5> <h5>AUTO-201912171009539752</h5> Apply Now Report This Job RealTime Recruitment View Agency Profile <ul><li> Arnott House, 3rd Floor, 12-16 Bridge Street, Belfast, BT1 1LU View More Vacancies from RealTime Recruitment </li></ul><h5>EMAIL ME JOBS LIKE THIS</h5> Please enter your email address Please enter a valid email address Show More Email me jobs similar to: Senior Java Engineer (Consultancy <h5>WITHOUT THE TRAVEL</h5>)<ul><li>£55k Please enter your email address Please enter a valid email address</li></ul>",
        "city_name": "Belfast, Northern Ireland",
        "company_name": "RealTime Recruitment",
        "expired": "2020-01-17",
        "id": "b13ac43575314315ba27521270602e68",
        "posted": "2019-12-17",
        "score": 14.864116,
        "title_raw": "Senior Java Engineer (Consultancy WITHOUT THE TRAVEL) - £55k",
        "url": []
      },
      {
        "body": "<!--id: 66541396b26744ffb856dbdda44640bd-->Java Technical Lead Glasgow Lead / Senior Java Software Engineer - Greenfield Development of enterprise applications using the latest technology. Market leading salary, an excellent <span class=\"jpa-keyword-highlight\">work</span>/<span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>, excellent bonus, 27 days paid holidays (+public), family private healthcare and much much more Java 6, Ext-JS, Spring, J2EE, Tomcat/WAS, Mule ESB, MQ, jBPM, Drools, FpML, FIX, Oversight/Splunk, Selenium, Fitnesse, JUnit/Cucumber, Maven, Jenkins, ARM, GreenPlum, GemFire, Cassandra, MongoDB, Hadoop, Spark etc. Search IT are recruiting multiple, senior level Lead Software Engineers for a Glasgow based client currently investing heavilly in a technology refresh / application re-write programme. In this hands on role, you will be responsible for building and leading a team of highly skilled software engineers tasked with building the next generation applications capable of handling 150+ million transactions per day. To be successful in this role, you will be a Java Technologist with a passion for solving complex problems by producing world-class software. In return, you will be offered the opportunity to work with some of the best technologists in the county using the best technology in a physical environment designed for producing software in an Agile way. This client offer a market leading salary, an excellent <span class=\"jpa-keyword-highlight\">work</span>/<span class=\"jpa-keyword-highlight\">life</span> <span class=\"jpa-keyword-highlight\">balance</span>, excellent bonus, 27 days paid holidays (+public), family private healthcare and much much more. Apply now or call Marc Wilson on 0131 718 8045 for a confidential discussion. <h5>Job Reference:</h5> Req/336396 <h5>Closing Date:</h5> 15 September 2015",
        "city_name": "Glasgow, Scotland",
        "company_name": "Search Consultancy Group Plc",
        "expired": null,
        "id": "66541396b26744ffb856dbdda44640bd",
        "posted": "2015-09-08",
        "score": 14.795752,
        "title_raw": "Java Technical Lead",
        "url": [
          "http://www.s1jobs.com/job/it-telecommunications/architecture/glasgow/591692948.html",
          "http://www.s1jobs.com/job/it-telecommunications/software-development/glasgow/593236605.html"
        ]
      }
    ],
    "unique_postings": 1652,
    "viewable_postings": 1652
  }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="422">

Your request wasn't valid (bad keyword expression).


```json
{
  "errors": [
    {
      "status": 422,
      "title": "Invalid request content",
      "detail": "Invalid keyword search expression syntax:\n\t\"general merchandise\" OR \"apparel\" OR \"grocery\" OR\n\t                                                  ^"
    }
  ]
}
```


</div>


</div>




### `GET` <span class="from-raml uri-prefix">/postings</span>/{postingId}

Get a single posting by its id.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>postingId</code><div class="type">string</div> | Job posting id.<br>Example: `d250f05feb1b4cbdb8151c7e51052774`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/uk-jpa/postings/d250f05feb1b4cbdb8151c7e51052774",
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
    "body": "<!--id: d250f05feb1b4cbdb8151c7e51052774-->Lead Java Developer<ul><li>AWS, Microservices, Docker Recruiter Understanding Recruitment Ltd Location UK Salary Competitive Posted 27 Jun 2019 Closes 27 Jul 2019 Ref 1191238758 Sector Technology & New Media Contract Type Permanent Hours Full Time Lead Java Developer</li> ... <li> 3rd Line Support / Technical Specialist</li><li>York + York, UK + Competitive + STK iTech Ltd + 1 day ago + You need to sign in or create an account to save</ul></li>•",
    "city_name": "York",
    "company_name": "Understanding Recruitment Ltd",
    "employment_type_name": "Full-time (> 32 hours)",
    "expired": "2019-07-03",
    "id": "d250f05feb1b4cbdb8151c7e51052774",
    "max_years_experience": null,
    "min_years_experience": null,
    "posted": "2019-06-30",
    "score": 12.145,
    "skills": [
      "KS120YP719X2MH1K76LX",
      "KS1272Y6RFNZKNGWDWMB",
      "KS1220L60W8P557BJZJS",
      "KS120B874P2P6BK1MQ0T",
      "KSZX7YZWNR5IDR1I2VMZ",
      "KSY4WFI1S164RQUBSPCC",
      "KSDJCA4E89LB98JAZ7LZ",
      "KS6840J6LR0TLQ86LZJC",
      "KS7G8G66BTD4V8K3NCVF",
      "KS1265D6RGJL2Y4J6V5B",
      "KS120076FGP5WGWYMP0F",
      "KS120FG6YP8PQYYNQY9B"
    ],
    "skills_name": [
      "Behavior-Driven Development",
      "NoSQL",
      "Cloud Infrastructure",
      "Agile Software Development",
      "Microservices",
      "Docker",
      "React.js",
      "Front End (Software Engineering)",
      "Test-Driven Development (TDD)",
      "Market Research",
      "Java (Programming Language)",
      "Amazon Web Services"
    ],
    "title_name": "Java Developer",
    "url": []
  }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="404">

The facet you requested wasn't found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized facet 'foo'"
    }
  ]
}
```


</div>


</div>



## /taxonomies

Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete), or list taxonomy items.

### `GET` <span class="from-raml uri-prefix"></span>/taxonomies

Get a list of current available taxonomy facets.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/uk-jpa/taxonomies",
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
    "city",
    "company",
    "contract_type",
    "country",
    "employment_type",
    "lau1",
    "nuts1",
    "nuts3",
    "skills",
    "soc1",
    "soc2",
    "soc3",
    "soc4",
    "title"
  ]
}
```


</div>


</div>




### `GET` <span class="from-raml uri-prefix">/taxonomies</span>/{facet}

Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete).


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>facet</code><div class="type">enum</div> | Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a `q` query parameter).<br>Example: `title`<br>Must be one of: `city`, `company`, `country`, `employment_type`, `lau1`, `nuts1`, `nuts3`, `skills`, `soc1`, `soc2`, `soc3`, `soc4`, `title`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of whole or partial keywords to search for. Only when `autocomplete` is true is `q` is assumed to be a prefix. If `q` is omitted, the response will list results sorted by id of length `limit`.<br>This parameter is optional.<br>Example: `data sci`
<code>autocomplete</code><div class="type">boolean</div> | Autocomplete search terms. Only used in combination with `q`.<br><ul><li>`true` - Performs fast prefix-enabled search using only primary and, if available, alternate names (alternate names currently available for skills).</li><li>`false` - Performs more extensive search using name(s).</li></ul><br>This parameter is optional.<br>Default: `true`
<code>limit</code><div class="type">integer</div> | How many search results to return.<br>This parameter is optional.<br>Minimum: `1`<br>Maximum: `10000`<br>Default: `10`
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/uk-jpa/taxonomies/title",
  "show": true,
  "headers": [
    {
      "name": "Authorization",
      "value": "Bearer <ACCESS_TOKEN>"
    }
  ],
  "queryString": [
    {
      "name": "q",
      "value": "data sci"
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
      "id": "ET3B93055220D592C8",
      "name": "Data Scientists",
      "properties": {
        "singular_name": "Data Scientist",
        "unique_postings": 2293
      },
      "score": 8.407919
    },
    {
      "id": "ETFCE878A7B95881A6",
      "name": "Data Specialists",
      "properties": {
        "singular_name": "Data Specialist",
        "unique_postings": 1683
      },
      "score": 5.7275753
    },
    {
      "id": "ET4FFD0730E6B6C21A",
      "name": "Database Specialists",
      "properties": {
        "singular_name": "Database Specialist",
        "unique_postings": 927
      },
      "score": 5.7275753
    },
    {
      "id": "ET85FAA8C1FD151D5C",
      "name": "Minimum Data Set (MDS) Nurses",
      "properties": {
        "singular_name": "Minimum Data Set (MDS) Nurse",
        "unique_postings": 821
      },
      "score": 4.0093026
    },
    {
      "id": "ETECC216EB6E8D41E0",
      "name": "Minimum Data Set (MDS) Coordinators",
      "properties": {
        "singular_name": "Minimum Data Set (MDS) Coordinator",
        "unique_postings": 764
      },
      "score": 4.0093026
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="404">

The facet you requested wasn't found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized facet 'foo'"
    }
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/taxonomies</span>/{facet}/lookup

Lookup taxonomy items by ID.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>facet</code><div class="type">enum</div> | Which taxonomy to to look up IDs in.<br>Example: `title`<br>Must be one of: `city`, `company`, `country`, `employment_type`, `lau1`, `nuts1`, `nuts3`, `skills`, `soc1`, `soc2`, `soc3`, `soc4`, `title`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>area_version</code><div class="type">enum</div> | Specify area taxonomy version to use.<br>This parameter is optional.<br>Default: `uk_area_2015`<br>Must be one of: `uk_area_2015`, `uk_area_2013_1`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    "ETEB3BB8E555C79368"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/taxonomy-lookup.schema.json",
    "type": "object",
    "properties": {
        "ids": {
            "title": "Array of taxonomy item IDs to look up",
            "description": "Invalid IDs will be dropped.\n\nMaximum number of ids: `10000`",
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ],
                "minLength": 1,
                "minimum": 0
            },
            "minItems": 1,
            "maxItems": 10000
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
  "url": "https://emsiservices.com/uk-jpa/taxonomies/title/lookup",
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
    "text": "{ \"ids\": [ \"ETEB3BB8E555C79368\" ] }"
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
      "id": "ETEB3BB8E555C79368",
      "name": "Data Scientists",
      "properties": {
        "singular_name": "Data Scientist",
        "unique_postings": 2293
      }
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
      "title": "Malformed Request",
      "detail": "Expected array"
    }
  ]
}
```


</div>


<div data-tab="404">

The facet you requested wasn't found.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "URL not found",
      "detail": "Unrecognized facet 'foo'"
    }
  ]
}
```


</div>


</div>

