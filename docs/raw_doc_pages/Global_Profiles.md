# Global Profiles 
#### v1.10.2
##### Information on past releases can be found in the [Changelog](/updates/global-profiles-changelog).

## Overview

### Use case
This is an interface for retrieving aggregated Emsi Global Profile data that is filtered, sorted and ranked by various properties of the profiles.

### About the data
Profiles are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

### Content Type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the Global Profiles API, you must request an OAuth bearer token with the scope `profiles:global`.

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
          "value": "profiles:global"
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

#### unique_companies
The number of unique companies represented in your filtered set of profiles.

#### significance
The relative concentration of each ranked/faceted item based on your filters as compared to all available profiles. Larger scores mean these ranked/faceted items occur more frequently in your filtered profiles than in all other profiles.

## /status

Service status (health)

### `GET` <span class="from-raml uri-prefix"></span>/status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-profiles/status",
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

Get info on taxonomies and attribution.

### `GET` <span class="from-raml uri-prefix"></span>/meta

Get service metadata, including taxonomies and attribution text. Caching is encouraged, but the metadata may change weekly.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-profiles/meta",
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
      "body": "Emsi Global profiles are collected from various public online sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.",
      "title": "Emsi Global Profiles"
    },
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
      "onet",
      "onet_name",
      "schools",
      "schools_name",
      "skills",
      "skills_name",
      "soft_skills",
      "soft_skills_name",
      "title",
      "title_name"
    ],
    "filters": [
      "company",
      "company_name",
      "educations",
      "educations.schools",
      "educations.schools_name",
      "market",
      "market_name",
      "nation",
      "nation_name",
      "occupation",
      "occupation_name",
      "onet",
      "onet_name",
      "skills",
      "skills_name",
      "title",
      "title_name"
    ],
    "metrics": [
      "profiles",
      "significance",
      "unique_companies"
    ],
    "supportsAdvancedFilters": true,
    "taxonomies": {
      "area_global": "global_area_v1",
      "occupation_global": "global_occ_v1",
      "onet": "onet23_emsi",
      "skills": "skillsv7.40",
      "title": "emsi_title_v4.13"
    }
  }
}
```


</div>


</div>



## /totals

Get summary metrics on all profiles matching the filters.

### `POST` <span class="from-raml uri-prefix"></span>/totals






#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "nation": [
      "AUS"
    ],
    "skills_name": [
      "SQL (Programming Language)"
    ]
  },
  "metrics": [
    "profiles"
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
                "nation": {
                    "title": "Filter by nation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "AUS"
                    ],
                    "additionalProperties": false
                },
                "nation_name": {
                    "title": "Filter by nation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "Australia"
                    ],
                    "additionalProperties": false
                },
                "market": {
                    "title": "Filter by market ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "AUS_M_6000"
                    ],
                    "additionalProperties": false
                },
                "market_name": {
                    "title": "Filter by market names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "Detroit-Warren-Dearborn, MI"
                    ],
                    "additionalProperties": false
                },
                "occupation": {
                    "title": "Filter by occupation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "e41a"
                    ],
                    "additionalProperties": false
                },
                "occupation_name": {
                    "title": "Filter by occupation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "Sales Representatives"
                    ],
                    "additionalProperties": false
                },
                "educations": {
                    "title": "Filter by educational credentials",
                    "description": "An object or list of objects describing educational credentials. Educations in a list will be ANDed together, fields within an education object will be ANDed together, values in an education field will be ORed together.\n\nMinimum educations: `1`\n\nMaximum educations: `10`\n\n*Example: Find profiles which have a degree from Yale or Harvard*\n\n```json\n{\n\t\"filter\": {\n\t\t\"educations\": [\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Yale University\",\n\t\t\t\t\t\"Harvard University\"\n\t\t\t\t]\n\t\t\t}\n\t\t]\n\t}\n}\n```",
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
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "properties": {
                                "include": {
                                    "description": "List of values to include in the filter.",
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "minLength": 1,
                                        "__nodocs": true
                                    },
                                    "minItems": 1,
                                    "__nodocs": true
                                },
                                "exclude": {
                                    "description": "List of values to exclude from the filter.",
                                    "type": "array",
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
                                    "type": "string",
                                    "minLength": 1,
                                    "__nodocs": true
                                },
                                "minItems": 1,
                                "properties": {
                                    "include": {
                                        "description": "List of values to include in the filter.",
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "minLength": 1,
                                            "__nodocs": true
                                        },
                                        "minItems": 1,
                                        "__nodocs": true
                                    },
                                    "exclude": {
                                        "description": "List of values to exclude from the filter.",
                                        "type": "array",
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
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "29-1141.00"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
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
                "onet_name": {
                    "title": "Filter by Emsi O*NET names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Registered Nurses"
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
                    "title": "Filter by normalized company names",
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
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                "gender": {
                    "title": "Filter by gender codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "0"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
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
                "gender_name": {
                    "title": "Filter by gender names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Female"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
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
        "metrics": {
            "title": "Metrics to include in the summary",
            "description": "Some metrics may be approximations for performance reasons.",
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "profiles",
                    "unique_companies"
                ]
            },
            "default": [
                "profiles"
            ],
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
  "url": "https://emsiservices.com/global-profiles/totals",
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
    "text": "{ \"filter\": { \"nation\": [ \"AUS\" ], \"skills_name\": [ \"SQL (Programming Language)\" ] }, \"metrics\": [ \"profiles\" ] }"
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
      "unique_companies": 30,
      "profiles": 50
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

Group and rank profiles by available facets.

### `GET` <span class="from-raml uri-prefix"></span>/rankings

Get a list of current available ranking facets.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-profiles/rankings",
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
    "onet",
    "onet_name",
    "schools",
    "schools_name",
    "skills",
    "skills_name",
    "soft_skills",
    "soft_skills_name",
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
<code>rankingFacet</code><div class="type">enum</div> | Example: `title`<br>Must be one of: `nation`, `market`, `occupation`, `onet`, `schools`, `schools_name`, `company`, `company_name`, `title`, `title_name`, `skills`, `skills_name`, `hard_skills`, `hard_skills_name`, `soft_skills`, `soft_skills_name`, `certifications`, `certifications_name`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "filter": {
    "nation": [
      "AUS"
    ],
    "skills_name": [
      "SQL (Programming Language)"
    ]
  },
  "rank": {
    "by": "profiles",
    "limit": 20,
    "extra_metrics": [
      "unique_companies"
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
                "nation": {
                    "title": "Filter by nation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "AUS"
                    ],
                    "additionalProperties": false
                },
                "nation_name": {
                    "title": "Filter by nation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "Australia"
                    ],
                    "additionalProperties": false
                },
                "market": {
                    "title": "Filter by market ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "AUS_M_6000"
                    ],
                    "additionalProperties": false
                },
                "market_name": {
                    "title": "Filter by market names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "Detroit-Warren-Dearborn, MI"
                    ],
                    "additionalProperties": false
                },
                "occupation": {
                    "title": "Filter by occupation ids",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "e41a"
                    ],
                    "additionalProperties": false
                },
                "occupation_name": {
                    "title": "Filter by occupation names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
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
                    "example": [
                        "Sales Representatives"
                    ],
                    "additionalProperties": false
                },
                "educations": {
                    "title": "Filter by educational credentials",
                    "description": "An object or list of objects describing educational credentials. Educations in a list will be ANDed together, fields within an education object will be ANDed together, values in an education field will be ORed together.\n\nMinimum educations: `1`\n\nMaximum educations: `10`\n\n*Example: Find profiles which have a degree from Yale or Harvard*\n\n```json\n{\n\t\"filter\": {\n\t\t\"educations\": [\n\t\t\t{\n\t\t\t\t\"schools_name\": [\n\t\t\t\t\t\"Yale University\",\n\t\t\t\t\t\"Harvard University\"\n\t\t\t\t]\n\t\t\t}\n\t\t]\n\t}\n}\n```",
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
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "properties": {
                                "include": {
                                    "description": "List of values to include in the filter.",
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "minLength": 1,
                                        "__nodocs": true
                                    },
                                    "minItems": 1,
                                    "__nodocs": true
                                },
                                "exclude": {
                                    "description": "List of values to exclude from the filter.",
                                    "type": "array",
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
                                    "type": "string",
                                    "minLength": 1,
                                    "__nodocs": true
                                },
                                "minItems": 1,
                                "properties": {
                                    "include": {
                                        "description": "List of values to include in the filter.",
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "minLength": 1,
                                            "__nodocs": true
                                        },
                                        "minItems": 1,
                                        "__nodocs": true
                                    },
                                    "exclude": {
                                        "description": "List of values to exclude from the filter.",
                                        "type": "array",
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
                "title": {
                    "title": "Filter by job title codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "29-1141.00"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
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
                "onet_name": {
                    "title": "Filter by Emsi O*NET names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).\n\nFor version see [/meta](#meta).",
                    "example": [
                        "Registered Nurses"
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
                    "title": "Filter by normalized company names",
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
                "skills": {
                    "title": "Filter by skill codes (any skill type)",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
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
                "gender": {
                    "title": "Filter by gender codes",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "0"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
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
                "gender_name": {
                    "title": "Filter by gender names",
                    "description": "This value may be an array of values to filter by (inclusively) or an object describing more nuanced filtering (for details see [Filtering](#filtering) above).",
                    "type": [
                        "array",
                        "object"
                    ],
                    "example": [
                        "Female"
                    ],
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1,
                    "properties": {
                        "include": {
                            "description": "List of values to include in the filter.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1,
                            "__nodocs": true
                        },
                        "exclude": {
                            "description": "List of values to exclude from the filter.",
                            "type": "array",
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
        "rank": {
            "title": "Choose how to rank your results",
            "type": "object",
            "properties": {
                "by": {
                    "title": "What metric to use to rank the ranking facet",
                    "description": "Some metrics may be approximations for performance reasons.",
                    "type": "string",
                    "enum": [
                        "profiles",
                        "unique_companies",
                        "significance"
                    ],
                    "default": "profiles"
                },
                "limit": {
                    "title": "Limit the number of ranked items returned",
                    "description": "Unlimited rankings (passing a maximum of `0`) are not valid for job titles, cities, companies, schools, skills, and certifications facets.",
                    "type": "integer",
                    "default": 10,
                    "minimum": 0,
                    "maximum": 1000
                },
                "extra_metrics": {
                    "title": "Request additional metrics for each ranked group returned",
                    "description": "In addition to 'by' metric, calculate these metrics for each ranked group. Some metrics may be approximations for performance reasons.",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "profiles",
                            "unique_companies"
                        ]
                    },
                    "default": [
                        "profiles"
                    ],
                    "minItems": 1
                },
                "min_profiles": {
                    "title": "Require ranked items to have this many profiles",
                    "description": "Require ranked items to have at least this many profiles matching the filter.\n\n*Default is `10` for `significance` rankings, `1` for all other rankings*",
                    "type": "integer",
                    "default": 1,
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
  "url": "https://emsiservices.com/global-profiles/rankings/title",
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
    "text": "{ \"filter\": { \"nation\": [ \"AUS\" ], \"skills_name\": [ \"SQL (Programming Language)\" ] }, \"rank\": { \"by\": \"profiles\", \"limit\": 20, \"extra_metrics\": [ \"unique_companies\" ], \"min_profiles\": 1 } }"
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
      "unique_companies": 1646,
      "profiles": 5551
    },
    "ranking": {
      "facet": "company",
      "rank_by": "unique_companies",
      "limit": 20,
      "buckets": [
        {
          "name": "Apple Inc.",
          "unique_companies": 1043,
          "profiles": 2049
        },
        {
          "name": "Facebook",
          "unique_companies": 603,
          "profiles": 3502
        }
      ]
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
  "url": "https://emsiservices.com/global-profiles/taxonomies",
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
    "onet",
    "schools",
    "skills",
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
<code>facet</code><div class="type">enum</div> | Which taxonomy to search for ID/name suggestions.<br>Example: `title`<br>Must be one of: `title`, `company`, `skills`, `market`, `nation`, `occupation`, `onet`, `schools`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of whole or partial keywords to search for. Only when `autocomplete` is true is `q` assumed to be a prefix.<br>This parameter is optional.<br>Example: `data sci`
<code>autocomplete</code><div class="type">boolean</div> | Autocomplete search terms.<br><ul><li>`true` - Performs fast prefix-enabled search using only primary and, if available, alternate names (alternate names currently available for ONET and skills).</li><li>`false` - Performs more extensive search using both name(s) and, if available, description (description currently only available for SOC and ONET search).</li></ul><br>This parameter is optional.<br>Default: `true`
<code>limit</code><div class="type">integer</div> | How many search results to return.<br>This parameter is optional.<br>Minimum: `1`<br>Maximum: `10000`<br>Default: `10`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/global-profiles/taxonomies/title",
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
      "id": "15.30650",
      "name": "Data Scientists",
      "score": 8.407919
    },
    {
      "id": "15.1073",
      "name": "Data Specialists",
      "score": 5.7275753
    },
    {
      "id": "15.1219",
      "name": "Database Specialists",
      "score": 5.7275753
    },
    {
      "id": "29.144",
      "name": "Minimum Data Set (MDS) Nurses",
      "score": 4.0093026
    },
    {
      "id": "29.38",
      "name": "Minimum Data Set (MDS) Coordinators",
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
<code>facet</code><div class="type">enum</div> | Which taxonomy to to look up IDs in.<br>Example: `title`<br>Must be one of: `title`, `company`, `skills`, `market`, `nation`, `occupation`, `onet`, `schools`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    "15.30650"
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
            "title": "Taxonomy facet identifiers (invalid ids will be dropped)\n\nMinimum ids: `1`\n\nMaximum ids: `10000`\n\n",
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
  "url": "https://emsiservices.com/global-profiles/taxonomies/title/lookup",
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
    "text": "{ \"ids\": [ \"15.30650\" ] }"
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
      "id": "15.30650",
      "name": "Data Scientists"
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

