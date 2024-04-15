# Companies API
#### v1.0.0

##### Information on past releases can be found in the [Changelog](/updates/companies-api-changelog).

> **Note:** By default, all clients are allowed a maximum of 5 requests per second. Contact us [here](mailto:api-support@emsibg.com) if you need an adjustment.

## Overview
Emsi companies is a comprehensive library of companies defined by Emsi.

This API exposes the complete collection of Emsi companies, which includes curated industry and staffing information along with other metadata for each company, and normalization functionality to transform raw company names to Emsi companies.

### Content type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the companies API, you must request an OAuth bearer token with the scope `emsi_open`.

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
          "value": "emsi_open"
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

By default all clients have specific endpoint quotas of 10 requests per year, their quota can be changed through Emsi Auth claims (see below). For more detail on the quota system see our [Emsi Auth Quota](/guides/emsi-auth-quota) document.

**/versions/{verison}/normalize** <br> **/versions/{version}/normalize/inspect** <br> **/versions/{version}/normalize/bulk**

A client's rate-limit (default 5 per second) can be changed through a `companies:rate-limit` Emsi Auth claim. To increase a client's limit to 20 per second use `companies:rate-limit:20/1` and to grant them unlimited access use `companies:rate-limit:unlimited`.

A client's normalize quota can be changed through a `companies:normalize:quota` Emsi Auth claim. To increase a client's monthly quota to 100 per month use `companies:normalize:quota:100/month` and to grant them unlimited access use `companies:normalize:quota:unlimited`.

**Access Claims**:

**`companies:full_access`**
* Grants access to `/versions/{verison}/normalize`

**`companies:normalize:bulk`**
* Grants access to `/versions/{version}/normalize/bulk`

</div>

## /status

Health check endpoint.

### `GET` Get service status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/companies/status",
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

Get info on latest version, and attribution text.

### `GET` Get service metadata

Get service metadata, including latest version, and attribution text. Caching is encouraged, but the metadata can change weekly.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/companies/meta",
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
      "title": "Emsi Companies",
      "body": "Emsi companies is a comprehensive library of companies defined by Emsi."
    },
    "latestVersion": "1.42"
  }
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "$id": "responses/meta.schema.json",
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
                "latestVersion": {
                    "title": "Latest company version available in the service",
                    "type": "string",
                    "minLength": 1
                }
            },
            "required": [
                "attribution",
                "latestVersion"
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



## /versions

A list of available company versions.

### `GET` List all versions

Version `latest` can be used as an alias to the latest company version.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/companies/versions",
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
    "1.42",
    "1.41",
    "1.40"
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/versions.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "List of available company versions",
            "type": "array",
            "items": {
                "type": "string",
                "__nodocs": true
            },
            "minItems": 1
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



## /versions/{version}

Version specific metadata.

### `GET` Get version metadata

Get version specific metadata including available fields and data versions.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The company version.<br>Example: `latest`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/companies/versions/latest",
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
    "version": "1.39",
    "fields": [
      "id",
      "name",
      "naics",
      "isStaffing",
      "isFortune1000"
    ]
  }
}
```


</div>


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "company": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: invaildVersion"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/version-meta.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Version specific meta data object",
            "type": "object",
            "properties": {
                "version": {
                    "title": "Company version number",
                    "type": "string",
                    "minLength": 1
                },
                "fields": {
                    "title": "List of available values for fields query parameter",
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
                "version",
                "fields"
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



## /versions/{version}/companies

Returns a list of all companies in {version} sorted by company id.

### `GET` List all companies




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The company version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of companies to search for.<br>This parameter is optional.<br>Example: `Amazon`
<code>fields</code><div class="type">string</div> | List of fields to return per company. See [/versions/{version}](#versions-version) for available fields.<br>This parameter is optional.<br>Default: `id,name`
<code>limit</code><div class="type">integer</div> | Limit the number of companies returned in the response.<br>This parameter is optional.<br>Minimum: `1`<br>Maximum: `1000`<br>Default: `10`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/companies/versions/latest/companies",
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
      "value": "Amazon"
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
      "id": "9",
      "name": "MISCELLANEOUS FOREIGN CONTRACTORS",
      "naics": "238990",
      "isStaffing": true,
      "isFortune1000": false
    },
    {
      "id": "12",
      "name": "Adecco",
      "naics": "561311",
      "isStaffing": true,
      "isFortune1000": false
    },
    {
      "id": "20",
      "name": "Amazon",
      "naics": "454110",
      "isStaffing": false,
      "isFortune1000": true
    }
  ]
}
```


</div>


<div data-tab="400">

