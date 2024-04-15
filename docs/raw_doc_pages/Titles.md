# Titles API
#### v1.11.0

##### Information on past releases can be found in the [Changelog](/updates/titles-api-changelog).

## Overview
Emsi Titles is a comprehensive library of job titles defined by Emsi.

This API exposes the complete collection of Emsi titles which includes curated occupation and skill mappings for each title and normalization functionality to transform raw job titles to Emsi titles.

### Content type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the Titles API, you must request an OAuth bearer token with the scope `emsi_open`.

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

By default all clients have specific endpoint quotas of 50 requests per year, their quota can be changed through Emsi Auth claims (see below). For more detail on the quota system see our [Emsi Auth Quota](/guides/emsi-auth-quota) document.

**/versions/{verison}/normalize** <br> **/versions/{version}/normalize/inspect** <br> **/versions/{version}/normalize/bulk**

A client's normalize quota can be changed through a `titles:normalize:quota` Emsi Auth claim. To increase a client's monthly quota to 100 per month use `titles:normalize:quota:100/month`, to grant them unlimited access use `titles:normalize:quota:unlimited`.

**Access Claims**:

**`titles:full_access`**
* Grants access to `/versions/{verison}/normalize` and `/versions/{verison}/titles/mappings`
* Grants access to `mapping` field in each endpoint

**`titles:normalize:bulk`**
* Grants access to `/versions/{version}/normalize/bulk`

</div>

## /status

Health check endpoint

### `GET` Get service status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/titles/status",
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
  "url": "https://emsiservices.com/titles/meta",
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
      "body": "Emsi Titles is a comprehensive library of job titles defined by Emsi.",
      "title": "Emsi Titles"
    },
    "latestVersion": "4.0"
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
                    "title": "Latest title version available in the service",
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

A list of available title versions

### `GET` List all versions

Version `latest` can be used as an alias to the latest title version. See our [Titles Classification Changelog](/updates/titles-classification-changelog) for version updates.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/titles/versions",
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
    "4.0"
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
            "title": "List of available title versions",
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

Version specific metadata

### `GET` Get version metadata

