import pandas as pd
import numpy as np
import json
import os

# 1. Carregar dados
try:
    df = pd.read_excel('resultados_e_metas_ufs_2025.xlsx', header=1)
except Exception as e:
    print(f"Erro ao ler arquivo: {e}")
    exit(1)

# 2. Limpeza básica
# Limpar as colunas de "META_FINAL" e "PC_ALUNO" que tenham ">80"
cols_to_clean = [c for c in df.columns if 'PC_ALUNO' in c or 'META_FINAL' in c]
for c in cols_to_clean:
    df[c] = df[c].astype(str).str.replace('>', '').str.replace('<', '').str.strip()
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Renomear colunas para o padrão
df = df.rename(columns={
    'PC_ALUNO_ALFABETIZADO_2023': 'ALF_2023',
    'PC_ALUNO_ALFABETIZADO_2024': 'ALF_2024',
    'PC_ALUNO_ALFABETIZADO_2025': 'ALF_2025',
    'META_FINAL_2024': 'META_2024',
    'META_FINAL_2025': 'META_2025',
    'META_FINAL_2026': 'META_2026',
    'META_FINAL_2027': 'META_2027',
    'META_FINAL_2028': 'META_2028',
    'META_FINAL_2029': 'META_2029',
    'META_FINAL_2030': 'META_2030',
    'PC_AVALIADOS_LP': 'PARTICIPACAO'
})

# Dicionário de regiões
regiao_map = {
    'AC': 'Norte', 'AM': 'Norte', 'AP': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}

# 3. Separar Brasil e criar base UFs
df_brasil = df[df['NOME_UF'] == 'Brasil'].copy()
df_uf = df[df['NOME_UF'] != 'Brasil'].copy()

# Remover linhas nulas sem UF (se tiver)
df_uf = df_uf.dropna(subset=['SIGLA_UF'])
df_uf['REGIAO'] = df_uf['SIGLA_UF'].map(regiao_map)

# 4. Criar Métricas Calculadas
df_uf['VAR_23_24'] = df_uf['ALF_2024'] - df_uf['ALF_2023']
df_uf['VAR_24_25'] = df_uf['ALF_2025'] - df_uf['ALF_2024']
df_uf['VAR_23_25'] = df_uf['ALF_2025'] - df_uf['ALF_2023']

df_uf['GAP_META_2024'] = df_uf['ALF_2024'] - df_uf['META_2024']
df_uf['GAP_META_2025'] = df_uf['ALF_2025'] - df_uf['META_2025']

# Tendência e Projeção Simples (Taxa média anual de crescimento baseada no histórico 23-25)
# Algumas UFs não têm 2023. Para essas, a tendência será a variação de 24-25
df_uf['TENDENCIA_ANUAL'] = np.where(
    df_uf['ALF_2023'].notna(), 
    (df_uf['ALF_2025'] - df_uf['ALF_2023']) / 2, 
    df_uf['ALF_2025'] - df_uf['ALF_2024']
)

for y in range(2026, 2030):
    df_uf[f'PROJ_{y}'] = np.clip(df_uf['ALF_2025'] + df_uf['TENDENCIA_ANUAL'] * (y - 2025), a_min=0, a_max=100)
    # Status atingimento
    df_uf[f'STATUS_{y}'] = np.where(df_uf[f'PROJ_{y}'] >= df_uf[f'META_{y}'], 'Atinge', 'Não atinge')

df_uf['STATUS_2025'] = np.where(df_uf['ALF_2025'] >= df_uf['META_2025'], 'Acima da Meta', 'Abaixo da Meta')

# Exportar para JSON para uso no dashboard
data_json = df_uf.to_dict(orient='records')
brasil_json = df_brasil.to_dict(orient='records')[0] if len(df_brasil) > 0 else {}

with open('dados_dashboard.json', 'w', encoding='utf-8') as f:
    json.dump({'ufs': data_json, 'brasil': brasil_json}, f, ensure_ascii=False, indent=2)

print("Processamento de dados concluído. dados_dashboard.json gerado com sucesso!")
