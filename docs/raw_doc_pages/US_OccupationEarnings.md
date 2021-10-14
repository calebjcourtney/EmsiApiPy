# Occupational Earnings API
## Overview
This API provides real-time aggregation of occupational earnings percentiles and estimates of the number jobs at or below a certain wage.

### Authentication
The service allows authentication via OAuth2.  You can view a full tutorial for this flow on [here](/guides/oauth-2-0).
You must request the `occearn` scope when requesting a token.

## Data Endpoints
Base URL: https://earnings.emsicloud.com

### `GET` /status
If the service is healthy, returns an OK `200` response.

### `GET` /v1/us/
List the available versions of Emsi's dataset.

#### Code Examples

```har
{
  "method": "GET",
  "url": "https://earnings.emsicloud.com/v1/us",
  "headers": [
    {"name":"Authorization", "value":"Bearer <access_token>"}
  ]
}
```

#### Response Examples

<div class='tabs'>
<div data-tab='200'>

```json
[
    "2018.2",
    "2018.3",
    "2018.4"
]
```

</div>
</div>

### `GET` /v1/us/{datarun}/years
List the available earnings years in the datarun.

#### Code Examples

```har
{
  "method": "GET",
  "url": "https://earnings.emsicloud.com/v1/us/2018.4/years",
  "headers": [
    {"name":"Authorization", "value":"Bearer <access_token>"}
  ]
}
```

#### Response Examples

<div class='tabs'>
<div data-tab='200'>

```json
[
    "2017"
]
```

</div>
</div>

### `POST` /v1/us/{datarun}/percentile_wages

#### Request Body
<div class='tabs'>
<div data-tab='Example'>

```json
{
    "geotype": "fips",
    "areas": ["16057", "53075"],
    "occupations": ["15-1132", "15-1134"],
    "classes": [1, 2],
    "percentiles": ["15.0", "60.0"]
}
```

</div>

<div data-tab='Full Reference'>

| Name         | Type          | Description |
|--------------|---------------|-------------|
| occupations  | array&lt;string&gt; | Optional, defaults to all occupations. One or codes from the SOC occupation taxonomy. |
| geotype      | string        | Either `fips` for the FIPS geography taxonomy (nation/state/county) or `zip` for ZIP codes |
| areas        | array&lt;string&gt;    | One or more FIPS codes (if `geotype` is `fips`) or ZIP codes (if `geotype` is `zip`). |
| classes      | array&lt;integer&gt;    | One or more class of worker codes. |
| year         | integer       | Optional, defaults to latest year. Earnings year to aggregate; must be one of the available years for the selected datarun. |
| wage_per     | string        | Optional, defaults to `hourly`.  Specify `annual` for annual wage. |
| percentiles  | array&lt;string&gt; | Optional, defaults to [10, 25, 50, 75, 90].  Array of percentiles to calculate.  Values should be numeric though represented as strings and in sorted order, low to high. |

</div>
</div>

#### Code Examples

```har
{
    "method": "POST",
    "url": "https://earnings.emsicloud.com/v1/us/2018.4/percentile_wages",
  "headers": [
    {"name":"Authorization", "value":"Bearer <access_token>"},
    {"name":"Content-Type", "value":"application/json"}
  ],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"geotype\": \"fips\", \"areas\":[\"16057\"], \"classes\":[1], \"occupations\":[\"15-1132\", \"15-1134\"], \"percentiles\": [\"15\", \"75\"]}"
    }
}
```

#### Response Examples

<div class='tabs'>
<div data-tab='200'>

```json
{"datarun":"2018.4","year":2017,"geotype":"fips","areas":["16057"],"occupations":["15-1132","15-1134"],"classes":[1],"wage_per":"hourly","percentiles":[{"percentile":"15","wage":15.62762978331486},{"percentile":"75","wage":37.46854617530022}],"timings":{"validation":2,"query":7,"aggregate":23,"invert":0,"interpolate":0}}
```

</div>
</div>


### `POST` /v1/us/{datarun}/employment_at_wage
This endpoint produces estimates of the number of jobs currently at or below the specified wages.  This allows the client to answer questions such as "how many forklift drivers are willing to work for 12.50 an hour?"

#### Request Body
<div class='tabs'>
<div data-tab='Example'>

