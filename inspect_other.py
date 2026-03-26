import pandas as pd
import json

files = ['resultados_e_metas_ufs.xlsx', 'resultados_e_metas_ufs_2024_2.xlsx', 'resultados_e_metas_ufs_2025.xlsx']
out = {}

for file in files:
    try:
        df = pd.read_excel(file, header=1)
        out[file] = df.columns.tolist()
    except Exception as e:
        out[file] = str(e)

with open('columns.json', 'w') as f:
    json.dump(out, f, indent=2)
