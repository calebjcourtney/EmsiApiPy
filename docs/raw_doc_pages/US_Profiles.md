# Aggregate Profiles 
#### v1.15.2
##### Information on past releases can be found in the [Changelog](/updates/aggregate-profile-data-api-changelog).

## Overview

### Use case
This is an interface for retrieving aggregated Emsi profile data that is filtered, sorted and ranked by various properties of the profiles.

### About the data
Profiles are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

### Content Type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the US Profiles API, you must request an OAuth bearer token with the scope `profiles:us`.

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
          "value": "profiles:us"
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
All data endpoints have an extensive filter request property allowing you to filter profiles down to specific subsets for analysis. A list of all of the available facets, filters, and metrics can be found in the [/meta](#meta) endpoint.

Most filters are associated with a particular taxonomy and have both id filters and name filters. For instance, to filter by job title you may use the
`title` filter with job title codes or the `title_name` filter with job title names. These filters require exact matches, including capitalization, punctuation, and
whitespace, in order to work as expected. Supported codes and/or names can be found by performing a ranking along the filter's facet (see [/rankings](#rankings) for more
details) or by searching in one of the taxonomy endpoints (see [/taxonomies](#taxonomies)).

Each taxonomy filter has both a shorthand and a verbose syntax.

1. **Shorthand**: a list of items.
  ```json
  {
    "title_name": ["Data Scientist", "Computer Scientist"]
  }
  ```
  These filters match all profiles that include either one of the job titles "Data Scientist" or "Computer Scientist".

  This shorthand filter syntax is equivalent to the following in the verbose form:
  ```json
  {
    "title_name": {
      "include": ["Data Scientist", "Computer Scientist"],
      "include_op": "or"
    }
  }
  ```

2. **Verbose**: an object defining inclusive/exclusive items and optional operators defining how to match those items in a profile.
  ```json
  {
    "skills_name": {
      "include": ["SQL (Programming Lanague)", "C++ (Programming Language)"],
      "include_op": "and",
      "exclude": ["Java (Programming Language)", "C Sharp (Programming Language)"],
      "exclude_op": "or"
    }
  }
  ```
  These filters match all profiles that mention both SQL and C++ skills while not mention Java or C# skills.

  **Note:** the `include_op` and `exclude_op` fields apply to `include` and `exclude` fields respectively, they default to `or` if unspecified.
  * `and` – match profiles that include/exclude all items in the list
  * `or` – match profiles that include/exclude any of the items in the list

  Combining multiple values in the `include`/`exclude` fields of a filter with an `and` operator currently is only useful for filters that have multiple values per profile
  (e.g., skills and certifications). Using this approach on filters that only have a single value per profile (i.e., company, occupation, job title, etc.) would always result
  in `0` matching profiles.

  **Note:** the `include_op` and `exclude_op` fields can only be used with an `or` operator on the `educations` filter.

All filters applied to a request must be true for a profile to be included in the response. See the "Full Reference" tab under each
endpoint for the full listing of filters and metrics that can be applied to your requests.

### Glossary

#### profiles
The number of profiles that match your filters.

#### unique_schools
The number of unique schools represented in your filtered set of profiles.

#### unique_companies
The number of unique companies represented in your filtered set of profiles.

#### significance
The relative concentration of each ranked/faceted item based on your filters as compared to all available profiles in the filtered timeframe. Positive scores mean these ranked/faceted items occur more frequently in your filtered profiles than in all other profiles.

## /status

Service status (health).

### `GET` <span class="from-raml uri-prefix"></span>/status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/profiles/status",
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

Get info on taxonomies, available data years, and attribution.

### `GET` <span class="from-raml uri-prefix"></span>/meta

Get service metadata, including taxonomies, available years of data (first and last year in which any available profiles were updated), and attribution text. Caching is encouraged, but the metadata may change weekly.



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/profiles/meta",
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
      "body": "Emsi profiles are collected from various public online sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography. Emsi performs additional filtering and processing to improve compatibility with Emsi data.",
      "title": "Emsi Profiles"
    },
    "earliest_year": "2000",
    "facets": [
      "certifications",
      "certifications_name",
      "cip2",
      "cip2_name",
      "cip4",
      "cip4_name",
      "cip6",
      "cip6_name",
      "city",
      "city_name",
      "company",
      "company_name",
      "county",
      "edulevels",
      "edulevels_name",
      "fips",
      "hard_skills",
      "hard_skills_name",
      "msa",
      "naics2",
      "naics3",
      "naics4",
      "naics5",
      "naics6",
      "onet",
      "schools",
      "schools_ipeds",
      "schools_name",
      "skills",
      "skills_name",
      "soc2",
      "soc3",
      "soc4",
      "soc5",
      "soft_skills",
      "soft_skills_name",
      "state",
      "title",
      "title_name"
    ],
    "filters": [
      "city",
      "city_name",
      "company",
      "company_name",
      "county",
      "educations",
      "educations.cip2",
      "educations.cip2_name",
      "educations.cip4",
      "educations.cip4_name",
      "educations.cip6",
      "educations.cip6_name",
      "educations.edulevels",
      "educations.edulevels_name",
      "educations.schools",
      "educations.schools_ipeds",
      "educations.schools_name",
      "fips",
      "keywords",
      "keywords.current_job_only",
      "keywords.query",
      "last_updated",
      "last_updated.end",
      "last_updated.start",
      "msa",
      "naics2",
      "naics3",
      "naics4",
      "naics5",
      "naics6",
      "onet",
      "skills",
      "skills_name",
      "soc2",
      "soc3",
      "soc4",
      "soc5",
      "state",
      "title",
      "title_name"
    ],
    "latest_year": "2021",
    "metrics": [
      "profiles",
      "significance",
      "unique_companies",
      "unique_schools"
    ],
    "supportsAdvancedFilters": true,
    "taxonomies": {
      "area": "us_area_2021_2",
      "cip": "cip2010",
      "company": "company",
      "industry": "naics_std_2017",
      "onet": "onet25_emsi",
      "skills": "skillsv7.50",
      "soc": "soc_emsi_2019",
      "title": "emsi_title_v4.23"
    },
    "taxonomy_versions": {
      "cip": [
        "cip2010",
        "cip2020"
      ],
      "company": [
        "company",
        "emsi_company"
      ],
      "soc": [
        "soc_emsi_2019",
        "soc_emsi_2017"
      ],
      "title": [
        "emsi"
      ]
    }
  }
}
```


</div>


</div>



## /totals

Get summary metrics on all profiles matching the filters.

### `POST` <span class="from-raml uri-prefix"></span>/totals





#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "last_updated": {
      "start": "2020"
    },
    "company_name": [
      "Intel Corporation"
    ],
    "skills_name": {
      "include": [
        "C++ (Programming Language)"
      ],
      "exclude": [
        "R (Programming Language)"
      ]
    }
  },
  "metrics": [
    "profiles",
    "unique_schools"
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
            "title": "Add filters to your profiles query",
            "type": "object",
            "properties": {
                "last_updated": {
                    "title": "Filter profiles by the date they were last updated",
                    "type": "object",
                    "properties": {
                        "start": {
                            "title": "Filter to profiles after this date (inclusive)",
                            "description": "Minimum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2018-10-04"
                        },
                        "end": {
                            "title": "Filter to profiles before this date (inclusive)",
                            "description": "Maximum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2019-04-05"
                        }
                    },
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "ChIJ0WHAIi0hoFQRbK3q5g0V_T4"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Moscow, ID"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "county": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "fips": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "educations": {
                    "title": "Filter by educational credentials",
                    "description": "An object or list of objects describing educational credentials. Educations in a list will be ANDed together, fields within an education object will be ANDed together, values in an education field will be ORed together.\n\nMinimum educations: `1`\n\nMaximum educations: `10`\n\n*Example: Find profiles which have a Masters from Yale or Harvard and a Doctorate from Stanford*\n\n```json\n{\n\t\"filter\": {\n\t\t\"educations\": [\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Yale University\",\n\t\t\t\t\t\"Harvard University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Master's Degree\"\n\t\t\t\t]\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Stanford University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Doctorate\"\n\t\t\t\t]\n\t\t\t}\n\t\t]\n\t}\n}\n```",
                    "type": [
                        "object",
                        "array"
                    ],
                    "properties": {
                        "schools": {
                            "title": "Filter by school ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "53bff579e4b04710d09fde45"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_name": {
                            "title": "Filter by school names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "University of Idaho"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_ipeds": {
                            "title": "Filter by school ipeds ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "214777"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6": {
                            "title": "Filter by 6-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.1302"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6_name": {
                            "title": "Filter by 6-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Creative Writing"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4": {
                            "title": "Filter by 4-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.13"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4_name": {
                            "title": "Filter by 4-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Rhetoric and Composition/Writing Studies"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2": {
                            "title": "Filter by 2-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2_name": {
                            "title": "Filter by 2-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "English Language and Literature/Letters"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels": {
                            "title": "Filter by normalized education level codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "CE3211"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels_name": {
                            "title": "Filter by normalized education level names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Doctorate"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        }
                    },
                    "additionalProperties": false,
                    "items": {
                        "description": "An object describing a single educational credential.",
                        "type": "object",
                        "properties": {
                            "schools": {
                                "title": "Filter by school ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "53bff579e4b04710d09fde45"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_name": {
                                "title": "Filter by school names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "University of Idaho"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_ipeds": {
                                "title": "Filter by school ipeds ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "214777"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6": {
                                "title": "Filter by 6-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.1302"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6_name": {
                                "title": "Filter by 6-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Creative Writing"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4": {
                                "title": "Filter by 4-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.13"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4_name": {
                                "title": "Filter by 4-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Rhetoric and Composition/Writing Studies"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2": {
                                "title": "Filter by 2-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2_name": {
                                "title": "Filter by 2-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "English Language and Literature/Letters"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels": {
                                "title": "Filter by normalized education level codes",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "CE3211"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels_name": {
                                "title": "Filter by normalized education level names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Doctorate"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            }
                        },
                        "additionalProperties": false
                    },
                    "minItems": 1,
                    "maxItems": 10
                },
                "msa": {
                    "title": "Filter by Emsi MSA codes (metro or micro)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "10180"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "state": {
                    "title": "Filter by 2-digit state fips",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "36"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "15.11"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Web Developers"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "onet": {
                    "title": "Filter by Emsi O*NET codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "29-1141.00"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 2 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-0000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 3 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 4 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1010"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "soc5": {
                    "title": "Filter by Emsi level 5 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1011"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics2": {
                    "title": "Filter by normalized 2-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "31"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics3": {
                    "title": "Filter by normalized 3-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics4": {
                    "title": "Filter by normalized 4-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "3341"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics5": {
                    "title": "Filter by normalized 5-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "33411"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics6": {
                    "title": "Filter by normalized 6-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334111"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "SQL (Programming Language)"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "keywords": {
                    "title": "Filter by keyword",
                    "description": "Keyword search expression filter for keywords in additional profile text. Does NOT search standardized fields like company name, school name, or standard skills.",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter profiles",
                            "description": "Keyword search expression with boolean operators (all-caps `AND`, `OR`, `NOT`), parentheses, and double-quoted phrases allowed.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match profiles that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "type": "string",
                            "example": "workday AND \"payroll processing\"",
                            "minLength": 1
                        },
                        "current_job_only": {
                            "title": "Type of keyword search to run",
                            "description": "If `true`, search only most recent job title/description text plus any non-standardized skill keywords. Otherwise, include education and job history text as well.",
                            "type": "boolean",
                            "default": false
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                }
            },
            "additionalProperties": false
        },
        "metrics": {
            "title": "Metrics to include in the summary",
            "description": "Some metrics may be approximations for performance reasons.",
            "default": [
                "profiles"
            ],
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "profiles",
                    "unique_schools",
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
  "url": "https://emsiservices.com/profiles/totals",
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
    "text": "{ \"filter\": { \"last_updated\": { \"start\": \"2020\" }, \"company_name\": [ \"Intel Corporation\" ], \"skills_name\": { \"include\": [ \"C++ (Programming Language)\" ], \"exclude\": [ \"R (Programming Language)\" ] } }, \"metrics\": [ \"profiles\", \"unique_schools\" ] }"
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
      "profiles": 8448,
      "unique_schools": 2117
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



## /recency

Group filtered profile metrics by year, based on profile recency (when they were last updated).


### `POST` <span class="from-raml uri-prefix"></span>/recency





#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "last_updated": {
      "start": "2019"
    },
    "onet": [
      "17-2071.00"
    ],
    "skills_name": {
      "include": [
        "C++ (Programming Language)"
      ]
    },
    "educations": {
      "schools_name": [
        "Stanford University"
      ]
    }
  },
  "metrics": [
    "profiles",
    "unique_schools"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/recency.schema.json",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your profiles query",
            "type": "object",
            "properties": {
                "last_updated": {
                    "title": "Filter profiles by the date they were last updated",
                    "type": "object",
                    "properties": {
                        "start": {
                            "title": "Filter to profiles after this date (inclusive)",
                            "description": "Minimum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2018-10-04"
                        },
                        "end": {
                            "title": "Filter to profiles before this date (inclusive)",
                            "description": "Maximum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2019-04-05"
                        }
                    },
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "ChIJ0WHAIi0hoFQRbK3q5g0V_T4"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Moscow, ID"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "county": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "fips": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "educations": {
                    "title": "Filter by educational credentials",
                    "description": "An object or list of objects describing educational credentials. Educations in a list will be ANDed together, fields within an education object will be ANDed together, values in an education field will be ORed together.\n\nMinimum educations: `1`\n\nMaximum educations: `10`\n\n*Example: Find profiles which have a Masters from Yale or Harvard and a Doctorate from Stanford*\n\n```json\n{\n\t\"filter\": {\n\t\t\"educations\": [\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Yale University\",\n\t\t\t\t\t\"Harvard University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Master's Degree\"\n\t\t\t\t]\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Stanford University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Doctorate\"\n\t\t\t\t]\n\t\t\t}\n\t\t]\n\t}\n}\n```",
                    "type": [
                        "object",
                        "array"
                    ],
                    "properties": {
                        "schools": {
                            "title": "Filter by school ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "53bff579e4b04710d09fde45"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_name": {
                            "title": "Filter by school names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "University of Idaho"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_ipeds": {
                            "title": "Filter by school ipeds ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "214777"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6": {
                            "title": "Filter by 6-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.1302"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6_name": {
                            "title": "Filter by 6-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Creative Writing"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4": {
                            "title": "Filter by 4-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.13"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4_name": {
                            "title": "Filter by 4-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Rhetoric and Composition/Writing Studies"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2": {
                            "title": "Filter by 2-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2_name": {
                            "title": "Filter by 2-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "English Language and Literature/Letters"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels": {
                            "title": "Filter by normalized education level codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "CE3211"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels_name": {
                            "title": "Filter by normalized education level names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Doctorate"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        }
                    },
                    "additionalProperties": false,
                    "items": {
                        "description": "An object describing a single educational credential.",
                        "type": "object",
                        "properties": {
                            "schools": {
                                "title": "Filter by school ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "53bff579e4b04710d09fde45"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_name": {
                                "title": "Filter by school names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "University of Idaho"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_ipeds": {
                                "title": "Filter by school ipeds ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "214777"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6": {
                                "title": "Filter by 6-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.1302"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6_name": {
                                "title": "Filter by 6-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Creative Writing"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4": {
                                "title": "Filter by 4-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.13"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4_name": {
                                "title": "Filter by 4-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Rhetoric and Composition/Writing Studies"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2": {
                                "title": "Filter by 2-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2_name": {
                                "title": "Filter by 2-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "English Language and Literature/Letters"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels": {
                                "title": "Filter by normalized education level codes",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "CE3211"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels_name": {
                                "title": "Filter by normalized education level names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Doctorate"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            }
                        },
                        "additionalProperties": false
                    },
                    "minItems": 1,
                    "maxItems": 10
                },
                "msa": {
                    "title": "Filter by Emsi MSA codes (metro or micro)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "10180"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "state": {
                    "title": "Filter by 2-digit state fips",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "36"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "15.11"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Web Developers"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "onet": {
                    "title": "Filter by Emsi O*NET codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "29-1141.00"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 2 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-0000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 3 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 4 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1010"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "soc5": {
                    "title": "Filter by Emsi level 5 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1011"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics2": {
                    "title": "Filter by normalized 2-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "31"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics3": {
                    "title": "Filter by normalized 3-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics4": {
                    "title": "Filter by normalized 4-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "3341"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics5": {
                    "title": "Filter by normalized 5-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "33411"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics6": {
                    "title": "Filter by normalized 6-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334111"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "SQL (Programming Language)"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "keywords": {
                    "title": "Filter by keyword",
                    "description": "Keyword search expression filter for keywords in additional profile text. Does NOT search standardized fields like company name, school name, or standard skills.",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter profiles",
                            "description": "Keyword search expression with boolean operators (all-caps `AND`, `OR`, `NOT`), parentheses, and double-quoted phrases allowed.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match profiles that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "type": "string",
                            "example": "workday AND \"payroll processing\"",
                            "minLength": 1
                        },
                        "current_job_only": {
                            "title": "Type of keyword search to run",
                            "description": "If `true`, search only most recent job title/description text plus any non-standardized skill keywords. Otherwise, include education and job history text as well.",
                            "type": "boolean",
                            "default": false
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                }
            },
            "additionalProperties": false
        },
        "metrics": {
            "title": "Metrics to calculate per year",
            "default": [
                "profiles"
            ],
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "profiles",
                    "unique_schools",
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
  "url": "https://emsiservices.com/profiles/recency",
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
    "text": "{ \"filter\": { \"last_updated\": { \"start\": \"2019\" }, \"onet\": [ \"17-2071.00\" ], \"skills_name\": { \"include\": [ \"C++ (Programming Language)\" ] }, \"educations\": { \"schools_name\": [ \"Stanford University\" ] } }, \"metrics\": [ \"profiles\", \"unique_schools\" ] }"
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
    "recency": {
      "profiles": [
        0,
        8,
        144
      ],
      "unique_schools": [
        0,
        12,
        126
      ],
      "year": [
        "2019",
        "2020",
        "2021"
      ]
    },
    "totals": {
      "profiles": 152,
      "unique_schools": 126
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

Group and rank profiles by available facets.

### `GET` <span class="from-raml uri-prefix"></span>/rankings

Get a list of current available ranking facets.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/profiles/rankings",
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
    "cip2",
    "cip2_name",
    "cip4",
    "cip4_name",
    "cip6",
    "cip6_name",
    "city",
    "city_name",
    "company",
    "company_name",
    "county",
    "edulevels",
    "edulevels_name",
    "fips",
    "hard_skills",
    "hard_skills_name",
    "msa",
    "naics2",
    "naics3",
    "naics4",
    "naics5",
    "naics6",
    "onet",
    "schools",
    "schools_ipeds",
    "schools_name",
    "skills",
    "skills_name",
    "soc2",
    "soc3",
    "soc4",
    "soc5",
    "soft_skills",
    "soft_skills_name",
    "state",
    "title",
    "title_name"
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/rankings</span>/{rankingFacet}




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>rankingFacet</code><div class="type">enum</div> | Example: `city_name`<br>Must be one of: `city`, `city_name`, `county`, `fips`, `msa`, `state`, `onet`, `soc2`, `soc3`, `soc4`, `soc5`, `naics2`, `naics3`, `naics4`, `naics5`, `naics6`, `schools`, `schools_name`, `schools_ipeds`, `edulevels`, `edulevels_name`, `cip2`, `cip2_name`, `cip4`, `cip4_name`, `cip6`, `cip6_name`, `company`, `company_name`, `title`, `title_name`, `skills`, `skills_name`, `hard_skills`, `hard_skills_name`, `soft_skills`, `soft_skills_name`, `certifications`, `certifications_name`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "last_updated": {
      "start": "2018",
      "end": "2019"
    },
    "skills_name": {
      "include": [
        "C++ (Programming Language)"
      ]
    },
    "educations": {
      "schools_name": [
        "University of California, Davis"
      ]
    }
  },
  "rank": {
    "by": "profiles",
    "limit": 5,
    "extra_metrics": [
      "unique_schools"
    ],
    "min_profiles": 1
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
            "title": "Add filters to your profiles query",
            "type": "object",
            "properties": {
                "last_updated": {
                    "title": "Filter profiles by the date they were last updated",
                    "type": "object",
                    "properties": {
                        "start": {
                            "title": "Filter to profiles after this date (inclusive)",
                            "description": "Minimum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2018-10-04"
                        },
                        "end": {
                            "title": "Filter to profiles before this date (inclusive)",
                            "description": "Maximum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2019-04-05"
                        }
                    },
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "ChIJ0WHAIi0hoFQRbK3q5g0V_T4"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Moscow, ID"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "county": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "fips": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "educations": {
                    "title": "Filter by educational credentials",
                    "description": "An object or list of objects describing educational credentials. Educations in a list will be ANDed together, fields within an education object will be ANDed together, values in an education field will be ORed together.\n\nMinimum educations: `1`\n\nMaximum educations: `10`\n\n*Example: Find profiles which have a Masters from Yale or Harvard and a Doctorate from Stanford*\n\n```json\n{\n\t\"filter\": {\n\t\t\"educations\": [\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Yale University\",\n\t\t\t\t\t\"Harvard University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Master's Degree\"\n\t\t\t\t]\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Stanford University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Doctorate\"\n\t\t\t\t]\n\t\t\t}\n\t\t]\n\t}\n}\n```",
                    "type": [
                        "object",
                        "array"
                    ],
                    "properties": {
                        "schools": {
                            "title": "Filter by school ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "53bff579e4b04710d09fde45"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_name": {
                            "title": "Filter by school names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "University of Idaho"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_ipeds": {
                            "title": "Filter by school ipeds ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "214777"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6": {
                            "title": "Filter by 6-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.1302"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6_name": {
                            "title": "Filter by 6-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Creative Writing"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4": {
                            "title": "Filter by 4-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.13"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4_name": {
                            "title": "Filter by 4-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Rhetoric and Composition/Writing Studies"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2": {
                            "title": "Filter by 2-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2_name": {
                            "title": "Filter by 2-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "English Language and Literature/Letters"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels": {
                            "title": "Filter by normalized education level codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "CE3211"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels_name": {
                            "title": "Filter by normalized education level names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Doctorate"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        }
                    },
                    "additionalProperties": false,
                    "items": {
                        "description": "An object describing a single educational credential.",
                        "type": "object",
                        "properties": {
                            "schools": {
                                "title": "Filter by school ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "53bff579e4b04710d09fde45"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_name": {
                                "title": "Filter by school names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "University of Idaho"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_ipeds": {
                                "title": "Filter by school ipeds ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "214777"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6": {
                                "title": "Filter by 6-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.1302"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6_name": {
                                "title": "Filter by 6-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Creative Writing"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4": {
                                "title": "Filter by 4-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.13"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4_name": {
                                "title": "Filter by 4-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Rhetoric and Composition/Writing Studies"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2": {
                                "title": "Filter by 2-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2_name": {
                                "title": "Filter by 2-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "English Language and Literature/Letters"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels": {
                                "title": "Filter by normalized education level codes",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "CE3211"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels_name": {
                                "title": "Filter by normalized education level names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Doctorate"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            }
                        },
                        "additionalProperties": false
                    },
                    "minItems": 1,
                    "maxItems": 10
                },
                "msa": {
                    "title": "Filter by Emsi MSA codes (metro or micro)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "10180"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "state": {
                    "title": "Filter by 2-digit state fips",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "36"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "15.11"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Web Developers"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "onet": {
                    "title": "Filter by Emsi O*NET codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "29-1141.00"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 2 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-0000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 3 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 4 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1010"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "soc5": {
                    "title": "Filter by Emsi level 5 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1011"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics2": {
                    "title": "Filter by normalized 2-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "31"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics3": {
                    "title": "Filter by normalized 3-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics4": {
                    "title": "Filter by normalized 4-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "3341"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics5": {
                    "title": "Filter by normalized 5-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "33411"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics6": {
                    "title": "Filter by normalized 6-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334111"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "SQL (Programming Language)"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "keywords": {
                    "title": "Filter by keyword",
                    "description": "Keyword search expression filter for keywords in additional profile text. Does NOT search standardized fields like company name, school name, or standard skills.",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter profiles",
                            "description": "Keyword search expression with boolean operators (all-caps `AND`, `OR`, `NOT`), parentheses, and double-quoted phrases allowed.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match profiles that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "type": "string",
                            "example": "workday AND \"payroll processing\"",
                            "minLength": 1
                        },
                        "current_job_only": {
                            "title": "Type of keyword search to run",
                            "description": "If `true`, search only most recent job title/description text plus any non-standardized skill keywords. Otherwise, include education and job history text as well.",
                            "type": "boolean",
                            "default": false
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                }
            },
            "additionalProperties": false
        },
        "rank": {
            "title": "Choose how to rank your results",
            "type": "object",
            "properties": {
                "by": {
                    "title": "What metric to use to rank the ranking facet",
                    "description": "Some metrics may be approximations for performance reasons.",
                    "default": "profiles",
                    "type": "string",
                    "enum": [
                        "profiles",
                        "unique_schools",
                        "unique_companies",
                        "significance"
                    ]
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a maximum of `0`) are not valid for job titles, cities, companies, schools, skills, and certifications facets.",
                    "default": 10,
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to 'by' metric, calculate these metrics for each ranked group. Some metrics may be approximations for performance reasons.",
                    "default": [
                        "profiles"
                    ],
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "profiles",
                            "unique_schools",
                            "unique_companies"
                        ]
                    },
                    "minItems": 1
                },
                "min_profiles": {
                    "title": "Require ranked items to have this many profiles",
                    "description": "Require ranked items to have at least this many profiles matching the filter.\n\n*Default is `10` for `significance` rankings, `1` for all other rankings*",
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
  "url": "https://emsiservices.com/profiles/rankings/city_name",
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
    "text": "{ \"filter\": { \"last_updated\": { \"start\": \"2018\", \"end\": \"2019\" }, \"skills_name\": { \"include\": [ \"C++ (Programming Language)\" ] }, \"educations\": { \"schools_name\": [ \"University of California, Davis\" ] } }, \"rank\": { \"by\": \"profiles\", \"limit\": 5, \"extra_metrics\": [ \"unique_schools\" ], \"min_profiles\": 1 } }"
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
          "name": "San Francisco, CA",
          "profiles": 95,
          "unique_schools": 57
        },
        {
          "name": "Davis, CA",
          "profiles": 73,
          "unique_schools": 44
        },
        {
          "name": "Sacramento, CA",
          "profiles": 35,
          "unique_schools": 20
        },
        {
          "name": "San Jose, CA",
          "profiles": 13,
          "unique_schools": 10
        },
        {
          "name": "Los Angeles, CA",
          "profiles": 11,
          "unique_schools": 11
        },
        {
          "name": "San Diego, CA",
          "profiles": 7,
          "unique_schools": 4
        },
        {
          "name": "New York, NY",
          "profiles": 6,
          "unique_schools": 12
        },
        {
          "name": "Fremont, CA",
          "profiles": 4,
          "unique_schools": 4
        },
        {
          "name": "Campbell, CA",
          "profiles": 3,
          "unique_schools": 3
        },
        {
          "name": "Castro Valley, CA",
          "profiles": 3,
          "unique_schools": 2
        },
        {
          "name": "Milpitas, CA",
          "profiles": 3,
          "unique_schools": 1
        },
        {
          "name": "Oakland, CA",
          "profiles": 3,
          "unique_schools": 4
        },
        {
          "name": "Orange, CA",
          "profiles": 3,
          "unique_schools": 9
        },
        {
          "name": "Palo Alto, CA",
          "profiles": 3,
          "unique_schools": 5
        },
        {
          "name": "Santa Clara, CA",
          "profiles": 3,
          "unique_schools": 5
        },
        {
          "name": "Washington, DC",
          "profiles": 3,
          "unique_schools": 7
        },
        {
          "name": "Berkeley, CA",
          "profiles": 2,
          "unique_schools": 4
        },
        {
          "name": "Cupertino, CA",
          "profiles": 2,
          "unique_schools": 2
        },
        {
          "name": "Dublin, CA",
          "profiles": 2,
          "unique_schools": 3
        },
        {
          "name": "Elk Grove, CA",
          "profiles": 2,
          "unique_schools": 2
        }
      ],
      "facet": "city_name",
      "limit": 20,
      "rank_by": "profiles"
    },
    "totals": {
      "profiles": 344,
      "unique_schools": 164
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


<div class="internal-only">

## /samples

**This endpoint is not included in profiles API access.**
Get a sample of individual profiles that match a set of filters.


### `POST` <span class="from-raml uri-prefix"></span>/samples





#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "last_updated": {
      "start": "2018",
      "end": "2019"
    }
  },
  "limit": 1,
  "offset": 0
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/samples.schema.json",
    "description": "*Access to this endpoint requires additional permissions. Please contact Emsi for more information.*",
    "type": "object",
    "additionalProperties": false,
    "properties": {
        "filter": {
            "title": "Add filters to your profiles query",
            "type": "object",
            "properties": {
                "last_updated": {
                    "title": "Filter profiles by the date they were last updated",
                    "type": "object",
                    "properties": {
                        "start": {
                            "title": "Filter to profiles after this date (inclusive)",
                            "description": "Minimum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2018-10-04"
                        },
                        "end": {
                            "title": "Filter to profiles before this date (inclusive)",
                            "description": "Maximum date for when any part of a person's online presence was last updated.\n\nAccepted formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`",
                            "type": [
                                "string",
                                "integer"
                            ],
                            "example": "2019-04-05"
                        }
                    },
                    "additionalProperties": false
                },
                "city": {
                    "title": "Filter by city ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "ChIJ0WHAIi0hoFQRbK3q5g0V_T4"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Moscow, ID"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "county": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "fips": {
                    "title": "Filter by Emsi county fips codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "16057"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "educations": {
                    "title": "Filter by educational credentials",
                    "description": "An object or list of objects describing educational credentials. Educations in a list will be ANDed together, fields within an education object will be ANDed together, values in an education field will be ORed together.\n\nMinimum educations: `1`\n\nMaximum educations: `10`\n\n*Example: Find profiles which have a Masters from Yale or Harvard and a Doctorate from Stanford*\n\n```json\n{\n\t\"filter\": {\n\t\t\"educations\": [\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Yale University\",\n\t\t\t\t\t\"Harvard University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Master's Degree\"\n\t\t\t\t]\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Stanford University\"\n\t\t\t\t],\n\t\t\t\t\"edulevels_name\": [\n\t\t\t\t\t\"Doctorate\"\n\t\t\t\t]\n\t\t\t}\n\t\t]\n\t}\n}\n```",
                    "type": [
                        "object",
                        "array"
                    ],
                    "properties": {
                        "schools": {
                            "title": "Filter by school ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "53bff579e4b04710d09fde45"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_name": {
                            "title": "Filter by school names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "University of Idaho"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "schools_ipeds": {
                            "title": "Filter by school ipeds ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "214777"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6": {
                            "title": "Filter by 6-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.1302"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip6_name": {
                            "title": "Filter by 6-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Creative Writing"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4": {
                            "title": "Filter by 4-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23.13"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip4_name": {
                            "title": "Filter by 4-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Rhetoric and Composition/Writing Studies"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2": {
                            "title": "Filter by 2-digit CIP ids",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "23"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "cip2_name": {
                            "title": "Filter by 2-digit CIP names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "English Language and Literature/Letters"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels": {
                            "title": "Filter by normalized education level codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "CE3211"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "edulevels_name": {
                            "title": "Filter by normalized education level names",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Doctorate"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        }
                    },
                    "additionalProperties": false,
                    "items": {
                        "description": "An object describing a single educational credential.",
                        "type": "object",
                        "properties": {
                            "schools": {
                                "title": "Filter by school ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "53bff579e4b04710d09fde45"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_name": {
                                "title": "Filter by school names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "University of Idaho"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "schools_ipeds": {
                                "title": "Filter by school ipeds ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "214777"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6": {
                                "title": "Filter by 6-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above)\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.1302"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip6_name": {
                                "title": "Filter by 6-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Creative Writing"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4": {
                                "title": "Filter by 4-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23.13"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip4_name": {
                                "title": "Filter by 4-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Rhetoric and Composition/Writing Studies"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2": {
                                "title": "Filter by 2-digit CIP ids",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "23"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "cip2_name": {
                                "title": "Filter by 2-digit CIP names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "English Language and Literature/Letters"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels": {
                                "title": "Filter by normalized education level codes",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "CE3211"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "edulevels_name": {
                                "title": "Filter by normalized education level names",
                                "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                                "type": [
                                    "array",
                                    "object"
                                ],
                                "example": [
                                    "Doctorate"
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
                                        "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                        "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            }
                        },
                        "additionalProperties": false
                    },
                    "minItems": 1,
                    "maxItems": 10
                },
                "msa": {
                    "title": "Filter by Emsi MSA codes (metro or micro)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "10180"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "state": {
                    "title": "Filter by 2-digit state fips",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "36"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "15.11"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Web Developers"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "onet": {
                    "title": "Filter by Emsi O*NET codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "29-1141.00"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 2 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-0000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 3 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1000"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by Emsi level 4 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1010"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "soc5": {
                    "title": "Filter by Emsi level 5 SOC codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "11-1011"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "title": "Filter by normalized company codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Microsoft Corporation"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics2": {
                    "title": "Filter by normalized 2-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "31"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics3": {
                    "title": "Filter by normalized 3-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics4": {
                    "title": "Filter by normalized 4-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "3341"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics5": {
                    "title": "Filter by normalized 5-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "33411"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "naics6": {
                    "title": "Filter by normalized 6-digit company NAICS 2012 codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "334111"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "KS440W865GC4VRBW6LJP"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "SQL (Programming Language)"
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
                            "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                "keywords": {
                    "title": "Filter by keyword",
                    "description": "Keyword search expression filter for keywords in additional profile text. Does NOT search standardized fields like company name, school name, or standard skills.",
                    "type": "object",
                    "properties": {
                        "query": {
                            "title": "Keyword(s) by which to filter profiles",
                            "description": "Keyword search expression with boolean operators (all-caps `AND`, `OR`, `NOT`), parentheses, and double-quoted phrases allowed.\n\nAlternatively, you can prefix a word with `-` to exclude it; e.g. `\"games Android -iOS\"` would match profiles that mention 'games' and 'Android' but exclude those that mention 'iOS'.",
                            "type": "string",
                            "example": "workday AND \"payroll processing\"",
                            "minLength": 1
                        },
                        "current_job_only": {
                            "title": "Type of keyword search to run",
                            "description": "If `true`, search only most recent job title/description text plus any non-standardized skill keywords. Otherwise, include education and job history text as well.",
                            "type": "boolean",
                            "default": false
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": false
                }
            },
            "additionalProperties": false
        },
        "limit": {
            "title": "Limit the number of ranked items returned",
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
        },
        "offset": {
            "title": "Zero based offset used for paginating sample profiles",
            "description": "Samples can only be viewed up to the 10,000th profile matching your filter (i.e. `offset + limit <= 10,000`).\n\n*Maximum number of returned profiles will always be `10,000 - limit`*",
            "type": "integer",
            "minimum": 0,
            "default": 0
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
  "url": "https://emsiservices.com/profiles/samples",
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
    "text": "{ \"filter\": { \"last_updated\": { \"start\": \"2018\", \"end\": \"2019\" } }, \"limit\": 1, \"offset\": 0 }"
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
    "profiles": 610,
    "samples": [
      {
        "acquired_timestamp": "2016-04-15",
        "city_name": "Raritan, NJ",
        "company": "068715424-Ortho-Clinical Diagnostics, Inc.",
        "company_name": "Ortho-Clinical Diagnostics, Inc.",
        "country": "US",
        "county": 34035,
        "educations": [
          {
            "cip6_name": null,
            "level_name": null,
            "field_raw": null,
            "grad_year": null,
            "level_raw": null,
            "school_id": "53bff579e4b04710d09fbd9c",
            "school_name": "Michigan Technological University",
            "school_raw": "michigan technological university"
          },
          {
            "cip6_name": null,
            "level_name": null,
            "field_raw": "engineering",
            "grad_year": null,
            "level_raw": "engineering",
            "school_id": "53bff579e4b04710d09fdac8",
            "school_name": "United States Naval Academy",
            "school_raw": "united states naval academy"
          }
        ],
        "id": "78108545-e39c-39d4-af8f-5d0d6d238e06",
        "last_updated": "2016-04-15",
        "msa": 35620,
        "naics6": 325412,
        "onet": "11-3021.00",
        "skills": [
          "KS1270N6Z7WJQ5KVN0GG",
          "KS121966TYHFTSKSFV8R",
          "KS1218C6C8TX2Y1KRN37",
          "KS121996C1P31W0YZVNF",
          "KS1282M68WL9T4YH3SLF",
          "KS1254G739VBXHP430DV",
          "KS441075WGFJJ4GRFG2Q",
          "KS1219261TYVPMGX8KVQ",
          "KS1267F6MSPN366LX7ST",
          "KS4400V6459G7LYV1X6V",
          "KS125P46YVZ3V87LP697",
          "KS1203T6J7F2P3TG6Y6K",
          "KS121T569X502KJPS0F3",
          "KS120L96KMYTDJ48NRSH",
          "KS1270P6SLFCFT476Y3R",
          "KS125ZB6BWF5RY40BH1B"
        ],
        "skills_name": [
          "New Business Development",
          "Business Process Improvement",
          "Business Analysis",
          "Strategic Management",
          "Product Management",
          "Information Management",
          "Strategic Thinking",
          "Strategic Planning",
          "Project Management",
          "Requirements Analysis",
          "Laboratory Information Management Systems",
          "Account Management",
          "Change Management",
          "Software Development",
          "New Product Development",
          "Risk Management"
        ],
        "state": 34,
        "title": "ET061A46E66D20BCC3",
        "title_name": "Chief Technology Officer (CTO)",
        "title_raw": "CTO",
        "personal_info": {
          "emails": [
            "hiro.nakamura@iamhiro.com"
          ],
          "employment_history": [
            {
              "company_name_raw": "Ortho Clinical Diagnostics",
              "description": null,
              "job_end_ym": null,
              "job_start_ym": "2015-8",
              "title_raw": "CTO"
            },
            {
              "company_name_raw": "Biomet",
              "description": "Worked to enable the IT transformational goals of the company as they moved from many legacy systems to a smaller core of modern SAP based ERP systems. In the short period of time we did data center consolidations of SAP and non-SAP systems from an acquisition and in-sourced a large and very well integrated ECC, BW, Solman, OpenText, set of systems from EMEA. Built out an SAP environment with multiple go-lives in SAP GTS, EWM, TRex,PI/PO with the B2B Add-On for EDI, BW, BPC, BOBJ, SAP HR, Pilots on ME/Mii, OpenText, Early Customer experience through Ramp-up and prod on SAP's BW on HANA on IBM pSeries. Worked to build the highest performing team I've ever had the privilege to work with and integrated them into an extremely talented & dedicated team of folks that were already in place. Truly a highlight to be associated with such great people! Worked on our integration of Biomet's systems prior to and during the acquisition by Zimmer Holdings. Helped build a successful POC of how to consolidate our new combined financials into an S/4 simple finance system using SLT from existing SAP ECC along with legacy JDE and Infor XA ERPs.",
              "job_end_ym": "2015-8",
              "job_start_ym": "2013-2",
              "title_raw": "CTO & Principal Architect"
            }
          ],
          "job_description": "",
          "name": "Hiro Nacamura",
          "names": [
            "Hiro Nacamura"
          ],
          "phones": [
            "+1 333-333-3333"
          ],
          "profile_urls": [],
          "title_raw": "CTO"
        }
      }
    ]
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


<div data-tab="403">

You don't have access to sample profiles.


```json
{
  "errors": [
    {
      "status": 403,
      "title": "Forbidden",
      "detail": "You don't have access to sample profiles."
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


</div>
<div class="internal-only">

## /transitions

Group and rank profile job transitions by available facets.

### `GET` <span class="from-raml uri-prefix"></span>/transitions

List available filters and facets for job transitions.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/profiles/transitions",
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
    "company_name",
    "naics6",
    "soc2",
    "soc5"
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/transitions</span>/{sourceFacet}/{destinationFacet}

Get a matrix of job transitions from facet to facet.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>sourceFacet</code><div class="type">enum</div> | The facet used to rank source job transitions on.<br>Example: `company_name`<br>Must be one of: `company`, `company_name`, `soc2`, `soc5`, `naics6`
<code>destinationFacet</code><div class="type">enum</div> | The facet used to rank destination job transitions on.<br>Example: `company_name`<br>Must be one of: `company`, `company_name`, `soc2`, `soc5`, `naics6`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "source": {
    "filter": {
      "company_name": [
        "Amazon.com, Inc."
      ]
    },
    "limit": 5
  },
  "destination": {
    "filter": {
      "company_name": [
        "Google Inc."
      ]
    },
    "limit": 5
  }
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "$id": "requests/transitions.schema.json",
    "properties": {
        "source": {
            "title": "Source job transition information",
            "description": "Filter and limit the jobs people come from during job transitions.",
            "type": "object",
            "properties": {
                "filter": {
                    "title": "Add job transition filters",
                    "type": "object",
                    "properties": {
                        "company": {
                            "title": "Filter by normalized company codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "title": "Filter by normalized company codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Microsoft Corporation"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "title": "Filter by Emsi level 2 SOC codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "11-0000"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "soc5": {
                            "title": "Filter by Emsi level 5 SOC codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "11-1011"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "naics6": {
                            "title": "Filter by normalized 6-digit company NAICS 2012 codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "334111"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        }
                    },
                    "additionalProperties": false
                },
                "limit": {
                    "title": "Limit then number of results returned for the facet",
                    "description": "There will always be an `_other_` field in the response, summing up all unlisted transitions.",
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100
                }
            },
            "additionalProperties": false
        },
        "destination": {
            "title": "Destination job transition information",
            "description": "Filter and limit the jobs people come from during job transitions.",
            "type": "object",
            "properties": {
                "filter": {
                    "title": "Add job transition filters",
                    "type": "object",
                    "properties": {
                        "company": {
                            "title": "Filter by normalized company codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "NC9d0d7c83-619e-46eb-ae10-7bd2876a6857"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "title": "Filter by normalized company codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "Microsoft Corporation"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                            "title": "Filter by Emsi level 2 SOC codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "11-0000"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "soc5": {
                            "title": "Filter by Emsi level 5 SOC codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above). \n\nFor version see [/meta](#meta).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "11-1011"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        "naics6": {
                            "title": "Filter by normalized 6-digit company NAICS 2012 codes",
                            "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                            "type": [
                                "array",
                                "object"
                            ],
                            "example": [
                                "334111"
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
                                    "description": "Logical operator used when scanning profiles for inclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                                    "description": "Logical operator used when scanning profiles for exclusive filtering; whether to filter for profiles matching any of the given values (`or`) or all of the given values (`and`).",
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
                        }
                    },
                    "additionalProperties": false
                },
                "limit": {
                    "title": "Limit then number of results returned for the facet",
                    "description": "There will always be an `_other_` field in the response, summing up all unlisted transitions.",
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100
                }
            },
            "additionalProperties": false
        }
    },
    "required": [
        "source",
        "destination"
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
  "url": "https://emsiservices.com/profiles/transitions/company_name/company_name",
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
    "text": "{ \"source\": { \"filter\": { \"company_name\": [ \"Amazon.com, Inc.\" ] }, \"limit\": 5 }, \"destination\": { \"filter\": { \"company_name\": [ \"Google Inc.\" ] }, \"limit\": 5 } }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">

The transitions response shows the number of job transitions between each source and
destination as a matrix under a `transitions` 2-dimensional array. All filtered sources
and destinations are listed under `source` and `destination` fields respectively, showing
the top items under their requested facet.

`source` items designate the facet names of the transition matrix rows, and `destination`
items designate the facet names of the transition matrix columns. The last item will always
be an "_other_" bucket, enumerating the count of all other transitions not represented in the
top items.



```json
{
  "data": {
    "destination": {
      "facet": "company_name",
      "items": [
        "Google Inc.",
        "_other_"
      ],
      "limit": 5
    },
    "source": {
      "facet": "company_name",
      "items": [
        "Amazon.com, Inc.",
        "_other_"
      ],
      "limit": 5
    },
    "totals": {
      "transitions": 2927
    },
    "transitions": [
      [
        2927,
        0
      ],
      [
        0,
        0
      ]
    ]
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


</div>

## /taxonomies

Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete), or list taxonomy items.

### `GET` <span class="from-raml uri-prefix"></span>/taxonomies

Get a list of current available taxonomy facets.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/profiles/taxonomies",
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
    "cip2",
    "cip4",
    "cip6",
    "city",
    "company",
    "county",
    "edulevels",
    "fips",
    "msa",
    "naics2",
    "naics3",
    "naics4",
    "naics5",
    "naics6",
    "onet",
    "schools",
    "schools_ipeds",
    "skills",
    "soc2",
    "soc3",
    "soc4",
    "soc5",
    "state",
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
<code>facet</code><div class="type">enum</div> | Which taxonomy to search for ID/name suggestions. (Cities will always have a null ID.)<br>Example: `title`<br>Must be one of: `city`, `county`, `fips`, `msa`, `state`, `onet`, `soc2`, `soc3`, `soc4`, `soc5`, `naics2`, `naics3`, `naics4`, `naics5`, `naics6`, `schools`, `cip2`, `cip4`, `cip6`, `edulevels`, `title`, `company`, `skills`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of whole or partial keywords to search for. Only when `autocomplete` is true is `q` assumed to be a prefix.<br>This parameter is optional.<br>Example: `data sci`
<code>autocomplete</code><div class="type">boolean</div> | Autocomplete search terms.<br><ul><li>`true` - Performs fast prefix-enabled search using only primary and, if available, alternate names (alternate names currently available for ONET and skills).</li><li>`false` - Performs more extensive search using both name(s) and, if available, description (description currently only available for SOC and ONET search).</li></ul><br>This parameter is optional.<br>Default: `true`
<code>limit</code><div class="type">integer</div> | How many search results to return.<br>This parameter is optional.<br>Minimum: `1`<br>Maximum: `10000`<br>Default: `10`
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
<code>company_version</code><div class="type">enum</div> | Specify company taxonomy version to use.<br>This parameter is optional.<br>Default: `company`<br>Must be one of: `company`, `emsi_company`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/profiles/taxonomies/title",
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
        "profiles": 74205,
        "singular_name": "Data Scientist"
      },
      "score": 115.72626
    },
    {
      "id": "ET66EFA7BC3A32BB32",
      "name": "Managers/Data Scientists",
      "properties": {
        "profiles": 20745,
        "singular_name": "Manager/Data Scientist"
      },
      "score": 102.61432
    },
    {
      "id": "ET3B7D691B9A3FCB65",
      "name": "Data Science Interns",
      "properties": {
        "profiles": 18368,
        "singular_name": "Data Science Intern"
      },
      "score": 98.123924
    },
    {
      "id": "ET6F4C400F82935C3E",
      "name": "Data Science Managers",
      "properties": {
        "profiles": 7863,
        "singular_name": "Data Science Manager"
      },
      "score": 93.68677
    },
    {
      "id": "ETB15B6675998124CE",
      "name": "Lead Data Scientists",
      "properties": {
        "profiles": 6377,
        "singular_name": "Lead Data Scientist"
      },
      "score": 88.615845
    },
    {
      "id": "ET8428FBC2C9F2D438",
      "name": "Directors of Data Science",
      "properties": {
        "profiles": 7306,
        "singular_name": "Director of Data Science"
      },
      "score": 87.80374
    },
    {
      "id": "ETC81FBF8B48383129",
      "name": "Clinical Data Scientists",
      "properties": {
        "profiles": 3957,
        "singular_name": "Clinical Data Scientist"
      },
      "score": 87.298096
    },
    {
      "id": "ETE22C6070B93851E0",
      "name": "Data Science Fellows",
      "properties": {
        "profiles": 5384,
        "singular_name": "Data Science Fellow"
      },
      "score": 87.09463
    },
    {
      "id": "ET486D61EA8B4CBC36",
      "name": "Data Science Consultants",
      "properties": {
        "profiles": 3569,
        "singular_name": "Data Science Consultant"
      },
      "score": 84.95645
    },
    {
      "id": "ET64F3ADF2602703BD",
      "name": "Data Science and Analytics Managers",
      "properties": {
        "profiles": 6138,
        "singular_name": "Data Science and Analytics Manager"
      },
      "score": 84.30433
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
<code>facet</code><div class="type">enum</div> | Which taxonomy to to look up IDs in.<br>Example: `title`<br>Must be one of: `city`, `county`, `fips`, `msa`, `state`, `onet`, `soc2`, `soc3`, `soc4`, `soc5`, `naics2`, `naics3`, `naics4`, `naics5`, `naics6`, `schools`, `schools_ipeds`, `cip2`, `cip4`, `cip6`, `edulevels`, `title`, `company`, `skills`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>soc_version</code><div class="type">enum</div> | Specify SOC taxonomy version to use.<br>This parameter is optional.<br>Default: `soc_emsi_2019`<br>Must be one of: `soc_emsi_2017`, `soc_emsi_2019`
<code>title_version</code><div class="type">enum</div> | Specify Job Title taxonomy version to use.<br>This parameter is optional.<br>Default: `emsi`<br>Must be one of: `emsi`
<code>cip_version</code><div class="type">enum</div> | Specify CIP taxonomy version to use.<br>This parameter is optional.<br>Default: `cip2010`<br>Must be one of: `cip2010`, `cip2020`
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
            "title": "Taxonomy facet identifiers (invalid IDs will be dropped)\n\nMinimum ids: `1`\n\nMaximum ids: `10000`\n\n",
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ],
                "minLength": 1
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
  "url": "https://emsiservices.com/profiles/taxonomies/title/lookup",
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
      "name": ".NET Developers",
      "properties": {
        "profiles": 37469,
        "singular_name": ".NET Developer"
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