Invalid request.


```json
{
  "errors": [
    {
      "status": 400,
      "company": "Invalid request",
      "detail": "Invalid request body"
    }
  ]
}
```


</div>


<div data-tab="401">

You don't have access to the normalization endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "company": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "company": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: invaildVersion"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/companies.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Company search response object",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Company id",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1
                    },
                    "name": {
                        "title": "Company name",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1
                    },
                    "naics": {
                        "title": "naics code",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1
                    },
                    "isStaffing": {
                        "title": "Shows if company is currently hiring",
                        "type": "boolean"
                    },
                    "isFortune1000": {
                        "title": "Shows if company is among fortune 1000",
                        "type": "boolean"
                    }
                }
            }
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




### `POST` List requested companies




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The company version.<br>Example: `latest`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    "20"
  ],
  "fields": [
    "id",
    "name",
    "naics",
    "isStaffing",
    "isFortune1000"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/companies-lookup.schema.json",
    "type": "object",
    "properties": {
        "ids": {
            "title": "Company ids",
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ],
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1
        },
        "fields": {
            "title": "List of fields to return per company",
            "description": "See [/versions/{version}](#versions-version) for available fields.",
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1,
            "default": [
                "id",
                "name"
            ]
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
  "url": "https://emsiservices.com/companies/versions/latest/companies",
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
    "text": "{ \"ids\": [ \"20\" ], \"fields\": [ \"id\", \"name\", \"naics\", \"isStaffing\", \"isFortune1000\" ] }"
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
      "id": "20",
      "name": "Amazon",
      "naics": "454110",
      "isStaffing": false,
      "isFortune1000": true
    }
  ]
}
```


</div>


<div data-tab="400">

Invalid request.


```json
{
  "errors": [
    {
      "status": 400,
      "company": "Invalid request",
      "detail": "Invalid request body"
    }
  ]
}
```


</div>


<div data-tab="401">

You don't have access to the normalization endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "company": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "company": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: invaildVersion"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/companies.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Company search response object",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Company id",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1
                    },
                    "name": {
                        "title": "Company name",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1
                    },
                    "naics": {
                        "title": "naics code",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1
                    },
                    "isStaffing": {
                        "title": "Shows if company is currently hiring",
                        "type": "boolean"
                    },
                    "isFortune1000": {
                        "title": "Shows if company is among fortune 1000",
                        "type": "boolean"
                    }
                }
            }
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



## /versions/{version}/companies/{companyId}

Returns information about a specific company.

### `GET` Get a company by ID




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The company version.<br>Example: `latest`
<code>companyId</code><div class="type">string</div> | Company id<br>Example: `20`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/companies/versions/latest/companies/20",
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
    "id": "20",
    "name": "Amazon",
    "naics": "454110",
    "isStaffing": false,
    "isFortune1000": true
  }
}
```


