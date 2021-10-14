# Occupation Automation Index 
#### v1.1.2
##### Information on past releases can be found in the [Changelog](/updates/automation-index-changelog).

<div class="internal-only">

Automation index will continue to be available for internal use only.

</div>

<div>

> **Deprecated**
>
> This API will no longer be available.

</div>


## Overview

### Use Case
This is an interface for retrieving occupation automation index data for US and UK occupations.

### About the data
Emsi's Automation Index has different methodologies based on characteristics unique to each nation.

**US Automation Index**

Emsi's US Automation Index analyzes the potential automation risk of occupations based on job task content—derived from ONET work activities. Combining that data with the Frey and Osborne findings at the occupation level, we identify which job tasks are "at risk" and which are resilient. We also incorporate data to identify where occupations cluster in industries facing disruption, and where workers' skills mean their nearest job options are also facing automation risk.

This is a 100-based index, meaning that occupations with an automation index above 100 have an above average risk of automation, while occupations with an automation index of below 100 have a below average risk of automation.

**UK Automation Index**

Emsi's UK Automation Index uses data from different sources to assess the proportion of working time spent in each occupation performing tasks which are at "high risk" of disruption through automation and other technological change anticipated over the next 20 to 30 years. Estimates of how much time is spent performing those tasks are constructed using the frequencies for different Work Activities in the US ONET database, and mapped across to UK SOC. The relationship between different 38 task categories and Frey and Osborne's estimates of the "probability of computerisation" is used to classify each task category as high, middle, or low risk, depending on the significance and direction of that relationship.

The index is directly applicable as the amount of working time which could be disrupted by technological change; it ranges between 0% (no working time spent performing tasks at high risk) to 100% (all working time spent performing tasks at high risk).

### Content Type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the Occupation Automation Index API, you must request an OAuth bearer token with the scope `automation-index`.

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
          "value": "automation-index"
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

## /



### `GET` <span class="from-raml uri-prefix"></span>/

List available endpoints.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/automation-index/",
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
    "endpoints": [
      "/status",
      "/uk",
      "/us"
    ]
  }
}
```


</div>


</div>



## /status

Health check endpoint.

### `GET` <span class="from-raml uri-prefix"></span>/status

Get the health of the service. Be sure to check the `healthy` attribute of the response, not just the status code. Caching not recommended.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/automation-index/status",
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



## /{nation}



### `GET` <span class="from-raml uri-prefix"></span>/{nation}

List available nation endpoints.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>nation</code><div class="type">enum</div> | Example: `us`<br>Must be one of: `us`, `uk`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/automation-index/us",
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
    "endpoints": [
      "/us/meta",
      "/us/data"
    ]
  }
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
      "title": "Invalid nation 'ca', expecting one of: 'uk','us'",
      "detail": "URL not found"
    }
  ]
}
```


</div>


</div>




### `GET` <span class="from-raml uri-prefix">/{nation}</span>/meta

Get service metadata, including taxonomies and attribution text. Caching is encouraged, but the metadata may change quarterly.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>nation</code><div class="type">enum</div> | Example: `us`<br>Must be one of: `us`, `uk`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/automation-index/us/meta",
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
      "body": "Emsi's US Automation Index analyzes the potential automation risk of occupations based on job task content—derived from ONET work activities. Combining that data with the Frey and Osborne findings at the occupation level, we identify which job tasks are \"at risk\" and which are resilient. We also incorporate data to identify where occupations cluster in industries facing disruption, and where workers' skills mean their nearest job options are also facing automation risk. This is a 100-based index, meaning that occupations with an automation index above 100 have an above average risk of automation, while occupations with an automation index of below 100 have a below average risk of automation.",
      "title": "Automation Index Data"
    },
    "taxonomies": {
      "soc": "soc_emsi_2017"
    }
  }
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
      "title": "Invalid nation 'ca', expecting one of: 'uk','us'",
      "detail": "URL not found"
    }
  ]
}
```


</div>


</div>




### `GET` <span class="from-raml uri-prefix">/{nation}</span>/data

Get the occupation automation index index for all available occupation codes. Given the small size of the dataset, you may find caching the entire dataset rather than querying as-needed to be optimal.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>nation</code><div class="type">enum</div> | Example: `us`<br>Must be one of: `us`, `uk`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/automation-index/us/data",
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
    "53-1011": 81.6,
    "53-7064": 123.1
  }
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
      "title": "Invalid nation 'ca', expecting one of: 'uk','us'",
      "detail": "URL not found"
    }
  ]
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{nation}</span>/data

Get occupation automation index index for requested set of occupation codes. Occupation codes that are invalid or don't exist in the data will be returned with the value `null`.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>nation</code><div class="type">enum</div> | Example: `us`<br>Must be one of: `us`, `uk`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
[
  "53-1011",
  "53-7064"
]
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "array",
    "$id": "data.schema.json",
    "items": {
        "description": "An occupation code",
        "type": ["string", "integer"],
        "minLength": 1,
        "minimum": 0
    },
    "minItems": 1
}

```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/automation-index/us/data",
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
    "text": "[ \"53-1011\", \"53-7064\" ]"
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
    "53-1011": 81.6,
    "53-7064": 123.1
  }
}
```


</div>


<div data-tab="400">




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
      "title": "Invalid nation 'ca', expecting one of: 'uk','us'",
      "detail": "URL not found"
    }
  ]
}
```


</div>


</div>

