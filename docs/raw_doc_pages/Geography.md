# Geography API (GIS)
#### v1.13.2
##### Information on past releases can be found in the [Changelog](/updates/geography-changelog).

## Overview

### What is this service for?
Performing geo operations on standard area definitions.

### Where does this data come from?
Geo-data is collected from various sources and processed by Emsi.

### Content Type
Unless otherwise noted, all requests that require a body accept `application/json`. Likewise, all response bodies are `application/json`.

### Authentication
All endpoints require an OAuth bearer token. Tokens are granted through the Emsi Auth API at `https://auth.emsicloud.com/connect/token` and are valid for 1 hour. For access to the GIS API, you must request an OAuth bearer token with the scope `gis`.

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
          "value": "gis"
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
  "url": "https://emsiservices.com/gis/v1/status",
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



## /



### `GET` <span class="from-raml uri-prefix"></span>/

Discovery endpoint; get a list of available countries in the API.





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/gis/v1/",
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
  "countries": [
    "us",
    "uk",
    "ca"
  ]
}
```


</div>


</div>



## /{country}



### `GET` <span class="from-raml uri-prefix"></span>/{country}

Discovery endpoint; get a list of available levels and versions in the API for the specified {country}.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/gis/v1/us",
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
  "dataVersions": [
    "2016.2",
    "2016.3",
    "2016.4",
    "2017.1"
  ],
  "levels": [
    "nation",
    "state",
    "msa",
    "fips",
    "zip"
  ]
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>



## /{country}/{version}/{level}



### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/withinproximity

Search for all regions within a radius.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "centroid": {
    "lat": 46.73,
    "lon": -117
  },
  "radius": 1,
  "radiusUnit": "miles",
  "intersectionMethod": "touching",
  "calculationType": "planar"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/withinproximity.schema.json#",
    "type": "object",
    "properties": {
        "radius": {
            "title": "Raidus distance in `radiusUnit` units",
            "type": "number",
            "minimum": 0
        },
        "radiusUnit": {
            "title": "Unit of measure for `radius`",
            "type": "string",
            "enum": [
                "miles",
                "meters",
                "degrees"
            ],
            "default": "miles"
        },
        "centroid": {
            "title": "A lat/lon point",
            "type": "object",
            "properties": {
                "lat": {
                    "title": "Latitude coordinate",
                    "type": "number",
                    "minimum": -90,
                    "maximum": 90
                },
                "lon": {
                    "title": "Longitude coordinate",
                    "type": "number",
                    "minimum": -180,
                    "maximum": 180
                }
            },
            "additionalProperties": false,
            "required": [
                "lat",
                "lon"
            ]
        },
        "intersectionMethod": {
            "title": "The method of determining if a region is included in the response",
            "description": "* `touching` - Any region that is touching (intersects) the requested area.\n\n* `centroid` - Any region's who's centroid lies inside of the requested area.\n\n* `contained` - Any region that lies entirely inside of the requested area.",
            "type": "string",
            "enum": [
                "contained",
                "centroid",
                "touching"
            ],
            "default": "touching"
        },
        "calculationType": {
            "title": "The method used to calculate distances between regions",
            "description": "* `planar` - Calculate distance as if on a flat plane (faster)\n\n* `geodetic` - Calculate distance on the surface of the earth (more accurate).",
            "type": "string",
            "enum": [
                "planar",
                "geodetic"
            ],
            "default": "planar"
        }
    },
    "additionalProperties": false,
    "required": [
        "centroid",
        "radius"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/withinproximity",
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
    "text": "{ \"centroid\": { \"lat\": 46.73, \"lon\": -117 }, \"radius\": 1, \"radiusUnit\": \"miles\", \"intersectionMethod\": \"touching\", \"calculationType\": \"planar\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "codes": [
    "16057"
  ]
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/closest

Search for the closest region to a point.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "lat": 46.73,
  "lon": -117,
  "maxDistance": 70,
  "maxDistanceUnit": "miles",
  "calculationType": "planar"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/closest.schema.json#",
    "type": "object",
    "properties": {
        "lat": {
            "title": "Latitude coordinate",
            "type": "number",
            "minimum": -90,
            "maximum": 90
        },
        "lon": {
            "title": "Longitude coordinate",
            "type": "number",
            "minimum": -180,
            "maximum": 180
        },
        "maxDistance": {
            "title": "The maximum distance to check for closest regions in `maxDistanceUnit` units",
            "description": "A max distance of `0` specifies no distance limit.",
            "type": "number",
            "format": "double",
            "minimum": 0,
            "default": 0
        },
        "maxDistanceUnit": {
            "title": "Unit of measure for `maxDistance`",
            "type": "string",
            "enum": [
                "miles",
                "meters",
                "degrees"
            ],
            "default": "miles"
        },
        "calculationType": {
            "title": "The method used to calculate distances between regions",
            "description": "* `planar` - Calculate distance as if on a flat plane (faster)\n\n* `geodetic` - Calculate distance on the surface of the earth (more accurate).",
            "type": "string",
            "enum": [
                "planar",
                "geodetic"
            ],
            "default": "planar"
        }
    },
    "additionalProperties": false,
    "required": [
        "lat",
        "lon"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/closest",
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
    "text": "{ \"lat\": 46.73, \"lon\": -117, \"maxDistance\": 70, \"maxDistanceUnit\": \"miles\", \"calculationType\": \"planar\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "codes": [
    "16057"
  ]
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/contains

Search for the region that contains a point.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "lat": 46.73,
  "lon": -117
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/contains.schema.json#",
    "type": "object",
    "properties": {
        "lat": {
            "title": "Latitude coordinate",
            "type": "number",
            "minimum": -90,
            "maximum": 90
        },
        "lon": {
            "title": "Longitude coordinate",
            "type": "number",
            "minimum": -180,
            "maximum": 180
        }
    },
    "additionalProperties": false,
    "required": [
        "lat",
        "lon"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/contains",
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
    "text": "{ \"lat\": 46.73, \"lon\": -117 }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "codes": [
    "16057"
  ]
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/centroid

Find the aggregated centroid, or disaggregated centroids, of a set of regions. When the set of regions are \"aggregated\", all regions will be treated as if they were \"combined\", or \"aggregated\" into one region. Only a single pair of longitude/latitude coordinates will be returned for the entire aggregated region. When the set of regions are \"disaggregated\", the centroid for each region will be calculated \"separately\", or \"disaggregated\". A pair of longitude/latitude coordinates will be returned for each region individually.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "codes": [
    "16057",
    "53075"
  ],
  "aggregate": true
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/centroid.schema.json#",
    "type": "object",
    "properties": {
        "codes": {
            "title": "A list of codes",
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ]
            },
            "minItems": 1
        },
        "aggregate": {
            "title": "Indicate whether to return aggregated or disaggregated results",
            "description": "* When `aggregate` is `true`, all areas will be treated as if they were \"combined\", or \"aggregated\" into one area, and only a single pair of longitude/latitude coordinates will be returned.\n\n* When `aggregate` is `false`, the centroid for each area will be calculated \"separately\", or \"disaggregated\", and a pair of longitude/latitude coordinates will be returned for each area specified in the request.",
            "type": "boolean",
            "default": true
        }
    },
    "additionalProperties": false,
    "required": [
        "codes"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/centroid",
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
    "text": "{ \"codes\": [ \"16057\", \"53075\" ], \"aggregate\": true }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "centroid": {
    "lat": 46.8730693962212,
    "lon": -117.25473946351
  }
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/mbr

Find the minimum bounding rectangle of a set of regions.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>



#### Query Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>allow_crossing_dateline</code><div class="type">string</div> | **Experimental** Allow bounding rectangle to extend beyond the dateline (<-180), useful when trying to get the bounding box of Alaska for a map, which crosses the dateline.<br>This parameter is optional.<br>Default: `false`

</div>



#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "codes": [
    "16057",
    "53075"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/mbr.schema.json#",
    "type": "object",
    "properties": {
        "codes": {
            "title": "A list of codes",
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ]
            },
            "minItems": 1
        }
    },
    "additionalProperties": false,
    "required": [
        "codes"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/mbr",
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
    "text": "{ \"codes\": [ \"16057\", \"53075\" ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "mbr": {
    "bottomLeft": {
      "lat": 46.417189,
      "lon": -118.249203
    },
    "topRight": {
      "lat": 47.260449,
      "lon": -116.329279
    }
  }
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/mbc

Find the minimum bounding circle of a set of regions.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "codes": [
    "16057",
    "53075"
  ],
  "radiusUnit": "degrees"
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/mbc.schema.json#",
    "type": "object",
    "properties": {
        "codes": {
            "title": "A list of codes",
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ]
            },
            "minItems": 1
        },
        "radiusUnit": {
            "title": "Unit of measure for `radius`",
            "type": "string",
            "enum": [
                "miles",
                "meters",
                "degrees"
            ],
            "default": "miles"
        }
    },
    "additionalProperties": false,
    "required": [
        "codes"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/mbc",
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
    "text": "{ \"codes\": [ \"16057\", \"53075\" ], \"radiusUnit\": \"degrees\" }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "mbc": {
    "centroid": {
      "lat": 46.8244302735706,
      "lon": -117.281379362775
    },
    "radius": 0.972302592467926,
    "radiusUnit": "degrees"
  }
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/geojson

Get GeoJson of a set of regions.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "codes": [
    "16057"
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/geojson.schema.json#",
    "type": "object",
    "properties": {
        "codes": {
            "title": "A list of codes",
            "type": "array",
            "items": {
                "type": [
                    "string",
                    "integer"
                ]
            },
            "minItems": 1
        }
    },
    "additionalProperties": false,
    "required": [
        "codes"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/geojson",
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
    "text": "{ \"codes\": [ \"16057\" ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
          [
            [
              [
                -117.039821051927,
                47.1272649526282
              ],
              [
                -117.035618,
                47.126803
              ],
              [
                -117.028723,
                47.127787
              ],
              [
                -117.019982,
                47.12804
              ],
              [
                -117.016505,
                47.130435
              ],
              [
                -117.001633,
                47.130465
              ],
              [
                -116.995274,
                47.126249
              ],
              [
                -116.9848,
                47.126396
              ],
              [
                -116.979601,
                47.122131
              ],
              [
                -116.97094,
                47.119918
              ],
              [
                -116.967691,
                47.115101
              ],
              [
                -116.970887,
                47.105452
              ],
              [
                -116.97599,
                47.098165
              ],
              [
                -116.976986,
                47.089319
              ],
              [
                -116.974693,
                47.085935
              ],
              [
                -116.96341,
                47.080333
              ],
              [
                -116.958369,
                47.074854
              ],
              [
                -116.957144,
                47.070687
              ],
              [
                -116.95502,
                47.068869
              ],
              [
                -116.944821,
                47.067058
              ],
              [
                -116.938242,
                47.073026
              ],
              [
                -116.932419,
                47.076157
              ],
              [
                -116.929415,
                47.079639
              ],
              [
                -116.92377,
                47.081526
              ],
              [
                -116.91361,
                47.079447
              ],
              [
                -116.911471,
                47.078104
              ],
              [
                -116.904286,
                47.077483
              ],
              [
                -116.901442,
                47.078493
              ],
              [
                -116.895757,
                47.077778
              ],
              [
                -116.887554,
                47.072212
              ],
              [
                -116.883971,
                47.071455
              ],
              [
                -116.883339,
                47.067515
              ],
              [
                -116.870927,
                47.058383
              ],
              [
                -116.861081,
                47.054633
              ],
              [
                -116.858248,
                47.052156
              ],
              [
                -116.852363,
                47.050988
              ],
              [
                -116.848062,
                47.047235
              ],
              [
                -116.843037,
                47.049227
              ],
              [
                -116.835083,
                47.045635
              ],
              [
                -116.835438,
                47.032576
              ],
              [
                -116.77131,
                47.032565
              ],
              [
                -116.771227,
                47.037472
              ],
              [
                -116.650055,
                47.03747
              ],
              [
                -116.500992,
                47.036366
              ],
              [
                -116.480073,
                47.037048
              ],
              [
                -116.458612,
                47.036635
              ],
              [
                -116.458265,
                47.022043
              ],
              [
                -116.329586,
                47.022442
              ],
              [
                -116.329587,
                46.934502
              ],
              [
                -116.329414,
                46.709605
              ],
              [
                -116.329279,
                46.6279
              ],
              [
                -116.392944,
                46.628996
              ],
              [
                -116.455881,
                46.629097
              ],
              [
                -116.595455,
                46.62811
              ],
              [
                -116.598697,
                46.627018
              ],
              [
                -116.604961,
                46.629873
              ],
              [
                -116.611101,
                46.630813
              ],
              [
                -116.616117,
                46.62904
              ],
              [
                -116.620597,
                46.629352
              ],
              [
                -116.625985,
                46.628041
              ],
              [
                -116.636434,
                46.622213
              ],
              [
                -116.638713,
                46.619188
              ],
              [
                -116.645145,
                46.61782
              ],
              [
                -116.643359,
                46.615978
              ],
              [
                -116.644661,
                46.612526
              ],
              [
                -116.651956,
                46.612813
              ],
              [
                -116.658913,
                46.612042
              ],
              [
                -116.664112,
                46.608832
              ],
              [
                -116.665076,
                46.606339
              ],
              [
                -116.672983,
                46.602873
              ],
              [
                -116.68034,
                46.596026
              ],
              [
                -116.681189,
                46.594146
              ],
              [
                -116.688456,
                46.588301
              ],
              [
                -116.693458,
                46.58685
              ],
              [
                -116.696642,
                46.587577
              ],
              [
                -116.70072,
                46.583481
              ],
              [
                -116.700885,
                46.578981
              ],
              [
                -116.705513,
                46.57365
              ],
              [
                -116.70514,
                46.570149
              ],
              [
                -116.709097,
                46.5645
              ],
              [
                -116.708616,
                46.561614
              ],
              [
                -116.71495,
                46.55294
              ],
              [
                -116.713785,
                46.550138
              ],
              [
                -116.719183,
                46.542789
              ],
              [
                -116.754053,
                46.542184
              ],
              [
                -117.039656676314,
                46.5417852467966
              ],
              [
                -117.039527679285,
                46.6207767332891
              ],
              [
                -117.039398,
                46.700186
              ],
              [
                -117.039828,
                46.815443
              ],
              [
                -117.039657,
                46.825798
              ],
              [
                -117.039704130724,
                46.9124068921815
              ],
              [
                -117.039734025588,
                46.9673426294541
              ],
              [
                -117.039778427879,
                47.0489376687176
              ],
              [
                -117.039821051927,
                47.1272649526282
              ]
            ]
          ]
        ]
      },
      "properties": {
        "areaid": "16057",
        "level": "fips",
        "name": "Latah"
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
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/svg

Create an svg from a set of layers defined by regions.


#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "width": 500,
  "height": 500,
  "style": {
    "stroke": "grey",
    "fill": "lightblue"
  },
  "codes": [
    "16001",
    "16003",
    "16005",
    "16007",
    "16009",
    "16011",
    "16013"
  ],
  "fgLayers": [
    {
      "level": "state",
      "codes": [
        "16"
      ],
      "primary": true,
      "style": {
        "stroke": "black",
        "fill": "transparent"
      }
    }
  ],
  "bgLayers": [
    {
      "level": "state",
      "codes": [
        "16"
      ],
      "style": {
        "fill": "#eee"
      }
    }
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/svg.schema.json#",
    "type": "object",
    "properties": {
        "width": {
            "title": "SVG canvas width",
            "type": "integer",
            "minimum": 1
        },
        "height": {
            "title": "SVG canvas height",
            "type": "integer",
            "minimum": 1
        },
        "codes": {
            "title": "List of codes or object keying codes to a numeric value",
            "type": [
                "array",
                "object"
            ],
            "items": {
                "type": [
                    "string",
                    "integer"
                ]
            },
            "patternProperties": {
                "^.*$": {
                    "description": "Value used to calculate the fill color of the given area. Values are normalized into color buckets defined by `choroplethFill`.",
                    "type": "number"
                }
            }
        },
        "style": {
            "title": "SVG styling parameters",
            "type": "object"
        },
        "fgLayers": {
            "title": "An ordered list of foreground layers to add to the SVG",
            "description": "Drawn front to back (first in front, last in back). Foreground layers are drawn in front of the base request layer and background layers. Non-renderable regions will not be included in the SVG layer. If the primary layer is not renderable the bottom-most renderable layer of the SVG will be chosen as the primary layer instead.",
            "type": "array",
            "items": {
                "title": "SVG Layer",
                "type": "object",
                "properties": {
                    "level": {
                        "title": "Area level for the codes in this layer",
                        "type": "string",
                        "minLength": 1
                    },
                    "style": {
                        "title": "SVG styling parameters",
                        "type": "object"
                    },
                    "codes": {
                        "title": "A list of codes",
                        "type": "array",
                        "items": {
                            "type": [
                                "string",
                                "integer"
                            ]
                        }
                    },
                    "primary": {
                        "title": "Primary layer",
                        "description": "Indicate this is the primary layer, setting the SVG view box to this layer. If multiple layers are set to primary the top most layer will be chosen (this includes foreground and background layers). If no layer is set to primary the base request layer will be used.",
                        "type": "boolean",
                        "default": false
                    }
                },
                "additionalProperties": false,
                "required": [
                    "level"
                ]
            },
            "maxItems": 10
        },
        "bgLayers": {
            "title": "An ordered list of background layers to add to the SVG",
            "description": "Drawn front to back (first in front, last in back). Background layers are drawn behind the foreground layers and base request layer. Non-renderable regions will not be included in the SVG layer. If the primary layer is not renderable the bottom-most renderable layer of the SVG will be chosen as the primary layer instead.",
            "type": "array",
            "items": {
                "title": "SVG Layer",
                "type": "object",
                "properties": {
                    "level": {
                        "title": "Area level for the codes in this layer",
                        "type": "string",
                        "minLength": 1
                    },
                    "style": {
                        "title": "SVG styling parameters",
                        "type": "object"
                    },
                    "codes": {
                        "title": "A list of codes",
                        "type": "array",
                        "items": {
                            "type": [
                                "string",
                                "integer"
                            ]
                        }
                    },
                    "primary": {
                        "title": "Primary layer",
                        "description": "Indicate this is the primary layer, setting the SVG view box to this layer. If multiple layers are set to primary the top most layer will be chosen (this includes foreground and background layers). If no layer is set to primary the base request layer will be used.",
                        "type": "boolean",
                        "default": false
                    }
                },
                "additionalProperties": false,
                "required": [
                    "level"
                ]
            },
            "maxItems": 10
        },
        "choroplethFill": {
            "title": "Color values used for bucketing code values into color buckets",
            "description": "Only applies if `codes` is an object of values keyed to their respective codes. The values will be normalized to their respective fill color based on if they are `positive`, `zero`, or `negative`. These values will overwrite any `style` fill specified.",
            "type": "object",
            "properties": {
                "positive": {
                    "title": "Color bucket values for positive code values in the SVG map",
                    "default": [
                        "#abdafc",
                        "#35a1dd",
                        "#1185c4",
                        "#115c9d"
                    ],
                    "type": "array",
                    "items": {
                        "description": "List of SVG fill colors for normalized buckets",
                        "type": "string",
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "zero": {
                    "title": "A SVG fill color for zero values in the choropleth SVG map",
                    "default": "#eee",
                    "type": "string"
                },
                "negative": {
                    "title": "Color bucket values for negative code values in the SVG map",
                    "default": [
                        "#b2182b",
                        "#d6604d",
                        "#f4a582",
                        "#fddbc7"
                    ],
                    "type": "array",
                    "items": {
                        "description": "List of SVG fill colors for normalized buckets",
                        "type": "string",
                        "__nodocs": true
                    },
                    "minItems": 1
                },
                "algorithm": {
                    "title": "The algorithm used for bucketing values",
                    "description": "* `natural_break` – Bucket around natural breaks in the data.\n\n* `quantile` – Bucket data into approximately equal sized groups.\n\n* `linear` – Bucket data on a linear scale.",
                    "default": "natural_break",
                    "type": "string",
                    "enum": [
                        "natural_break",
                        "quantile",
                        "linear"
                    ]
                }
            },
            "additionalProperties": false
        }
    },
    "additionalProperties": false,
    "required": [
        "width",
        "height"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/svg",
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
    "text": "{ \"width\": 500, \"height\": 500, \"style\": { \"stroke\": \"grey\", \"fill\": \"lightblue\" }, \"codes\": [ \"16001\", \"16003\", \"16005\", \"16007\", \"16009\", \"16011\", \"16013\" ], \"fgLayers\": [ { \"level\": \"state\", \"codes\": [ \"16\" ], \"primary\": true, \"style\": { \"stroke\": \"black\", \"fill\": \"transparent\" } } ], \"bgLayers\": [ { \"level\": \"state\", \"codes\": [ \"16\" ], \"style\": { \"fill\": \"#eee\" } } ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">

SVG paths are dynamically simplified based on rendered area to reduce response size.
The more zoomed out you are, or the smaller your canvas is, the more simplified the SVG paths will
be. Also, to save space, regions that cannot be seen in the viewport will be omitted from the SVG.




</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>




### `POST` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/traveltime

> Travel time analyses provided by [Targomo](https://www.targomo.com/developers/resources/attribution).

Search for all regions with a specified travel time of a point. By default, the maximum travel time is 120 minutes.

This endpoint requires additonal permissions, please [contact us](mailto:api-support@economicmodeling.com) if you'd like access to traveltime.

<div class="internal-only">

**Traveltime access claims**

The following scopes allow access to traveltime:

* `gis:traveltime_access` - Gives access to the `/traveltime` endpoint. Returns codes and traveltimes.
* `gis:traveltime_polygon` - Add this scope to return geojson polygon as well.

**Traveltime limit**:

By default, all clients with `gis:traveltime_access` claim can request up to 120 minutes travel time. This limit can be increased up to 300 minutes with a client claim of the form `gis:traveltime:{limit}`.

So for example, `gis:traveltime:300` will allow clients to request a maximum of 300 minutes travel time.

</div>



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`

