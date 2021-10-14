# Talent Benchmark 
#### v1.4.0
##### Information on past releases can be found in the [Changelog](/updates/talent-benchmark-changelog).

## Overview

### Use case
This is an interface for retrieving key indicators to help benchmark talent by location in the United States.

### About the data
The data in this API exposes key talent benchmarking metrics oriented around supply, demand, diversity, and compensation. These metrics are aggregated from various Emsi datasets including US job postings, US profiles, and US Diversity along with our Compensation model for any job title and city in the United States.

### Content type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the Benchmark API, you must request an OAuth bearer token with the scope `benchmark`.

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
          "value": "benchmark"
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

<div class="internal-only">

**Quotas**:

By default all clients have unlimited access, a quota can be added through Emsi Auth claims (see below). For more detail on the quota system see our [Emsi Auth Quota](/guides/emsi-auth-quota) document.

A quota for each benchmark endpoint can be changed through a `benchmark:{endpoint}:quota` Emsi Auth claim. For example, to set a client's quota to 100 requests per month on `/compensation` endpoint, use `benchmark:compensation:quota:100/month`. This quota will only apply to the `/compensation` endpoint, leaving the unlimited access on other endpoints.

Alternatively, quotas can be applied to all endpoints at once through a `benchmark:quota` claim. To set a client's quota to 100 requests per month on all endpoints, use `benchmark:quota:100/month`.

**Access Claims**:

The scope `benchmark:supply,demand,compensation,diversity,skills` will allow access to all endpoints as well as all summary data. To limit the scope add or remove accordingly. For example `benchmark:supply` will only grant access to the supply endpoint and supply summary data.

**Advanced Filtering**:

The scope `benchmark:advanced` will allow access to `advanced` filter in all endpoints.

</div>

### Advanced Filtering

