from __future__ import annotations

import EmsiApiPy

conn = EmsiApiPy.CoreLMIConnection()

dataset = "emsi.us.grossregionalproduct"

dimension = "Area"

df = conn.get_dimension_hierarchy_df(
    dataset=dataset,
    dimension=dimension,
    datarun="2023.1",
)

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
df = df.loc[df["level_name"] == "2"]

payload = {
    "metrics": [
        {
            "name": "Dollars.2019",
        },
    ],
    "constraints": [
        {
            "dimensionName": "Area",
            "map": {
                row[1]["name"]: [row[1]["child"]] for row in df.iterrows()
            },
        },
    ],
}

data_df = conn.post_retrieve_df(
    dataset=dataset,
    payload=payload,
    datarun="2023.1",
)
print(data_df.head())

"""
         Area  Dollars.2019
0     Alabama  2.234497e+11
1      Alaska  5.222207e+10
2     Arizona  3.504984e+11
3    Arkansas  1.297678e+11
4  California  3.013869e+12
"""