</div>




#### Request Body

<div class="tabs">
<div data-tab="Example">


```json
{
  "lat": 46.73,
  "lon": -117,
  "traveltimes": [
    1
  ]
}
```


</div>
<div data-tab="Full Reference">

```jsonschema
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "requests/traveltime.schema.json#",
    "type": "object",
    "properties": {
        "lat": {
            "title": "Latitude coordinate",
            "type": "number",
            "minimum": -90,
            "maximum": 90
        },
        "lon": {
            "title": "Longitude coordinate",
            "type": "number",
            "minimum": -180,
            "maximum": 180
        },
        "traveltimes": {
            "title": "List of travel times in minutes",
            "description": "Up to 6 travel times (drive times) can be run at a time. By default, the maximum travel time is 120 minutes, but more can be requested.",
            "example": [
                10,
                20,
                30
            ],
            "type": "array",
            "items": {
                "type": "integer",
                "multipleOf": 1,
                "minimum": 1,
                "__nodocs": true
            },
            "maxItems": 6
        },
        "intersectionMethod": {
            "title": "The method of determining if a region is included in the response",
            "description": "* `touching` - Any region that is touching (intersects) the requested area.\n\n* `centroid` - Any region's who's centroid lies inside of the requested area.\n\n* `contained` - Any region that lies entirely inside of the requested area.",
            "type": "string",
            "enum": [
                "contained",
                "centroid",
                "touching"
            ],
            "default": "touching"
        }
    },
    "additionalProperties": false,
    "required": [
        "lat",
        "lon",
        "traveltimes"
    ]
}
```

