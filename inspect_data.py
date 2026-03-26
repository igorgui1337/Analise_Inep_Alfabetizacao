import pandas as pd
import json

try:
    df = pd.read_excel('resultados_e_metas_ufs_2025.xlsx', header=None) # read without header first and see
    print("Writing to file...")
    with open('data_structure.txt', 'w', encoding='utf-8') as f:
        f.write("Columns (row 0):\n")
        f.write(str(df.iloc[0].tolist()) + "\n")
        f.write("Columns (row 1):\n")
        f.write(str(df.iloc[1].tolist()) + "\n")
        f.write("\nFirst 10 rows:\n")
        f.write(df.head(10).to_string())
except Exception as e:
    with open('data_structure.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
