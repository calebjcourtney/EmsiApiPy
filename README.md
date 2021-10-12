# EmsiApiPy
This library is designed as a helpful resource for connecting to [Emsi's APIs](https://api.emsidata.com/). It is provided as-is under no warranty by Emsi, but rather as an effort by various users to provide a centralized, coordinated way to access the APIs in an effective manner. It is currently under active development, so improvements are being added all the time, and these may include breaking changes.

## Table of Contents
1. [Installation](  #installation)
2. [Setup](  #Setup)
3. [Testing](  #Testing)
4. [Documentation Links](  #Usage)

## Installation
Clone the repository. Install the required packages in `requirements.txt` into a [python virtual environment](https://www.geeksforgeeks.org/python-virtual-environment/). Here's an example using [virtualenv](https://virtualenv.pypa.io/en/latest/), which is what the source code has been tested in .

```bash
virtualenv - p python3 venv
source venv/bin/activate
pip install - r requirements.txt
```

## Setup
There is a file in the repository named `permissions.py.sample`. When the repo is cloned, it will look like this:

```python
import os

if "emsi_client_id" in os.environ and "emsi_client_secret" in os.environ:
    DEFAULT = {
        "username": os.environ.get("emsi_client_id"),
        "password": os.environ.get("emsi_client_secret")
    }

else:
    # you can save your client_id and client_secret locally instead
    DEFAULT = {
        "username": "foo",
        "password": "bar"
    }

```

To setup the library so it can read your credentials, you have two options:
- Replace the `foo` and `bar` values to what was provided by the Emsi API support team. Please simply be careful about sharing the files
- Add two new environment variables called `emsi_client_id` and `emsi_client_secret`. To learn how to set an environment variable, I recommend [this article](https://www.schrodinger.com/kb/1842).

Be sure to rename the file to `permissions.py`. This is what the library will look for when connecting to the API.

Make sure that the EmsiApiPy folder is accessible from your [`PYTHONPATH`](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). You will know you've set it up correctly if you can run `import EmsiApiPy` from within your python environment.

## Testing
Tests can be run with `./tests/run_tests.sh`. Please be aware that this is testing all of the API connections available. If you don't have access to one of the APIs, then the tests will fail. It might be worth editing the `run_tests.sh` file to ensure that you are only running tests for the APIs that you want to access.


## APIs Covered
- [ACS Indicators](docs/acs_indicators.md)
- [Automation Index](docs/automation_index.md)
- [Canada Job Postings](docs/ca_postings.md)
- Companies
- [Core LMI](docs/core_lmi.md)
- Geography
- Global Postings
- Global Profiles
- Input-Output
- IPEDS
- [Open Skills](docs/open_skills.md)
- Talent Benchmark
- [Titles](docs/emsi_titles.md)
- UK Job Postings
- US Compensation
- [US Job Postings](docs/us_postings.md)
- [US Profiles](docs/us_profiles.md)