</div>
</div>


#### Code Examples

```har
{
  "method": "POST",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/traveltime",
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
    "text": "{ \"lat\": 46.73, \"lon\": -117, \"traveltimes\": [ 1 ] }"
  },
  "queryString": []
}
```

#### Response Examples

<div class="tabs">

<div data-tab="200">




```json
{
  "traveltimes": [
    {
      "codes": [
        "16057"
      ],
      "traveltime": 1
    }
  ]
}
```


</div>


<div data-tab="400">

Your request wasn't valid (bad parameter names or values).


```json
{
  "error": {
    "status": "400",
    "title": "Invalid request",
    "detail": "The browser (or proxy) sent a request that this server could not understand."
  }
}
```


</div>


<div data-tab="403">

You don't have access to traveltime data.


```json
{
  "error": {
    "status": "403",
    "title": "Forbidden",
    "detail": "You don't have access to traveltime data."
  }
}
```


</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>



<div class="internal-only">

### `GET` <span class="from-raml uri-prefix">/{country}/{version}/{level}</span>/tile/{z}/{x}/{y}.mvt

Mapbox vector tile endpoint. {z}, {x}, and {y} correspond to tile zoom and coordinates used by Mapbox
GL (or other vector mapping software) to request a specific tile at a particular zoom level.



