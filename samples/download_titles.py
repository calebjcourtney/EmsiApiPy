from __future__ import annotations

import EmsiApiPy
import pandas as pd

# create the connection
conn = EmsiApiPy.TitlesConnection()

# download the data
data = conn.get_list_all_titles()

# load into pandas df
df = pd.DataFrame(data)

# export
writer = pd.ExcelWriter("title_list.xlsx")
df.to_excel(writer, "Titles", index=False)
writer.save()
