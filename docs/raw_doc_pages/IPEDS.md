# IPEDS API

## Introduction
This API provides metadata about educational institutions reporting via IPEDS, and a translation layer between CIP and SOC codes.

Information and search functionality for institutions are exposed via the 
[institution](#institution-endpoints) family of endpoints.
A SOC-CIP mapping is provided via the [soccip endpoints](#soc-cip-mapping-endpoints).

## Authentication
This API requires authentication [via OAuth2](guides/oauth-2-0).

## Base URL and Status Endpoint
Base endpoint: https://ipeds.emsicloud.com

### `GET` /health/status
This endpoint checks the health of the service.  If the service is healthy, returns an empty `200 OK` response.

#### Code Examples

```har
{
    "method": "GET",
    "url": "https://ipeds.emsicloud.com/health/status"
}
```

## Institution Endpoints

### `POST` /institutions
Fetch information for one or more institutions.  The institution IDs are 
IPEDS Unit IDs.

#### Code Examples

```har
{
    "method":"POST",
    "url":"https://ipeds.emsicloud.com/institutions",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"},
		{"name":"Content-Type", "value":"application/json"}
	],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"institutionIds\": [247940, 166027]}"
    }
}
```

#### Response Examples

```json
{
  "rows": [
    {
      "id": 247940,
      "institutionName": "Owensboro Community and Technical College",
      "address": "4800 New Hartford Rd",
      "city": "Owensboro",
      "stateAbbr": "KY",
      "zip9": "42303",
      "telephone": "2706864400",
      "webAddr": "https://owensboro.kctcs.edu",
      "zipId": 42303,
      "stateFips": 21,
      "countyId": 21059,
      "sector": 4,
      "control": 1,
      "latitude": 37.717317,
      "longitude": -87.082995
    },
    {
      "id": 166027,
      "institutionName": "Harvard University",
      "address": "Massachusetts Hall",
      "city": "Cambridge",
      "stateAbbr": "MA",
      "zip9": "02138",
      "telephone": "6174951000",
      "webAddr": "www.harvard.edu",
      "zipId": 2138,
      "stateFips": 25,
      "countyId": 25017,
      "sector": 2,
      "control": 2,
      "latitude": 42.374471,
      "longitude": -71.118313
    }
  ],
  "errors": [],
  "timings": [
    "Execute query: 0.7182ms"
  ]
}
```

### `GET` /institutions/zip/{zip}
Return a list of institutions operating in the specified ZIP code.

#### Code Examples

```har
{
    "method": "GET",
    "url": "https://ipeds.emsicloud.com/institutions/zip/42303",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"}
    ]
}
```

#### Response Examples

```json
{
  "rows": [
    {
      "id": 247940,
      "institutionName": "Owensboro Community and Technical College",
      "address": "4800 New Hartford Rd",
      "city": "Owensboro",
      "stateAbbr": "KY",
      "zip9": "42303",
      "telephone": "2706864400",
      "webAddr": "https://owensboro.kctcs.edu",
      "zipId": 42303,
      "stateFips": 21,
      "countyId": 21059,
      "sector": 4,
      "control": 1,
      "latitude": 37.717317,
      "longitude": -87.082995
    },
    {
      "id": 484330,
      "institutionName": "Ross Medical Education Center-Owensboro",
      "address": "410 Southtown Boulevard",
      "city": "Owensboro",
      "stateAbbr": "KY",
      "zip9": "42303-7757",
      "telephone": "2706845334",
      "webAddr": "www.rosseducation.edu",
      "zipId": 42303,
      "stateFips": 21,
      "countyId": 21059,
      "sector": 9,
      "control": 3,
      "latitude": 37.72084,
      "longitude": -87.119151
    }
  ],
  "errors": [],
  "timings": [
    "Execute query: 0.0031ms"
  ]
}
```

### `GET` /institutions/fips/{fips}
Return a list of institutions operating in the specified state or county FIPS code.

#### Code Examples

```har
{
    "method": "GET",
    "url": "https://ipeds.emsicloud.com/institutions/fips/16",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"}
    ]
}
```

#### Response Examples

```json
{
  "rows": [
    {
      "id": 440396,
      "institutionName": "New Saint Andrews College",
      "address": "405 S. Main Street",
      "city": "Moscow",
      "stateAbbr": "ID",
      "zip9": "83843-1525",
      "telephone": "2088821566",
      "webAddr": "nsa.edu",
      "zipId": 83843,
      "stateFips": 16,
      "countyId": 16057,
      "sector": 2,
      "control": 2,
      "latitude": 46.731991,
      "longitude": -117.001732
    },
    {
      "id": 247047,
      "institutionName": "The Salon Professional Academy",
      "address": "120 Holly Street",
      "city": "Nampa",
      "stateAbbr": "ID",
      "zip9": "83686-5104",
      "telephone": "2084657660",
      "webAddr": "www.tspanampa.com",
      "zipId": 83686,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 6,
      "control": 3,
      "latitude": 43.567768,
      "longitude": -116.563413
    },
    {
      "id": 460899,
      "institutionName": "Stevens-Henager College",
      "address": "1444 Entertainment Avenue",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83709-6733",
      "telephone": "2083834540",
      "webAddr": "www.stevenshenager.edu/",
      "zipId": 83709,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 2,
      "control": 2,
      "latitude": 43.591087,
      "longitude": -116.27829
    },
    {
      "id": 467793,
      "institutionName": "Broadview University-Boise",
      "address": "2750 East Gala Court",
      "city": "Meridian",
      "stateAbbr": "ID",
      "zip9": "83642-0000",
      "telephone": "2085772900",
      "webAddr": "www.broadviewuniversity.edu/",
      "zipId": 83642,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 3,
      "control": 3,
      "latitude": 43.58943,
      "longitude": -116.360151
    },
    {
      "id": 244491,
      "institutionName": "The Beauty Institute Schwarzkopf Professional - Coeur D'Alene",
      "address": "410 Neider Ave. Suite B",
      "city": "Coeur D'Alene",
      "stateAbbr": "ID",
      "zip9": "83815",
      "telephone": "2086640541",
      "webAddr": "thebeautyinstituteskp.com",
      "zipId": 83815,
      "stateFips": 16,
      "countyId": 16055,
      "sector": 6,
      "control": 3,
      "latitude": 47.70605,
      "longitude": -116.793231
    },
    {
      "id": 142559,
      "institutionName": "College of Southern Idaho",
      "address": "315 Falls Ave.",
      "city": "Twin Falls",
      "stateAbbr": "ID",
      "zip9": "83301",
      "telephone": "2087339554",
      "webAddr": "www.csi.edu",
      "zipId": 83301,
      "stateFips": 16,
      "countyId": 16083,
      "sector": 4,
      "control": 1,
      "latitude": 42.579837,
      "longitude": -114.473901
    },
    {
      "id": 142416,
      "institutionName": "Mr Leon's School of Hair Design-Moscow",
      "address": "618 S Main St",
      "city": "Moscow",
      "stateAbbr": "ID",
      "zip9": "83843",
      "telephone": "2088822923",
      "webAddr": "mrleons.com",
      "zipId": 83843,
      "stateFips": 16,
      "countyId": 16057,
      "sector": 6,
      "control": 3,
      "latitude": 46.729394,
      "longitude": -117.001352
    },
    {
      "id": 440466,
      "institutionName": "University of Phoenix-Idaho",
      "address": "999 West Main Street",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83642-5114",
      "telephone": "8667660766",
      "webAddr": "www.phoenix.edu",
      "zipId": 83642,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 3,
      "control": 3,
      "latitude": 43.5733829462643,
      "longitude": -116.40136189556
    },
    {
      "id": 476869,
      "institutionName": "Austin Kade Academy",
      "address": "1646 South Woodruff Avenue",
      "city": "Idaho Falls",
      "stateAbbr": "ID",
      "zip9": "83404-5540",
      "telephone": "2083467300",
      "webAddr": "www.austinkade.com",
      "zipId": 83404,
      "stateFips": 16,
      "countyId": 16019,
      "sector": 6,
      "control": 3,
      "latitude": 43.482859,
      "longitude": -112.001128
    },
    {
      "id": 460808,
      "institutionName": "College of Massage Therapy",
      "address": "98 Poplar Street",
      "city": "Blackfoot",
      "stateAbbr": "ID",
      "zip9": "83221-1758",
      "telephone": "2087852327",
      "webAddr": "www.collegemassagetherapy.com",
      "zipId": 83221,
      "stateFips": 16,
      "countyId": 16011,
      "sector": 7,
      "control": 1,
      "latitude": 43.193422,
      "longitude": -112.346975
    },
    {
      "id": 142090,
      "institutionName": "Boise Bible College",
      "address": "8695 W Marigold St",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83714-1220",
      "telephone": "2083767731",
      "webAddr": "www.boisebible.edu",
      "zipId": 83714,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 2,
      "control": 2,
      "latitude": 43.657437,
      "longitude": -116.290607
    },
    {
      "id": 432278,
      "institutionName": "BCRI Career Training",
      "address": "1951 S. Saturn Way #120",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83709",
      "telephone": "2083228517",
      "webAddr": "www.cri.org",
      "zipId": 83709,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 6,
      "control": 3,
      "latitude": 43.5497069202887,
      "longitude": -116.289371327976
    },
    {
      "id": 474906,
      "institutionName": "Stevens-Henager College",
      "address": "901 Pier View Drive Suite 105",
      "city": "Idaho Falls",
      "stateAbbr": "ID",
      "zip9": "83402",
      "telephone": "2085220887",
      "webAddr": "www.stevenshenager.edu/",
      "zipId": 83402,
      "stateFips": 16,
      "countyId": 16019,
      "sector": 2,
      "control": 2,
      "latitude": 43.48346,
      "longitude": -112.05156
    },
    {
      "id": 142276,
      "institutionName": "Idaho State University",
      "address": "921 S 8th Ave",
      "city": "Pocatello",
      "stateAbbr": "ID",
      "zip9": "83209",
      "telephone": "2082822700",
      "webAddr": "www.isu.edu/",
      "zipId": 83209,
      "stateFips": 16,
      "countyId": 16005,
      "sector": 1,
      "control": 1,
      "latitude": 42.864108,
      "longitude": -112.429084
    },
    {
      "id": 247010,
      "institutionName": "Headmasters School of Hair Design",
      "address": "602 Main St",
      "city": "Lewiston",
      "stateAbbr": "ID",
      "zip9": "83501",
      "telephone": "2087431512",
      "webAddr": "www.headmasters.edu",
      "zipId": 83501,
      "stateFips": 16,
      "countyId": 16069,
      "sector": 6,
      "control": 3,
      "latitude": 46.421026,
      "longitude": -117.025943
    },
    {
      "id": 142115,
      "institutionName": "Boise State University",
      "address": "1910 University Dr",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83725",
      "telephone": "2084261000",
      "webAddr": "www.boisestate.edu",
      "zipId": 83725,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 1,
      "control": 1,
      "latitude": 43.604403,
      "longitude": -116.205789
    },
    {
      "id": 488998,
      "institutionName": "Paul Mitchell the School-Nampa",
      "address": "16803 North Marketplace Boulevard",
      "city": "Nampa",
      "stateAbbr": "ID",
      "zip9": "83687-0000",
      "telephone": "2082874060",
      "webAddr": "paulmitchell.edu/nampa/",
      "zipId": 83687,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 6,
      "control": 3,
      "latitude": 43.613794,
      "longitude": -116.594823
    },
    {
      "id": 455114,
      "institutionName": "College of Western Idaho",
      "address": "5500 East Opportunity Drive",
      "city": "Nampa",
      "stateAbbr": "ID",
      "zip9": "83687",
      "telephone": "2085623000",
      "webAddr": "cwidaho.cc/",
      "zipId": 83687,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 4,
      "control": 1,
      "latitude": 43.614106,
      "longitude": -116.507314
    },
    {
      "id": 461652,
      "institutionName": "Aveda Institute-Boise",
      "address": "10222 W Fairview Ave",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83704-4406",
      "telephone": "2083456164",
      "webAddr": "www.avedaidaho.com",
      "zipId": 83704,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 6,
      "control": 3,
      "latitude": 43.620545,
      "longitude": -116.309994
    },
    {
      "id": 142285,
      "institutionName": "University of Idaho",
      "address": "875 Perimeter Drive MS 2282",
      "city": "Moscow",
      "stateAbbr": "ID",
      "zip9": "83844-2282",
      "telephone": "8888843246",
      "webAddr": "www.uidaho.edu",
      "zipId": 83844,
      "stateFips": 16,
      "countyId": 16057,
      "sector": 1,
      "control": 1,
      "latitude": 46.726894,
      "longitude": -117.024296
    },
    {
      "id": 476762,
      "institutionName": "Velvet Touch Academy of Cosmetology",
      "address": "5820 East Franklin Road",
      "city": "Nampa",
      "stateAbbr": "ID",
      "zip9": "83687-5020",
      "telephone": "2089080123",
      "webAddr": "www.velvettouchacademy.com",
      "zipId": 83687,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 6,
      "control": 3,
      "latitude": 43.605098,
      "longitude": -116.510657
    },
    {
      "id": 455859,
      "institutionName": "Oliver Finley Academy of Cosmetology",
      "address": "6843 N Strawberry Glen Rd. #140",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83714",
      "telephone": "2086581115",
      "webAddr": "oliverfinley.com",
      "zipId": 83714,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 6,
      "control": 3,
      "latitude": 43.667102,
      "longitude": -116.281478
    },
    {
      "id": 460525,
      "institutionName": "Milan Institute-Nampa",
      "address": "1021 W. Hemingway",
      "city": "Nampa",
      "stateAbbr": "ID",
      "zip9": "83651",
      "telephone": "2084610616",
      "webAddr": "www.milaninstitute.edu",
      "zipId": 83651,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 9,
      "control": 3,
      "latitude": 43.600244,
      "longitude": -116.594362
    },
    {
      "id": 142443,
      "institutionName": "North Idaho College",
      "address": "1000 West Garden Avenue",
      "city": "Coeur d'Alene",
      "stateAbbr": "ID",
      "zip9": "83814-2199",
      "telephone": "2087693300",
      "webAddr": "www.nic.edu/",
      "zipId": 83814,
      "stateFips": 16,
      "countyId": 16055,
      "sector": 4,
      "control": 1,
      "latitude": 47.676416,
      "longitude": -116.798399
    },
    {
      "id": 142124,
      "institutionName": "Career Beauty College",
      "address": "57 College Ave",
      "city": "Rexburg",
      "stateAbbr": "ID",
      "zip9": "83440-1964",
      "telephone": "2083560222",
      "webAddr": "careerbeautycollege.com",
      "zipId": 83440,
      "stateFips": 16,
      "countyId": 16065,
      "sector": 6,
      "control": 3,
      "latitude": 43.824776,
      "longitude": -111.782334
    },
    {
      "id": 476957,
      "institutionName": "Academy di Firenze",
      "address": "149 West Main Street",
      "city": "Jerome",
      "stateAbbr": "ID",
      "zip9": "83338-2329",
      "telephone": "2086441546",
      "webAddr": "www.academydifirenze.com",
      "zipId": 83338,
      "stateFips": 16,
      "countyId": 16053,
      "sector": 6,
      "control": 3,
      "latitude": 42.723871,
      "longitude": -114.519826
    },
    {
      "id": 142328,
      "institutionName": "Lewis-Clark State College",
      "address": "500 8th Ave",
      "city": "Lewiston",
      "stateAbbr": "ID",
      "zip9": "83501-2698",
      "telephone": "2087925272",
      "webAddr": "www.lcsc.edu",
      "zipId": 83501,
      "stateFips": 16,
      "countyId": 16069,
      "sector": 1,
      "control": 1,
      "latitude": 46.412199,
      "longitude": -117.024875
    },
    {
      "id": 445780,
      "institutionName": "Cosmetology School of Arts and Science LLC",
      "address": "529 Overland Avenue",
      "city": "Burley",
      "stateAbbr": "ID",
      "zip9": "83318",
      "telephone": "2086784454",
      "webAddr": "cosmetologyschoolof-art.com",
      "zipId": 83318,
      "stateFips": 16,
      "countyId": 16031,
      "sector": 6,
      "control": 3,
      "latitude": 42.546938,
      "longitude": -113.792788
    },
    {
      "id": 454935,
      "institutionName": "Evans Hairstyling College-Rexburg",
      "address": "67 Winn Dr",
      "city": "Rexburg",
      "stateAbbr": "ID",
      "zip9": "83440",
      "telephone": "2083598141",
      "webAddr": "www.evanshairstylingcollege.com",
      "zipId": 83440,
      "stateFips": 16,
      "countyId": 16065,
      "sector": 6,
      "control": 3,
      "latitude": 43.824716,
      "longitude": -111.812372
    },
    {
      "id": 455600,
      "institutionName": "Brown Mackie College-Boise",
      "address": "9050 W Overland Rd, Ste 101",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83709",
      "telephone": "2083218800",
      "webAddr": "www.brownmackie.edu",
      "zipId": 83709,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 3,
      "control": 3,
      "latitude": 43.590789,
      "longitude": -116.295147
    },
    {
      "id": 440846,
      "institutionName": "Milan Institute-Boise",
      "address": "8590 W. Fairview Avenue",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83704-8320",
      "telephone": "2086729500",
      "webAddr": "www.milaninstitute.edu",
      "zipId": 83704,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 9,
      "control": 3,
      "latitude": 43.620897,
      "longitude": -116.288005
    },
    {
      "id": 142522,
      "institutionName": "Brigham Young University-Idaho",
      "address": "525 S Center",
      "city": "Rexburg",
      "stateAbbr": "ID",
      "zip9": "83460-1690",
      "telephone": "2084961411",
      "webAddr": "www.byui.edu",
      "zipId": 83460,
      "stateFips": 16,
      "countyId": 16065,
      "sector": 2,
      "control": 2,
      "latitude": 43.818408,
      "longitude": -111.782431
    },
    {
      "id": 260929,
      "institutionName": "Paul Mitchell the School-Boise",
      "address": "1270 S Vinnell Way",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83709",
      "telephone": "2082874032",
      "webAddr": "paulmitchell.edu/boise/",
      "zipId": 83709,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 6,
      "control": 3,
      "latitude": 43.594479,
      "longitude": -116.286058
    },
    {
      "id": 142461,
      "institutionName": "Northwest Nazarene University",
      "address": "623 S. University Blvd.",
      "city": "Nampa",
      "stateAbbr": "ID",
      "zip9": "83686-5897",
      "telephone": "2084678011",
      "webAddr": "www.nnu.edu",
      "zipId": 83686,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 2,
      "control": 2,
      "latitude": 43.562411,
      "longitude": -116.565783
    },
    {
      "id": 482033,
      "institutionName": "Milan Institute of Cosmetology-Nampa",
      "address": "1009 W. Hemingway",
      "city": "Nampa",
      "stateAbbr": "ID",
      "zip9": "83651",
      "telephone": "2084610616",
      "webAddr": "www.milaninstitute.edu",
      "zipId": 83651,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 6,
      "control": 3,
      "latitude": 43.60065,
      "longitude": -116.593951
    },
    {
      "id": 142054,
      "institutionName": "Carrington College-Boise",
      "address": "1122 N. Liberty St.",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83704-8742",
      "telephone": "2083778080",
      "webAddr": "www.carrington.edu",
      "zipId": 83704,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 6,
      "control": 3,
      "latitude": 43.615935,
      "longitude": -116.260571
    },
    {
      "id": 457493,
      "institutionName": "D & L Academy of Hair Design",
      "address": "113 Main Ave E",
      "city": "Twin Falls",
      "stateAbbr": "ID",
      "zip9": "83301",
      "telephone": "2087364972",
      "webAddr": "dandlacademyofhair.com",
      "zipId": 83301,
      "stateFips": 16,
      "countyId": 16083,
      "sector": 6,
      "control": 3,
      "latitude": 42.555677,
      "longitude": -114.469494
    },
    {
      "id": 142407,
      "institutionName": "Aveda Institute-Twin Falls",
      "address": "837 Pole Line Road Suite 103",
      "city": "Twin Falls",
      "stateAbbr": "ID",
      "zip9": "83301",
      "telephone": "2087337777",
      "webAddr": "www.avedaidaho.com",
      "zipId": 83301,
      "stateFips": 16,
      "countyId": 16083,
      "sector": 6,
      "control": 3,
      "latitude": 42.593695,
      "longitude": -114.461693
    },
    {
      "id": 454944,
      "institutionName": "Paul Mitchell the School-Rexburg",
      "address": "557 Mariah Ave",
      "city": "Rexburg",
      "stateAbbr": "ID",
      "zip9": "83440",
      "telephone": "2086560800",
      "webAddr": "paulmitchell.edu/rexburg",
      "zipId": 83440,
      "stateFips": 16,
      "countyId": 16065,
      "sector": 6,
      "control": 3,
      "latitude": 43.814418,
      "longitude": -111.80516
    },
    {
      "id": 142489,
      "institutionName": "Elevate Salon Institute-Chubbuck",
      "address": "141 East Chubbuck Road",
      "city": "Chubbuck",
      "stateAbbr": "ID",
      "zip9": "83202",
      "telephone": "2082329170",
      "webAddr": "https://www.esichubbuck.com",
      "zipId": 83202,
      "stateFips": 16,
      "countyId": 16005,
      "sector": 6,
      "control": 3,
      "latitude": 42.920006,
      "longitude": -112.465046
    },
    {
      "id": 142294,
      "institutionName": "The College of Idaho",
      "address": "2112 Cleveland Blvd",
      "city": "Caldwell",
      "stateAbbr": "ID",
      "zip9": "83605-4432",
      "telephone": "2084595011",
      "webAddr": "www.collegeofidaho.edu",
      "zipId": 83605,
      "stateFips": 16,
      "countyId": 16027,
      "sector": 2,
      "control": 2,
      "latitude": 43.652653,
      "longitude": -116.676838
    },
    {
      "id": 476850,
      "institutionName": "Boise Barber College",
      "address": "7709 W. Overland Rd. 100",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83709",
      "telephone": "2083789933",
      "webAddr": "boisebarbercollege.com",
      "zipId": 83709,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 6,
      "control": 3,
      "latitude": 43.5497069202887,
      "longitude": -116.289371327976
    },
    {
      "id": 443942,
      "institutionName": "The Beauty Institute Schwarzkopf Professional - Boise",
      "address": "7709 W. Overland Road Suite 100",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83709",
      "telephone": "2084298070",
      "webAddr": "thebeautyinstituteskp.com",
      "zipId": 83709,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 6,
      "control": 3,
      "latitude": 43.5888,
      "longitude": -116.277841
    },
    {
      "id": 436100,
      "institutionName": "Mr Leon's School of Hair Design-Lewiston",
      "address": "205 10th St",
      "city": "Lewiston",
      "stateAbbr": "ID",
      "zip9": "83501",
      "telephone": "2088822923",
      "webAddr": "mrleons.com",
      "zipId": 83501,
      "stateFips": 16,
      "countyId": 16069,
      "sector": 6,
      "control": 3,
      "latitude": 46.418004,
      "longitude": -117.02046
    },
    {
      "id": 142179,
      "institutionName": "College of Eastern Idaho",
      "address": "1600 S 25th E",
      "city": "Idaho Falls",
      "stateAbbr": "ID",
      "zip9": "83404-5788",
      "telephone": "2085353000",
      "webAddr": "www.eitc.edu",
      "zipId": 83404,
      "stateFips": 16,
      "countyId": 16019,
      "sector": 4,
      "control": 1,
      "latitude": 43.486041,
      "longitude": -111.985519
    },
    {
      "id": 142337,
      "institutionName": "ITT Technical Institute-Boise",
      "address": "12302 W. Explorer Dr",
      "city": "Boise",
      "stateAbbr": "ID",
      "zip9": "83713-1529",
      "telephone": "2083228844",
      "webAddr": "www.itt-tech.edu",
      "zipId": 83713,
      "stateFips": 16,
      "countyId": 16001,
      "sector": 3,
      "control": 3,
      "latitude": 43.660091,
      "longitude": -116.335509
    },
    {
      "id": 457509,
      "institutionName": "Master Educators Beauty School",
      "address": "1205 Filer Ave E",
      "city": "Twin Falls",
      "stateAbbr": "ID",
      "zip9": "83301-4118",
      "telephone": "2087360044",
      "webAddr": "www.mastereducatorsbeautyschool.com",
      "zipId": 83301,
      "stateFips": 16,
      "countyId": 16083,
      "sector": 6,
      "control": 3,
      "latitude": 42.571146,
      "longitude": -114.458186
    }
  ],
  "errors": [],
  "timings": [
    "Execute query: 0.0049ms"
  ]
}
```
### `GET` /institutions/{search}
Return a list of institutions matching the supplied name.

#### Code Examples

```har
{
    "method": "GET",
    "url": "https://ipeds.emsicloud.com/institutions/Harvard",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"}
    ]
}
```

#### Response Examples

```json
{
  "rows": [
    {
      "id": 166027,
      "institutionName": "Harvard University",
      "address": "Massachusetts Hall",
      "city": "Cambridge",
      "stateAbbr": "MA",
      "zip9": "02138",
      "telephone": "6174951000",
      "webAddr": "www.harvard.edu",
      "zipId": 2138,
      "stateFips": 25,
      "countyId": 25017,
      "sector": 2,
      "control": 2,
      "latitude": 42.374471,
      "longitude": -71.118313
    },
    {
      "id": 417220,
      "institutionName": "Harvard H Ellis Regional Vocational Technical Sch",
      "address": "613 Upper Maple St",
      "city": "Danielson",
      "stateAbbr": "CT",
      "zip9": "06239",
      "telephone": "8607748511",
      "webAddr": " ",
      "zipId": 6239,
      "stateFips": 9,
      "countyId": 9015,
      "sector": 7,
      "control": 1,
      "latitude": 41.819752,
      "longitude": -71.892916
    }
  ],
  "errors": [],
  "timings": [
    "Execute Query: 208.7225ms"
  ]
}
```

### `POST` /institutions/search
Search institutions using multiple values.
Valid search types are `zip`, `fips`, `city`, `id`, and `name`.

#### Code Examples

##### Search multiple ZIP codes
```har
{
    "method":"POST",
    "url":"https://ipeds.emsicloud.com/institutions/search",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"},
		{"name":"Content-Type", "value":"application/json"}
	],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"searchType\": \"zip\", \"values\":[\"83843\", \"42303\"]}"
    }
}
```

#### Response Examples

```json
{
  "rows": [
    {
      "id": 440396,
      "institutionName": "New Saint Andrews College",
      "address": "405 S. Main Street",
      "city": "Moscow",
      "stateAbbr": "ID",
      "zip9": "83843-1525",
      "telephone": "2088821566",
      "webAddr": "nsa.edu",
      "zipId": 83843,
      "stateFips": 16,
      "countyId": 16057,
      "sector": 2,
      "control": 2,
      "latitude": 46.731991,
      "longitude": -117.001732
    },
    {
      "id": 142416,
      "institutionName": "Mr Leon's School of Hair Design-Moscow",
      "address": "618 S Main St",
      "city": "Moscow",
      "stateAbbr": "ID",
      "zip9": "83843",
      "telephone": "2088822923",
      "webAddr": "mrleons.com",
      "zipId": 83843,
      "stateFips": 16,
      "countyId": 16057,
      "sector": 6,
      "control": 3,
      "latitude": 46.729394,
      "longitude": -117.001352
    },
    {
      "id": 247940,
      "institutionName": "Owensboro Community and Technical College",
      "address": "4800 New Hartford Rd",
      "city": "Owensboro",
      "stateAbbr": "KY",
      "zip9": "42303",
      "telephone": "2706864400",
      "webAddr": "https://owensboro.kctcs.edu",
      "zipId": 42303,
      "stateFips": 21,
      "countyId": 21059,
      "sector": 4,
      "control": 1,
      "latitude": 37.717317,
      "longitude": -87.082995
    },
    {
      "id": 484330,
      "institutionName": "Ross Medical Education Center-Owensboro",
      "address": "410 Southtown Boulevard",
      "city": "Owensboro",
      "stateAbbr": "KY",
      "zip9": "42303-7757",
      "telephone": "2706845334",
      "webAddr": "www.rosseducation.edu",
      "zipId": 42303,
      "stateFips": 21,
      "countyId": 21059,
      "sector": 9,
      "control": 3,
      "latitude": 37.72084,
      "longitude": -87.119151
    }
  ],
  "errors": [],
  "timings": [
    "Validate query parameters: 0.0016ms",
    "Execute query: 0.0143ms"
  ]
}
```

##### Search multiple names
```har
{
    "method":"POST",
    "url":"https://ipeds.emsicloud.com/institutions/search",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"},
		{"name":"Content-Type", "value":"application/json"}
	],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"searchType\": \"name\", \"values\":[\"Harvard\", \"Yale\"]}"
    }
}
```

#### Response Examples

```json
{
  "rows": [
    {
      "id": 166027,
      "institutionName": "Harvard University",
      "address": "Massachusetts Hall",
      "city": "Cambridge",
      "stateAbbr": "MA",
      "zip9": "02138",
      "telephone": "6174951000",
      "webAddr": "www.harvard.edu",
      "zipId": 2138,
      "stateFips": 25,
      "countyId": 25017,
      "sector": 2,
      "control": 2,
      "latitude": 42.374471,
      "longitude": -71.118313
    },
    {
      "id": 382267,
      "institutionName": "Royale College of Beauty and Barbering",
      "address": "27485 Commerce Center Dr",
      "city": "Temecula",
      "stateAbbr": "CA",
      "zip9": "92590",
      "telephone": "9516760833",
      "webAddr": "www.rcofb.com",
      "zipId": 92590,
      "stateFips": 6,
      "countyId": 6065,
      "sector": 9,
      "control": 3,
      "latitude": 33.515476,
      "longitude": -117.164001
    },
    {
      "id": 130785,
      "institutionName": "Yale-New Haven Hospital Dietetic Internship",
      "address": "20 York St EPB 806",
      "city": "New Haven",
      "stateAbbr": "CT",
      "zip9": "06510",
      "telephone": "2036888822",
      "webAddr": "www.ynhh.org",
      "zipId": 6510,
      "stateFips": 9,
      "countyId": 9009,
      "sector": 2,
      "control": 2,
      "latitude": 41.304214,
      "longitude": -72.935579
    },
    {
      "id": 130794,
      "institutionName": "Yale University",
      "address": "Woodbridge Hall",
      "city": "New Haven",
      "stateAbbr": "CT",
      "zip9": "06520",
      "telephone": "2034324771",
      "webAddr": "www.yale.edu",
      "zipId": 6520,
      "stateFips": 9,
      "countyId": 9009,
      "sector": 2,
      "control": 2,
      "latitude": 41.311158,
      "longitude": -72.926688
    },
    {
      "id": 417220,
      "institutionName": "Harvard H Ellis Regional Vocational Technical Sch",
      "address": "613 Upper Maple St",
      "city": "Danielson",
      "stateAbbr": "CT",
      "zip9": "06239",
      "telephone": "8607748511",
      "webAddr": " ",
      "zipId": 6239,
      "stateFips": 9,
      "countyId": 9015,
      "sector": 7,
      "control": 1,
      "latitude": 41.819752,
      "longitude": -71.892916
    }
  ],
  "errors": [],
  "timings": [
    "Validate query parameters: 0.0016ms",
    "Execute query: 130.2112ms"
  ]
}
```

### `GET` /institutions/all/{offset}/{limit}
Lists all institutions with pagination.

#### Code Examples
```har
{
    "method":"GET",
    "url":"https://ipeds.emsicloud.com/institutions/all/0/10",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"}
	]
}
```

#### Response Examples
```json
[
  {
    "id": 218867,
    "institutionName": "Sumter Beauty College",
    "address": "921 Carolina Ave",
    "city": "Sumter",
    "stateAbbr": "SC",
    "zip9": "29150-2871",
    "telephone": "8037737311",
    "webAddr": "www.sumterbeautycollege.com",
    "zipId": 29150,
    "stateFips": 45,
    "countyId": 45085,
    "sector": 9,
    "control": 3,
    "latitude": 33.94459,
    "longitude": -80.351865
  },
  {
    "id": 198367,
    "institutionName": "Craven Community College",
    "address": "800 College Ct",
    "city": "New Bern",
    "stateAbbr": "NC",
    "zip9": "28562-4900",
    "telephone": "2526387200",
    "webAddr": "www.cravencc.edu",
    "zipId": 28562,
    "stateFips": 37,
    "countyId": 37049,
    "sector": 4,
    "control": 1,
    "latitude": 35.111516,
    "longitude": -77.102232
  },
  {
    "id": 216454,
    "institutionName": "Triangle Tech Inc-Dubois",
    "address": "225 Tannery Row Road",
    "city": "Falls Creek",
    "stateAbbr": "PA",
    "zip9": "15840-3333",
    "telephone": "8143712090",
    "webAddr": "www.triangle-tech.edu",
    "zipId": 15840,
    "stateFips": 42,
    "countyId": 42065,
    "sector": 6,
    "control": 3,
    "latitude": 41.147974,
    "longitude": -78.795923
  },
  {
    "id": 485582,
    "institutionName": "MKG Beauty & Business",
    "address": "379 Atwood Avenue",
    "city": "Cranston",
    "stateAbbr": "RI",
    "zip9": "02920-4358",
    "telephone": "4012286889",
    "webAddr": "www.avedainstituteri.edu",
    "zipId": 2920,
    "stateFips": 44,
    "countyId": 44007,
    "sector": 9,
    "control": 3,
    "latitude": 41.78608,
    "longitude": -71.472161
  },
  {
    "id": 451130,
    "institutionName": "Wolford College",
    "address": "1336 Creekside Boulevard, Suite 2",
    "city": "Naples",
    "stateAbbr": "FL",
    "zip9": "34108",
    "telephone": "2395131135",
    "webAddr": "https://www.wolford.edu/",
    "zipId": 34108,
    "stateFips": 12,
    "countyId": 12021,
    "sector": 3,
    "control": 3,
    "latitude": 26.268251,
    "longitude": -81.791959
  },
  {
    "id": 210669,
    "institutionName": "Allegheny College",
    "address": "520 N Main St",
    "city": "Meadville",
    "stateAbbr": "PA",
    "zip9": "16335-3902",
    "telephone": "8143323100",
    "webAddr": "www.allegheny.edu",
    "zipId": 16335,
    "stateFips": 42,
    "countyId": 42039,
    "sector": 2,
    "control": 2,
    "latitude": 41.648068,
    "longitude": -80.146922
  },
  {
    "id": 176770,
    "institutionName": "Cox College",
    "address": "1423 N Jefferson",
    "city": "Springfield",
    "stateAbbr": "MO",
    "zip9": "65802",
    "telephone": "4172693401",
    "webAddr": "www.coxcollege.edu",
    "zipId": 65802,
    "stateFips": 29,
    "countyId": 29077,
    "sector": 2,
    "control": 2,
    "latitude": 37.225116,
    "longitude": -93.290233
  },
  {
    "id": 196662,
    "institutionName": "Troy School of Beauty Culture",
    "address": "86 Congress St",
    "city": "Troy",
    "stateAbbr": "NY",
    "zip9": "12180",
    "telephone": "5182735144",
    "webAddr": "",
    "zipId": 12180,
    "stateFips": 36,
    "countyId": 36083,
    "sector": 9,
    "control": 3,
    "latitude": 42.7506345083317,
    "longitude": -73.6022584289222
  },
  {
    "id": 482510,
    "institutionName": "DeVry University-Michigan",
    "address": "26999 Central Park Blvd., Ste. 125",
    "city": "Southfield",
    "stateAbbr": "MI",
    "zip9": "48076",
    "telephone": "2482131610",
    "webAddr": "www.devry.edu",
    "zipId": 48076,
    "stateFips": 26,
    "countyId": 26125,
    "sector": 3,
    "control": 3,
    "latitude": 42.487451,
    "longitude": -83.244788
  },
  {
    "id": 441812,
    "institutionName": "GENESIS VOCATIONAL TRAINING",
    "address": "7111 HARWIN STE 105",
    "city": "HOUSTON",
    "stateAbbr": "TX",
    "zip9": "77036",
    "telephone": "7139956217",
    "webAddr": "www.gvttexas.com",
    "zipId": 77036,
    "stateFips": 48,
    "countyId": 48201,
    "sector": 9,
    "control": 3,
    "latitude": 29.7016995750462,
    "longitude": -95.5358686240504
  }
]
```

## SOC/CIP Mapping Endpoints
### `POST` /soccip/cip2soc
This endpoint maps a CIP (Classification of Instructional Programs) code to the
SOC (Standard Occupation Classification) codes it most likely trains for.
For more information on CIP codes, see the [NCES site](https://nces.ed.gov/ipeds/cipcode/Default.aspx?y=56).

#### Code Examples

##### What do Criminology and National Security Policy Studies train for?
```har
{
    "method":"POST",
    "url":"https://ipeds.emsicloud.com/soccip/cip2soc",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"},
		{"name":"Content-Type", "value":"application/json"}
	],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"cipCodes\": [\"45.0902\", \"45.0401\"]}"
    }
}
```

#### Response Examples
```json
{
  "mapping": [
    {
      "code": "45.0902",
      "corresponding": [
        "11-9199",
        "19-3094",
        "25-1099"
      ]
    },
    {
      "code": "45.0401",
      "corresponding": [
        "19-3041"
      ]
    }
  ],
  "errors": [],
  "timings": [
    "Execute query: 0.0067ms"
  ]
}
```

### `POST` /soccip/soc2cip
This endpoint maps from one or more SOC codes to the CIP codes of the programs
which most likely train for them.

#### Code Examples

##### Which programs train for Political Scientists?
```har
{
    "method":"POST",
    "url":"https://ipeds.emsicloud.com/soccip/soc2cip",
    "headers": [
		{"name":"Authorization", "value":"Bearer <access_token>"},
		{"name":"Content-Type", "value":"application/json"}
	],
    "postData": {
        "mimeType": "application/json",
        "text": "{\"socCodes\": [\"19-3094\"]}"
    }
}
```

#### Response Examples
```json
{
  "mapping": [
    {
      "code": "19-3094",
      "corresponding": [
        "30.2001",
        "44.0501",
        "44.0504",
        "45.0901",
        "45.0902",
        "45.0999",
        "45.1001",
        "45.1002",
        "45.1003",
        "45.1004",
        "45.1099"
      ]
    }
  ],
  "errors": [],
  "timings": [
    "Execute query: 0.4458ms"
  ]
}
```