</div>


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "company": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: invaildVersion"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/single-company-lookup.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Single company search response object",
            "type": "object",
            "properties": {
                "id": {
                    "title": "Company id",
                    "type": [
                        "string",
                        "null"
                    ],
                    "minLength": 1
                },
                "name": {
                    "title": "Company name",
                    "type": [
                        "string",
                        "null"
                    ],
                    "minLength": 1
                },
                "naics": {
                    "title": "naics code",
                    "type": [
                        "string",
                        "null"
                    ],
                    "minLength": 1
                },
                "isStaffing": {
                    "title": "Shows if company is currently hiring",
                    "type": "boolean"
                },
                "isFortune1000": {
                    "title": "Shows if company is among fortune 1000",
                    "type": "boolean"
                }
            },
            "required": [
                "id",
                "name",
                "naics",
                "isStaffing",
                "isFortune1000"
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



## /versions/{version}/normalize

Normalize a raw company string to the best matching Emsi company.

Supported document types and their expected Content-Type (**Document must be UTF-8 encoded.**):
  * JSON – `application/json`
  * Plain text – `text/plain`

Raw company size is limited to 1kB.

Note that this endpoint has a base tier yearly quota of 10 requests. [Contact us](mailto:api-support@emsibg.com) if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, `RateLimit-Remaining` and `RateLimit-Reset`, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.


### `POST` Normalize a company

> This endpoint requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to normalization.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The company version.<br>Example: `latest`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "term": "Amazon AWS",
  "fields": [
    "id",
    "name",
    "isStaffing",
    "isFortune1000",
    "naics"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/normalize.schema.json",
    "type": "object",
    "properties": {
        "term": {
            "title": "Company name",
            "type": "string",
            "minLength": 1
        },
        "fields": {
            "title": "List of fields to return per company",
            "description": "See [/versions/{version}](#versions-version) for available fields.",
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1,
            "default": [
                "id",
                "name"
            ]
        }
    },
    "required": [
        "term"
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
  "url": "https://emsiservices.com/companies/versions/latest/normalize",
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
    "text": "{ \"term\": \"Amazon AWS\", \"fields\": [ \"id\", \"name\", \"isStaffing\", \"isFortune1000\", \"naics\" ] }"
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
    "company": {
      "id": "20",
      "name": "Amazon",
      "naics": "454110",
      "isStaffing": false,
      "isFortune1000": true
    }
  }
}
```


</div>


<div data-tab="400">

Invalid request.


```json
{
  "errors": [
    {
      "status": 400,
      "company": "Invalid request",
      "detail": "Invalid request body"
    }
  ]
}
```


</div>


<div data-tab="401">

You don't have access to the normalization endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "company": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "company": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: invaildVersion"
    }
  ]
}
```


</div>


<div data-tab="413">

Request size too large.


```json
{
  "errors": [
    {
      "detail": "Request size too large",
      "status": 413,
      "company": "Payload Too Large"
    }
  ]
}
```


</div>


<div data-tab="415">

Unsupported Content Type.


```json
{
  "errors": [
    {
      "detail": "Accepted Content-Type(s): 'application/json', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'",
      "status": 415,
      "company": "Unsupported Content Type"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/normalize.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Company normalize response object",
            "type": "object",
            "properties": {
                "company": {
                    "title": "Normalized company",
                    "type": "object",
                    "properties": {
                        "id": {
                            "title": "Company id",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "name": {
                            "title": "Company name",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "naics": {
                            "title": "naics code",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1
                        },
                        "isStaffing": {
                            "title": "Shows if company is currently hiring",
                            "type": "boolean"
                        },
                        "isFortune1000": {
                            "title": "Shows if company is among fortune 1000",
                            "type": "boolean"
                        }
                    },
                    "additionalProperties": false
                }
            },
            "required": [
                "company"
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



## /versions/{version}/normalize/inspect

Normalize a raw company string to a list of the top matching Emsi companies.

Supported document types and their expected Content-Type (**Document must be UTF-8 encoded.**):
  * JSON – `application/json`
  * Plain text – `text/plain`

Raw company size is limited to 1kB.

Note that this endpoint has a base tier yearly quota of 10 requests. [Contact us](mailto:api-support@emsibg.com) if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, `RateLimit-Remaining` and `RateLimit-Reset`, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.


### `POST` Inspect company normalization




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The company version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>limit</code><div class="type">integer</div> | Limit the number of normalized companies for the given term (this query param does not apply for JSON requests).<br>Minimum: `1`<br>Maximum: `100`<br>Default: `5`
<code>fields</code><div class="type">string</div> | List of fields to return per title. See [/versions/{version}](#versions-version) for available fields (this query param does not apply for JSON requests).<br>This parameter is optional.<br>Default: `id,name`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "term": "Google Inc.",
  "limit": 2,
  "fields": [
    "id",
    "name",
    "isStaffing",
    "isFortune1000",
    "naics"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/inspect-normalize.schema.json",
    "type": "object",
    "properties": {
        "term": {
            "title": "Company name",
            "type": "string",
            "minLength": 1
        },
        "fields": {
            "title": "List of fields to return per company",
            "description": "See [/versions/{version}](#versions-version) for available fields.",
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1,
            "default": [
                "id",
                "name"
            ]
        },
        "limit": {
            "title": "Limit the number of normalized companies for the given term",
            "type": "integer",
            "minimum": 1,
            "maximum": 100,
            "default": 5
        }
    },
    "required": [
        "term"
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
  "url": "https://emsiservices.com/companies/versions/latest/normalize/inspect",
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
    "text": "{ \"term\": \"Google Inc.\", \"limit\": 2, \"fields\": [ \"id\", \"name\", \"isStaffing\", \"isFortune1000\", \"naics\" ] }"
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
      "company": {
        "id": "16932009",
        "name": "Google",
        "naics": "519130",
        "isStaffing": false,
        "isFortune1000": false
      }
    }
  ]
}
```


</div>


<div data-tab="400">

Invalid request.


```json
{
  "errors": [
    {
      "status": 400,
      "company": "Invalid request",
      "detail": "Invalid request body"
    }
  ]
}
```


</div>


<div data-tab="401">

You don't have access to the normalization endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "company": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "company": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: invaildVersion"
    }
  ]
}
```


</div>


<div data-tab="413">

Request size too large.


```json
{
  "errors": [
    {
      "detail": "Request size too large",
      "status": 413,
      "company": "Payload Too Large"
    }
  ]
}
```


</div>


<div data-tab="415">

Unsupported Content Type.


```json
{
  "errors": [
    {
      "detail": "Accepted Content-Type(s): 'application/json', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'",
      "status": 415,
      "company": "Unsupported Content Type"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/inspect-normalize.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Company normalize response object",
            "type": "array",
            "items": {
                "title": "Company normalize response object",
                "type": "object",
                "properties": {
                    "company": {
                        "title": "Normalized company",
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Company id",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1
                            },
                            "name": {
                                "title": "Company name",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1
                            },
                            "naics": {
                                "title": "naics code",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1
                            },
                            "isStaffing": {
                                "title": "Shows if company is currently hiring",
                                "type": "boolean"
                            },
                            "isFortune1000": {
                                "title": "Shows if company is among fortune 1000",
                                "type": "boolean"
                            }
                        },
                        "additionalProperties": false
                    }
                },
                "required": [
                    "company"
                ],
                "additionalProperties": false
            }
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



## /versions/{version}/normalize/bulk

Normalize multiple raw company strings to a list of best matching Emsi companies.

Supported document types and their expected Content-Type (**Document must be UTF-8 encoded.**):
  * JSON – `application/json`
  * Plain text – `text/plain`

There is a limit of 500 companies per request.

Raw company size is limited to 1kB per company.


### `POST` Normalize companies in bulk

> This endpoint requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to bulk normalization.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The company version.<br>Example: `latest`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "terms": [
    "Amazon Go",
    "Alphabet Inc."
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/bulk-normalize.schema.json",
    "type": "object",
    "properties": {
        "terms": {
            "title": "List of terms to normalize",
            "description": "Maximum number of terms: `500`",
            "type": "array",
            "items": {
                "title": "Company name",
                "type": "string",
                "minLength": 1
            },
            "minItems": 1
        },
        "fields": {
            "title": "List of fields to return per company",
            "description": "See [/versions/{version}](#versions-version) for available fields.",
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1,
            "default": [
                "id",
                "name"
            ]
        }
    },
    "required": [
        "terms"
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
  "url": "https://emsiservices.com/companies/versions/latest/normalize/bulk",
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
    "text": "{ \"terms\": [ \"Amazon Go\", \"Alphabet Inc.\" ] }"
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
      "company": {
        "id": "3B93055220D592C8",
        "name": "Emsi Burning Glass",
        "isStaffing": true,
        "isFortune1000": false,
        "naics": "1234"
      },
      "term": "Emsi Burning Glass"
    },
    {
      "company": {
        "id": "3B93088220D592C8",
        "name": "Google Inc.",
        "isStaffing": true,
        "isFortune1000": true,
        "naics": "1234"
      },
      "term": "Google Inc."
    }
  ]
}
```


</div>


<div data-tab="400">

Invalid request.


```json
{
  "errors": [
    {
      "status": 400,
      "company": "Invalid request",
      "detail": "Invalid request body"
    }
  ]
}
```


</div>


<div data-tab="401">

You don't have access to bulk normalize endpoint.


```json
{
  "errors": [
    {
      "status": 401,
      "company": "Unauthorized",
      "detail": "You do not have access to this endpoint, please contact us at 'api-support@emsibg.com' to request access."
    }
  ]
}
```


</div>


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "company": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: invaildVersion"
    }
  ]
}
```


</div>


<div data-tab="413">

Request size too large.


```json
{
  "errors": [
    {
      "detail": "Request size too large",
      "status": 413,
      "company": "Payload Too Large"
    }
  ]
}
```


</div>


<div data-tab="415">

Unsupported Content Type.


```json
{
  "errors": [
    {
      "detail": "Accepted Content-Type(s): 'application/json', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'",
      "status": 415,
      "company": "Unsupported Content Type"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/bulk-normalize.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "List of normalized object response",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {
                        "title": "Normalized company",
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Company id",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1
                            },
                            "name": {
                                "title": "Company name",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1
                            },
                            "naics": {
                                "title": "naics code",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1
                            },
                            "isStaffing": {
                                "title": "Shows if company is currently hiring",
                                "type": "boolean"
                            },
                            "isFortune1000": {
                                "title": "Shows if company is among fortune 1000",
                                "type": "boolean"
                            }
                        },
                        "additionalProperties": false
                    },
                    "term": {
                        "title": "Original term of the normalized company",
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": [
                    "company",
                    "term"
                ],
                "additionalProperties": false
            }
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
