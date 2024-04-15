"""
Use case
This is an interface for retrieving key indicators to help benchmark talent by location in the United States.

About the data
The data in this API exposes key talent benchmarking metrics oriented around supply, demand, diversity, and compensation.
These metrics are aggregated from various Emsi datasets including US job postings, US profiles, and US Diversity
along with our Compensation model for any job title and city in the United States.

Docs:
# create the connection
from EmsiApiPy import TalentBenchmarkConnection
conn = TalentBenchmarkConnection()

# get the status of the service
conn.get_status()
# or, optionally:
conn.get_service_status()
```
{
    "message": "Service is healthy",
    "healthy": true
}
```

# get the metadata
conn.get_service_metadata()
```
{
    "attribution": {
      "title": "Talent Benchmark",
      "body": "Emsi's Talent Benchmark API aggregates data points from our US job postings, US profiles, and US Diversity datasets along with our Compensation model estimates."
    },
    "access": [
      "supply",
      "demand",
      "compensation",
      "diversity"
    ]
}
```

# get the benchmark summary
conn.post_benchmark_summary(
    city = "moscow id",
    title = "web developer"
)
```
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
      "profiles": 28,
      "companies": 12
    },
    "demand": {
      "postings": 3,
      "companies": 2
    },
    "compensation": {
      "minSalary": 20208,
      "medianSalary": 49832,
      "maxSalary": 103298
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

# get the supply benchmark data
conn.post_supply_benchmark_data(
    city = "moscow id",
    title = "web developer"
)
```
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
      "profiles": 28,
      "companies": 12
    },
    "topCompanies": [
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
    "topSkills": [
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
    "topTitles": [
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

# get the demand benchmark data
conn.post_demand_benchmark_data(
    city = "moscow id",
    title = "web developer"
)
```
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
      "postings": 3,
      "companies": 2
    },
    "topCompanies": [
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
    "topSkills": [
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
    "topTitles": [
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

# get the compensation information
conn.post_compensation_benchmark_data(
    city = "moscow id",
    title = "web developer"
)
```
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
      "minSalary": 20208,
      "medianSalary": 49832,
      "maxSalary": 103298
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

# get the diversity benchmark data
conn.post_diversity_benchmark_data(
    city = "moscow id",
    title = "web developer"
)
```
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

"""
from __future__ import annotations

from .base import EmsiBaseConnection


class TalentBenchmarkConnection(EmsiBaseConnection):
    """
    Use case
    This is an interface for retrieving key indicators to help benchmark talent by location in the United States.

    About the data
    The data in this API exposes key talent benchmarking metrics oriented around supply, demand, diversity, and compensation.
    These metrics are aggregated from various Emsi datasets including US job postings, US profiles,
    and US Diversity along with our Compensation model for any job title and city in the United States.

    Attributes:
        base_url (str): what every url has to start with to query the API
        scope (str): the scope for requesting the proper access token
        token (str): the auth token received from the auth API
    """

    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://emsiservices.com/benchmark/"
        self.scope = "benchmark"

        self.get_new_token()

        self.name = "Talent_Benchmark"

    def get_service_status(self) -> str:
        # same as get_status, but this is more in line with the Emsi documentation
        return self.get_status()

    def __send_request(self, endpoint, city, title) -> dict:
        """
        Private function to abstract the building of the payload and making the request

        Returns:
            dict: the body of the response from the API as a json object
        """
        payload = {"title": title, "city": city}
        return self.download_data(endpoint, payload=payload).json()

    def get_service_metadata(self) -> dict:
        """
        https://api.emsidata.com/apis/talent-benchmark#get-get-service-metadata
        Get service metadata, including access information and attribution text.

        Returns:
            dict: dictionary of attribution and access available to the given client_id
        """
        return self.download_data("meta").json()["data"]

    def post_benchmark_summary(self, city: str, title: str) -> dict:
        """
        https://api.emsidata.com/apis/talent-benchmark#post-get-benchmark-summary
        Get summary data on each metric that you have access to.

        Returns:
            dict: search parameters and data response from the API
        """
        return self.__send_request("", city, title)

    def post_supply_benchmark_data(self, city: str, title: str) -> dict:
        """
        https://api.emsidata.com/apis/talent-benchmark#post-get-supply-benchmark-data
        Emsi aggregates online social profiles from all over the web. The details in this endpoint provide aggregate totals for the top employers, top titles, and top skills associated with the profiles matching your search.

        Returns:
            dict: search parameters and data response from the API
        """
        return self.__send_request("supply", city, title)

    def post_demand_benchmark_data(self, city: str, title: str) -> dict:
        """
        https://api.emsidata.com/apis/talent-benchmark#post-get-demand-benchmark-data
        Emsi aggregates job posting details from all over the web. The details in this endpoint provide aggregate totals for the top employers, top titles, and top skills associated with the postings matching your search.

        Returns:
            dict: search parameters and data response from the API
        """
        return self.__send_request("demand", city, title)

    def post_compensation_benchmark_data(self, city: str, title: str) -> dict:
        """
        https://api.emsidata.com/apis/talent-benchmark#post-get-compensation-benchmark-data
        Emsi models compensation data using government data and advertised salary observations identified from job postings data.

        Returns:
            dict: search parameters and data response from the API
        """
        return self.__send_request("compensation", city, title)

    def post_diversity_benchmark_data(self, city: str, title: str) -> dict:
        """
        https://api.emsidata.com/apis/talent-benchmark#post-get-diversity-benchmark-data
        Emsi models diversity data by applying a staffing pattern to government data related to industries.

        Returns:
            dict: search parameters and data response from the API
        """
        return self.__send_request("diversity", city, title)