For more granular filtering, an `advanced` filter is available for all benchmark data endpoints. The advanced filter value will not be normalized by the API, and will be used directly to filter benchmark metrics. Version information for the advanced filters can be found in [/meta](#meta).

Note that the `advanced` filter cannot be used along with `title` and `city` filters, and when it is used `searchParams.area` in response will return a list of area objects instead of an object. To access this feature contact us [here](mailto:api-support@emsibg.com).

<div data-toggle="Advanced Filtering Details">

<div class="tabs">
<div data-tab="Request Example">


```json
{
  "advanced": {
    "occupations": ["15-1256"],
    "skills": ["KS125716TLTGH6SDHJD1", "KS1219W70LY1GXZDSKW5"],
    "counties": ["16001", "16003"]
  }
}
```

</div>
<div data-tab="Request Full Reference">

```jsonschema
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "$id": "requests/request.schema.json",
  "type": "object",
  "properties": {
    "advanced": {
      "title": "Add advanced filters for benchmark metrics",
      "type": "object",
      "properties": {
        "occupations": {
          "title": "List of 5-digit SOC codes to filter",
          "description": "For version see [/meta](#meta).",
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1,
            "__nodocs": true
          },
          "minItems": 1
        },
        "skills": {
          "title": "List of skill ids to filter",
          "description": "For version see [/meta](#meta).",
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1,
            "__nodocs": true
          },
          "minItems": 1
        },
        "counties": {
          "title": "List of county FIPS codes to filter",
          "description": "For version see [/meta](#meta).",
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1,
            "__nodocs": true
          },
          "minItems": 1
        }
      },
      "required": [
          "occupations"
      ],
      "additionalProperties": false
    }
  },
  "required": [
      "advanced"
  ],
  "additionalProperties": false
}
```

</div>
</div>

</div>

## /status

Service status (health)

### `GET` Get service status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/benchmark/status",
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


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/status.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Status response object",
            "type": "object",
            "properties": {
                "message": {
                    "title": "Message describing the health of the service",
                    "type": "string",
                    "minLength": 1
                },
                "healthy": {
                    "title": "Boolean value to show if the service is healthy",
                    "type": "boolean"
                }
            },
            "required": [
                "message",
                "healthy"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /meta

Get API metadata information.

### `GET` Get service metadata

Get service metadata, including access information and attribution text.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/benchmark/meta",
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
      "title": "Talent Benchmark",
      "body": "Emsi's Talent Benchmark API aggregates data points from our US job postings, US profiles, and US Diversity datasets along with our Compensation model estimates."
    },
    "access": [
      "supply",
      "demand",
      "compensation",
      "diversity"
    ],
    "taxonomies": {
      "area": "us_area_2021_2",
      "occupations": "soc_emsi_2019",
      "skills": "skillsv7.42"
    }
  }
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/meta.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Meta response object",
            "type": "object",
            "properties": {
                "attribution": {
                    "title": "Service attribution object",
                    "type": "object",
                    "properties": {
                        "title": {
                            "title": "Name of the service",
                            "type": "string",
                            "minLength": 1
                        },
                        "body": {
                            "title": "Service description",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "title",
                        "body"
                    ],
                    "additionalProperties": false
                },
                "access": {
                    "title": "List of accessible benchmark metrics",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    }
                },
                "taxonomies": {
                    "title": "Versions of taxonomies used in advanced filtering",
                    "description": "For more detail on advanced filtering see [Advanced Filtering](#advanced-filtering) section of this documentation.",
                    "type": "object",
                    "properties": {
                        "area": {
                            "title": "Area version used in advanced filtering",
                            "type": "string",
                            "minLength": 1
                        },
                        "occupations": {
                            "title": "SOC version used in advanced filtering",
                            "type": "string",
                            "minLength": 1
                        },
                        "skills": {
                            "title": "Skills version used in advanced filtering",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "area",
                        "occupations",
                        "skills"
                    ],
                    "additionalProperties": false
                }
            },
            "required": [
                "attribution",
                "access",
                "taxonomies"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /

Get summary on all benchmark metrics.

### `POST` Get benchmark summary

Get summary data on each metric that you have access to.

Advanced filtering is available for this endpoint. For more details, take a look at [Advanced Filtering](#advanced-filtering) section of this documentation.





#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "title": "web developer",
  "city": "moscow id"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/request.schema.json",
    "type": "object",
    "properties": {
        "city": {
            "title": "City name to search on",
            "type": [
                "string",
                "null"
            ],
            "minLength": 1
        },
        "title": {
            "title": "Job title to search on",
            "type": "string",
            "minLength": 1
        },
        "advanced": {
            "title": "Add advanced filters for benchmark metrics",
            "type": "object",
            "properties": {
                "occupations": {
                    "title": "List of 5-digit SOC codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "skills": {
                    "title": "List of skill ids to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "counties": {
                    "title": "List of county FIPS codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                }
            },
            "__nodocs": true,
            "required": [
                "occupations"
            ],
            "additionalProperties": false
        }
    },
    "additionalProperties": false
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/benchmark/",
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
    "text": "{ \"title\": \"web developer\", \"city\": \"moscow id\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "searchParams": {
    "area": {
      "id": "34140",
      "level": "MSA",
      "name": "Moscow, ID"
    },
    "title": {
      "id": "ET35635562C89DD29C",
      "name": "Web Developers"
    },
    "occupations": [
      {
        "id": "15-1257",
        "name": "Web Developers and Digital Interface Designers"
      }
    ],
    "skills": []
  },
  "data": {
    "supply": {
      "benchmarkIndex": 1.2,
      "profiles": 28,
      "companies": 12
    },
    "demand": {
      "benchmarkIndex": 1.2,
      "postings": 3,
      "companies": 2
    },
    "compensation": {
      "benchmarkIndex": 1.2,
      "minSalary": 20208,
      "medianSalary": 49832,
      "maxSalary": 103298,
      "medianAdvertisedSalary": 62400
    },
    "diversity": {
      "regional": 1,
      "regionalPct": 0.0345,
      "national": 42946,
      "nationalPct": 0.231
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


<div data-tab="401">

You don't have access to the endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "title": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

Could not normalize title 'invalid'.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "Not Found",
      "detail": "Could not normalize title 'invalid'"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "$id": "responses/summary.schema.json",
    "properties": {
        "searchParams": {
            "title": "Normalized search parameters",
            "type": "object",
            "properties": {
                "area": {
                    "title": "Normalized area info",
                    "description": "This field will return a list of area objects if `advanced` filter was used. Otherwise, it will be an area object.",
                    "type": [
                        "object",
                        "array"
                    ],
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Normalized area id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Normalized area name",
                                "type": "string",
                                "minLength": 1
                            },
                            "level": {
                                "title": "Normalized area level",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "__nodocs": true,
                        "required": [
                            "id",
                            "name",
                            "level"
                        ],
                        "additionalProperties": false
                    },
                    "properties": {
                        "id": {
                            "title": "Normalized area id",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized area name",
                            "type": "string",
                            "minLength": 1
                        },
                        "level": {
                            "title": "Normalized area level",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name",
                        "level"
                    ],
                    "additionalProperties": false
                },
                "title": {
                    "title": "Normalized Emsi title",
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "id": {
                            "title": "Normalized Emsi title id",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized Emsi title name",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name"
                    ],
                    "additionalProperties": false
                },
                "occupations": {
                    "title": "Occupations mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "5-digit SOC id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "5-digit SOC name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "Skills mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Emsi skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Emsi skill name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "area",
                "title",
                "occupations",
                "skills"
            ],
            "additionalProperties": false
        },
        "data": {
            "title": "Benchmark metrics summary",
            "type": "object",
            "properties": {
                "supply": {
                    "title": "Summary of supply benchmark metrics",
                    "type": "object",
                    "properties": {
                        "benchmarkIndex": {
                            "title": "Benchmark index",
                            "description": "Our supply benchmark index is a multiplier, comparing regional supply to national supply.\n\n`1.0` indicates the region is on par with national supply\n\n`null` indicates a lack of information to estimate the index.",
                            "type": [
                                "number",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "profiles": {
                            "title": "Number of profiles for a given job",
                            "type": "integer",
                            "minimum": 0
                        },
                        "companies": {
                            "title": "Number of employers of the matching profiles for a given job",
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "benchmarkIndex",
                        "profiles",
                        "companies"
                    ],
                    "additionalProperties": false
                },
                "demand": {
                    "title": "Summary of demand benchmark metrics",
                    "type": "object",
                    "properties": {
                        "benchmarkIndex": {
                            "title": "Benchmark index",
                            "description": "Our demand benchmark index is a multiplier, comparing regional demand to national demand.\n\n`1.0` indicates the region is on par with national demand\n\n`null` indicates a lack of information to estimate the index.",
                            "type": [
                                "number",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "companies": {
                            "title": "Number of companies in demand of a given job",
                            "type": "integer",
                            "minimum": 0
                        },
                        "postings": {
                            "title": "Number of postings for a given job",
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "benchmarkIndex",
                        "companies",
                        "postings"
                    ],
                    "additionalProperties": false
                },
                "compensation": {
                    "title": "Summary of compensation benchmark metrics",
                    "type": "object",
                    "properties": {
                        "benchmarkIndex": {
                            "title": "Benchmark index",
                            "description": "Our compensation benchmark index is a multiplier, comparing regional compensation to national compensation.\n\n`1.0` indicates the region is on par with national compensation\n\n`null` indicates a lack of information to estimate the index.",
                            "type": [
                                "number",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "maxSalary": {
                            "title": "Maximum regional salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "minSalary": {
                            "title": "Minimum regional salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "medianSalary": {
                            "title": "Median regional salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "medianAdvertisedSalary": {
                            "title": "Median advertised salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        }
                    },
                    "required": [
                        "benchmarkIndex",
                        "maxSalary",
                        "minSalary",
                        "medianSalary",
                        "medianAdvertisedSalary"
                    ],
                    "additionalProperties": false
                },
                "diversity": {
                    "title": "Summary of diversity benchmark metrics",
                    "type": "object",
                    "properties": {
                        "regional": {
                            "title": "Regional number of non-white workers",
                            "type": "number",
                            "minimum": 0
                        },
                        "regionalPct": {
                            "title": "Regional percentage of non-white workers",
                            "type": "number",
                            "minimum": 0
                        },
                        "national": {
                            "title": "National number of non-white workers",
                            "type": "number",
                            "minimum": 0
                        },
                        "nationalPct": {
                            "title": "National percentage of non-white workers",
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "regional",
                        "regionalPct",
                        "national",
                        "nationalPct"
                    ],
                    "additionalProperties": false
                }
            },
            "additionalProperties": false
        }
    },
    "required": [
        "searchParams",
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /supply

Get matching profiles for jobs at a location.

### `POST` Get supply benchmark data

Emsi aggregates online social profiles from all over the web. The details in this endpoint provide aggregate totals for the top employers, top titles, and top skills associated with the profiles matching your search.

Advanced filtering is available for this endpoint. For more details, take a look at [Advanced Filtering](#advanced-filtering) section of this documentation.





#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "title": "web developer",
  "city": "moscow id"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/request.schema.json",
    "type": "object",
    "properties": {
        "city": {
            "title": "City name to search on",
            "type": [
                "string",
                "null"
            ],
            "minLength": 1
        },
        "title": {
            "title": "Job title to search on",
            "type": "string",
            "minLength": 1
        },
        "advanced": {
            "title": "Add advanced filters for benchmark metrics",
            "type": "object",
            "properties": {
                "occupations": {
                    "title": "List of 5-digit SOC codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "skills": {
                    "title": "List of skill ids to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "counties": {
                    "title": "List of county FIPS codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                }
            },
            "__nodocs": true,
            "required": [
                "occupations"
            ],
            "additionalProperties": false
        }
    },
    "additionalProperties": false
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/benchmark/supply",
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
    "text": "{ \"title\": \"web developer\", \"city\": \"moscow id\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "searchParams": {
    "area": {
      "id": "34140",
      "level": "MSA",
      "name": "Moscow, ID"
    },
    "title": {
      "id": "ET35635562C89DD29C",
      "name": "Web Developers"
    },
    "occupations": [
      {
        "id": "15-1257",
        "name": "Web Developers and Digital Interface Designers"
      }
    ],
    "skills": []
  },
  "data": {
    "summary": {
      "benchmarkIndex": 1.2,
      "profiles": 28,
      "companies": 12
    },
    "companies": [
      {
        "id": "NC7b041b70-89a9-4cf9-9c8b-9d7082813dc5",
        "name": "The Fenway Group LLC",
        "profiles": 1
      },
      {
        "id": "NCc3fd73ae-5521-4805-9613-d7e9c8ccfdb2",
        "name": "University of Idaho",
        "profiles": 6
      },
      {
        "id": "NC55e9a336-3e98-4f9d-be26-110e7cc6f232",
        "name": "Timevalue Software",
        "profiles": 1
      },
      {
        "id": "NC25f58580-7ae8-49fa-ae6a-8b838028c263",
        "name": "College of Veterinarian Medicine",
        "profiles": 1
      },
      {
        "id": "NC46d297f3-add3-4d66-a992-92ffc22eff19",
        "name": "Bobbin, Inc.",
        "profiles": 1
      },
      {
        "id": "NC9d85abbd-e1b3-4117-9b75-3254bb3b7c44",
        "name": "EMSI",
        "profiles": 5
      },
      {
        "id": "NCaab24495-f8ba-45d9-954a-17db49ab3467",
        "name": "Washington State University",
        "profiles": 2
      },
      {
        "id": "NC991730fd-4127-4065-a6f4-5bb03b63b2d0",
        "name": "Eps Corporation",
        "profiles": 1
      },
      {
        "id": "NC23b818a3-c01b-419c-9447-04b9663e3d12",
        "name": "Center On Disablities & Human Development",
        "profiles": 1
      },
      {
        "id": "NC63bba034-f758-4817-bbf7-81eac8dba543",
        "name": "Alpha PHI International Fraternity Incorporated",
        "profiles": 1
      }
    ],
    "skills": [
      {
        "id": "KS122VP5W9LZ8TRNFJY0",
        "name": "Web Design",
        "profiles": 8
      },
      {
        "id": "KS122Z36QK3N5097B5JH",
        "name": "Web Development",
        "profiles": 10
      },
      {
        "id": "KS124JZ5VYRZ5MJ85N2B",
        "name": "Public Speaking",
        "profiles": 9
      },
      {
        "id": "KS121F45VPV8C9W3QFYH",
        "name": "Cascading Style Sheets (CSS)",
        "profiles": 11
      },
      {
        "id": "KS1200578T5QCYT0Z98G",
        "name": "HyperText Markup Language (HTML)",
        "profiles": 7
      },
      {
        "id": "KS121Z26S4VJLQ1WXN21",
        "name": "Customer Service",
        "profiles": 8
      },
      {
        "id": "KS1203C6N9B52QGB4H67",
        "name": "Research",
        "profiles": 7
      },
      {
        "id": "KS1206Y6W7F5JS3VBTFL",
        "name": "Adobe Photoshop",
        "profiles": 8
      },
      {
        "id": "KS1200771D9CR9LB4MWW",
        "name": "JavaScript (Programming Language)",
        "profiles": 6
      },
      {
        "id": "KS1218W78FGVPVP2KXPX",
        "name": "Management",
        "profiles": 7
      }
    ],
    "titles": [
      {
        "id": "ET3844BF712F449AE0",
        "name": "UX Designers",
        "profiles": 2
      },
      {
        "id": "ET4A6F170CAC2A3313",
        "name": "Front End Developers/Designers",
        "profiles": 1
      },
      {
        "id": "ET35635562C89DD29C",
        "name": "Web Developers",
        "profiles": 5
      },
      {
        "id": "ET1AF7B8583528C79E",
        "name": "Designers/Makers",
        "profiles": 1
      },
      {
        "id": "ET27D061410C435EE6",
        "name": "Web Coordinators",
        "profiles": 6
      },
      {
        "id": "ET0000000000000000",
        "name": "Unclassified",
        "profiles": 1
      },
      {
        "id": "ET50828432D24BA35A",
        "name": "Full Stack Developers",
        "profiles": 1
      },
      {
        "id": "ETAD4D509C925DA184",
        "name": "Wordpress Developers",
        "profiles": 1
      },
      {
        "id": "ET3819ACCBFBDDE5FC",
        "name": "Product Photographers",
        "profiles": 1
      },
      {
        "id": "ETA58C0A7AF98A6DDA",
        "name": "Shipping Managers",
        "profiles": 1
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


<div data-tab="401">

You don't have access to the endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "title": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

Could not normalize title 'invalid'.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "Not Found",
      "detail": "Could not normalize title 'invalid'"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/supply.schema.json",
    "definitions": {
        "supply-items": {
            "type": "object",
            "properties": {
                "id": {
                    "title": "Dimension id",
                    "type": "string",
                    "minLength": 1
                },
                "name": {
                    "title": "Dimension name",
                    "type": "string",
                    "minLength": 1
                },
                "profiles": {
                    "title": "Number of worker profiles",
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": [
                "id",
                "name",
                "profiles"
            ],
            "additionalProperties": false
        }
    },
    "type": "object",
    "properties": {
        "searchParams": {
            "title": "Normalized search parameters",
            "type": "object",
            "properties": {
                "area": {
                    "title": "Normalized area info",
                    "description": "This field will return a list of area objects if `advanced` filter was used. Otherwise, it will be an area object.",
                    "type": [
                        "object",
                        "array"
                    ],
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Normalized area id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Normalized area name",
                                "type": "string",
                                "minLength": 1
                            },
                            "level": {
                                "title": "Normalized area level",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "__nodocs": true,
                        "required": [
                            "id",
                            "name",
                            "level"
                        ],
                        "additionalProperties": false
                    },
                    "properties": {
                        "id": {
                            "title": "Normalized area id",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized area name",
                            "type": "string",
                            "minLength": 1
                        },
                        "level": {
                            "title": "Normalized area level",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name",
                        "level"
                    ],
                    "additionalProperties": false
                },
                "title": {
                    "title": "Normalized Emsi title",
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "id": {
                            "title": "Normalized Emsi title id",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized Emsi title name",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name"
                    ],
                    "additionalProperties": false
                },
                "occupations": {
                    "title": "Occupations mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "5-digit SOC id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "5-digit SOC name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "Skills mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Emsi skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Emsi skill name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "area",
                "title",
                "occupations",
                "skills"
            ],
            "additionalProperties": false
        },
        "data": {
            "title": "Supply benchmark data",
            "type": "object",
            "properties": {
                "summary": {
                    "title": "Summary of supply benchmark metrics",
                    "type": "object",
                    "properties": {
                        "benchmarkIndex": {
                            "title": "Benchmark index",
                            "description": "Our supply benchmark index is a multiplier, comparing regional supply to national supply.\n\n`1.0` indicates the region is on par with national supply\n\n`null` indicates a lack of information to estimate the index.",
                            "type": [
                                "number",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "profiles": {
                            "title": "Number of profiles for a given job",
                            "type": "integer",
                            "minimum": 0
                        },
                        "companies": {
                            "title": "Number of employers of the matching profiles for a given job",
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "benchmarkIndex",
                        "profiles",
                        "companies"
                    ],
                    "additionalProperties": false
                },
                "companies": {
                    "title": "List of companies with highest supply of workers",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "profiles": {
                                "title": "Number of worker profiles",
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "profiles"
                        ],
                        "additionalProperties": false
                    }
                },
                "titles": {
                    "title": "List of titles with highest supply of workers",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "profiles": {
                                "title": "Number of worker profiles",
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "profiles"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "List of skills with highest supply of workers",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "profiles": {
                                "title": "Number of worker profiles",
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "profiles"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "summary",
                "companies",
                "titles",
                "skills"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "searchParams",
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /demand

Get what companies, jobs, and skills are in demand in specified location and occupation.

### `POST` Get demand benchmark data

Emsi aggregates job posting details from all over the web. The details in this endpoint provide aggregate totals for the top employers, top titles, and top skills associated with the postings matching your search.

Advanced filtering is available for this endpoint. For more details, take a look at [Advanced Filtering](#advanced-filtering) section of this documentation.





#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "title": "web developer",
  "city": "moscow id"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/request.schema.json",
    "type": "object",
    "properties": {
        "city": {
            "title": "City name to search on",
            "type": [
                "string",
                "null"
            ],
            "minLength": 1
        },
        "title": {
            "title": "Job title to search on",
            "type": "string",
            "minLength": 1
        },
        "advanced": {
            "title": "Add advanced filters for benchmark metrics",
            "type": "object",
            "properties": {
                "occupations": {
                    "title": "List of 5-digit SOC codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "skills": {
                    "title": "List of skill ids to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "counties": {
                    "title": "List of county FIPS codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                }
            },
            "__nodocs": true,
            "required": [
                "occupations"
            ],
            "additionalProperties": false
        }
    },
    "additionalProperties": false
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/benchmark/demand",
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
    "text": "{ \"title\": \"web developer\", \"city\": \"moscow id\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "searchParams": {
    "area": {
      "id": "34140",
      "level": "MSA",
      "name": "Moscow, ID"
    },
    "title": {
      "id": "ET35635562C89DD29C",
      "name": "Web Developers"
    },
    "occupations": [
      {
        "id": "15-1257",
        "name": "Web Developers and Digital Interface Designers"
      }
    ],
    "skills": []
  },
  "data": {
    "summary": {
      "benchmarkIndex": 1.2,
      "postings": 3,
      "companies": 2
    },
    "companies": [
      {
        "id": "NC5b71f3eb-462d-4031-9fe4-1df21aaf8ee6",
        "name": "Love Story Inc",
        "postings": 1
      },
      {
        "id": "EC19DEA3B2-30BC-550A-9041-39E14AFE5746",
        "name": "Revature",
        "postings": 2
      }
    ],
    "skills": [
      {
        "id": "KS441PL6JPXW200W0GRQ",
        "name": "User Experience",
        "postings": 1
      },
      {
        "id": "KS121F45VPV8C9W3QFYH",
        "name": "Cascading Style Sheets (CSS)",
        "postings": 1
      },
      {
        "id": "KSZYONH2OKW1M20H8FQ0",
        "name": "Yoast",
        "postings": 1
      },
      {
        "id": "KS122556LMQ829GZCCRV",
        "name": "Communications",
        "postings": 2
      },
      {
        "id": "KS1200578T5QCYT0Z98G",
        "name": "HyperText Markup Language (HTML)",
        "postings": 1
      },
      {
        "id": "KS124FP642Q7P7TBPPZN",
        "name": "Search Engine Optimization",
        "postings": 1
      },
      {
        "id": "KS125KJ77JNWBRCS031V",
        "name": "Journaling File Systems",
        "postings": 1
      },
      {
        "id": "KS122YN6108R0RSDXXRC",
        "name": "Digital Marketing",
        "postings": 1
      }
    ],
    "titles": [
      {
        "id": "ETC9C61E01043162B3",
        "name": "Front End Developers",
        "postings": 1
      },
      {
        "id": "ETD64C539037F6269A",
        "name": "Creative Writers",
        "postings": 1
      },
      {
        "id": "ETD83A33E887E6513D",
        "name": "HTML Developers",
        "postings": 1
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


<div data-tab="401">

You don't have access to the endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "title": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

Could not normalize title 'invalid'.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "Not Found",
      "detail": "Could not normalize title 'invalid'"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/demand.schema.json",
    "definitions": {
        "demand-items": {
            "type": "object",
            "properties": {
                "id": {
                    "title": "Dimension id",
                    "type": "string",
                    "minLength": 1
                },
                "name": {
                    "title": "Dimension name",
                    "type": "string",
                    "minLength": 1
                },
                "postings": {
                    "title": "Number of unique postings",
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": [
                "id",
                "name",
                "postings"
            ],
            "additionalProperties": false
        }
    },
    "type": "object",
    "properties": {
        "searchParams": {
            "title": "Normalized search parameters",
            "type": "object",
            "properties": {
                "area": {
                    "title": "Normalized area info",
                    "description": "This field will return a list of area objects if `advanced` filter was used. Otherwise, it will be an area object.",
                    "type": [
                        "object",
                        "array"
                    ],
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Normalized area id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Normalized area name",
                                "type": "string",
                                "minLength": 1
                            },
                            "level": {
                                "title": "Normalized area level",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "__nodocs": true,
                        "required": [
                            "id",
                            "name",
                            "level"
                        ],
                        "additionalProperties": false
                    },
                    "properties": {
                        "id": {
                            "title": "Normalized area id",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized area name",
                            "type": "string",
                            "minLength": 1
                        },
                        "level": {
                            "title": "Normalized area level",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name",
                        "level"
                    ],
                    "additionalProperties": false
                },
                "title": {
                    "title": "Normalized Emsi title",
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "id": {
                            "title": "Normalized Emsi title id",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized Emsi title name",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name"
                    ],
                    "additionalProperties": false
                },
                "occupations": {
                    "title": "Occupations mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "5-digit SOC id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "5-digit SOC name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "Skills mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Emsi skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Emsi skill name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "area",
                "title",
                "occupations",
                "skills"
            ],
            "additionalProperties": false
        },
        "data": {
            "title": "Demand benchmark data",
            "type": "object",
            "properties": {
                "summary": {
                    "title": "Summary of demand benchmark metrics",
                    "type": "object",
                    "properties": {
                        "benchmarkIndex": {
                            "title": "Benchmark index",
                            "description": "Our demand benchmark index is a multiplier, comparing regional demand to national demand.\n\n`1.0` indicates the region is on par with national demand\n\n`null` indicates a lack of information to estimate the index.",
                            "type": [
                                "number",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "companies": {
                            "title": "Number of companies in demand of a given job",
                            "type": "integer",
                            "minimum": 0
                        },
                        "postings": {
                            "title": "Number of postings for a given job",
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "benchmarkIndex",
                        "companies",
                        "postings"
                    ],
                    "additionalProperties": false
                },
                "companies": {
                    "title": "List of companies with highest demand",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "postings": {
                                "title": "Number of unique postings",
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "postings"
                        ],
                        "additionalProperties": false
                    }
                },
                "titles": {
                    "title": "List of job titles with highest demand",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "postings": {
                                "title": "Number of unique postings",
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "postings"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "List of skills with highest demand",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "postings": {
                                "title": "Number of unique postings",
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "postings"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "summary",
                "companies",
                "titles",
                "skills"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "searchParams",
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /compensation

Get compensation percentile data for specified location and occupation with the nation values included for context.

### `POST` Get compensation benchmark data

Emsi models compensation data using government data and advertised salary observations identified from job postings data.

Advanced filtering is available for this endpoint. For more details, take a look at [Advanced Filtering](#advanced-filtering) section of this documentation.





#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "title": "web developer",
  "city": "moscow id"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/request.schema.json",
    "type": "object",
    "properties": {
        "city": {
            "title": "City name to search on",
            "type": [
                "string",
                "null"
            ],
            "minLength": 1
        },
        "title": {
            "title": "Job title to search on",
            "type": "string",
            "minLength": 1
        },
        "advanced": {
            "title": "Add advanced filters for benchmark metrics",
            "type": "object",
            "properties": {
                "occupations": {
                    "title": "List of 5-digit SOC codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "skills": {
                    "title": "List of skill ids to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "counties": {
                    "title": "List of county FIPS codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                }
            },
            "__nodocs": true,
            "required": [
                "occupations"
            ],
            "additionalProperties": false
        }
    },
    "additionalProperties": false
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/benchmark/compensation",
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
    "text": "{ \"title\": \"web developer\", \"city\": \"moscow id\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "searchParams": {
    "area": {
      "id": "34140",
      "level": "MSA",
      "name": "Moscow, ID"
    },
    "title": {
      "id": "ET35635562C89DD29C",
      "name": "Web Developers"
    },
    "occupations": [
      {
        "id": "15-1257",
        "name": "Web Developers and Digital Interface Designers"
      }
    ],
    "skills": []
  },
  "data": {
    "summary": {
      "benchmarkIndex": 1.2,
      "minSalary": 20208,
      "medianSalary": 49832,
      "maxSalary": 103298,
      "medianAdvertisedSalary": 62400
    },
    "percentiles": [
      {
        "percentile": 10,
        "regional": 27809,
        "national": 41008
      },
      {
        "percentile": 25,
        "regional": 38930,
        "national": 54992
      },
      {
        "percentile": 50,
        "regional": 49832,
        "national": 74992
      },
      {
        "percentile": 75,
        "regional": 61806,
        "national": 103216
      },
      {
        "percentile": 90,
        "regional": 75134,
        "national": 145008
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


<div data-tab="401">

You don't have access to the endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "title": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

Could not normalize title 'invalid'.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "Not Found",
      "detail": "Could not normalize title 'invalid'"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/compensation.schema.json",
    "type": "object",
    "properties": {
        "searchParams": {
            "title": "Normalized search parameters",
            "type": "object",
            "properties": {
                "area": {
                    "title": "Normalized area info",
                    "description": "This field will return a list of area objects if `advanced` filter was used. Otherwise, it will be an area object.",
                    "type": [
                        "object",
                        "array"
                    ],
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Normalized area id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Normalized area name",
                                "type": "string",
                                "minLength": 1
                            },
                            "level": {
                                "title": "Normalized area level",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "__nodocs": true,
                        "required": [
                            "id",
                            "name",
                            "level"
                        ],
                        "additionalProperties": false
                    },
                    "properties": {
                        "id": {
                            "title": "Normalized area id",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized area name",
                            "type": "string",
                            "minLength": 1
                        },
                        "level": {
                            "title": "Normalized area level",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name",
                        "level"
                    ],
                    "additionalProperties": false
                },
                "title": {
                    "title": "Normalized Emsi title",
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "id": {
                            "title": "Normalized Emsi title id",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized Emsi title name",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name"
                    ],
                    "additionalProperties": false
                },
                "occupations": {
                    "title": "Occupations mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "5-digit SOC id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "5-digit SOC name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "Skills mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Emsi skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Emsi skill name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "area",
                "title",
                "occupations",
                "skills"
            ],
            "additionalProperties": false
        },
        "data": {
            "title": "Compensation benchmark data",
            "type": "object",
            "properties": {
                "summary": {
                    "title": "Summary of compensation benchmark metrics",
                    "type": "object",
                    "properties": {
                        "benchmarkIndex": {
                            "title": "Benchmark index",
                            "description": "Our compensation benchmark index is a multiplier, comparing regional compensation to national compensation.\n\n`1.0` indicates the region is on par with national compensation\n\n`null` indicates a lack of information to estimate the index.",
                            "type": [
                                "number",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "maxSalary": {
                            "title": "Maximum regional salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "minSalary": {
                            "title": "Minimum regional salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "medianSalary": {
                            "title": "Median regional salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "medianAdvertisedSalary": {
                            "title": "Median advertised salary",
                            "description": "`null` if compensation data does not exist for given filters.",
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        }
                    },
                    "required": [
                        "benchmarkIndex",
                        "maxSalary",
                        "minSalary",
                        "medianSalary",
                        "medianAdvertisedSalary"
                    ],
                    "additionalProperties": false
                },
                "percentiles": {
                    "title": "List of compensation percentile data",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "percentile": {
                                "title": "Regional percentile",
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100
                            },
                            "regional": {
                                "title": "Regional salary within percentile",
                                "type": "integer",
                                "minimum": 0
                            },
                            "national": {
                                "title": "National salary within percentile",
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "percentile",
                            "regional",
                            "national"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "summary",
                "percentiles"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "searchParams",
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /diversity

Get diversity values for specified location and occupation, with the nation values included for context.

### `POST` Get diversity benchmark data

Emsi models diversity data by applying a staffing pattern to government data related to industries.

Advanced filtering is available for this endpoint. For more details, take a look at [Advanced Filtering](#advanced-filtering) section of this documentation.





#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "title": "web developer",
  "city": "moscow id"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/request.schema.json",
    "type": "object",
    "properties": {
        "city": {
            "title": "City name to search on",
            "type": [
                "string",
                "null"
            ],
            "minLength": 1
        },
        "title": {
            "title": "Job title to search on",
            "type": "string",
            "minLength": 1
        },
        "advanced": {
            "title": "Add advanced filters for benchmark metrics",
            "type": "object",
            "properties": {
                "occupations": {
                    "title": "List of 5-digit SOC codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "skills": {
                    "title": "List of skill ids to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "counties": {
                    "title": "List of county FIPS codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                }
            },
            "__nodocs": true,
            "required": [
                "occupations"
            ],
            "additionalProperties": false
        }
    },
    "additionalProperties": false
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/benchmark/diversity",
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
    "text": "{ \"title\": \"web developer\", \"city\": \"moscow id\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "searchParams": {
    "area": {
      "id": "34140",
      "level": "MSA",
      "name": "Moscow, ID"
    },
    "title": {
      "id": "ET35635562C89DD29C",
      "name": "Web Developers"
    },
    "occupations": [
      {
        "id": "15-1257",
        "name": "Web Developers and Digital Interface Designers"
      }
    ],
    "skills": []
  },
  "data": {
    "summary": {
      "regional": 1,
      "regionalPct": 0.0345,
      "national": 42946,
      "nationalPct": 0.231
    },
    "age": [
      {
        "id": 4,
        "name": "25-34",
        "regional": 11,
        "regionalPct": 0.3793,
        "national": 70501,
        "nationalPct": 0.3793
      },
      {
        "id": 5,
        "name": "35-44",
        "regional": 8,
        "regionalPct": 0.2758,
        "national": 54339,
        "nationalPct": 0.2923
      },
      {
        "id": 6,
        "name": "45-54",
        "regional": 3,
        "regionalPct": 0.1034,
        "national": 28520,
        "nationalPct": 0.1534
      },
      {
        "id": 3,
        "name": "22-24",
        "regional": 2,
        "regionalPct": 0.069,
        "national": 11407,
        "nationalPct": 0.0614
      },
      {
        "id": 7,
        "name": "55-64",
        "regional": 1,
        "regionalPct": 0.0345,
        "national": 13184,
        "nationalPct": 0.0709
      },
      {
        "id": 1,
        "name": "14-18",
        "regional": 0,
        "regionalPct": 0,
        "national": 1171,
        "nationalPct": 0.0063
      },
      {
        "id": 2,
        "name": "19-21",
        "regional": 0,
        "regionalPct": 0,
        "national": 3472,
        "nationalPct": 0.0187
      },
      {
        "id": 8,
        "name": "65-99",
        "regional": 0,
        "regionalPct": 0,
        "national": 3279,
        "nationalPct": 0.0176
      }
    ],
    "demographics": [
      {
        "id": 1,
        "name": "White",
        "regional": 25,
        "regionalPct": 0.862,
        "national": 142929,
        "nationalPct": 0.7689
      },
      {
        "id": 4,
        "name": "Asian",
        "regional": 1,
        "regionalPct": 0.0345,
        "national": 24395,
        "nationalPct": 0.1312
      },
      {
        "id": 3,
        "name": "American Indian or Alaska Native",
        "regional": 0,
        "regionalPct": 0,
        "national": 686,
        "nationalPct": 0.0037
      },
      {
        "id": 2,
        "name": "Black or African American",
        "regional": 0,
        "regionalPct": 0,
        "national": 11501,
        "nationalPct": 0.0619
      },
      {
        "id": 5,
        "name": "Native Hawaiian or Other Pacific Islander",
        "regional": 0,
        "regionalPct": 0,
        "national": 240,
        "nationalPct": 0.0013
      },
      {
        "id": 7,
        "name": "Two or More Races",
        "regional": 0,
        "regionalPct": 0,
        "national": 6124,
        "nationalPct": 0.0329
      }
    ],
    "gender": [
      {
        "id": 1,
        "name": "Male",
        "regional": 21,
        "regionalPct": 0.7241,
        "national": 124422,
        "nationalPct": 0.6694
      },
      {
        "id": 2,
        "name": "Female",
        "regional": 7,
        "regionalPct": 0.2414,
        "national": 61455,
        "nationalPct": 0.3306
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


<div data-tab="401">

You don't have access to the endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "title": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

Could not normalize title 'invalid'.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "Not Found",
      "detail": "Could not normalize title 'invalid'"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/diversity.schema.json",
    "definitions": {
        "diversity-items": {
            "type": "object",
            "properties": {
                "id": {
                    "title": "Dimension id",
                    "type": "number"
                },
                "name": {
                    "title": "Dimension name",
                    "type": "string",
                    "minLength": 1
                },
                "regional": {
                    "title": "Regional number of jobs",
                    "type": "number",
                    "minimum": 0
                },
                "regionalPct": {
                    "title": "Regional percentage of jobs",
                    "type": "number",
                    "minimum": 0
                },
                "national": {
                    "title": "National number of jobs",
                    "type": "number",
                    "minimum": 0
                },
                "nationalPct": {
                    "title": "National percentage of jobs",
                    "type": "number",
                    "minimum": 0
                }
            },
            "required": [
                "id",
                "name",
                "regional",
                "regionalPct",
                "national",
                "nationalPct"
            ],
            "additionalProperties": false
        }
    },
    "type": "object",
    "properties": {
        "searchParams": {
            "title": "Normalized search parameters",
            "type": "object",
            "properties": {
                "area": {
                    "title": "Normalized area info",
                    "description": "This field will return a list of area objects if `advanced` filter was used. Otherwise, it will be an area object.",
                    "type": [
                        "object",
                        "array"
                    ],
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Normalized area id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Normalized area name",
                                "type": "string",
                                "minLength": 1
                            },
                            "level": {
                                "title": "Normalized area level",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "__nodocs": true,
                        "required": [
                            "id",
                            "name",
                            "level"
                        ],
                        "additionalProperties": false
                    },
                    "properties": {
                        "id": {
                            "title": "Normalized area id",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized area name",
                            "type": "string",
                            "minLength": 1
                        },
                        "level": {
                            "title": "Normalized area level",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name",
                        "level"
                    ],
                    "additionalProperties": false
                },
                "title": {
                    "title": "Normalized Emsi title",
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "id": {
                            "title": "Normalized Emsi title id",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized Emsi title name",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name"
                    ],
                    "additionalProperties": false
                },
                "occupations": {
                    "title": "Occupations mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "5-digit SOC id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "5-digit SOC name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "Skills mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Emsi skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Emsi skill name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "area",
                "title",
                "occupations",
                "skills"
            ],
            "additionalProperties": false
        },
        "data": {
            "title": "Diversity benchmark data",
            "type": "object",
            "properties": {
                "summary": {
                    "title": "Summary of diversity benchmark metrics",
                    "type": "object",
                    "properties": {
                        "regional": {
                            "title": "Regional number of non-white workers",
                            "type": "number",
                            "minimum": 0
                        },
                        "regionalPct": {
                            "title": "Regional percentage of non-white workers",
                            "type": "number",
                            "minimum": 0
                        },
                        "national": {
                            "title": "National number of non-white workers",
                            "type": "number",
                            "minimum": 0
                        },
                        "nationalPct": {
                            "title": "National percentage of non-white workers",
                            "type": "number",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "regional",
                        "regionalPct",
                        "national",
                        "nationalPct"
                    ],
                    "additionalProperties": false
                },
                "age": {
                    "title": "Age diversity breakdown",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "number"
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "regional": {
                                "title": "Regional number of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "regionalPct": {
                                "title": "Regional percentage of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "national": {
                                "title": "National number of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "nationalPct": {
                                "title": "National percentage of jobs",
                                "type": "number",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "regional",
                            "regionalPct",
                            "national",
                            "nationalPct"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 1
                },
                "demographics": {
                    "title": "Demographics diversity breakdown",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "number"
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "regional": {
                                "title": "Regional number of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "regionalPct": {
                                "title": "Regional percentage of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "national": {
                                "title": "National number of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "nationalPct": {
                                "title": "National percentage of jobs",
                                "type": "number",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "regional",
                            "regionalPct",
                            "national",
                            "nationalPct"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 1
                },
                "gender": {
                    "title": "Gender diversity breakdown",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Dimension id",
                                "type": "number"
                            },
                            "name": {
                                "title": "Dimension name",
                                "type": "string",
                                "minLength": 1
                            },
                            "regional": {
                                "title": "Regional number of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "regionalPct": {
                                "title": "Regional percentage of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "national": {
                                "title": "National number of jobs",
                                "type": "number",
                                "minimum": 0
                            },
                            "nationalPct": {
                                "title": "National percentage of jobs",
                                "type": "number",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "id",
                            "name",
                            "regional",
                            "regionalPct",
                            "national",
                            "nationalPct"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 1
                }
            },
            "required": [
                "summary",
                "age",
                "demographics",
                "gender"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "searchParams",
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /skills

Get what skills are in supply and demand in specified location and occupation.

### `POST` Get skills benchmark data

Emsi aggregates job posting details, and online social profiles from all over the web. The details in this endpoint provide top skills associated with the postings and profiles matching your search.

Advanced filtering is available for this endpoint. For more details, take a look at [Advanced Filtering](#advanced-filtering) section of this documentation.





#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "title": "web developer",
  "city": "moscow id"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/request.schema.json",
    "type": "object",
    "properties": {
        "city": {
            "title": "City name to search on",
            "type": [
                "string",
                "null"
            ],
            "minLength": 1
        },
        "title": {
            "title": "Job title to search on",
            "type": "string",
            "minLength": 1
        },
        "advanced": {
            "title": "Add advanced filters for benchmark metrics",
            "type": "object",
            "properties": {
                "occupations": {
                    "title": "List of 5-digit SOC codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "skills": {
                    "title": "List of skill ids to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "counties": {
                    "title": "List of county FIPS codes to filter",
                    "description": "For version see [/meta](#meta).",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    },
                    "minItems": 1
                }
            },
            "__nodocs": true,
            "required": [
                "occupations"
            ],
            "additionalProperties": false
        }
    },
    "additionalProperties": false
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/benchmark/skills",
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
    "text": "{ \"title\": \"web developer\", \"city\": \"moscow id\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "searchParams": {
    "area": {
      "id": "34140",
      "level": "MSA",
      "name": "Moscow, ID"
    },
    "title": {
      "id": "ET35635562C89DD29C",
      "name": "Web Developers"
    },
    "occupations": [
      {
        "id": "15-1257",
        "name": "Web Developers and Digital Interface Designers"
      }
    ],
    "skills": []
  },
  "data": {
    "demand": {
      "hardSkills": [
        {
          "id": "KS1200C5XQWW78VQ5ZYL",
          "name": "PHP (Scripting Language)",
          "postings": 19
        },
        {
          "id": "KS1200771D9CR9LB4MWW",
          "name": "JavaScript (Programming Language)",
          "postings": 17
        },
        {
          "id": "KS1200578T5QCYT0Z98G",
          "name": "HyperText Markup Language (HTML)",
          "postings": 17
        },
        {
          "id": "KS121F45VPV8C9W3QFYH",
          "name": "Cascading Style Sheets (CSS)",
          "postings": 15
        },
        {
          "id": "KS441LY691MT0N689MWR",
          "name": "User Interface",
          "postings": 9
        },
        {
          "id": "KS120RM619V18NJXTHV1",
          "name": "HTML5",
          "postings": 9
        },
        {
          "id": "KS122VP5W9LZ8TRNFJY0",
          "name": "Web Design",
          "postings": 9
        },
        {
          "id": "KS6840J6LR0TLQ86LZJC",
          "name": "Front End (Software Engineering)",
          "postings": 9
        },
        {
          "id": "ES3937EEC3D5D7345412",
          "name": "Full Stack Software Engineering",
          "postings": 8
        },
        {
          "id": "KS1206Y6W7F5JS3VBTFL",
          "name": "Adobe Photoshop",
          "postings": 7
        }
      ],
      "softSkills": [
        {
          "id": "KS122556LMQ829GZCCRV",
          "name": "Communications",
          "postings": 10
        },
        {
          "id": "KS125716TLTGH6SDHJD1",
          "name": "Integration",
          "postings": 8
        },
        {
          "id": "KS1218W78FGVPVP2KXPX",
          "name": "Management",
          "postings": 6
        },
        {
          "id": "KS1253H61TTR1FZWSRH4",
          "name": "Innovation",
          "postings": 5
        },
        {
          "id": "KS1280B68GD79P4WMVYW",
          "name": "Presentations",
          "postings": 4
        },
        {
          "id": "KSMNXY6MPS1EDWJ8P6B0",
          "name": "Enthusiasm",
          "postings": 4
        },
        {
          "id": "KS125F678LV2KB3Z5XW0",
          "name": "Problem Solving",
          "postings": 4
        },
        {
          "id": "KS61D1BF7H22K0UZ9C3V",
          "name": "Team Oriented",
          "postings": 4
        },
        {
          "id": "KS1203C6N9B52QGB4H67",
          "name": "Research",
          "postings": 3
        },
        {
          "id": "ES8B03DAD3B526316ED9",
          "name": "Organizational Skills",
          "postings": 3
        }
      ]
    },
    "supply": {
      "hardSkills": [
        {
          "id": "KS121F45VPV8C9W3QFYH",
          "name": "Cascading Style Sheets (CSS)",
          "profiles": 11
        },
        {
          "id": "KS122Z36QK3N5097B5JH",
          "name": "Web Development",
          "profiles": 10
        },
        {
          "id": "KS122VP5W9LZ8TRNFJY0",
          "name": "Web Design",
          "profiles": 8
        },
        {
          "id": "KS1206Y6W7F5JS3VBTFL",
          "name": "Adobe Photoshop",
          "profiles": 8
        },
        {
          "id": "KS1200578T5QCYT0Z98G",
          "name": "HyperText Markup Language (HTML)",
          "profiles": 7
        },
        {
          "id": "KS1200771D9CR9LB4MWW",
          "name": "JavaScript (Programming Language)",
          "profiles": 6
        },
        {
          "id": "KS120RM619V18NJXTHV1",
          "name": "HTML5",
          "profiles": 5
        },
        {
          "id": "KS1207164CW5X2SJPW43",
          "name": "Adobe Creative Suite",
          "profiles": 5
        },
        {
          "id": "KS124H46Q2PP8YC1WQ06",
          "name": "Graphic Design",
          "profiles": 5
        },
        {
          "id": "KS122CZ71K19596XHQ92",
          "name": "Event Planning",
          "profiles": 5
        }
      ],
      "softSkills": [
        {
          "id": "KS124JZ5VYRZ5MJ85N2B",
          "name": "Public Speaking",
          "profiles": 9
        },
        {
          "id": "KS121Z26S4VJLQ1WXN21",
          "name": "Customer Service",
          "profiles": 8
        },
        {
          "id": "KS1203C6N9B52QGB4H67",
          "name": "Research",
          "profiles": 7
        },
        {
          "id": "KS1218W78FGVPVP2KXPX",
          "name": "Management",
          "profiles": 7
        },
        {
          "id": "KS123X777H5WFNXQ6BPM",
          "name": "Sales",
          "profiles": 6
        },
        {
          "id": "KS120PP6GL94HJDMN0TQ",
          "name": "Editing",
          "profiles": 5
        },
        {
          "id": "KS124JB619VXG6RQ810C",
          "name": "Leadership",
          "profiles": 5
        },
        {
          "id": "KS1200365FTR9X0M96T9",
          "name": "Microsoft Word",
          "profiles": 5
        },
        {
          "id": "KS120PQ6XD1JWMFQVJNW",
          "name": "Teaching",
          "profiles": 5
        },
        {
          "id": "KS126HY6YLTB9R7XJC4Z",
          "name": "Microsoft Office",
          "profiles": 5
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


<div data-tab="401">

You don't have access to the endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "title": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

Could not normalize title 'invalid'.


```json
{
  "errors": [
    {
      "status": 404,
      "title": "Not Found",
      "detail": "Could not normalize title 'invalid'"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/skills.schema.json",
    "definitions": {
        "demand-items": {
            "type": "object",
            "properties": {
                "id": {
                    "title": "Dimension id",
                    "type": "string",
                    "minLength": 1
                },
                "name": {
                    "title": "Dimension name",
                    "type": "string",
                    "minLength": 1
                },
                "postings": {
                    "title": "Number of unique postings",
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": [
                "id",
                "name",
                "postings"
            ],
            "additionalProperties": false
        },
        "supply-items": {
            "type": "object",
            "properties": {
                "id": {
                    "title": "Dimension id",
                    "type": "string",
                    "minLength": 1
                },
                "name": {
                    "title": "Dimension name",
                    "type": "string",
                    "minLength": 1
                },
                "profiles": {
                    "title": "Number of unique profiles",
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": [
                "id",
                "name",
                "profiles"
            ],
            "additionalProperties": false
        }
    },
    "type": "object",
    "properties": {
        "searchParams": {
            "title": "Normalized search parameters",
            "type": "object",
            "properties": {
                "area": {
                    "title": "Normalized area info",
                    "description": "This field will return a list of area objects if `advanced` filter was used. Otherwise, it will be an area object.",
                    "type": [
                        "object",
                        "array"
                    ],
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Normalized area id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Normalized area name",
                                "type": "string",
                                "minLength": 1
                            },
                            "level": {
                                "title": "Normalized area level",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "__nodocs": true,
                        "required": [
                            "id",
                            "name",
                            "level"
                        ],
                        "additionalProperties": false
                    },
                    "properties": {
                        "id": {
                            "title": "Normalized area id",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized area name",
                            "type": "string",
                            "minLength": 1
                        },
                        "level": {
                            "title": "Normalized area level",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name",
                        "level"
                    ],
                    "additionalProperties": false
                },
                "title": {
                    "title": "Normalized Emsi title",
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "id": {
                            "title": "Normalized Emsi title id",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "name": {
                            "title": "Normalized Emsi title name",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name"
                    ],
                    "additionalProperties": false
                },
                "occupations": {
                    "title": "Occupations mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "5-digit SOC id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "5-digit SOC name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "Skills mapped to the normalized title",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Emsi skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Emsi skill name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    }
                }
            },
            "required": [
                "area",
                "title",
                "occupations",
                "skills"
            ],
            "additionalProperties": false
        },
        "data": {
            "title": "Skills benchmark data",
            "type": "object",
            "properties": {
                "demand": {
                    "type": "object",
                    "properties": {
                        "hardSkills": {
                            "title": "List of top Hard skills",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "title": "Dimension id",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "Dimension name",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "postings": {
                                        "title": "Number of unique postings",
                                        "type": "integer",
                                        "minimum": 0
                                    }
                                },
                                "required": [
                                    "id",
                                    "name",
                                    "postings"
                                ],
                                "additionalProperties": false
                            }
                        },
                        "softSkills": {
                            "title": "List of top Soft skills",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "title": "Dimension id",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "Dimension name",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "postings": {
                                        "title": "Number of unique postings",
                                        "type": "integer",
                                        "minimum": 0
                                    }
                                },
                                "required": [
                                    "id",
                                    "name",
                                    "postings"
                                ],
                                "additionalProperties": false
                            }
                        }
                    },
                    "required": [
                        "hardSkills",
                        "softSkills"
                    ],
                    "additionalProperties": false
                },
                "supply": {
                    "type": "object",
                    "properties": {
                        "hardSkills": {
                            "title": "List of top Hard skills",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "title": "Dimension id",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "Dimension name",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "profiles": {
                                        "title": "Number of unique profiles",
                                        "type": "integer",
                                        "minimum": 0
                                    }
                                },
                                "required": [
                                    "id",
                                    "name",
                                    "profiles"
                                ],
                                "additionalProperties": false
                            }
                        },
                        "softSkills": {
                            "title": "List of top Soft skills",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "title": "Dimension id",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "Dimension name",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "profiles": {
                                        "title": "Number of unique profiles",
                                        "type": "integer",
                                        "minimum": 0
                                    }
                                },
                                "required": [
                                    "id",
                                    "name",
                                    "profiles"
                                ],
                                "additionalProperties": false
                            }
                        }
                    },
                    "required": [
                        "hardSkills",
                        "softSkills"
                    ],
                    "additionalProperties": false
                }
            },
            "required": [
                "demand",
                "supply"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "searchParams",
        "data"
    ],
    "additionalProperties": false
}
```

</div>

</div>

