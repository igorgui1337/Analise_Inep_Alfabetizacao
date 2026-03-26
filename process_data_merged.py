import pandas as pd
import numpy as np
import json

# Função para limpeza genérica
def clean_cols(df):
    cols = [c for c in df.columns if 'PC_' in c or 'META_' in c or 'SAEB_' in c]
    for c in cols:
        df[c] = df[c].astype(str).str.replace('>', '').str.replace('<', '').str.replace('*', '').str.strip()
        df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

try:
    df_2023 = clean_cols(pd.read_excel('resultados_e_metas_ufs.xlsx', header=1))
    df_2024 = clean_cols(pd.read_excel('resultados_e_metas_ufs_2024_2.xlsx', header=1))
    df_2025 = clean_cols(pd.read_excel('resultados_e_metas_ufs_2025.xlsx', header=1))
except Exception as e:
    print(f"Erro ao ler os arquivos: {e}")
    exit(1)

# Extrair as colunas exclusivas de 2023
# SAEB_2019, SAEB_2021, PC_AVALIADOS_LP (renomear para PART_2023)
df_2023_sub = df_2023[['SIGLA_UF', 'SAEB_2019', 'SAEB_2021', 'PC_AVALIADOS_LP']].rename(
    columns={'PC_AVALIADOS_LP': 'PARTICIPACAO_2023'}
)

# Extrair a participação de 2024
df_2024_sub = df_2024[['SIGLA_UF', 'PC_AVALIADOS_LP']].rename(
    columns={'PC_AVALIADOS_LP': 'PARTICIPACAO_2024'}
)

# Base principal (2025) já contém as alfabetizações e metas principais
df_main = df_2025.rename(columns={
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
    'PC_AVALIADOS_LP': 'PARTICIPACAO_2025'
})

# Merge das 3 bases
df_merged = df_main.merge(df_2023_sub, on='SIGLA_UF', how='left')
df_merged = df_merged.merge(df_2024_sub, on='SIGLA_UF', how='left')

# Regiões
regiao_map = {
    'AC': 'Norte', 'AM': 'Norte', 'AP': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}

df_brasil = df_merged[df_merged['NOME_UF'] == 'Brasil'].copy()
df_uf = df_merged[df_merged['NOME_UF'] != 'Brasil'].copy()
df_uf = df_uf.dropna(subset=['SIGLA_UF'])
df_uf['REGIAO'] = df_uf['SIGLA_UF'].map(regiao_map)

# Métricas originais
df_uf['VAR_23_24'] = df_uf['ALF_2024'] - df_uf['ALF_2023']
df_uf['VAR_24_25'] = df_uf['ALF_2025'] - df_uf['ALF_2024']
df_uf['VAR_23_25'] = df_uf['ALF_2025'] - df_uf['ALF_2023']
df_uf['GAP_META_2024'] = df_uf['ALF_2024'] - df_uf['META_2024']
df_uf['GAP_META_2025'] = df_uf['ALF_2025'] - df_uf['META_2025']

def projetar_conservador(row):
    """
    Modelo conservador com desaceleração progressiva (damped growth).
    
    Lógica:
    1. Calcula a tendência observada 2023->2025 (ou 2024->2025 se 2023 faltar)
    2. A cada ano futuro, a taxa de crescimento é reduzida proporcionalmente ao 
       quanto ainda falta para atingir 100%: crescimento_real = taxa * (100 - valor_atual) / 100
    3. Isso simula a saturação natural — estados com taxas altas crescem mais devagar.
    4. Adiciona um penalizador extra se a taxa histórica for negativa (estados em declínio).
    """
    alf_2025 = row.get('ALF_2025')
    alf_2024 = row.get('ALF_2024')
    alf_2023 = row.get('ALF_2023')

    if alf_2025 is None or np.isnan(alf_2025):
        return pd.Series({f'PROJ_{y}': None for y in range(2026, 2031)} | {'TENDENCIA_ANUAL': None})

    # Tendência observada (media dos 2 últimos anos disponíveis)
    if alf_2023 is not None and not np.isnan(alf_2023):
        tendencia_base = (alf_2025 - alf_2023) / 2.0
    elif alf_2024 is not None and not np.isnan(alf_2024):
        tendencia_base = alf_2025 - alf_2024
    else:
        tendencia_base = 0.0

    result = {}
    valor_atual = alf_2025

    for y in range(2026, 2031):
        if tendencia_base >= 0:
            # Crescimento com desaceleração logística: menos espaço → menos crescimento
            margem = max(0, 100 - valor_atual)
            crescimento = tendencia_base * (margem / 100.0)
        else:
            # Se a tendência é negativa (declínio), aplicar diretamente sem amortecimento
            crescimento = tendencia_base

        valor_atual = float(np.clip(valor_atual + crescimento, 0, 100))
        result[f'PROJ_{y}'] = round(valor_atual, 1)

    result['TENDENCIA_ANUAL'] = round(tendencia_base, 2)
    return pd.Series(result)

# Aplicar modelo conservador linha a linha
proj_cols = df_uf.apply(projetar_conservador, axis=1)
df_uf = pd.concat([df_uf, proj_cols], axis=1)

# Variações e gaps
df_uf['VAR_23_24'] = df_uf['ALF_2024'] - df_uf['ALF_2023']
df_uf['VAR_24_25'] = df_uf['ALF_2025'] - df_uf['ALF_2024']
df_uf['VAR_23_25'] = df_uf['ALF_2025'] - df_uf['ALF_2023']
df_uf['GAP_META_2024'] = df_uf['ALF_2024'] - df_uf['META_2024']
df_uf['GAP_META_2025'] = df_uf['ALF_2025'] - df_uf['META_2025']

# Status de atingimento por ano
for y in range(2026, 2031):
    df_uf[f'STATUS_{y}'] = np.where(df_uf[f'PROJ_{y}'] >= df_uf[f'META_{y}'], 'Atinge', 'Não atinge')

df_uf['STATUS_2025'] = np.where(df_uf['ALF_2025'] >= df_uf['META_2025'], 'Acima da Meta', 'Abaixo da Meta')

# Dump to JSON
data_json = df_uf.to_dict(orient='records')
brasil_json = df_brasil.to_dict(orient='records')[0] if len(df_brasil) > 0 else {}

with open('dados_dashboard.json', 'w', encoding='utf-8') as f:
    json.dump({'ufs': data_json, 'brasil': brasil_json}, f, ensure_ascii=False, indent=2)

# Imprimir resumo
print("\n=== RESUMO DAS PROJEÇÕES CONSERVADORAS — Damped Growth (2030) ===")
resumo = df_uf[['SIGLA_UF', 'ALF_2025', 'TENDENCIA_ANUAL', 'PROJ_2026', 'PROJ_2028', 'PROJ_2030', 'META_2030', 'STATUS_2030']].sort_values('STATUS_2030')
print(resumo.to_string(index=False))
print(f"\nTotal que ATINGE meta 2030: {(df_uf['STATUS_2030'] == 'Atinge').sum()}")
print(f"Total em RISCO em 2030:     {(df_uf['STATUS_2030'] == 'Não atinge').sum()}")
print("\nProcessamento concluído — Modelo Conservador (Damped Growth).")


