from __future__ import annotations

import EmsiApiPy
import pandas as pd

# create the connection
conn = EmsiApiPy.SkillsClassificationConnection()

# download all the skills
data = conn.get_list_all_skills()["data"]

# load into pandas
df = pd.DataFrame(
    {
        "id": [record["id"] for record in data],
        "infoUrl": [record["infoUrl"] for record in data],
        "name": [record["name"] for record in data],
        "type": [record["type"]["name"] for record in data],
    },
)

# export
writer = pd.ExcelWriter("skills_list.xlsx")
df.to_excel(writer, "Skills", index=False)
writer.save()