#### URL Parameters

<div class="schema-table">

Name | Description
-----|------------
<code>country</code><div class="type">string</div> | Country abreviation.<br>Example: `us`
<code>version</code><div class="type">string</div> | Data version for the country.<br>Example: `2018.3`
<code>level</code><div class="type">string</div> | A country's region level.<br>Example: `fips`
<code>z</code><div class="type">string</div> | Tile zoom level<br>Example: `9`
<code>x</code><div class="type">string</div> | Tile x coordinate<br>Example: `88`
<code>y</code><div class="type">string</div> | Tile y coordinate<br>Example: `181`

</div>





#### Code Examples

```har
{
  "method": "GET",
  "url": "https://emsiservices.com/gis/v1/us/2018.3/fips/tile/9/88/181.mvt",
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

The response is a Mapbox Vector Tile. Use this endpoint as a 'source' of a Mapbox layer, see their
[docs](https://www.mapbox.com/mapbox-gl-js/example/third-party/) for more information.

Note that the returned tiles have two layers, a geometry layer, and a label layer. The geometry layer's
name is the same as the `level` parameter used in the request, the label layer's name is `level`-label
(see `source-layer` in the snippet below). Features returned have three properties: `code`, `name`,
and `level`. Currently feature ids are not supported, therefore feature highlighting/restyling in
Mapbox GL is not supported.

**Example Mapbox GL snippet**:
```javascript
let username = '<your username>';
let password = '<your password>';
mapboxgl.accessToken = '<your access token>';
let map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v9',
  zoom: 4,
  center: [-100.447303, 37.753574],
  // add basic auth for gis requests
  transformRequest: (url, resourceType) => {
    if(resourceType == 'Tile' && url.startsWith('https://emsiservices.com')) {
      return {
        url: url,
        headers: {
          'Authorization': 'Basic ' + btoa(`${username}:${password}`)
        }
      };
    }
  }
});

