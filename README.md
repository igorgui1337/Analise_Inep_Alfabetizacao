# 📊 Bússola da Alfabetização

## 🔍 Visão Geral
O **EduDash Br** (Evolução da Alfabetização no Brasil) é um dashboard interativo focado em monitorar e projetar os índices de alfabetização em todo o Brasil (2019 a 2030). Unificando dados consolidados do MEC/Inep (SAEB), a ferramenta permite analisar detalhadamente o desempenho por estado e região, avaliar o gap em relação à meta estipulada e projetar tendências anuais futuras analisando o risco de atingimento até 2030.

## 🎯 Problema de Negócio
"O Brasil vai bater a meta de 80% até 2030?"

## 📈 Principais Insights
- +10 p.p. de recuperação pós-pandemia
- 20/27 UFs acima da meta
- Desigualdade forte entre regiões (ex: Norte vs Centro-Oeste)
- Risco de não atingir 80% no ritmo atual

## 🧠 Abordagem
- Análise histórica (2019–2025)
- Comparação com metas
- Projeção linear até 2030

## 🛠️ Tecnologias
- **Backend & Processamento:** Python (manipulação de dados e geração automatizada via script)
- **Frontend:** HTML5, Tailwind CSS e tipografia Inter
- **Dataviz:** JavaScript, Chart.js e ChartDataLabels

## 🌐 Acesse o Dashboard
Para acessar o painel interativo localmente, basta abrir o arquivo [**`dashboard_alfabetizacao.html`**](./dashboard_alfabetizacao.html) no seu navegador web.

## 📎 Relatório completo
Os dados processados podem ser explorados na base [`dados_dashboard.json`](./dados_dashboard.json). O fluxo de consolidação dos dados está disponível nos scripts Python deste repositório (`process_data_merged.py`, `gen_stats.py` e `build_dashboard_merged.py`).
