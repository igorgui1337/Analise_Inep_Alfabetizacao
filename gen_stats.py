import json
import pandas as pd
import numpy as np

with open('dados_dashboard.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ufs = pd.DataFrame(data['ufs'])
brasil = data['brasil']

def fmt(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return 'N/D'
    return f"{float(val):.1f}%"

# ---------- Estatísticas Globais ----------
alf_2025 = ufs[ufs['ALF_2025'].notna()].sort_values('ALF_2025', ascending=False)
alf_var = ufs[ufs['VAR_23_25'].notna()].sort_values('VAR_23_25', ascending=False)
gap = ufs[ufs['GAP_META_2025'].notna()].sort_values('GAP_META_2025')

acima_meta = ufs[ufs['STATUS_2025'] == 'Acima da Meta']
abaixo_meta = ufs[ufs['STATUS_2025'] == 'Abaixo da Meta']

# Rankings regionais
def regiao_media(campo):
    return ufs.groupby('REGIAO')[campo].mean().sort_values(ascending=False)

rm = regiao_media('ALF_2025')
rm_var = regiao_media('VAR_23_25')

# Projeções 2030
atinge_2030 = ufs[ufs['STATUS_2030'] == 'Atinge']
nao_atinge_2030 = ufs[ufs['STATUS_2030'] == 'Não atinge']

out = {}
out['brasil'] = brasil
out['top_alf'] = alf_2025.head(5)[['SIGLA_UF','NOME_UF','REGIAO','ALF_2023','ALF_2024','ALF_2025','META_2025','GAP_META_2025']].to_dict('records')
out['bottom_alf'] = alf_2025.tail(5)[['SIGLA_UF','NOME_UF','REGIAO','ALF_2023','ALF_2024','ALF_2025','META_2025','GAP_META_2025']].to_dict('records')
out['top_avanco'] = alf_var.head(5)[['SIGLA_UF','VAR_23_24','VAR_24_25','VAR_23_25']].to_dict('records')
out['regiao_alf'] = rm.reset_index().to_dict('records')
out['regiao_var'] = rm_var.reset_index().to_dict('records')
out['acima_meta'] = acima_meta[['SIGLA_UF','ALF_2025','META_2025','GAP_META_2025']].to_dict('records')
out['abaixo_meta'] = abaixo_meta[['SIGLA_UF','ALF_2025','META_2025','GAP_META_2025']].to_dict('records')
out['atinge_2030_count'] = len(atinge_2030)
out['nao_atinge_2030_count'] = len(nao_atinge_2030)
out['atinge_2030_ufs'] = atinge_2030['SIGLA_UF'].tolist()
out['nao_atinge_2030_ufs'] = nao_atinge_2030[['SIGLA_UF','PROJ_2030','META_2030']].to_dict('records')

with open('stats_relatorio.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

print("Stats geradas com sucesso!")