map.on('load', () => {
  let level = 'state';

  map.addSource('test-source', {
    type: 'vector',
    tiles: [`https://emsiservices.com/gis/v1/us/2018.3/${level}/tile/{z}/{x}/{y}.mvt`]
  });

  // geometry layer
  map.addLayer({
    id: 'test',
    type: 'fill',
    source: 'test-source',
    'source-layer': level,
    paint: {
      'fill-color': 'blue',
      'fill-opacity': 0.6
    }
  });
  // label layer
  map.addLayer({
    id: 'test-label',
    type: 'symbol',
    source: 'test-source',
    'source-layer': `${level}-label`,
    paint: {
      'text-color': '#666',
      'text-halo-color': 'rgba(255,255,255,0.95)',
      'text-halo-width': 2
    },
    layout: {
      'symbol-placement': 'point',
      'text-field': "{name}",
      'text-font': [
        "Open Sans Semibold",
        "Arial Unicode MS Bold"
      ],
      'text-letter-spacing': 0.1,
      'text-size': 12
    }
  });
});
```




</div>


<div data-tab="204">

Tiles that do not have data will respond with a 204 response code.



</div>


<div data-tab="404">

Resource not found.


```json
{
  "error": {
    "status": "404",
    "title": "URL not found",
    "detail": "Invalid country, version, or level."
  }
}
```


</div>


</div>

</div>
