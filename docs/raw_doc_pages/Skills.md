# Emsi Skills API
#### v2.6.1

> Transitioning from v1 of the Skills API? See our [v2 upgrade notes](/updates/upgrade-to-skills-v2) for changes in the new version.

##### Information on past releases can be found in the [Changelog](/updates/skills-api-changelog).

## Overview
Emsi's complete collection of skills.
This API exposes all of our skills along with their type and unique identifier.
You can learn more about Emsi's skills classification [here](https://skills.emsidata.com).

### Content type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

<div class="internal-only">

### Related Skills Endpoint

`/versions/{version}/related` endpoint utilizes the `Related Skills Model` to return related skills from input skills. The model compresses skills found in the postings data and scores them against the input skills using k-trucated Singular Value Decompsition(SVD) method. The highest scored skills are returned as related skills in the response. The mathematical details of the model can be found in the [README](https://gitlab.economicmodeling.com/emsi-services/skill-sifter-py#related-skills-model) of Micro's `Related Skills Model` Python wrapper.

In this model, the word "related" has two meanings:

1. `most likely (predictive)` -
These are skills a person/job is likely to have, based on the input skills. Think of it as predicting what skills someone forgot to include in the list. It typically returns skills that are more common. It works best for a mix of hard and soft input skills, such as all the skills on a job posting or resume. Scores are not true probabilities but can be interpreted that way.

2. `most relevant ("keep similar company")` -
These are skills that are used in contexts similar to the input skill(s). Best for inputs of single skills or relatively small, cohesive skillsets. It prioritizes returning the most focused, specific, and closely related results. Scores can be interpreted as weighted-average similarities between the given output skill and all input skills.

Internally, the API alternates between `most likely` and `most relevant` skills depending on the number of input skills for the best result. We don't plan to expose the option for clients to manually switch between the two.

</div>

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the Skills API, you must request an OAuth bearer token with the scope `emsi_open`.

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

By default all clients have specific endpoint quotas of 50 requests per month, their quota can be changed through Emsi Auth claims (see below). For more detail on the quota system see our [Emsi Auth Quota](/guides/emsi-auth-quota) document.

**/versions/{verison}/extract** <br> **/versions/{version}/extract/trace**

A client's extract quota can be changed through a `skills:extract:quota` Emsi Auth claim. To increase a client's monthly quota to 100 per month use `skills:extract:quota:100/month`, to grant them unlimited access use `skills:extract:quota:unlimited`.

**/versions/{version}/related**

A client's related skills quota can be changed through a `skills:related:quota` Emsi Auth claim. To increase a client's monthly quota to 100 per month use `skills:related:quota:100/month`, to grant them unlimited access use `skills:related:quota:unlimited`.

</div>

### Attribution

* Wikipedia extracts are distributed under the [CC BY-SA license](https://creativecommons.org/licenses/by-sa/3.0/)

## /status

Health check endpoint

### `GET` Get service status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/skills/status",
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
  "url": "https://emsiservices.com/skills/meta",
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
      "body": "Emsi Skills is an open, comprehensive library of skills that uses the same terminology we use in the real world. We select skills that are truly relevant to people, employers, and educators—meaning, they are commonly listed on real-world resumes, professional profiles, and job postings—and we take suggestions from the community.",
      "title": "Emsi Skills"
    },
    "latestVersion": "7.10"
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
                    "title": "Latest skills version available in the service",
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

A list of available skill classification versions

### `GET` List all versions

Version `latest` can be used as an alias to the latest skill version. See our [Skills Classification Changelog](/updates/skills-classification-changelog) for the updates in each version.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/skills/versions",
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
    "7.7",
    "7.6",
    "7.5",
    "7.4",
    "7.3",
    "7.2",
    "7.1",
    "7.0",
    "6.16",
    "6.15",
    "6.14",
    "6.13",
    "6.12",
    "6.11",
    "6.10",
    "6.9",
    "6.8",
    "6.7",
    "6.6",
    "6.5",
    "6.4",
    "6.3",
    "6.2",
    "6.1",
    "6.0",
    "5.1"
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
            "title": "List of available skills versions",
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

Get version specific metadata including available fields, types, skill counts and removed skill counts.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/skills/versions/latest",
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
    "fields": [
      "tags",
      "id",
      "name",
      "type"
    ],
    "removedSkillCount": 2225,
    "skillCount": 31302,
    "types": [
      {
        "description": "Hard skills are unique (or technical) skills related to a specialty.",
        "id": "ST1",
        "name": "Hard Skill"
      },
      {
        "description": "Soft skills are common (or human) skills which are broad statements of ability.",
        "id": "ST2",
        "name": "Soft Skill"
      },
      {
        "description": "Certification skills are recognizable qualification standards assigned by industry or education bodies.",
        "id": "ST3",
        "name": "Certification"
      }
    ],
    "version": "7.17"
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
      "detail": "Unrecognized version: 77"
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
                    "title": "Skill classification version number",
                    "type": "string",
                    "minLength": 1
                },
                "skillCount": {
                    "title": "Total number of available skills",
                    "type": "integer",
                    "minimum": 0
                },
                "removedSkillCount": {
                    "title": "Total number of removed skills",
                    "type": "integer",
                    "minimum": 0
                },
                "types": {
                    "title": "List of skill type information",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "title": "Type description",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "Skill type ID",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Skill type name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "description",
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 1
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
                "skillCount",
                "removedSkillCount",
                "types",
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
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/skills/versions/latest/changes",
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
        "name": "Interactive Design",
        "type": "Hard Skill",
        "id": "ES127D44352769195DDE"
      }
    ],
    "consolidations": [
      {
        "idFrom": "ES2AAD427D871251857E",
        "idTo": "KS120KH6HWMTVV6K1K0K",
        "nameFrom": "Smartphone Operation",
        "nameTo": "Apple IPhone"
      }
    ],
    "taggingImprovements": [
      {
        "name": "ArcSight Enterprise Security Manager",
        "id": "ES72FFEE143C63225C75"
      }
    ],
    "removals": [
      {
        "name": ".NET Assemblies",
        "id": "KS126XS6CQCFGC3NG79X"
      }
    ],
    "renames": [
      {
        "newName": "Surface Modeling",
        "oldName": "3d Solid And Surface Modeling",
        "id": "KS7G7CK623H1CJ6F8LQH"
      }
    ],
    "typeChanges": [
      {
        "newType": "Certification",
        "oldType": "Hard Skill",
        "name": "Air Operations Area (AOA) Badge",
        "id": "ES8F068E243B4693BE6A"
      }
    ]
  }
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
            "title": "Categorized skill version changes",
            "type": "object",
            "properties": {
                "additions": {
                    "title": "List of newly added skills",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "title": "New skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "type": {
                                "title": "New skill type",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "New skill id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "name",
                            "type",
                            "id"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
                },
                "consolidations": {
                    "title": "List of consolidated skills",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "idFrom": {
                                "title": "Old skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "idTo": {
                                "title": "New skill id",
                                "type": "string",
                                "minLength": 1
                            },
                            "nameFrom": {
                                "title": "Old skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "nameTo": {
                                "title": "New skill name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "idFrom",
                            "idTo",
                            "nameFrom",
                            "nameTo"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
                },
                "taggingImprovements": {
                    "title": "List of skills that had their tagging improved",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "title": "Improved skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "Improved skill id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "name",
                            "id"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
                },
                "removals": {
                    "title": "List of removed skills",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "title": "Removed skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "Removed skill id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "name",
                            "id"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
                },
                "renames": {
                    "title": "List of renamed skills",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "newName": {
                                "title": "New skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "oldName": {
                                "title": "Old skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "Skill id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "newName",
                            "oldName",
                            "id"
                        ],
                        "additionalProperties": false
                    },
                    "minItems": 0
                },
                "typeChanges": {
                    "title": "List of skill type changes",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "newType": {
                                "title": "New skill type",
                                "type": "string",
                                "minLength": 1
                            },
                            "oldType": {
                                "title": "Old skill type",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "id": {
                                "title": "Skill id",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "newType",
                            "oldType",
                            "name",
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



## /versions/{version}/skills

Returns a list of all skills in {version} sorted by skill name

### `GET` List all skills




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>q</code><div class="type">string</div> | A query string of skill names to search for.<br>This parameter is optional.<br>Example: `.NET`
<code>typeIds</code><div class="type">string</div> | A comma-separated list of type IDs to filter the skills list. See [/versions/{version}](#versions-version) for available filters. By default all types are included.<br>This parameter is optional.<br>Example: `ST1,ST2`
<code>fields</code><div class="type">string</div> | A comma-separated list of items to include. See [/versions/{version}](#versions-version) for available include keys. By default id, name, type, and infoUrl are included.<br>This parameter is optional.<br>Example: `id,name,type,infoUrl`
<code>limit</code><div class="type">integer</div> | Limit the number of skills returned in the response.<br>This parameter is optional.<br>Example: `5`

</div>




#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/skills/versions/latest/skills",
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
      "name": "typeIds",
      "value": "ST1,ST2"
    },
    {
      "name": "fields",
      "value": "id,name,type,infoUrl"
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
  "attributions": [
    {
      "name": "Wikipedia",
      "text": "Wikipedia extracts are distributed under the CC BY-SA license (https://creativecommons.org/licenses/by-sa/3.0/)"
    }
  ],
  "data": [
    {
      "id": "KS120P86XDXZJT3B7KVJ",
      "name": "(American Society For Quality) ASQ Certified",
      "type": {
        "id": "ST3",
        "name": "Certification"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS120P86XDXZJT3B7KVJ"
    },
    {
      "id": "KS126XS6CQCFGC3NG79X",
      "name": ".NET Assemblies",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS126XS6CQCFGC3NG79X"
    },
    {
      "id": "KS1200B62W5ZF38RJ7TD",
      "name": ".NET Framework",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS1200B62W5ZF38RJ7TD"
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


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "title": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: 77"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/skills-search.schema.json",
    "type": "object",
    "properties": {
        "attributions": {
            "title": "Data attribution information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "title": "Attribution name",
                        "type": "string",
                        "minLength": 1
                    },
                    "text": {
                        "title": "Licensing information",
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": [
                    "name",
                    "text"
                ],
                "additionalProperties": false
            },
            "minItems": 1
        },
        "data": {
            "title": "List of available skill information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "title": "Skill type information object",
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Skill type ID",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Skill type name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    },
                    "id": {
                        "title": "Skill ID",
                        "type": "string",
                        "minLength": 1
                    },
                    "name": {
                        "title": "Skill name",
                        "type": "string",
                        "minLength": 1
                    },
                    "tags": {
                        "title": "List of tag information of the skill",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "key": {
                                    "title": "Skill tag key",
                                    "type": "string",
                                    "minLength": 1
                                },
                                "value": {
                                    "title": "Skill tag value",
                                    "type": "string",
                                    "minLength": 1
                                }
                            },
                            "required": [
                                "key",
                                "value"
                            ],
                            "additionalProperties": false
                        }
                    },
                    "infoUrl": {
                        "title": "URL for a publicly accessible web page that includes information about the skill",
                        "type": "string",
                        "pattern": "https://skills.emsidata.com/skills/.+"
                    }
                },
                "additionalProperties": false
            }
        }
    },
    "required": [
        "data",
        "attributions"
    ],
    "additionalProperties": false
}
```

</div>

</div>




### `POST` List requested skills




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>typeIds</code><div class="type">string</div> | A comma-separated list of type IDs to filter the skills list. See [/versions/{version}](#versions-version) for available filters. By default all types are included.<br>This parameter is optional.<br>Example: `ST1,ST2`
<code>fields</code><div class="type">string</div> | A comma-separated list of items to include. See [/versions/{version}](#versions-version) for available include keys. By default id, name, type, and infoUrl are included.<br>This parameter is optional.<br>Example: `id,name,type,infoUrl`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    "KS1200364C9C1LK3V5Q1",
    "KS1275N74XZ574T7N47D",
    "KS125QD6K0QLLKCTPJQ0"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/skills-lookup.schema.json",
    "type": "object",
    "properties": {
        "ids": {
            "title": "Filter by skill ids",
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
  "url": "https://emsiservices.com/skills/versions/latest/skills",
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
    "text": "{ \"ids\": [ \"KS1200364C9C1LK3V5Q1\", \"KS1275N74XZ574T7N47D\", \"KS125QD6K0QLLKCTPJQ0\" ] }"
  },
  "queryString": [
    {
      "name": "typeIds",
      "value": "ST1,ST2"
    },
    {
      "name": "fields",
      "value": "id,name,type,infoUrl"
    }
  ]
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "attributions": [
    {
      "name": "Wikipedia",
      "text": "Wikipedia extracts are distributed under the CC BY-SA license (https://creativecommons.org/licenses/by-sa/3.0/)"
    }
  ],
  "data": [
    {
      "id": "KS1200364C9C1LK3V5Q1",
      "name": "C (Programming Language)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS1200364C9C1LK3V5Q1"
    },
    {
      "id": "KS125QD6K0QLLKCTPJQ0",
      "name": "C-Based Programming Languages",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS125QD6K0QLLKCTPJQ0"
    },
    {
      "id": "KS1275N74XZ574T7N47D",
      "name": "Objective-C (Programming Language)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS1275N74XZ574T7N47D"
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


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "title": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: 77"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/skills-lookup.schema.json",
    "type": "object",
    "properties": {
        "attributions": {
            "title": "Data attribution information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "title": "Attribution name",
                        "type": "string",
                        "minLength": 1
                    },
                    "text": {
                        "title": "Licensing information",
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": [
                    "name",
                    "text"
                ],
                "additionalProperties": false
            },
            "minItems": 1
        },
        "data": {
            "title": "List of requested skill information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "title": "Skill type information object",
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Skill type ID",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Skill type name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    },
                    "id": {
                        "title": "Skill ID",
                        "type": "string",
                        "minLength": 1
                    },
                    "name": {
                        "title": "Skill name",
                        "type": "string",
                        "minLength": 1
                    },
                    "tags": {
                        "title": "List of tag information of the skill",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "key": {
                                    "title": "Skill tag key",
                                    "type": "string",
                                    "minLength": 1
                                },
                                "value": {
                                    "title": "Skill tag value",
                                    "type": "string",
                                    "minLength": 1
                                }
                            },
                            "required": [
                                "key",
                                "value"
                            ],
                            "additionalProperties": false
                        }
                    },
                    "infoUrl": {
                        "title": "URL for a publicly accessible web page that includes information about the skill",
                        "type": "string",
                        "pattern": "https://skills.emsidata.com/skills/.+"
                    }
                },
                "additionalProperties": false
            }
        }
    },
    "required": [
        "data",
        "attributions"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /versions/{version}/skills/{skill_id}

Returns information about a specific skill.

### `GET` Get a skill by ID

If a skill that has been removed is requested, it will return with when and why it was removed in the `removedDescription` and will be of type `Remove`.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`
<code>skill_id</code><div class="type">string</div> | Skill ID.<br>Example: `KS124JB619VXG6RQ810C`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/skills/versions/latest/skills/KS124JB619VXG6RQ810C",
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
  "attributions": [
    {
      "name": "Wikipedia",
      "text": "Wikipedia extracts are distributed under the CC BY-SA license (https://creativecommons.org/licenses/by-sa/3.0/)"
    }
  ],
  "data": {
    "id": "KS126XS6CQCFGC3NG79X",
    "name": ".NET Assemblies",
    "removedDescription": null,
    "tags": [
      {
        "key": "wikipediaUrl",
        "value": "https://en.wikipedia.org/wiki/.NET_assemblies"
      }
    ],
    "type": {
      "id": "ST1",
      "name": "Hard Skill"
    },
    "infoUrl": "https://skills.emsidata.com/skills/KS126XS6CQCFGC3NG79X"
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
      "detail": "Unrecognized version: 77"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/single-skill-search.schema.json",
    "type": "object",
    "properties": {
        "attributions": {
            "title": "Data attribution information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "title": "Attribution name",
                        "type": "string",
                        "minLength": 1
                    },
                    "text": {
                        "title": "Licensing information",
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": [
                    "name",
                    "text"
                ],
                "additionalProperties": false
            },
            "minItems": 1
        },
        "data": {
            "title": "List of extracted skill information",
            "type": "object",
            "properties": {
                "type": {
                    "title": "Skill type information object",
                    "type": "object",
                    "properties": {
                        "id": {
                            "title": "Skill type ID",
                            "type": "string",
                            "minLength": 1
                        },
                        "name": {
                            "title": "Skill type name",
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "id",
                        "name"
                    ],
                    "additionalProperties": false
                },
                "id": {
                    "title": "Skill ID",
                    "type": "string",
                    "minLength": 1
                },
                "name": {
                    "title": "Skill name",
                    "type": "string",
                    "minLength": 1
                },
                "tags": {
                    "title": "List of tag information of the skill",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "key": {
                                "title": "Skill tag key",
                                "type": "string",
                                "minLength": 1
                            },
                            "value": {
                                "title": "Skill tag value",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "key",
                            "value"
                        ],
                        "additionalProperties": false
                    }
                },
                "removedDescription": {
                    "title": "If the skill has been removed, a description of when and why the skill was removed. Otherwise `null`",
                    "type": [
                        "string",
                        "null"
                    ],
                    "minLength": 1
                },
                "infoUrl": {
                    "title": "URL for a publicly accessible web page that includes information about the skill",
                    "type": "string",
                    "pattern": "https://skills.emsidata.com/skills/.+"
                }
            },
            "required": [
                "type",
                "id",
                "name",
                "tags",
                "removedDescription",
                "infoUrl"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "data",
        "attributions"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /versions/{version}/related

Returns a list of skills that are related to the requested skills.

Note that this endpoint has a free tier monthly quota of 50 requests. [Contact us](https://skills.emsidata.com/contact) if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, `RateLimit-Remaining` and `RateLimit-Reset`, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.


### `POST` Find related skills




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "ids": [
    "KS1200364C9C1LK3V5Q1",
    "KS1275N74XZ574T7N47D",
    "KS125QD6K0QLLKCTPJQ0"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/related.schema.json",
    "type": "object",
    "properties": {
        "ids": {
            "title": "Skill ids to get related skill for",
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1
        },
        "limit": {
            "title": "The number of realted skills to be returned",
            "type": "integer",
            "minimum": 1,
            "maximum": 100,
            "default": 10
        },
        "fields": {
            "title": "List of fields to return per skill",
            "default": [
                "id",
                "name",
                "type",
                "infoUrl"
            ],
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "__nodocs": true
            },
            "minItems": 1
        },
        "typeId": {
            "title": "Skill type to filter results to",
            "description": "If not specified skills of all types are returned.",
            "type": "string",
            "minLength": 1
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
  "url": "https://emsiservices.com/skills/versions/latest/related",
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
    "text": "{ \"ids\": [ \"KS1200364C9C1LK3V5Q1\", \"KS1275N74XZ574T7N47D\", \"KS125QD6K0QLLKCTPJQ0\" ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "attributions": [
    {
      "name": "Wikipedia",
      "text": "Wikipedia extracts are distributed under the CC BY-SA license (https://creativecommons.org/licenses/by-sa/3.0/)"
    }
  ],
  "data": [
    {
      "id": "KS1214N6T5D95P429K77",
      "name": "Booting (BIOS)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS1214N6T5D95P429K77"
    },
    {
      "id": "KSTWANLFILYE9I0PARK2",
      "name": "Cheminformatics",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KSTWANLFILYE9I0PARK2"
    },
    {
      "id": "KS1227K6FY9569LLFZ2N",
      "name": "Computer Forensics",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS1227K6FY9569LLFZ2N"
    },
    {
      "id": "ESD2382F603410DC8CB5",
      "name": "EnCase (Digital Intelligence Software)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/ESD2382F603410DC8CB5"
    },
    {
      "id": "KS124296011QWR6GSGG4",
      "name": "Forensic Toolkits",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS124296011QWR6GSGG4"
    },
    {
      "id": "ESF069EA5CC33233649E",
      "name": "IDA Pro",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/ESF069EA5CC33233649E"
    },
    {
      "id": "KS0OVHL8NPO0QXLXTZ2U",
      "name": "JetBrains IDE",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS0OVHL8NPO0QXLXTZ2U"
    },
    {
      "id": "KS1277W6N8B43PHF6DB1",
      "name": "OllyDBg",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS1277W6N8B43PHF6DB1"
    },
    {
      "id": "KS4402G6S6DZM37VHM3B",
      "name": "Reverse Engineering",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KS4402G6S6DZM37VHM3B"
    },
    {
      "id": "KSVI4JJO3LEBXZXJ60BE",
      "name": "Screen Size",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      },
      "infoUrl": "https://skills.emsidata.com/skills/KSVI4JJO3LEBXZXJ60BE"
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


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "title": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: 77"
    }
  ]
}
```


</div>


<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "responses/related.schema.json",
    "type": "object",
    "properties": {
        "attributions": {
            "title": "Data attribution information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "title": "Attribution name",
                        "type": "string",
                        "minLength": 1
                    },
                    "text": {
                        "title": "Licensing information",
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": [
                    "name",
                    "text"
                ],
                "additionalProperties": false
            },
            "minItems": 1
        },
        "data": {
            "title": "List of related skills",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "title": "Skill type information object",
                        "type": "object",
                        "properties": {
                            "id": {
                                "title": "Skill type ID",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Skill type name",
                                "type": "string",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "id",
                            "name"
                        ],
                        "additionalProperties": false
                    },
                    "id": {
                        "title": "Skill ID",
                        "type": "string",
                        "minLength": 1
                    },
                    "name": {
                        "title": "Skill name",
                        "type": "string",
                        "minLength": 1
                    },
                    "tags": {
                        "title": "List of tag information of the skill",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "key": {
                                    "title": "Skill tag key",
                                    "type": "string",
                                    "minLength": 1
                                },
                                "value": {
                                    "title": "Skill tag value",
                                    "type": "string",
                                    "minLength": 1
                                }
                            },
                            "required": [
                                "key",
                                "value"
                            ],
                            "additionalProperties": false
                        }
                    },
                    "infoUrl": {
                        "title": "URL for a publicly accessible web page that includes information about the skill",
                        "type": "string",
                        "pattern": "https://skills.emsidata.com/skills/.+"
                    }
                },
                "additionalProperties": false
            }
        }
    },
    "required": [
        "data",
        "attributions"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /versions/{version}/extract

Returns a list of skills found in a document.

Supported document types and their expected Content-Type:
  * JSON – `application/json` **Document must be UTF-8 encoded.**
  * Plain text – `text/plain`
  * PDF – `application/pdf`
  * Word (docx) – `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

Request document size is limited to 10MB, text parsed from the document is limited to 50KB.

Note that this endpoint has a free tier monthly quota of 50 requests. [Contact us](https://skills.emsidata.com/contact) if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, `RateLimit-Remaining` and `RateLimit-Reset`, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.


### `POST` Extract skills from document




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>confidenceThreshold</code><div class="type">number</div> | Filter out skills with a confidence value lower than this threshold (this query param does not apply for JSON requests)<br>Minimum: `0`<br>Maximum: `1`<br>Default: `0.5`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "text": "... Great candidates also have\n\n Experience with a particular JS MV* framework (we happen to use React)\n Experience working with databases\n Experience with AWS\n Familiarity with microservice architecture\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ...",
  "confidenceThreshold": 0.6
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/extract.schema.json",
    "type": "object",
    "properties": {
        "text": {
            "title": "Document to be used in the skills extraction process",
            "type": "string"
        },
        "confidenceThreshold": {
            "title": "Filter out skills with a confidence value lower than this threshold",
            "type": "number",
            "example": 0.6,
            "default": 0.5,
            "minimum": 0,
            "maximum": 1
        }
    },
    "required": [
        "text"
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
  "url": "https://emsiservices.com/skills/versions/latest/extract",
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
    "text": "{ \"text\": \"... Great candidates also have\\n\\n Experience with a particular JS MV* framework (we happen to use React)\\n Experience working with databases\\n Experience with AWS\\n Familiarity with microservice architecture\\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ...\", \"confidenceThreshold\": 0.6 }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "attributions": [
    {
      "name": "Wikipedia",
      "text": "Wikipedia extracts are distributed under the CC BY-SA license (https://creativecommons.org/licenses/by-sa/3.0/)"
    }
  ],
  "data": [
    {
      "confidence": 1,
      "skill": {
        "id": "KSDJCA4E89LB98JAZ7LZ",
        "name": "React.js",
        "infoUrl": "https://skills.emsidata.com/skills/KSDJCA4E89LB98JAZ7LZ",
        "tags": [
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/React.js"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
      }
    },
    {
      "confidence": 1,
      "skill": {
        "id": "KS120FG6YP8PQYYNQY9B",
        "name": "Amazon Web Services",
        "infoUrl": "https://skills.emsidata.com/skills/KS120FG6YP8PQYYNQY9B",
        "tags": [
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/Amazon_Web_Services"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
      }
    },
    {
      "confidence": 1,
      "skill": {
        "id": "KS121F45VPV8C9W3QFYH",
        "name": "Cascading Style Sheets (CSS)",
        "infoUrl": "https://skills.emsidata.com/skills/KS121F45VPV8C9W3QFYH",
        "tags": [
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/Cascading_Style_Sheets_-_CSS"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
      }
    },
    {
      "confidence": 0.9994209408760071,
      "skill": {
        "id": "KS1200771D9CR9LB4MWW",
        "name": "JavaScript (Programming Language)",
        "infoUrl": "https://skills.emsidata.com/skills/KS1200771D9CR9LB4MWW",
        "tags": [
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/Javascript_(programming_language)"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
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


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "title": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: 77"
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
    "$id": "responses/extract.schema.json",
    "type": "object",
    "properties": {
        "attributions": {
            "title": "Data attribution information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "title": "Attribution name",
                        "type": "string",
                        "minLength": 1
                    },
                    "text": {
                        "title": "Licensing information",
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": [
                    "name",
                    "text"
                ],
                "additionalProperties": false
            },
            "minItems": 1
        },
        "data": {
            "title": "List of extracted skill information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "confidence": {
                        "title": "A number between 0 and 1 representing the confidence of the skill classification",
                        "type": "number"
                    },
                    "skill": {
                        "title": "Extracted skill information object",
                        "type": "object",
                        "properties": {
                            "type": {
                                "title": "Skill type information object",
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "title": "Skill type ID",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "Skill type name",
                                        "type": "string",
                                        "minLength": 1
                                    }
                                },
                                "required": [
                                    "id",
                                    "name"
                                ],
                                "additionalProperties": false
                            },
                            "id": {
                                "title": "Skill ID",
                                "type": "string",
                                "minLength": 1
                            },
                            "name": {
                                "title": "Skill name",
                                "type": "string",
                                "minLength": 1
                            },
                            "tags": {
                                "title": "List of tag information of the skill",
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "key": {
                                            "title": "Skill tag key",
                                            "type": "string",
                                            "minLength": 1
                                        },
                                        "value": {
                                            "title": "Skill tag value",
                                            "type": "string",
                                            "minLength": 1
                                        }
                                    },
                                    "required": [
                                        "key",
                                        "value"
                                    ],
                                    "additionalProperties": false
                                }
                            },
                            "infoUrl": {
                                "title": "URL for a publicly accessible web page that includes information about the skill",
                                "type": "string",
                                "pattern": "https://skills.emsidata.com/skills/.+"
                            }
                        },
                        "required": [
                            "type",
                            "tags",
                            "id",
                            "name",
                            "infoUrl"
                        ],
                        "additionalProperties": false
                    }
                },
                "required": [
                    "confidence",
                    "skill"
                ],
                "additionalProperties": false
            }
        }
    },
    "required": [
        "data",
        "attributions"
    ],
    "additionalProperties": false
}
```

</div>

</div>



## /versions/{version}/extract/trace

Returns a list of skills found in a document with its trace information, including contextual classification data found in the document that resulted in a skill match, and optionally the normalized text from the document used to extract skills.

Supported document types and their expected Content-Type:
  * JSON – `application/json` **Document must be UTF-8 encoded.**
  * Plain text – `text/plain`
  * PDF – `application/pdf`
  * Word (docx) – `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

> For the most accurate results mapping `sourceStart` and `sourceEnd` byte offsets on surface forms and context forms, be sure to request `includeNormalizedText` as `true`. Byte offsets are guaranteed to match the text returned in the `normalizedText` field.
>
> Note that these are byte offsets, be sure the language you are parsing this text in is representing the returned string's characters as 8-bit bytes for proper source offset referencing.

Request document size is limited to 10MB, text parsed from the document is limited to 50KB.

Note that this endpoint has a free tier monthly quota of 50 requests. [Contact us](https://skills.emsidata.com/contact) if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, `RateLimit-Remaining` and `RateLimit-Reset`, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.


### `POST` Extract skills with source tracing




#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>version</code><div class="type">string</div> | The skills classification version.<br>Example: `latest`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>includeNormalizedText</code><div class="type">boolean</div> | Include normalized text used in the extraction process in the response (this query param does not apply for JSON requests)

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "text": "... Great candidates also have\n\n Experience with a particular JS MV* framework (we happen to use React)\n Experience working with databases\n Experience with AWS\n Familiarity with microservice architecture\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ..."
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/extract-trace.schema.json",
    "type": "object",
    "properties": {
        "text": {
            "title": "Document to be used in the skills extraction process",
            "type": "string"
        },
        "includeNormalizedText": {
            "title": "Include normalized text used in the extraction process in the response",
            "type": "boolean",
            "default": false
        }
    },
    "required": [
        "text"
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
  "url": "https://emsiservices.com/skills/versions/latest/extract/trace",
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
    "text": "{ \"text\": \"... Great candidates also have\\n\\n Experience with a particular JS MV* framework (we happen to use React)\\n Experience working with databases\\n Experience with AWS\\n Familiarity with microservice architecture\\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ...\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "attributions": [
    {
      "name": "Wikipedia",
      "text": "Wikipedia extracts are distributed under the CC BY-SA license (https://creativecommons.org/licenses/by-sa/3.0/)"
    }
  ],
  "data": {
    "skills": [
      {
        "confidence": 1,
        "skill": {
          "id": "KSDJCA4E89LB98JAZ7LZ",
          "name": "React.js",
          "infoUrl": "https://skills.emsidata.com/skills/KSDJCA4E89LB98JAZ7LZ",
          "tags": [
            {
              "key": "wikipediaUrl",
              "value": "https://en.wikipedia.org/wiki/React.js"
            }
          ],
          "type": {
            "id": "ST1",
            "name": "Hard Skill"
          }
        }
      },
      {
        "confidence": 1,
        "skill": {
          "id": "KS120FG6YP8PQYYNQY9B",
          "name": "Amazon Web Services",
          "infoUrl": "https://skills.emsidata.com/skills/KS120FG6YP8PQYYNQY9B",
          "tags": [
            {
              "key": "wikipediaUrl",
              "value": "https://en.wikipedia.org/wiki/Amazon_Web_Services"
            }
          ],
          "type": {
            "id": "ST1",
            "name": "Hard Skill"
          }
        }
      },
      {
        "confidence": 1,
        "skill": {
          "id": "KS121F45VPV8C9W3QFYH",
          "name": "Cascading Style Sheets (CSS)",
          "infoUrl": "https://skills.emsidata.com/skills/KS121F45VPV8C9W3QFYH",
          "tags": [
            {
              "key": "wikipediaUrl",
              "value": "https://en.wikipedia.org/wiki/Cascading_Style_Sheets_-_CSS"
            }
          ],
          "type": {
            "id": "ST1",
            "name": "Hard Skill"
          }
        }
      },
      {
        "confidence": 0.9994209408760071,
        "skill": {
          "id": "KS1200771D9CR9LB4MWW",
          "name": "JavaScript (Programming Language)",
          "infoUrl": "https://skills.emsidata.com/skills/KS1200771D9CR9LB4MWW",
          "tags": [
            {
              "key": "wikipediaUrl",
              "value": "https://en.wikipedia.org/wiki/Javascript_(programming_language)"
            }
          ],
          "type": {
            "id": "ST1",
            "name": "Hard Skill"
          }
        }
      }
    ],
    "trace": [
      {
        "classificationData": {
          "contextForms": [
            {
              "sourceEnd": 232,
              "sourceStart": 229,
              "value": "CSS"
            },
            {
              "sourceEnd": 264,
              "sourceStart": 261,
              "value": "CSS"
            }
          ],
          "skills": [
            {
              "confidence": 0.9994209408760071,
              "skill": {
                "id": "KS1200771D9CR9LB4MWW",
                "name": "JavaScript (Programming Language)",
                "infoUrl": "https://skills.emsidata.com/skills/KS1200771D9CR9LB4MWW",
                "tags": [
                  {
                    "key": "wikipediaUrl",
                    "value": "https://en.wikipedia.org/wiki/Javascript_(programming_language)"
                  }
                ],
                "type": {
                  "id": "ST1",
                  "name": "Hard Skill"
                }
              }
            }
          ]
        },
        "surfaceForm": {
          "sourceEnd": 64,
          "sourceStart": 62,
          "value": "JS"
        }
      },
      {
        "classificationData": {
          "contextForms": [
            {
              "sourceEnd": 64,
              "sourceStart": 62,
              "value": "JS"
            },
            {
              "sourceEnd": 78,
              "sourceStart": 69,
              "value": "framework"
            },
            {
              "sourceEnd": 159,
              "sourceStart": 156,
              "value": "AWS"
            },
            {
              "sourceEnd": 232,
              "sourceStart": 229,
              "value": "CSS"
            },
            {
              "sourceEnd": 259,
              "sourceStart": 255,
              "value": "SASS"
            },
            {
              "sourceEnd": 264,
              "sourceStart": 261,
              "value": "CSS"
            },
            {
              "sourceEnd": 270,
              "sourceStart": 268,
              "value": "JS"
            }
          ],
          "skills": [
            {
              "confidence": 1,
              "skill": {
                "id": "KSDJCA4E89LB98JAZ7LZ",
                "name": "React.js",
                "infoUrl": "https://skills.emsidata.com/skills/KSDJCA4E89LB98JAZ7LZ",
                "tags": [
                  {
                    "key": "wikipediaUrl",
                    "value": "https://en.wikipedia.org/wiki/React.js"
                  }
                ],
                "type": {
                  "id": "ST1",
                  "name": "Hard Skill"
                }
              }
            }
          ]
        },
        "surfaceForm": {
          "sourceEnd": 102,
          "sourceStart": 97,
          "value": "React"
        }
      },
      {
        "classificationData": {
          "contextForms": [],
          "skills": [
            {
              "confidence": 1,
              "skill": {
                "id": "KS120FG6YP8PQYYNQY9B",
                "name": "Amazon Web Services",
                "infoUrl": "https://skills.emsidata.com/skills/KS120FG6YP8PQYYNQY9B",
                "tags": [
                  {
                    "key": "wikipediaUrl",
                    "value": "https://en.wikipedia.org/wiki/Amazon_Web_Services"
                  }
                ],
                "type": {
                  "id": "ST1",
                  "name": "Hard Skill"
                }
              }
            }
          ]
        },
        "surfaceForm": {
          "sourceEnd": 159,
          "sourceStart": 156,
          "value": "AWS"
        }
      },
      {
        "classificationData": {
          "contextForms": [],
          "skills": [
            {
              "confidence": 1,
              "skill": {
                "id": "KS121F45VPV8C9W3QFYH",
                "name": "Cascading Style Sheets (CSS)",
                "infoUrl": "https://skills.emsidata.com/skills/KS121F45VPV8C9W3QFYH",
                "tags": [
                  {
                    "key": "wikipediaUrl",
                    "value": "https://en.wikipedia.org/wiki/Cascading_Style_Sheets_-_CSS"
                  }
                ],
                "type": {
                  "id": "ST1",
                  "name": "Hard Skill"
                }
              }
            }
          ]
        },
        "surfaceForm": {
          "sourceEnd": 232,
          "sourceStart": 229,
          "value": "CSS"
        }
      },
      {
        "classificationData": {
          "contextForms": [],
          "skills": [
            {
              "confidence": 1,
              "skill": {
                "id": "KS121F45VPV8C9W3QFYH",
                "name": "Cascading Style Sheets (CSS)",
                "infoUrl": "https://skills.emsidata.com/skills/KS121F45VPV8C9W3QFYH",
                "tags": [
                  {
                    "key": "wikipediaUrl",
                    "value": "https://en.wikipedia.org/wiki/Cascading_Style_Sheets_-_CSS"
                  }
                ],
                "type": {
                  "id": "ST1",
                  "name": "Hard Skill"
                }
              }
            }
          ]
        },
        "surfaceForm": {
          "sourceEnd": 264,
          "sourceStart": 261,
          "value": "CSS"
        }
      },
      {
        "classificationData": {
          "contextForms": [
            {
              "sourceEnd": 232,
              "sourceStart": 229,
              "value": "CSS"
            },
            {
              "sourceEnd": 264,
              "sourceStart": 261,
              "value": "CSS"
            }
          ],
          "skills": [
            {
              "confidence": 0.9994209408760071,
              "skill": {
                "id": "KS1200771D9CR9LB4MWW",
                "name": "JavaScript (Programming Language)",
                "infoUrl": "https://skills.emsidata.com/skills/KS1200771D9CR9LB4MWW",
                "tags": [
                  {
                    "key": "wikipediaUrl",
                    "value": "https://en.wikipedia.org/wiki/Javascript_(programming_language)"
                  }
                ],
                "type": {
                  "id": "ST1",
                  "name": "Hard Skill"
                }
              }
            }
          ]
        },
        "surfaceForm": {
          "sourceEnd": 270,
          "sourceStart": 268,
          "value": "JS"
        }
      }
    ],
    "normalizedText": null
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


<div data-tab="404">

The version you requested wasn't found.


```json
{
  "errors": [
    {
      "title": "URL not found",
      "status": 404,
      "detail": "Unrecognized version: 77"
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
    "$id": "responses/extract-trace.schema.json",
    "type": "object",
    "properties": {
        "attributions": {
            "title": "Data attribution information",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "title": "Attribution name",
                        "type": "string",
                        "minLength": 1
                    },
                    "text": {
                        "title": "Licensing information",
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": [
                    "name",
                    "text"
                ],
                "additionalProperties": false
            },
            "minItems": 1
        },
        "data": {
            "title": "Extract with trace response object",
            "type": "object",
            "properties": {
                "trace": {
                    "title": "List of extracted skills and their sources",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "classificationData": {
                                "title": "Extracted skill's source information",
                                "type": "object",
                                "properties": {
                                    "contextForms": {
                                        "title": "List of context information",
                                        "description": "Provides information about context words that aided skill classifications",
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "sourceStart": {
                                                    "title": "The byte offset in the provided text where the context word begins",
                                                    "type": "integer"
                                                },
                                                "sourceEnd": {
                                                    "title": "The byte offset in the provided text where the context word ends",
                                                    "type": "integer"
                                                },
                                                "value": {
                                                    "title": "The context word as shown in the provided text",
                                                    "type": "string"
                                                }
                                            },
                                            "required": [
                                                "sourceEnd",
                                                "sourceStart",
                                                "value"
                                            ],
                                            "additionalProperties": false
                                        }
                                    },
                                    "skills": {
                                        "title": "List of extracted skill information",
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "confidence": {
                                                    "title": "A number between 0 and 1 representing the confidence of the skill classification",
                                                    "type": "number"
                                                },
                                                "skill": {
                                                    "title": "Extracted skill information object",
                                                    "type": "object",
                                                    "properties": {
                                                        "type": {
                                                            "title": "Skill type information object",
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {
                                                                    "title": "Skill type ID",
                                                                    "type": "string",
                                                                    "minLength": 1
                                                                },
                                                                "name": {
                                                                    "title": "Skill type name",
                                                                    "type": "string",
                                                                    "minLength": 1
                                                                }
                                                            },
                                                            "required": [
                                                                "id",
                                                                "name"
                                                            ],
                                                            "additionalProperties": false
                                                        },
                                                        "id": {
                                                            "title": "Skill ID",
                                                            "type": "string",
                                                            "minLength": 1
                                                        },
                                                        "name": {
                                                            "title": "Skill name",
                                                            "type": "string",
                                                            "minLength": 1
                                                        },
                                                        "tags": {
                                                            "title": "List of tag information of the skill",
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "key": {
                                                                        "title": "Skill tag key",
                                                                        "type": "string",
                                                                        "minLength": 1
                                                                    },
                                                                    "value": {
                                                                        "title": "Skill tag value",
                                                                        "type": "string",
                                                                        "minLength": 1
                                                                    }
                                                                },
                                                                "required": [
                                                                    "key",
                                                                    "value"
                                                                ],
                                                                "additionalProperties": false
                                                            }
                                                        },
                                                        "infoUrl": {
                                                            "title": "URL for a publicly accessible web page that includes information about the skill",
                                                            "type": "string",
                                                            "pattern": "https://skills.emsidata.com/skills/.+"
                                                        }
                                                    },
                                                    "required": [
                                                        "type",
                                                        "tags",
                                                        "id",
                                                        "name",
                                                        "infoUrl"
                                                    ],
                                                    "additionalProperties": false
                                                }
                                            },
                                            "required": [
                                                "confidence",
                                                "skill"
                                            ],
                                            "additionalProperties": false
                                        }
                                    }
                                },
                                "required": [
                                    "contextForms",
                                    "skills"
                                ],
                                "additionalProperties": false
                            },
                            "surfaceForm": {
                                "title": "The specific parts of the input text that were used to identify skills",
                                "description": "Provides information about the original word that is classified as a skill",
                                "type": "object",
                                "properties": {
                                    "sourceStart": {
                                        "title": "The byte offset in the provided text where the word begins",
                                        "type": "integer"
                                    },
                                    "sourceEnd": {
                                        "title": "The byte offset in the provided text where the word ends",
                                        "type": "integer"
                                    },
                                    "value": {
                                        "title": "The actual word as shown in the provided text",
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "sourceEnd",
                                    "sourceStart",
                                    "value"
                                ],
                                "additionalProperties": false
                            }
                        },
                        "required": [
                            "classificationData",
                            "surfaceForm"
                        ],
                        "additionalProperties": false
                    }
                },
                "skills": {
                    "title": "List of extracted skill information",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "confidence": {
                                "title": "A number between 0 and 1 representing the confidence of the skill classification",
                                "type": "number"
                            },
                            "skill": {
                                "title": "Extracted skill information object",
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "title": "Skill type information object",
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "title": "Skill type ID",
                                                "type": "string",
                                                "minLength": 1
                                            },
                                            "name": {
                                                "title": "Skill type name",
                                                "type": "string",
                                                "minLength": 1
                                            }
                                        },
                                        "required": [
                                            "id",
                                            "name"
                                        ],
                                        "additionalProperties": false
                                    },
                                    "id": {
                                        "title": "Skill ID",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "name": {
                                        "title": "Skill name",
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "tags": {
                                        "title": "List of tag information of the skill",
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "key": {
                                                    "title": "Skill tag key",
                                                    "type": "string",
                                                    "minLength": 1
                                                },
                                                "value": {
                                                    "title": "Skill tag value",
                                                    "type": "string",
                                                    "minLength": 1
                                                }
                                            },
                                            "required": [
                                                "key",
                                                "value"
                                            ],
                                            "additionalProperties": false
                                        }
                                    },
                                    "infoUrl": {
                                        "title": "URL for a publicly accessible web page that includes information about the skill",
                                        "type": "string",
                                        "pattern": "https://skills.emsidata.com/skills/.+"
                                    }
                                },
                                "required": [
                                    "type",
                                    "tags",
                                    "id",
                                    "name",
                                    "infoUrl"
                                ],
                                "additionalProperties": false
                            }
                        },
                        "required": [
                            "confidence",
                            "skill"
                        ],
                        "additionalProperties": false
                    }
                },
                "normalizedText": {
                    "title": "Normalized text used for extraction",
                    "description": "Surface form and context form trace offsets are guaranteed to match this document.\n\nIf the `includeNormalizedText` param is not specified or is `false` this will be `null`.",
                    "type": [
                        "string",
                        "null"
                    ],
                    "minLength": 1
                }
            },
            "required": [
                "trace",
                "skills",
                "normalizedText"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "data",
        "attributions"
    ],
    "additionalProperties": false
}
```

</div>

</div>