Get version specific metadata including available fields, data versions, title counts and removed title counts.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/titles/versions/latest",
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
    "version": "4.0",
    "fields": [
      "mapping",
      "id",
      "pluralName",
      "name"
    ],
    "mappingVersions": {
      "soc": [
        "soc_emsi_2019"
      ],
      "skill": [
        "7.24"
      ]
    },
    "titleCount": 75952,
    "removedTitleCount": 50
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
      "title": "URL not found",
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
                    "title": "Title version number",
                    "type": "string",
                    "minLength": 1
                },
                "titleCount": {
                    "title": "Total number of available titles",
                    "type": "integer",
                    "minimum": 0
                },
                "removedTitleCount": {
                    "title": "Total number of removed titles",
                    "type": "integer",
                    "minimum": 0
                },
                "mappingVersions": {
                    "title": "Skills and SOC codes mapping for titles",
                    "type": "object",
                    "properties": {
                        "soc": {
                            "title": "Available SOC code version for mapping",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            },
                            "minItems": 1
                        },
                        "skill": {
                            "title": "Available skill version for mapping",
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
                        "soc",
                        "skill"
                    ],
                    "additionalProperties": false
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
                "titleCount",
                "removedTitleCount",
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



## /versions/{version}/changes

Version specific changes

### `GET` Get version changes

Get version specific changes.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The titles classification version.<br>Example: `latest`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/titles/versions/latest/changes",
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
    "additions": [
      {
        "id": "ET72E64338B77E4585",
        "title": "Stock Taker"
      }
    ],
    "removals": [
      {
        "id": "ET4184BC17C5F67F27",
        "title": "PM Manager"
      }
    ],
    "alterations": [
      {
        "id": "ETCD7750DD30D06DBE",
        "title": "Crater"
      }
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
      "title": "URL not found",
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
    "$id": "responses/changes.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Categorized title version changes",
            "type": "object",
            "properties": {
                "additions": {
                    "title": "List of newly added titles",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "title": "New title name",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "New title id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "title",
                            "id"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
                },
                "removals": {
                    "title": "List of removed titles",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "title": "Removed title name",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "Removed title id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "title",
                            "id"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
                },
                "alterations": {
                    "title": "List of altered titles",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "title": "title name",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "title id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "title",
                            "id"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
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



## /versions/{version}/titles

Returns a list of all titles in {version} sorted by title name

### `GET` List all titles

> Requesting title mappings requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of title names to search for.<br>This parameter is optional.<br>Example: `.NET`
<code>fields</code><div class="type">string</div> | List of fields to return per title. See [/versions/{version}](#versions-version) for available fields. </br>`mappings` require additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.<br>This parameter is optional.<br>Default: `id,name`
<code>limit</code><div class="type">integer</div> | Limit the number of titles returned in the response.<br>This parameter is optional.<br>Example: `5`
<code>page</code><div class="type">integer</div> | Paginate the response and choose which page to return.<br>This parameter is optional.<br>Example: `2`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/titles/versions/latest/titles",
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
      "value": ".NET"
    },
    {
      "name": "limit",
      "value": "5"
    },
    {
      "name": "page",
      "value": "2"
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
      "id": "ETB9638ED17EEBE37D",
      "name": "Networker"
    },
    {
      "id": "ETAC9C14767C0F125C",
      "name": "Network Engineer/Network Administrator"
    },
    {
      "id": "ET02716A0AE13432E8",
      "name": "Networking Technician"
    },
    {
      "id": "ET057AF8DAB081D057",
      "name": "Network Designer"
    },
    {
      "id": "ET06255061AE3134B8",
      "name": "Network Lead"
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
      "title": "Invalid request",
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
      "title": "Unauthorized",
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
      "title": "URL not found",
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
    "$id": "responses/titles.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Title search response object",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Title id",
                        "type": "string",
                        "minLength": 1
                    },
                    "name": {
                        "title": "Title name",
                        "type": "string",
                        "minLength": 1
                    },
                    "pluralName": {
                        "title": "Plural form of title name",
                        "type": "string",
                        "minLength": 1
                    },
                    "mapping": {
                        "title": "Title SOC and skill mappings",
                        "type": "object",
                        "properties": {
                            "names": {
                                "title": "List of mapping names",
                                "description": "Mapping names are included in Titles v4.6 and onward.\n\nTitles may have zero or more mappings associated with them, the names of those mappings are listed here and represented in the unified list of skills and socs below.",
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "minLength": 1,
                                    "__nodocs": true
                                }
                            },
                            "socs": {
                                "title": "List of SOC mappings",
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "title": "SOC code",
                                            "type": "string",
                                            "minLength": 1
                                        },
                                        "name": {
                                            "title": "SOC name",
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
                                "title": "List of skill mappings",
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "title": "Skill id",
                                            "type": "string",
                                            "minLength": 1
                                        },
                                        "name": {
                                            "title": "Skill name",
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
                            "socs",
                            "skills",
                            "names"
                        ],
                        "additionalProperties": false
                    },
                    "isSupervisor": {
                        "title": "Boolean value indicating whether the title's role is supervisory",
                        "type": "boolean",
                        "__internal": true
                    },
                    "levelBand": {
                        "title": "Standardized job level category",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1,
                        "__internal": true
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




### `POST` List requested titles

> Requesting title mappings requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    "ET89954A897A9A69C4",
    "ET3B93055220D592C8",
    "ET28D75166A2288ED3"
  ],
  "fields": [
    "id",
    "name",
    "pluralName"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/titles-lookup.schema.json",
    "type": "object",
    "properties": {
        "ids": {
            "title": "Title ids",
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1
        },
        "fields": {
            "title": "List of fields to return per title",
            "description": "See [/versions/{version}](#versions-version) for available fields.\n\n`mappings` require additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.",
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
  "url": "https://emsiservices.com/titles/versions/latest/titles",
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
    "text": "{ \"ids\": [ \"ET89954A897A9A69C4\", \"ET3B93055220D592C8\", \"ET28D75166A2288ED3\" ], \"fields\": [ \"id\", \"name\", \"pluralName\" ] }"
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
      "id": "ET89954A897A9A69C4",
      "pluralName": "Computer Scientists",
      "name": "Computer Scientist"
    },
    {
      "id": "ET3B93055220D592C8",
      "pluralName": "Data Scientists",
      "name": "Data Scientist"
    },
    {
      "id": "ET28D75166A2288ED3",
      "pluralName": "Scientists",
      "name": "Scientist"
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
      "title": "Invalid request",
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
      "title": "Unauthorized",
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
      "title": "URL not found",
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
    "$id": "responses/titles.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Title search response object",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Title id",
                        "type": "string",
                        "minLength": 1
                    },
                    "name": {
                        "title": "Title name",
                        "type": "string",
                        "minLength": 1
                    },
                    "pluralName": {
                        "title": "Plural form of title name",
                        "type": "string",
                        "minLength": 1
                    },
                    "mapping": {
                        "title": "Title SOC and skill mappings",
                        "type": "object",
                        "properties": {
                            "names": {
                                "title": "List of mapping names",
                                "description": "Mapping names are included in Titles v4.6 and onward.\n\nTitles may have zero or more mappings associated with them, the names of those mappings are listed here and represented in the unified list of skills and socs below.",
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "minLength": 1,
                                    "__nodocs": true
                                }
                            },
                            "socs": {
                                "title": "List of SOC mappings",
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "title": "SOC code",
                                            "type": "string",
                                            "minLength": 1
                                        },
                                        "name": {
                                            "title": "SOC name",
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
                                "title": "List of skill mappings",
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "title": "Skill id",
                                            "type": "string",
                                            "minLength": 1
                                        },
                                        "name": {
                                            "title": "Skill name",
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
                            "socs",
                            "skills",
                            "names"
                        ],
                        "additionalProperties": false
                    },
                    "isSupervisor": {
                        "title": "Boolean value indicating whether the title's role is supervisory",
                        "type": "boolean",
                        "__internal": true
                    },
                    "levelBand": {
                        "title": "Standardized job level category",
                        "type": [
                            "string",
                            "null"
                        ],
                        "minLength": 1,
                        "__internal": true
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



## /versions/{version}/titles/{titleId}

Returns information about a specific title

### `GET` Get a title by ID

> Requesting title mappings requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`
<code>titleId</code><div class="type">string</div> | Title id.<br>Example: `ET89954A897A9A69C4`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/titles/versions/latest/titles/ET89954A897A9A69C4",
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
    "id": "ET89954A897A9A69C4",
    "name": "Computer Scientist",
    "pluralName": "Computer Scientists",
    "mapping": {
      "names": [
        "Computer and Information Scientists"
      ],
      "skills": [
        {
          "id": "KS1226Y6DNDT05G7FJ4J",
          "name": "Computer Science"
        }
      ],
      "socs": [
        {
          "id": "15-1221",
          "name": "Computer and Information Research Scientists"
        }
      ]
    },
    "removedVersion": null,
    "addedVersion": "1"
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
      "title": "URL not found",
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
    "$id": "responses/single-title-search.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Single title search response object",
            "type": "object",
            "properties": {
                "id": {
                    "title": "Title id",
                    "type": "string",
                    "minLength": 1
                },
                "name": {
                    "title": "Title name",
                    "type": "string",
                    "minLength": 1
                },
                "pluralName": {
                    "title": "Plural form of title name",
                    "type": "string",
                    "minLength": 1
                },
                "mapping": {
                    "title": "Title SOC and skill mappings",
                    "type": "object",
                    "properties": {
                        "names": {
                            "title": "List of mapping names",
                            "description": "Mapping names are included in Titles v4.6 and onward.\n\nTitles may have zero or more mappings associated with them, the names of those mappings are listed here and represented in the unified list of skills and socs below.",
                            "type": "array",
                            "items": {
                                "type": "string",
                                "minLength": 1,
                                "__nodocs": true
                            }
                        },
                        "socs": {
                            "title": "List of SOC mappings",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "title": "SOC code",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "SOC name",
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
                            "title": "List of skill mappings",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "title": "Skill id",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "Skill name",
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
                        "socs",
                        "skills",
                        "names"
                    ],
                    "additionalProperties": false
                },
                "isSupervisor": {
                    "title": "Boolean value indicating whether the title's role is supervisory",
                    "type": "boolean",
                    "__internal": true
                },
                "levelBand": {
                    "title": "Standardized job level category",
                    "type": [
                        "string",
                        "null"
                    ],
                    "minLength": 1,
                    "__internal": true
                },
                "removedVersion": {
                    "title": "Version when the title was removed",
                    "description": "`null` if the title has not been removed.",
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "addedVersion": {
                    "title": "Version when the title was added",
                    "type": "string"
                }
            },
            "required": [
                "id",
                "name",
                "pluralName",
                "removedVersion",
                "addedVersion"
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



## /versions/{version}/titles/mappings

Returns a list of all job title mappings in {version}

### `GET` List all mappings

> This endpoint requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of mapping names to search for.<br>This parameter is optional.<br>Example: `.NET Developers`
<code>limit</code><div class="type">integer</div> | Limit the number of mappings returned in the response.<br>This parameter is optional.<br>Example: `5`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/titles/versions/latest/titles/mappings",
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
      "value": ".NET Developers"
    },
    {
      "name": "limit",
      "value": "5"
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
      "name": ".NET Developers",
      "skills": [
        {
          "id": "KS1200B62W5ZF38RJ7TD",
          "name": ".NET Framework"
        }
      ],
      "socs": [
        {
          "id": "15-1256",
          "name": "Software Developers and Software Quality Assurance Analysts and Testers"
        }
      ]
    },
    {
      "name": "Visual Basic .NET Developers",
      "skills": [
        {
          "id": "KS126JW72Q0ST3JKR5K0",
          "name": "Visual Basic .NET (Programming Language)"
        }
      ],
      "socs": [
        {
          "id": "15-1256",
          "name": "Software Developers and Software Quality Assurance Analysts and Testers"
        }
      ]
    },
    {
      "name": ".NET Analysts",
      "skills": [
        {
          "id": "KS1200B62W5ZF38RJ7TD",
          "name": ".NET Framework"
        }
      ],
      "socs": [
        {
          "id": "15-1211",
          "name": "Computer Systems Analysts"
        }
      ]
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
      "title": "Invalid request",
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
      "title": "Unauthorized",
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
      "title": "URL not found",
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
    "$id": "responses/mappings.schema.json",
    "type": "object",
    "properties": {
        "data": {
            "title": "Mappings search response object",
            "description": "Unique list of mappings associated with a particular title search. Mapping names are included in Titles v4.6 and onward.",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "title": "Mapping name",
                        "type": "string",
                        "minLength": 1
                    },
                    "socs": {
                        "title": "List of SOC mappings",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "title": "SOC code",
                                    "type": "string",
                                    "minLength": 1
                                },
                                "name": {
                                    "title": "SOC name",
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
                        "title": "List of skill mappings",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "title": "Skill id",
                                    "type": "string",
                                    "minLength": 1
                                },
                                "name": {
                                    "title": "Skill name",
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
                    "socs",
                    "skills",
                    "name"
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



## /versions/{version}/normalize

Normalize a raw job title string to the best matching Emsi title

Supported document types and their expected Content-Type (**Document must be UTF-8 encoded.**):
  * JSON – `application/json`
  * Plain text – `text/plain`

Raw title size is limited to 1kB.

Note that this endpoint has a base tier yearly quota of 50 requests. [Contact us](mailto:api-support@emsibg.com) if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, `RateLimit-Remaining` and `RateLimit-Reset`, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.


### `POST` Normalize a title

> This endpoint requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to normalization.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>confidenceThreshold</code><div class="type">number</div> | Filter out titles with a confidence value lower than this threshold (this query param does not apply for JSON requests).<br>Minimum: `0`<br>Maximum: `1`<br>Default: `0.5`
<code>fields</code><div class="type">string</div> | List of fields to return per title. See [/versions/{version}](#versions-version) for available fields (this query param does not apply for JSON requests).<br>This parameter is optional.<br>Default: `id,name`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "term": "data scientist"
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
            "title": "Title name",
            "type": "string",
            "minLength": 1
        },
        "fields": {
            "title": "List of fields to return per title",
            "description": "See [/versions/{version}](#versions-version) for available fields.\n\n`mappings` require additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.",
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
        "confidenceThreshold": {
            "title": "Filter out normalized titles with a confidence value lower than this threshold",
            "type": "number",
            "default": 0.5,
            "minimum": 0,
            "maximum": 1
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
  "url": "https://emsiservices.com/titles/versions/latest/normalize",
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
    "text": "{ \"term\": \"data scientist\" }"
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
    "confidence": 1,
    "jobLevels": [],
    "title": {
      "id": "ET3B93055220D592C8",
      "name": "Data Scientist"
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
      "title": "Invalid request",
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
      "title": "Unauthorized",
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
      "title": "URL not found",
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
      "title": "Payload Too Large"
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
      "title": "Unsupported Content Type"
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
            "title": "Title normalize response object",
            "type": "object",
            "properties": {
                "title": {
                    "title": "Normalized title",
                    "type": "object",
                    "properties": {
                        "id": {
                            "title": "Title id",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Title name",
                            "type": "string",
                            "minLength": 1
                        },
                        "pluralName": {
                            "title": "Plural form of title name",
                            "type": "string",
                            "minLength": 1
                        },
                        "mapping": {
                            "title": "Title SOC and skill mappings",
                            "type": "object",
                            "properties": {
                                "names": {
                                    "title": "List of mapping names",
                                    "description": "Mapping names are included in Titles v4.6 and onward.\n\nTitles may have zero or more mappings associated with them, the names of those mappings are listed here and represented in the unified list of skills and socs below.",
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "minLength": 1,
                                        "__nodocs": true
                                    }
                                },
                                "socs": {
                                    "title": "List of SOC mappings",
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "title": "SOC code",
                                                "type": "string",
                                                "minLength": 1
                                            },
                                            "name": {
                                                "title": "SOC name",
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
                                    "title": "List of skill mappings",
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "title": "Skill id",
                                                "type": "string",
                                                "minLength": 1
                                            },
                                            "name": {
                                                "title": "Skill name",
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
                                "socs",
                                "skills",
                                "names"
                            ],
                            "additionalProperties": false
                        },
                        "isSupervisor": {
                            "title": "Boolean value indicating whether the title's role is supervisory",
                            "type": "boolean",
                            "__internal": true
                        },
                        "levelBand": {
                            "title": "Standardized job level category",
                            "type": [
                                "string",
                                "null"
                            ],
                            "minLength": 1,
                            "__internal": true
                        }
                    },
                    "additionalProperties": false
                },
                "confidence": {
                    "title": "A number between 0 and 1 representing the confidence of the title normalization",
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                },
                "jobLevels": {
                    "title": "List of normalized job seniority information",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "__nodocs": true
                    }
                }
            },
            "required": [
                "title",
                "confidence",
                "jobLevels"
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

Normalize a raw job title string to a list of the top matching Emsi titles

Supported document types and their expected Content-Type (**Document must be UTF-8 encoded.**):
  * JSON – `application/json`
  * Plain text – `text/plain`

Raw title size is limited to 1kB.

Note that this endpoint has a base tier yearly quota of 50 requests. [Contact us](mailto:api-support@emsibg.com) if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, `RateLimit-Remaining` and `RateLimit-Reset`, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.


### `POST` Inspect title normalization

> Requesting title mappings requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>confidenceThreshold</code><div class="type">number</div> | Filter out titles with a confidence value lower than this threshold (this query param does not apply for JSON requests).<br>Minimum: `0`<br>Maximum: `1`<br>Default: `0.5`
<code>limit</code><div class="type">integer</div> | Limit the number of normalized titles for the given term (this query param does not apply for JSON requests).<br>Minimum: `0`<br>Maximum: `100`<br>Default: `5`
<code>fields</code><div class="type">string</div> | List of fields to return per title. See [/versions/{version}](#versions-version) for available fields (this query param does not apply for JSON requests). </br>`mappings` require additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.<br>This parameter is optional.<br>Default: `id,name`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "term": "data scientist",
  "limit": 2
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
            "title": "Title name",
            "type": "string",
            "minLength": 1
        },
        "fields": {
            "title": "List of fields to return per title",
            "description": "See [/versions/{version}](#versions-version) for available fields.\n\n`mappings` require additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.",
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
        "confidenceThreshold": {
            "title": "Filter out normalized titles with a confidence value lower than this threshold",
            "type": "number",
            "default": 0.5,
            "minimum": 0,
            "maximum": 1
        },
        "limit": {
            "title": "Limit the number of normalized titles for the given term",
            "type": "integer",
            "minimum": 0,
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
  "url": "https://emsiservices.com/titles/versions/latest/normalize/inspect",
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
    "text": "{ \"term\": \"data scientist\", \"limit\": 2 }"
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
      "confidence": 1,
      "jobLevels": [],
      "title": {
        "id": "ET3B93055220D592C8",
        "name": "Data Scientist"
      }
    },
    {
      "confidence": 0.8584786653518677,
      "jobLevels": [],
      "title": {
        "id": "ET66EFA7BC3A32BB32",
        "name": "Manager/Data Scientist"
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
      "title": "Invalid request",
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
      "title": "Unauthorized",
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
      "title": "URL not found",
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
      "title": "Payload Too Large"
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
      "title": "Unsupported Content Type"
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
            "title": "Title normalize response object",
            "type": "array",
            "items": {
                "title": "Title normalize response object",
                "type": "object",
                "properties": {
                    "title": {
                        "title": "Normalized title",
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Title id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Title name",
                                "type": "string",
                                "minLength": 1
                            },
                            "pluralName": {
                                "title": "Plural form of title name",
                                "type": "string",
                                "minLength": 1
                            },
                            "mapping": {
                                "title": "Title SOC and skill mappings",
                                "type": "object",
                                "properties": {
                                    "names": {
                                        "title": "List of mapping names",
                                        "description": "Mapping names are included in Titles v4.6 and onward.\n\nTitles may have zero or more mappings associated with them, the names of those mappings are listed here and represented in the unified list of skills and socs below.",
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "minLength": 1,
                                            "__nodocs": true
                                        }
                                    },
                                    "socs": {
                                        "title": "List of SOC mappings",
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "title": "SOC code",
                                                    "type": "string",
                                                    "minLength": 1
                                                },
                                                "name": {
                                                    "title": "SOC name",
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
                                        "title": "List of skill mappings",
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "title": "Skill id",
                                                    "type": "string",
                                                    "minLength": 1
                                                },
                                                "name": {
                                                    "title": "Skill name",
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
                                    "socs",
                                    "skills",
                                    "names"
                                ],
                                "additionalProperties": false
                            },
                            "isSupervisor": {
                                "title": "Boolean value indicating whether the title's role is supervisory",
                                "type": "boolean",
                                "__internal": true
                            },
                            "levelBand": {
                                "title": "Standardized job level category",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1,
                                "__internal": true
                            }
                        },
                        "additionalProperties": false
                    },
                    "confidence": {
                        "title": "A number between 0 and 1 representing the confidence of the title normalization",
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "jobLevels": {
                        "title": "List of normalized job seniority information",
                        "type": "array",
                        "items": {
                            "type": "string",
                            "minLength": 1,
                            "__nodocs": true
                        }
                    }
                },
                "required": [
                    "title",
                    "confidence",
                    "jobLevels"
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

Normalize multiple raw job title strings to a list of best matching Emsi titles

Supported document types and their expected Content-Type (**Document must be UTF-8 encoded.**):
  * JSON – `application/json`
  * Plain text – `text/plain`

There is a limit of 500 titles per request.

Raw title size is limited to 1kB per title.


### `POST` Normalize titles in bulk

> This endpoint requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to bulk normalization.
> Requesting title mappings requires additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The title version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>confidenceThreshold</code><div class="type">number</div> | Filter out titles with a confidence value lower than this threshold (this query param does not apply for JSON requests).<br>Minimum: `0`<br>Maximum: `1`<br>Default: `0.5`
<code>fields</code><div class="type">string</div> | List of fields to return per title. See [/versions/{version}](#versions-version) for available fields (this query param does not apply for JSON requests).<br>This parameter is optional.<br>Default: `id,name`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "terms": [
    "data scientist",
    "software engineer"
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
                "title": "Title name",
                "type": "string",
                "minLength": 1
            },
            "minItems": 1
        },
        "fields": {
            "title": "List of fields to return per title",
            "description": "See [/versions/{version}](#versions-version) for available fields.\n\n`mappings` require additional permissions, please [contact us](mailto:api-support@emsibg.com) if you'd like access to mappings.",
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
        "confidenceThreshold": {
            "title": "Filter out normalized titles with a confidence value lower than this threshold",
            "type": "number",
            "default": 0.5,
            "minimum": 0,
            "maximum": 1
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
  "url": "https://emsiservices.com/titles/versions/latest/normalize/bulk",
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
    "text": "{ \"terms\": [ \"data scientist\", \"software engineer\" ] }"
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
      "confidence": 1,
      "term": "data scientist",
      "jobLevels": [],
      "title": {
        "id": "ET3B93055220D592C8",
        "name": "Data Scientist"
      }
    },
    {
      "confidence": 1,
      "term": "software engineer",
      "jobLevels": [],
      "title": {
        "id": "ET6850661D6AE5FA86",
        "name": "Software Engineer"
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
      "title": "Invalid request",
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
      "title": "Unauthorized",
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
      "title": "URL not found",
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
      "title": "Payload Too Large"
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
      "title": "Unsupported Content Type"
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
                    "title": {
                        "title": "Normalized title",
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Title id",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Title name",
                                "type": "string",
                                "minLength": 1
                            },
                            "pluralName": {
                                "title": "Plural form of title name",
                                "type": "string",
                                "minLength": 1
                            },
                            "mapping": {
                                "title": "Title SOC and skill mappings",
                                "type": "object",
                                "properties": {
                                    "names": {
                                        "title": "List of mapping names",
                                        "description": "Mapping names are included in Titles v4.6 and onward.\n\nTitles may have zero or more mappings associated with them, the names of those mappings are listed here and represented in the unified list of skills and socs below.",
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "minLength": 1,
                                            "__nodocs": true
                                        }
                                    },
                                    "socs": {
                                        "title": "List of SOC mappings",
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "title": "SOC code",
                                                    "type": "string",
                                                    "minLength": 1
                                                },
                                                "name": {
                                                    "title": "SOC name",
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
                                        "title": "List of skill mappings",
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "title": "Skill id",
                                                    "type": "string",
                                                    "minLength": 1
                                                },
                                                "name": {
                                                    "title": "Skill name",
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
                                    "socs",
                                    "skills",
                                    "names"
                                ],
                                "additionalProperties": false
                            },
                            "isSupervisor": {
                                "title": "Boolean value indicating whether the title's role is supervisory",
                                "type": "boolean",
                                "__internal": true
                            },
                            "levelBand": {
                                "title": "Standardized job level category",
                                "type": [
                                    "string",
                                    "null"
                                ],
                                "minLength": 1,
                                "__internal": true
                            }
                        },
                        "additionalProperties": false
                    },
                    "term": {
                        "title": "Original term of the normalized title",
                        "type": "string",
                        "minLength": 1
                    },
                    "jobLevels": {
                        "title": "List of normalized job seniority information",
                        "type": "array",
                        "items": {
                            "type": "string",
                            "minLength": 1,
                            "__nodocs": true
                        }
                    },
                    "confidence": {
                        "title": "A number between 0 and 1 representing the confidence of the title normalization",
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    }
                },
                "required": [
                    "title",
                    "term",
                    "jobLevels",
                    "confidence"
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