```json
{
    "geotype": "fips",
    "areas": ["16057", "53075"],
    "occupations": ["15-1132", "15-1134"],
    "classes": [1, 2],
    "wages": ["30.50", "40.00"]
}
```

</div>

<div data-tab='Full Reference'>

| Name         | Type          | Description |
|--------------|---------------|-------------|
| occupations  | array&lt;string&gt; | Optional, defaults to all occupations. One or codes from the SOC occupation taxonomy. |
| geotype      | string        | Either `fips` for the FIPS geography taxonomy (nation/state/county) or `zip` for ZIP codes |
| areas        | array&lt;string&gt;    | One or more FIPS codes (if `geotype` is `fips`) or ZIP codes (if `geotype` is `zip`). |
| classes      | array&lt;integer&gt;    | One or more class of worker codes. |
| year         | integer       | Optional, defaults to latest year. Earnings year to aggregate; must be one of the available years for the selected datarun. |
| wage_per     | string        | Optional, defaults to `hourly`.  Specify `annual` for annual wage. |
| wages  | array&lt;string&gt; | Array of wages to estimate employment at.  Values should be numeric though represented as strings and in sorted order, low to high. |

</div>
</div>

#### Code Examples

```har
{
    "method": "POST",
    "url": "https://earnings.emsicloud.com/v1/us/2018.4/employment_at_wage",
  "headers": [
    {"name":"Authorization", "value":"Bearer <access_token>"},
    {"name":"Content-Type", "value":"application/json"}
  ],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"geotype\": \"fips\", \"areas\":[\"16057\"], \"classes\":[1], \"occupations\":[\"15-1132\", \"15-1134\"], \"wages\": [\"30.50\", \"40.00\"]}"
    }
}
```

#### Response Examples

<div class='tabs'>
<div data-tab='200'>

```json
{
  "datarun": "2018.4",
  "year": 2017,
  "geotype": "fips",
  "areas": [
    "16057"
  ],
  "occupations": [
    "15-1132",
    "15-1134"
  ],
  "classes": [
    1
  ],
  "wage_per": "hourly",
  "employment_at_wages": [
    {
      "wage": "30.50",
      "employment": 26.14694261442614
    },
    {
      "wage": "40.00",
      "employment": 36.20888638171452
    }
  ]
}
```

</div>
</div>

### `POST` /v1/us/{datarun}/employment_at_wage_by_occ
This endpoint is similar to the `employment_at_wage` endpoint but produces results per occupation.  This enables the client to see which occupations have the most jobs at or below a specified wage.

#### Request Body
<div class='tabs'>
<div data-tab='Example'>

```json
{
    "geotype": "fips",
    "areas": ["16057", "53075"],
    "occupations": ["15-1132", "15-1134", "15-1211", "15-1212", "15-1221", "15-1231", "15-1232", "15-1241", "15-1242", "15-1243", "15-1244"],
    "classes": [1, 2],
    "wages": ["30.50", "40.00"]
}
```

</div>

<div data-tab='Full Reference'>

| Name         | Type          | Description |
|--------------|---------------|-------------|
| occupations  | array&lt;string&gt; | Optional, all occupations by default. One or codes from the SOC occupation taxonomy. |
| geotype      | string        | Either `fips` for the FIPS geography taxonomy (nation/state/county) or `zip` for ZIP codes |
| areas        | array&lt;string&gt;    | One or more FIPS codes (if `geotype` is `fips`) or ZIP codes (if `geotype` is `zip`). |
| classes      | array&lt;integer&gt;    | One or more class of worker codes. |
| year         | integer       | Optional, defaults to latest year. Earnings year to aggregate; must be one of the available years for the selected datarun. |
| wage_per     | string        | Optional, defaults to `hourly`.  Specify `annual` for annual wage. |
| wages  | array&lt;string&gt; | Array of wages to estimate employment at.  Values should be numeric though represented as strings and in sorted order, low to high. |
| topN  | integer | Optional, defaults to `10`.  How many occupations (sorted descending by employment) to return for each wage level. |

</div>
</div>

