import EmsiApiPy
import pandas as pd

# create the connection
conn = EmsiApiPy.SkillsClassificationConnection()

# download all the skills
data = conn.get_list_all_skills()

# load into pandas
df = pd.DataFrame(data['skills'])

# export
writer = pd.ExcelWriter("skills_list.xlsx")
df.to_excel(writer, 'Skills', index = False)
writer.save()
