# Global Job Postings 
#### v1.6.1
##### Information on past releases can be found in the [Changelog](/updates/global-job-postings-api-changelog).

## Overview

### Use case
This is an interface for retrieving global job posting data that is filtered, sorted and ranked by various properties of the job postings.

### About the data
Job postings are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

### Content type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the Global Job Postings API, you must request an OAuth bearer token with the scope `postings:global`.

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
          "value": "postings:global"
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

Most filters are associated with a particular taxonomy and have both id filters and name filters. For instance, to filter by skills you may use the
`skills` filter with skill codes or the `skills_name` filter with skill names. These filters require exact matches, including capitalization, punctuation, and
whitespace, in order to work as expected. Supported codes and/or names can be found by performing a ranking along the filter's facet (see [/rankings](#rankings) for more
details) or by searching in one of the taxonomy endpoints (see [/taxonomies](#taxonomies)).

Each taxonomy filter has both a shorthand and a verbose syntax.

1. **Shorthand**: a list of items.
  ```json
  {
    "when": {"start": "2018-01", "end": "2018-06"},
    "skills_name": ["SQL (Programming Lanague)", "C++ (Programming Language)"]
  }
  ```
  These filters match all job postings in the first 6 months of 2018 that include either one of the skills "SQL (Programming Language)" or "C++ (Programming Language)".

  This shorthand filter syntax is equivalent to the following in the verbose form:
  ```json
  {
    "when": {"start": "2018-01", "end": "2018-06"},
    "skills_name": {
      "include": ["SQL (Programming Lanague)", "C++ (Programming Language)"],
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
  (e.g., skills and education levels). Using this approach on filters that only have a single value per posting (i.e., company, occupation etc.) would always result
  in `0` matching postings.

All filters applied to a request must be true for a job posting to be included in the response. See the "Full Reference" tab under each
endpoint for the full listing of filters and metrics that can be applied to your requests.

### Glossary
The job posting metrics available in this API are listed below.

| Metric | Definition |
|------|------------|
|`unique_postings`|The number of unique (de-duplicated) monthly active job postings that match your filters. A posting is counted once for each month it is active.|
|`significance`|_This metric can only be used to rank `by` a facet in a ranking request, it cannot be used as a totals metric, or an extra ranking metric._<br>The relative concentration of each ranked item based on your filters as compared to all available postings in the filtered timeframe. Larger scores mean these ranked items occur more frequently in your filtered job postings than in all other postings in the filtered timeframe.|
|`unique_companies`|The number of unique companies represented in your filtered set of postings.|
|`median_posting_duration`|The median duration of closed job postings that match your filters. Duration is measured in days.|

## /status

Service status (health)

### `GET` <span class="from-raml uri-prefix"></span>/status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-postings/status",
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

Get info on taxonomies, available months of data, available filters and facets, etc.

### `GET` <span class="from-raml uri-prefix"></span>/meta

Get service metadata, including taxonomies, available months of data, facets, metrics, and attribution text. Caching is encouraged, but the metadata does change monthly.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-postings/meta",
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
      "2021-01",
      "2021-02",
      "2021-03",
      "2021-04",
      "2021-05"
    ],
    "facets": [
      "certifications",
      "certifications_name",
      "company",
      "company_name",
      "hard_skills",
      "hard_skills_name",
      "market",
      "market_name",
      "nation",
      "nation_name",
      "occupation",
      "occupation_name",
      "skills",
      "skills_name",
      "soft_skills",
      "soft_skills_name",
      "title",
      "title_name"
    ],
    "filters": [
      "company",
      "company_is_staffing",
      "company_name",
      "market",
      "market_name",
      "nation",
      "nation_name",
      "occupation",
      "occupation_name",
      "posting_duration",
      "posting_duration.lower_bound",
      "posting_duration.upper_bound",
      "skills",
      "skills_name",
      "title",
      "title_name",
      "when",
      "when.end",
      "when.start",
      "when.type"
    ],
    "latest_day": "2021-05-31",
    "metrics": [
      "median_posting_duration",
      "significance",
      "unique_companies",
      "unique_postings"
    ],
    "nation_start_month": {
      "ARG": "2020-08",
      "AUS": "2020-09",
      "AUT": "2019-01",
      "BEL": "2019-01",
      "CAN": "2019-01",
      "CHE": "2020-08",
      "COL": "2020-08",
      "DEU": "2019-01",
      "ESP": "2019-01",
      "FRA": "2019-01",
      "GBR": "2019-01",
      "HKG": "2020-08",
      "IRL": "2020-09",
      "ITA": "2019-01",
      "NIR": "2019-01",
      "NLD": "2019-01",
      "NZL": "2020-08",
      "SGP": "2020-04",
      "USA": "2019-01",
      "ZAF": "2020-09"
    },
    "supportsAdvancedFilters": true,
    "taxonomies": {
      "area_global": "global_area_v1",
      "company": "acme_v1.21",
      "occupation_global": "global_occ_v1",
      "skills": "skillsv7.40",
      "title": "emsi_title_v4.13"
    },
    "version": null
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


</div>



## /totals

Get summary metrics on all postings matching the filters.

### `POST` <span class="from-raml uri-prefix"></span>/totals






#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2019-03",
      "end": "2019-06"
    },
    "skills": [
      "KS123X777H5WFNXQ6BPM"
    ]
  },
  "metrics": [
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
                    "description": "Job posting time frame filter, can be `\"active\"` (except for the timeseries endpoints) to match all currently active postings, or a more granular time frame object detailed below.",
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
                            "example": "2018-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2019-06"
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
                "market": {
                    "title": "Filter by market ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR_M_001"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "market_name": {
                    "title": "Filter by market names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation": {
                    "title": "Filter by nation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation_name": {
                    "title": "Filter by nation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Great Britain"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation": {
                    "title": "Filter by occupation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "e41b"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation_name": {
                    "title": "Filter by occupation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Retail Sales Workers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "title": "Filter by normalized company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "ET6850661D6AE5FA86"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "Software Engineers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 0,
                            "type": "integer",
                            "minimum": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 30,
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "additionalProperties": false
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
                    "unique_companies",
                    "median_posting_duration"
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
  "url": "https://emsiservices.com/global-postings/totals",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2019-03\", \"end\": \"2019-06\" }, \"skills\": [ \"KS123X777H5WFNXQ6BPM\" ] }, \"metrics\": [ \"unique_postings\", \"median_posting_duration\" ] }"
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
      "median_posting_duration": null,
      "unique_postings": 17
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


</div>



## /timeseries

Get summary metrics just like the [/totals](#totals) endpoint but broken out by month or day. Use `YYYY-MM` date format in the time-frame filter, `when`, to get monthly summary, or use `YYYY-MM-DD` date format for daily summary data. When requesting a daily timeseries only up to 90 days may be requested at a time. Months or days with 0 postings will be included in the response.

`median_posting_duration` metric is not available by timeseries to avoid biased results.


### `POST` <span class="from-raml uri-prefix"></span>/timeseries






#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2019-05",
      "end": "2019-06",
      "type": "posted"
    }
  },
  "metrics": [
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
                    "description": "Job posting time frame filter, can be `\"active\"` (except for the timeseries endpoints) to match all currently active postings, or a more granular time frame object detailed below.",
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
                            "example": "2018-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2019-06"
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
                "market": {
                    "title": "Filter by market ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR_M_001"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "market_name": {
                    "title": "Filter by market names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation": {
                    "title": "Filter by nation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation_name": {
                    "title": "Filter by nation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Great Britain"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation": {
                    "title": "Filter by occupation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "e41b"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation_name": {
                    "title": "Filter by occupation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Retail Sales Workers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "title": "Filter by normalized company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "ET6850661D6AE5FA86"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "Software Engineers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 0,
                            "type": "integer",
                            "minimum": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 30,
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "additionalProperties": false
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
                    "unique_companies"
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
  "url": "https://emsiservices.com/global-postings/timeseries",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2019-05\", \"end\": \"2019-06\", \"type\": \"posted\" } }, \"metrics\": [ \"unique_postings\" ] }"
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
        "2019-05",
        "2019-06"
      ],
      "unique_postings": [
        0,
        100
      ]
    },
    "totals": {
      "unique_postings": 100
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


</div>



## /rankings

Group and rank postings by available facets.

### `GET` <span class="from-raml uri-prefix"></span>/rankings

Get a list of current available ranking facets.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-postings/rankings",
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
    "company",
    "company_name",
    "hard_skills",
    "hard_skills_name",
    "market",
    "market_name",
    "nation",
    "nation_name",
    "occupation",
    "occupation_name",
    "skills",
    "skills_name",
    "soft_skills",
    "soft_skills_name"
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
<code>rankingFacet</code><div class="type">enum</div> | Example: `company`<br>Must be one of: `company`, `company_name`, `market`, `market_name`, `nation`, `nation_name`, `occupation`, `occupation_name`, `skills`, `skills_name`, `hard_skills`, `hard_skills_name`, `soft_skills`, `soft_skills_name`, `certifications`, `certifications_name`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2019-03",
      "end": "2019-06",
      "type": "expired"
    }
  },
  "rank": {
    "by": "unique_postings",
    "limit": 10,
    "extra_metrics": [
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
                    "description": "Job posting time frame filter, can be `\"active\"` (except for the timeseries endpoints) to match all currently active postings, or a more granular time frame object detailed below.",
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
                            "example": "2018-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2019-06"
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
                "market": {
                    "title": "Filter by market ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR_M_001"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "market_name": {
                    "title": "Filter by market names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation": {
                    "title": "Filter by nation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation_name": {
                    "title": "Filter by nation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Great Britain"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation": {
                    "title": "Filter by occupation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "e41b"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation_name": {
                    "title": "Filter by occupation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Retail Sales Workers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "title": "Filter by normalized company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "ET6850661D6AE5FA86"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "Software Engineers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 0,
                            "type": "integer",
                            "minimum": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 30,
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "additionalProperties": false
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
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to the 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "unique_companies",
                            "median_posting_duration"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by the number of unique postings for each item",
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
  "url": "https://emsiservices.com/global-postings/rankings/company",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2019-03\", \"end\": \"2019-06\", \"type\": \"expired\" } }, \"rank\": { \"by\": \"unique_postings\", \"limit\": 10, \"extra_metrics\": [ \"median_posting_duration\" ] } }"
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
          "median_posting_duration": 3,
          "name": "875822de2984cf06301a",
          "unique_postings": 1
        }
      ],
      "facet": "company",
      "limit": 10,
      "rank_by": "unique_postings"
    },
    "totals": {
      "median_posting_duration": 3,
      "unique_postings": 1
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


</div>




### `POST` <span class="from-raml uri-prefix">/rankings/{rankingFacet}</span>/timeseries

Group and rank postings by {ranking_facet} with a monthly or daily timeseries for each ranked group. Use `YYYY-MM` date format in the timeseries time-frame filter, `timeseries.when`, to get monthly summary of each ranked group, or use `YYYY-MM-DD` date format for daily summary.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>rankingFacet</code><div class="type">enum</div> | Example: `company`<br>Must be one of: `company`, `company_name`, `market`, `market_name`, `nation`, `nation_name`, `occupation`, `occupation_name`, `skills`, `skills_name`, `hard_skills`, `hard_skills_name`, `soft_skills`, `soft_skills_name`, `certifications`, `certifications_name`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2019-03",
      "end": "2019-06",
      "type": "active"
    }
  },
  "rank": {
    "by": "unique_postings",
    "limit": 5
  },
  "timeseries": {
    "metrics": [
      "unique_postings"
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
                    "description": "Job posting time frame filter, can be `\"active\"` (except for the timeseries endpoints) to match all currently active postings, or a more granular time frame object detailed below.",
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
                            "example": "2018-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2019-06"
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
                "market": {
                    "title": "Filter by market ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR_M_001"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "market_name": {
                    "title": "Filter by market names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation": {
                    "title": "Filter by nation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation_name": {
                    "title": "Filter by nation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Great Britain"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation": {
                    "title": "Filter by occupation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "e41b"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation_name": {
                    "title": "Filter by occupation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Retail Sales Workers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "title": "Filter by normalized company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "ET6850661D6AE5FA86"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "Software Engineers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 0,
                            "type": "integer",
                            "minimum": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 30,
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "additionalProperties": false
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
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to the 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "unique_companies",
                            "median_posting_duration"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by the number of unique postings for each item",
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
            "title": "Choose metrics and adjusted time frames for a ranked time series",
            "type": "object",
            "properties": {
                "when": {
                    "title": "Filter postings by time",
                    "description": "Job posting time frame filter, can be `\"active\"` (except for the timeseries endpoints) to match all currently active postings, or a more granular time frame object detailed below.",
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
                            "example": "2018-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2019-06"
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
                            "unique_companies"
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
  "url": "https://emsiservices.com/global-postings/rankings/company/timeseries",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2019-03\", \"end\": \"2019-06\", \"type\": \"active\" } }, \"rank\": { \"by\": \"unique_postings\", \"limit\": 5 }, \"timeseries\": { \"metrics\": [ \"unique_postings\" ] } }"
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
          "name": "1ceab64396ffde137f81",
          "timeseries": {
            "month": [
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "unique_postings": [
              3,
              5,
              1,
              2
            ]
          },
          "unique_postings": 11
        },
        {
          "name": "35ac4f47bcc32d134aa6",
          "timeseries": {
            "month": [
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "unique_postings": [
              1,
              3,
              3,
              2
            ]
          },
          "unique_postings": 9
        },
        {
          "name": "d6ff076c42e0e2b05fd3",
          "timeseries": {
            "month": [
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "unique_postings": [
              4,
              0,
              3,
              2
            ]
          },
          "unique_postings": 9
        },
        {
          "name": "f54720fc83a5af82abf9",
          "timeseries": {
            "month": [
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "unique_postings": [
              0,
              2,
              4,
              2
            ]
          },
          "unique_postings": 8
        },
        {
          "name": "01bec3d5d77363154548",
          "timeseries": {
            "month": [
              "2019-03",
              "2019-04",
              "2019-05",
              "2019-06"
            ],
            "unique_postings": [
              6,
              0,
              1,
              1
            ]
          },
          "unique_postings": 7
        }
      ],
      "facet": "company",
      "limit": 5,
      "rank_by": "unique_postings"
    },
    "totals": {
      "unique_postings": 100
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


</div>




### `POST` <span class="from-raml uri-prefix">/rankings/{rankingFacet}</span>/rankings/{nestedRankingFacet}

Get a nested ranking (e.g. top companies, then top skills per company).


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>rankingFacet</code><div class="type">enum</div> | Example: `company`<br>Must be one of: `company`, `company_name`, `market`, `market_name`, `nation`, `nation_name`, `occupation`, `occupation_name`, `skills`, `skills_name`, `hard_skills`, `hard_skills_name`, `soft_skills`, `soft_skills_name`, `certifications`, `certifications_name`
<code>nestedRankingFacet</code><div class="type">enum</div> | Example: `company`<br>Must be one of: `company`, `company_name`, `market`, `market_name`, `nation`, `nation_name`, `occupation`, `occupation_name`, `skills`, `skills_name`, `hard_skills`, `hard_skills_name`, `soft_skills`, `soft_skills_name`, `certifications`, `certifications_name`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "when": {
      "start": "2019-03",
      "end": "2019-06",
      "type": "active"
    }
  },
  "rank": {
    "by": "unique_postings",
    "limit": 5,
    "extra_metrics": [
      "median_posting_duration"
    ]
  },
  "nested_rank": {
    "by": "significance",
    "min_unique_postings": 1,
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
                    "description": "Job posting time frame filter, can be `\"active\"` (except for the timeseries endpoints) to match all currently active postings, or a more granular time frame object detailed below.",
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
                            "example": "2018-06"
                        },
                        "end": {
                            "title": "Filter to postings before this date (inclusive)",
                            "description": "The end of a date range, an ISO-8061 year-month or year-month-day date format.",
                            "type": "string",
                            "pattern": "^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$",
                            "example": "2019-06"
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
                "market": {
                    "title": "Filter by market ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR_M_001"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "market_name": {
                    "title": "Filter by market names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation": {
                    "title": "Filter by nation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "GBR"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "nation_name": {
                    "title": "Filter by nation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Great Britain"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation": {
                    "title": "Filter by occupation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "e41b"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "occupation_name": {
                    "title": "Filter by occupation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Retail Sales Workers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "title": "Filter by normalized company names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "ET6850661D6AE5FA86"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                        "Software Engineers"
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
                            "description": "Logical operator used when scanning job postings for inclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                            "description": "Logical operator used when scanning job postings for exclusive filtering; whether to filter for postings matching any of the given values (`or`) or all of the given values (`and`).<br>Default: `\"or\"`",
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
                "posting_duration": {
                    "title": "Filter postings by how long they were active",
                    "description": "This filter operates on the number of days a posting has been active. This filter differs from the 'posting_duration' metric in that it will take into account currently active posting durations, where the metric only calculates duration of expired postings.",
                    "type": "object",
                    "properties": {
                        "lower_bound": {
                            "title": "Lower bound for posting duration",
                            "description": "Lower bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 0,
                            "type": "integer",
                            "minimum": 0
                        },
                        "upper_bound": {
                            "title": "Upper bound for posting duration",
                            "description": "Upper bound for the number of days a posting has been active for (days are inclusive).",
                            "example": 30,
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "additionalProperties": false
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
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to the 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "unique_companies",
                            "median_posting_duration"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by the number of unique postings for each item",
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
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a limit of `0`) are not valid for job companies, skills, and certifications facets. Additional maximum limits:\n* Nested rankings: `100`",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to the 'by' metric, calculate these metrics for each ranked group. The `median_posting_duration` metric only applies to closed job postings. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "unique_postings"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "unique_postings",
                            "unique_companies",
                            "median_posting_duration"
                        ]
                    },
                    "minItems": 1
                },
                "min_unique_postings": {
                    "title": "Filter ranked items by the number of unique postings for each item",
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
  "url": "https://emsiservices.com/global-postings/rankings/company/rankings/company",
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
    "text": "{ \"filter\": { \"when\": { \"start\": \"2019-03\", \"end\": \"2019-06\", \"type\": \"active\" } }, \"rank\": { \"by\": \"unique_postings\", \"limit\": 5, \"extra_metrics\": [ \"median_posting_duration\" ] }, \"nested_rank\": { \"by\": \"significance\", \"min_unique_postings\": 1, \"limit\": 5 } }"
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
          "median_posting_duration": null,
          "name": "1ceab64396ffde137f81",
          "ranking": {
            "buckets": [
              {
                "name": "1ceab64396ffde137f81",
                "significance": 24.5,
                "unique_postings": 2
              }
            ],
            "facet": "company",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 2
        },
        {
          "median_posting_duration": null,
          "name": "35ac4f47bcc32d134aa6",
          "ranking": {
            "buckets": [
              {
                "name": "35ac4f47bcc32d134aa6",
                "significance": 49,
                "unique_postings": 2
              }
            ],
            "facet": "company",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 2
        },
        {
          "median_posting_duration": null,
          "name": "d6ff076c42e0e2b05fd3",
          "ranking": {
            "buckets": [
              {
                "name": "d6ff076c42e0e2b05fd3",
                "significance": 49,
                "unique_postings": 2
              }
            ],
            "facet": "company",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 2
        },
        {
          "median_posting_duration": null,
          "name": "f54720fc83a5af82abf9",
          "ranking": {
            "buckets": [
              {
                "name": "f54720fc83a5af82abf9",
                "significance": 49,
                "unique_postings": 2
              }
            ],
            "facet": "company",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 2
        },
        {
          "median_posting_duration": null,
          "name": "01bec3d5d77363154548",
          "ranking": {
            "buckets": [
              {
                "name": "01bec3d5d77363154548",
                "significance": 50,
                "unique_postings": 1
              }
            ],
            "facet": "company",
            "limit": 5,
            "rank_by": "significance"
          },
          "unique_postings": 1
        }
      ],
      "facet": "company",
      "limit": 5,
      "rank_by": "unique_postings"
    },
    "totals": {
      "median_posting_duration": 3,
      "unique_postings": 100
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


</div>



## /taxonomies

Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete), or list taxonomy items.

### `GET` <span class="from-raml uri-prefix"></span>/taxonomies

Get a list of current available taxonomy facets.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-postings/taxonomies",
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
    "company",
    "market",
    "nation",
    "occupation",
    "skills"
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
<code>facet</code><div class="type">string</div> | Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a `q` query parameter).<br>Example: `occupation`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of whole or partial keywords to search for. Only when `autocomplete` is true is `q` is assumed to be a prefix. If `q` is omitted, the response will list results sorted by id of length `limit`.<br>This parameter is optional.<br>Example: `Analysts`
<code>autocomplete</code><div class="type">boolean</div> | Autocomplete search terms. Only used in combination with `q`.<br><ul><li>`true` - Performs fast prefix-enabled search using only primary and, if available, alternate names (alternate names currently available for skills).</li><li>`false` - Performs more extensive search using both name(s) and, if available, description (description currently only available for NOC search).</li></ul><br>This parameter is optional.<br>Default: `true`
<code>limit</code><div class="type">integer</div> | How many search results to return.<br>This parameter is optional.<br>Minimum: `1`<br>Maximum: `10000`<br>Default: `10`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-postings/taxonomies/occupation",
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
      "value": "Analysts"
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
      "id": "e15b",
      "name": "Analysts and Data Scientists",
      "score": 8.110737
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

Look up taxonomy items by ID.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>facet</code><div class="type">string</div> | Which taxonomy to look up IDs in.<br>Example: `occupation`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    "e15b"
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
  "url": "https://emsiservices.com/global-postings/taxonomies/occupation/lookup",
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
    "text": "{ \"ids\": [ \"e15b\" ] }"
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
      "id": "e15b",
      "name": "Analysts and Data Scientists"
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

