# EmsiApiPy
This library is designed as a helpful resource for connecting to [Emsi's APIs](https://api.emsidata.com/). It is provided as-is under no warranty by Emsi, but rather as an effort by various users to provide a centralized, coordinated way to access the APIs in an effective manner.

# Table of Contents
1. [Installation](#installation)
2. [Setup](#setup)
3. [Testing](#testing)
4. [Usage](#usage)
    - [Core LMI Usage Examples](#core-lmi-usage-examples)


# Installation
Clone the repository. Install the required packages in `requirements.txt` into a python [virtualenvironment](https://www.geeksforgeeks.org/python-virtual-environment/). Here's an example using [virtualenv](https://virtualenv.pypa.io/en/latest/), which is what the source code has been tested in.
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

# Setup
There is a file in the repository named `permissions.py.sample`. When the repo is cloned, it will look like this:
```
DEFAULT = {
    "username": "foo",
    "password": "bar"
}
```
You will need to change the `foo` and `bar` values to what was provided by the Emsi API support team, and rename the file to `permissions.py`.

Make sure that the EmsiApiPy folder is accessible from your [`PYTHONPATH`](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). You will know you've set it up correctly if you can run `import EmsiApiPy` from within your python environment.


# Testing
Tests can be run with `pytest tests/runTests.py`. Please be aware that this is testing all of the functions as they query the API, and this may take some time to run. Additionally, if you don't have access to some APIs, not all the tests will pass. Functionality may be added in the future to skip tests for APIs that you don't have access to.


# Usage
## Core LMI Usage Examples
```
import EmsiApiPy

conn = EmsiApiPy.CoreLMIConnection()

dataset = "emsi.us.grossregionalproduct"

dimension = "Area"

df = conn.get_dimension_hierarchy_df(dataset = dataset, dimension = dimension)

print(df.head())

"""
   child parent           name abbr level_name display_id
0      0      0  United States   US          1          0
1      1      0        Alabama   AL          2          1
2     10      0       Delaware   DE          2         10
3  10001     10           Kent   DE          3      10001
4  10003     10     New Castle   DE          3      10003
"""

# limit only to the states
df = df.loc[df['level_name'] == '2']

payload = {
    "metrics": [
        {
            "name": "Dollars.2019"
        }
    ],
    "constraints": [
        {
            "dimensionName": "Area",
            "map": {row[1]['name']: [row[1]["child"]] for row in df.iterrows()}
        }
    ]
}

data_df = conn.post_retrieve_df(dataset = dataset, payload = payload)
print(data_df.head())

"""
         Area  Dollars.2019
0     Alabama  2.234497e+11
1      Alaska  5.222207e+10
2     Arizona  3.504984e+11
3    Arkansas  1.297678e+11
4  California  3.013869e+12
"""

```