#### Code Examples
##### All Occupations
```har
{
    "method": "POST",
    "url": "https://earnings.emsicloud.com/v1/us/2018.4/employment_at_wage_by_occ",
  "headers": [
    {"name":"Authorization", "value":"Bearer <access_token>"},
    {"name":"Content-Type", "value":"application/json"}
  ],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"geotype\": \"fips\", \"areas\":[\"16057\"], \"classes\":[1], \"wages\": [\"30.50\", \"40.00\"],\"topN\":3}"
    }
}
```

##### Specific Pool of Occupations

```har
{
    "method": "POST",
    "url": "https://earnings.emsicloud.com/v1/us/2018.4/employment_at_wage_by_occ",
  "headers": [
    {"name":"Authorization", "value":"Bearer <access_token>"},
    {"name":"Content-Type", "value":"application/json"}
  ],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"geotype\": \"fips\", \"areas\":[\"16057\"], \"classes\":[1], \"occupations\":[\"15-1111\",\"15-1121\",\"15-1122\",\"15-1131\",\"15-1132\",\"15-1133\",\"15-1134\",\"15-1141\",\"15-1142\",\"15-1143\",\"15-1151\",\"15-1152\",\"15-1199\",\"15-2011\",\"15-2021\",\"15-2031\",\"15-2041\",\"15-2098\"], \"wages\": [\"30.50\", \"40.00\"],\"topN\":3}"
    }
}
```

#### Response Examples

<div class='tabs'>
<div data-tab='200 (All Occupations)'>

```json
{
  "datarun": "2018.4",
  "year": 2017,
  "topN": 3,
  "geotype": "fips",
  "areas": [
    "16057"
  ],
  "occupations": [
    "15-1111",
    "15-1121",
    "15-1122",
    "15-1131",
    "15-1132",
    "15-1133",
    "15-1134",
    "15-1141",
    "15-1142",
    "15-1143",
    "15-1151",
    "15-1152",
    "15-1199",
    "15-2011",
    "15-2021",
    "15-2031",
    "15-2041",
    "15-2098"
  ],
  "classes": [
    1
  ],
  "wage_per": "hourly",
  "sort_index": 0,
  "employment_at_wages": [
    {
      "wage": "30.50",
      "employment": 165.5510393598849
    },
    {
      "wage": "40.00",
      "employment": 218.7033314802609
    }
  ],
  "by_occupation": [
    {
      "occupation": "15-1151",
      "employment_at_wages": [
        {
          "wage": "30.50",
          "employment": 65.55056865103607
        },
        {
          "wage": "40.00",
          "employment": 75.02422608908032
        }
      ]
    },
    {
      "occupation": "15-1134",
      "employment_at_wages": [
        {
          "wage": "30.50",
          "employment": 18.72351145668988
        },
        {
          "wage": "40.00",
          "employment": 20.81921901013591
        }
      ]
    },
    {
      "occupation": "15-1142",
      "employment_at_wages": [
        {
          "wage": "30.50",
          "employment": 15.7236405674267
        },
        {
          "wage": "40.00",
          "employment": 28.15638636838832
        }
      ]
    }
  ]
}
```

</div>

<div data-tab='200 (Specific Pool of Occupations)'>

```json
{
  "datarun": "2018.4",
  "year": 2017,
  "topN": 3,
  "geotype": "fips",
  "areas": [
    "16057"
  ],
  "occupations": [],
  "classes": [
    1
  ],
  "wage_per": "hourly",
  "sort_index": 0,
  "employment_at_wages": [
    {
      "wage": "30.50",
      "employment": 11524.68311868261
    },
    {
      "wage": "40.00",
      "employment": 12558.63057222403
    }
  ],
  "by_occupation": [
    {
      "occupation": "41-2031",
      "employment_at_wages": [
        {
          "wage": "30.50",
          "employment": 631.9626687746737
        },
        {
          "wage": "40.00",
          "employment": 644.0493086170073
        }
      ]
    },
    {
      "occupation": "43-9061",
      "employment_at_wages": [
        {
          "wage": "30.50",
          "employment": 427.3977237700766
        },
        {
          "wage": "40.00",
          "employment": 427.3977237700766
        }
      ]
    },
    {
      "occupation": "41-2011",
      "employment_at_wages": [
        {
          "wage": "30.50",
          "employment": 368.7322435687612
        },
        {
          "wage": "40.00",
          "employment": 368.7322435687612
        }
      ]
    }
  ]
}
```

</div>

</div>
