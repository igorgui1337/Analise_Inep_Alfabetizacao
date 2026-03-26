import json

with open('dados_dashboard.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Carregar os dados como string JSON para embedding
data_json_str = json.dumps(data, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Evolução da Alfabetização no Brasil (2019-2025)</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
            color: #1f2937;
        }}
        .card {{
            background: #ffffff; border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
            padding: 1.5rem;
        }}
        .metric-title {{
            font-size: 0.875rem; color: #6b7280; text-transform: uppercase;
            letter-spacing: 0.05em; font-weight: 600;
        }}
        .metric-value {{ font-size: 2.25rem; font-weight: 700; color: #111827; margin-top: 0.5rem; }}
        .nav-link.active {{ border-bottom: 2px solid #2563eb; color: #2563eb; font-weight: 600; }}
    </style>
</head>
<body class="bg-gray-100">
    <div class="flex h-screen overflow-hidden">
        <!-- Sidebar -->
        <div class="w-64 bg-white shadow-lg z-10 hidden md:block">
            <div class="h-16 flex items-center justify-center border-b border-gray-200">
                <h1 class="text-xl font-bold text-blue-600">EduDash Br</h1>
            </div>
            <nav class="p-4 space-y-2">
                <a href="#" onclick="showPage('page1')" id="nav-page1" class="nav-link active block py-2 px-4 rounded bg-blue-50 text-blue-700">Visão Geral</a>
                <a href="#" onclick="showPage('page2')" id="nav-page2" class="nav-link block py-2 px-4 rounded hover:bg-gray-50">Regiões e Estados</a>
                <a href="#" onclick="showPage('page3')" id="nav-page3" class="nav-link block py-2 px-4 rounded hover:bg-gray-50">Participação e Projeções</a>
            </nav>
            <div class="p-4 mt-8 border-t border-gray-200">
                <p class="text-xs text-gray-500 mb-2">Filtro Global:</p>
                <select id="global-region-filter" onchange="applyFilters()" class="w-full text-sm p-2 border rounded border-gray-300">
                    <option value="Brasil">Todos (Brasil)</option>
                    <option value="Norte">Norte</option>
                    <option value="Nordeste">Nordeste</option>
                    <option value="Centro-Oeste">Centro-Oeste</option>
                    <option value="Sudeste">Sudeste</option>
                    <option value="Sul">Sul</option>
                </select>
            </div>
        </div>

        <!-- Main Content -->
        <div class="flex-1 overflow-x-hidden overflow-y-auto w-full">
            <!-- Header -->
            <header class="bg-white shadow flex items-center justify-between px-6 py-4">
                <h2 id="page-title" class="text-2xl font-semibold text-gray-800">Visão Geral</h2>
                <span class="text-sm text-gray-500">Dados consolidados: 3 bases do MEC/Inep (2023 a 2025)</span>
            </header>

            <main class="p-6">
                <!-- Page 1: Visão Geral -->
                <div id="page1" class="page-content block">
                    <!-- Cards -->
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                        <div class="card">
                            <div class="metric-title">MÉDIA BRASIL (2025)</div>
                            <div class="metric-value" id="card-media-brasil">--%</div>
                            <div class="text-sm flex items-center mt-2 font-medium" id="card-cresc-brasil">--</div>
                        </div>
                        <div class="card">
                            <div class="metric-title">UFs ACIMA DA META (2025)</div>
                            <div class="metric-value text-blue-600" id="card-ufs-acima">--</div>
                            <div class="text-sm text-gray-500 mt-2">de 27 UFs</div>
                        </div>
                        <div class="card">
                            <div class="metric-title">PARTICIPAÇÃO BRASIL (2025)</div>
                            <div class="metric-value text-purple-600" id="card-part-brasil">--%</div>
                            <div class="text-sm text-gray-500 mt-2">Escolas/Alunos avaliados</div>
                        </div>
                        <div class="card">
                            <div class="metric-title">ESTADO LÍDER (2025)</div>
                            <div class="metric-value text-emerald-600" id="card-estado-lider">--</div>
                            <div class="text-sm text-gray-500 mt-2" id="card-estado-lider-val">--% Alfabetizados</div>
                        </div>
                    </div>

                    <!-- Charts row 1 -->
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        <div class="card">
                            <h3 class="text-lg font-semibold mb-4">Evolução Histórica da Alfabetização (2019-2025)</h3>
                            <canvas id="chart-evolucao"></canvas>
                        </div>
                        <div class="card">
                            <h3 class="text-lg font-semibold mb-4">Resultado vs Meta 2025 (Regiões)</h3>
                            <canvas id="chart-metas-regiao"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Page 2: Regiões e Estados -->
                <div id="page2" class="page-content hidden">
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        <div class="card">
                            <h3 class="text-lg font-semibold mb-4">Ranking por Região (Alfabetização 2025)</h3>
                            <canvas id="chart-ranking-regioes"></canvas>
                        </div>
                        <div class="card">
                            <h3 class="text-lg font-semibold mb-4">UFs com Maior Avanço (2023 → 2025)</h3>
                            <canvas id="chart-maior-avanco"></canvas>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        <div class="card">
                            <h3 class="text-lg font-semibold mb-4">Top 5 Estados (2025)</h3>
                            <canvas id="chart-top5"></canvas>
                        </div>
                        <div class="card">
                            <h3 class="text-lg font-semibold mb-4">Bottom 5 Estados (2025)</h3>
                            <canvas id="chart-bottom5"></canvas>
                        </div>
                    </div>
                    <div class="card mb-6">
                        <h3 class="text-lg font-semibold mb-2">Visão do Gap para a Meta (2025)</h3>
                        <p class="text-sm text-gray-500 mb-4">Diferença entre o resultado atingido e a meta pactuada para 2025. Valores positivos indicam superação da meta.</p>
                        <canvas id="chart-gap-metas"></canvas>
                    </div>
                </div>

                <!-- Page 3: Participação e Projeções -->
                <div id="page3" class="page-content hidden">
                    
                    <div class="card mb-6">
                        <h3 class="text-lg font-semibold mb-2">Trajetória e Projeção até 2030</h3>
                        <p class="text-sm text-gray-500 mb-4">Acompanhamento contínuo da série histórica desde 2019 projetado linearmente até 2030, comparado com a meta estabelecida para o recorte atual.</p>
                        <canvas id="chart-projecao-longa" style="max-height: 400px;"></canvas>
                    </div>

                    <div class="card mb-6">
                        <h3 class="text-lg font-semibold mb-2">Evolução da Taxa de Participação (2023 - 2025)</h3>
                        <p class="text-sm text-gray-500 mb-4">Percentual de alunos/escolas que participaram da avaliação do Sistema SAEB por ano e região.</p>
                        <canvas id="chart-participacao" style="max-height: 350px;"></canvas>
                    </div>

                    <div class="card">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-lg font-semibold">Projeção e Risco de Atingimento Futuro (2026 - 2029)</h3>
                            <select id="projecao-ano-filter" onchange="renderProjectionsTable()" class="p-2 border rounded border-gray-300">
                                <option value="2026">Projeção 2026</option>
                                <option value="2027">Projeção 2027</option>
                                <option value="2028">Projeção 2028</option>
                                <option value="2029">Projeção 2029</option>
                                <option value="2030" selected>Projeção 2030</option>
                            </select>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="min-w-full text-left text-sm whitespace-nowrap">
                                <thead class="uppercase tracking-wider border-b-2 border-gray-200 bg-gray-50">
                                    <tr>
                                        <th class="px-4 py-3">UF</th>
                                        <th class="px-4 py-3">Res. 2025</th>
                                        <th class="px-4 py-3">Partic. 2025</th>
                                        <th class="px-4 py-3">Tendência a.a.</th>
                                        <th class="px-4 py-3" id="th-proj-ano">Proj. 2029</th>
                                        <th class="px-4 py-3" id="th-meta-ano">Meta 2029</th>
                                        <th class="px-4 py-3">Status Esperado</th>
                                    </tr>
                                </thead>
                                <tbody id="table-projections-body" class="divide-y divide-gray-200">
                                    <!-- Dynamic rows -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                </div>

            </main>
        </div>
    </div>

    <script>
        Chart.register(ChartDataLabels);
        Chart.defaults.font.family = "'Inter', sans-serif";
        Chart.defaults.color = "#4b5563";
        
        const db = {data_json_str};
        let filteredUfs = db.ufs;
        let charts = {{}};

        function showPage(pageId) {{
            document.querySelectorAll('.page-content').forEach(el => el.classList.add('hidden'));
            document.getElementById(pageId).classList.remove('hidden');
            
            document.querySelectorAll('.nav-link').forEach(el => {{
                el.classList.remove('active', 'bg-blue-50', 'text-blue-700');
            }});
            document.getElementById('nav-' + pageId).classList.add('active', 'bg-blue-50', 'text-blue-700');
            
            const titles = {{ 'page1': 'Visão Geral', 'page2': 'Análise por Regiões e Estados', 'page3': 'Participação e Projeções Futuras' }};
            document.getElementById('page-title').innerText = titles[pageId] || 'Dashboard';
            window.dispatchEvent(new Event('resize'));
        }}

        function applyFilters() {{
            const regiao = document.getElementById('global-region-filter').value;
            filteredUfs = regiao === "Brasil" ? db.ufs : db.ufs.filter(u => u.REGIAO === regiao);
            renderDashboard();
        }}

        const fPct = (val) => (val === null || isNaN(val)) ? '--' : Number(val).toFixed(1) + '%';
        const parseNum = (val) => isNaN(parseFloat(val)) ? null : parseFloat(val);

        function agruparRegiaoMedia(data, campos) {{
            const res = {{}};
            data.forEach(d => {{
                if(!res[d.REGIAO]) res[d.REGIAO] = {{}};
                campos.forEach(c => {{
                    if(!res[d.REGIAO][c]) res[d.REGIAO][c] = [];
                    const v = parseNum(d[c]);
                    if(v !== null) res[d.REGIAO][c].push(v);
                }});
            }});
            return Object.keys(res).map(r => {{
                let obj = {{ regiao: r }};
                campos.forEach(c => {{
                    obj[c] = res[r][c].length ? res[r][c].reduce((a,b)=>a+b,0) / res[r][c].length : null;
                }});
                return obj;
            }}).sort((a,b) => (b.ALF_2025||0) - (a.ALF_2025||0));
        }}

        function initChart(id, config) {{
            if (charts[id]) charts[id].destroy();
            const ctx = document.getElementById(id).getContext('2d');
            charts[id] = new Chart(ctx, config);
        }}

        function renderDashboard() {{
            renderCards();
            renderEvolucao();
            renderMetasRegiao();
            renderRankingRegioes();
            renderMaiorAvanco();
            renderTopBottom();
            renderGapMetas();
            renderParticipacao();
            renderProjecaoLonga();
            renderProjectionsTable();
        }}

        function renderCards() {{
            if(db.brasil && db.brasil.ALF_2025) {{
                document.getElementById('card-media-brasil').innerText = fPct(db.brasil.ALF_2025);
                const diff = (db.brasil.ALF_2025 - (db.brasil.ALF_2023||0)).toFixed(1);
                document.getElementById('card-cresc-brasil').innerHTML = 
                    `<span class="${{diff >= 0 ? 'text-green-600' : 'text-red-500'}}">${{diff >= 0 ? '↑' : '↓'}} ${{Math.abs(diff)}} p.p. vs 2023</span>`;
                
                document.getElementById('card-part-brasil').innerText = fPct(db.brasil.PARTICIPACAO_2025);
            }}

            const acima = filteredUfs.filter(u => u.STATUS_2025 === 'Acima da Meta').length;
            document.getElementById('card-ufs-acima').innerText = acima;

            const sortedUfs = [...filteredUfs].filter(u => u.ALF_2025 !== null).sort((a,b) => b.ALF_2025 - a.ALF_2025);
            if(sortedUfs.length > 0) {{
                document.getElementById('card-estado-lider').innerText = sortedUfs[0].SIGLA_UF;
                document.getElementById('card-estado-lider-val').innerText = fPct(sortedUfs[0].ALF_2025) + ' (' + sortedUfs[0].NOME_UF + ')';
            }}
        }}

        function renderEvolucao() {{
            const isBrasil = document.getElementById('global-region-filter').value === 'Brasil';
            let datasets = [];
            const labels = ['2019 (SAEB)', '2021 (SAEB)', '2023', '2024', '2025'];
            
            if (isBrasil && db.brasil) {{
                datasets.push({{
                    label: 'Média Brasil',
                    data: [db.brasil.SAEB_2019, db.brasil.SAEB_2021, db.brasil.ALF_2023, db.brasil.ALF_2024, db.brasil.ALF_2025],
                    borderColor: '#2563eb', backgroundColor: 'rgba(37,99,235,0.1)', fill: true, tension: 0.3, borderWidth: 3
                }});
            }}

            const colors = ['#059669', '#d97706', '#7c3aed', '#db2777', '#0891b2'];
            const regioes = [...new Set(filteredUfs.map(u => u.REGIAO))];
            regioes.forEach((r, idx) => {{
                let rgUfs = filteredUfs.filter(u => u.REGIAO === r);
                const avg = (campo) => {{
                    let vals = rgUfs.map(u => parseNum(u[campo])).filter(v => v !== null);
                    return vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : null;
                }};
                datasets.push({{
                    label: `Média ${{r}}`,
                    data: [avg('SAEB_2019'), avg('SAEB_2021'), avg('ALF_2023'), avg('ALF_2024'), avg('ALF_2025')],
                    borderColor: colors[idx%colors.length], borderDash: isBrasil ? [5, 5] : [], tension: 0.3
                }});
            }});

            initChart('chart-evolucao', {{
                type: 'line', data: {{ labels, datasets }},
                options: {{ plugins: {{ datalabels: {{ display: false }}, legend: {{ position: 'bottom' }} }} }}
            }});
        }}

        function renderMetasRegiao() {{
            const rData = agruparRegiaoMedia(filteredUfs, ['ALF_2025', 'META_2025']);
            initChart('chart-metas-regiao', {{
                type: 'bar',
                data: {{
                    labels: rData.map(d => d.regiao),
                    datasets: [
                        {{ label: 'Resultado 2025', data: rData.map(d => d.ALF_2025), backgroundColor: '#3b82f6', borderRadius: 4 }},
                        {{ label: 'Meta 2025', data: rData.map(d => d.META_2025), backgroundColor: '#d1d5db', type: 'line', borderWidth: 0, pointRadius: 10, pointBackgroundColor: '#4b5563', pointStyle: 'rectRot' }}
                    ]
                }},
                options: {{ plugins: {{ datalabels: {{ color: '#fff', font: {{weight: 'bold'}}, formatter: v => v?.toFixed(0)+'%' }} }} }}
            }});
        }}

        function renderRankingRegioes() {{
               const rData = agruparRegiaoMedia(db.ufs, ['ALF_2025']);
               initChart('chart-ranking-regioes', {{
                   type: 'bar',
                   data: {{
                       labels: rData.map(d => d.regiao),
                       datasets: [{{
                           label: 'Média Alfabetização 2025 (%)',
                           data: rData.map(d => d.ALF_2025),
                           backgroundColor: rData.map((d,i) => i===0 ? '#10b981' : (i===rData.length-1 ? '#f43f5e' : '#6366f1')),
                           borderRadius: 4
                       }}]
                   }},
                   options: {{ indexAxis: 'y', plugins: {{ datalabels: {{ anchor: 'end', align: 'left', color: '#fff', formatter: v=>v?.toFixed(1)+'%' }}, legend: {{display:false}} }} }}
               }});
        }}

        function renderTopBottom() {{
            const sorted = [...filteredUfs].filter(u => u.ALF_2025).sort((a,b) => b.ALF_2025 - a.ALF_2025);
            const top5 = sorted.slice(0, 5);
            const bottom5 = sorted.slice(-5).reverse();

            initChart('chart-top5', {{
                type: 'bar', data: {{ labels: top5.map(d => d.SIGLA_UF), datasets: [{{ data: top5.map(d => d.ALF_2025), backgroundColor: '#10b981', borderRadius: 4 }}] }},
                options: {{ plugins: {{ legend: {{display:false}} }}, scales: {{y: {{min: 40}}}} }}
            }});

            initChart('chart-bottom5', {{
                type: 'bar', data: {{ labels: bottom5.map(d => d.SIGLA_UF), datasets: [{{ data: bottom5.map(d => d.ALF_2025), backgroundColor: '#f43f5e', borderRadius: 4 }}] }},
                options: {{ plugins: {{ legend: {{display:false}} }}, scales: {{y: {{min: 20}}}} }}
            }});
        }}

        function renderMaiorAvanco() {{
            const sorted = [...filteredUfs].filter(u => u.VAR_23_25 !== null && !isNaN(u.VAR_23_25)).sort((a,b) => b.VAR_23_25 - a.VAR_23_25);
            initChart('chart-maior-avanco', {{
                type: 'bar', data: {{ labels: sorted.slice(0, 5).map(d => d.SIGLA_UF), datasets: [{{ label: 'Evolução + (p.p.)', data: sorted.slice(0, 5).map(d => d.VAR_23_25), backgroundColor: '#0ea5e9' }}] }},
                options: {{ plugins: {{ datalabels: {{ anchor: 'end', align: 'top', formatter: v=>'+'+v.toFixed(1) }}, legend: {{display:false}} }} }}
            }});
        }}

        function renderGapMetas() {{
            const sorted = [...filteredUfs].filter(u => u.GAP_META_2025 !== null && !isNaN(u.GAP_META_2025)).sort((a,b) => b.GAP_META_2025 - a.GAP_META_2025);
            initChart('chart-gap-metas', {{
                type: 'bar',
                data: {{ labels: sorted.map(u => u.SIGLA_UF), datasets: [{{ label: 'Gap vs Meta 2025 (p.p.)', data: sorted.map(u => u.GAP_META_2025), backgroundColor: sorted.map(v => v >= 0 ? '#10b981' : '#f43f5e') }}] }},
                options: {{ plugins: {{ datalabels: {{ formatter: v=> (v>0?'+':'') + v.toFixed(1), anchor: (ctx) => ctx.dataset.data[ctx.dataIndex] >= 0 ? 'end' : 'start', align: (ctx) => ctx.dataset.data[ctx.dataIndex] >= 0 ? 'top' : 'bottom' }}, legend: {{display:false}} }} }}
            }});
        }}

        function renderParticipacao() {{
            const isBrasil = document.getElementById('global-region-filter').value === 'Brasil';
            let datasets = [];
            const labels = ['2023', '2024', '2025'];
            
            if (isBrasil && db.brasil) {{
                datasets.push({{
                    label: 'Média Brasil',
                    data: [db.brasil.PARTICIPACAO_2023, db.brasil.PARTICIPACAO_2024, db.brasil.PARTICIPACAO_2025],
                    backgroundColor: '#8b5cf6', borderRadius: 4
                }});
            }}

            const colors = ['#059669', '#d97706', '#7c3aed', '#db2777', '#0891b2'];
            const rData = agruparRegiaoMedia(filteredUfs, ['PARTICIPACAO_2023', 'PARTICIPACAO_2024', 'PARTICIPACAO_2025']);
            
            if(!isBrasil) {{
                rData.forEach((d, idx) => {{
                    datasets.push({{
                        label: `Região ${{d.regiao}}`,
                        data: [d.PARTICIPACAO_2023, d.PARTICIPACAO_2024, d.PARTICIPACAO_2025],
                        backgroundColor: colors[idx%colors.length], borderRadius: 4
                    }});
                }});
            }}

            initChart('chart-participacao', {{
                type: 'bar', data: {{ labels, datasets }},
                options: {{ plugins: {{ datalabels: {{ color: '#fff', formatter: v => v?.toFixed(0)+'%' }} }}, scales: {{ y: {{ min: 50, max: 100 }} }} }}
            }});
        }}

        function renderProjecaoLonga() {{
            let datasets = [];
            const labels = ['2019', '2021', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'];
            
            const avg = (campo) => {{
                let vals = filteredUfs.map(u => parseNum(u[campo])).filter(v => v !== null && !isNaN(v));
                return vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : null;
            }};

            const histData = [avg('SAEB_2019'), avg('SAEB_2021'), avg('ALF_2023'), avg('ALF_2024'), avg('ALF_2025'), null, null, null, null, null];
            const projData = [null, null, null, null, avg('ALF_2025'), avg('PROJ_2026'), avg('PROJ_2027'), avg('PROJ_2028'), avg('PROJ_2029'), avg('PROJ_2030')];
            const metaData = [null, null, null, avg('META_2024'), avg('META_2025'), avg('META_2026'), avg('META_2027'), avg('META_2028'), avg('META_2029'), avg('META_2030')];

            datasets.push({{
                label: 'Resultados (%)', data: histData, borderColor: '#2563eb', backgroundColor: '#2563eb', tension: 0.3, fill: false, borderWidth: 3
            }});
            datasets.push({{
                label: 'Projeção Linear (%)', data: projData, borderColor: '#2563eb', borderDash: [5, 5], tension: 0.3, fill: false, borderWidth: 3
            }});
            datasets.push({{
                label: 'Meta Nacional/Local (%)', data: metaData, borderColor: '#9ca3af', backgroundColor: '#9ca3af', type: 'line', pointStyle: 'rectRot', borderDash: [2, 2], fill: false, pointRadius: 5
            }});

            initChart('chart-projecao-longa', {{
                type: 'line', data: {{ labels, datasets }},
                options: {{ 
                    plugins: {{ datalabels: {{ 
                        align: 'top', 
                        formatter: v => v ? v.toFixed(0)+'%' : '' 
                    }} }}, 
                    scales: {{ y: {{ suggestedMin: 40 }} }}
                }}
            }});
        }}

        function renderProjectionsTable() {{
            const ano = document.getElementById('projecao-ano-filter').value;
            const tbody = document.getElementById('table-projections-body');
            document.getElementById('th-proj-ano').innerText = 'Proj. ' + ano;
            document.getElementById('th-meta-ano').innerText = 'Meta ' + ano;
            
            let projField = 'PROJ_' + ano;
            let metaField = 'META_' + ano;
            let statusField = 'STATUS_' + ano;

            const sorted = [...filteredUfs].sort((a,b) => {{
                if(a[statusField] !== b[statusField]) return a[statusField] === 'Não atinge' ? -1 : 1;
                return (b[projField]||0) - (a[projField]||0);
            }});

            tbody.innerHTML = sorted.map((u, i) => {{
                const statusHtml = u[statusField] === 'Atinge' 
                    ? '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">Atinge</span>'
                    : '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800">Em Risco</span>';
                
                return `
                <tr class="${{i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}} hover:bg-gray-100">
                    <td class="px-4 py-2 font-medium text-gray-900">${{u.SIGLA_UF}}</td>
                    <td class="px-4 py-2">${{fPct(u.ALF_2025)}}</td>
                    <td class="px-4 py-2 text-indigo-600">${{fPct(u.PARTICIPACAO_2025)}}</td>
                    <td class="px-4 py-2 text-gray-500">${{u.TENDENCIA_ANUAL > 0 ? '+' : ''}}${{u.TENDENCIA_ANUAL ? u.TENDENCIA_ANUAL.toFixed(1) : '--'}} p.p./a.</td>
                    <td class="px-4 py-2 font-semibold text-gray-800">${{fPct(u[projField])}}</td>
                    <td class="px-4 py-2 text-gray-600">${{u[metaField] ? u[metaField] + '%' : 'N/A'}}</td>
                    <td class="px-4 py-2">${{statusHtml}}</td>
                </tr>
                `;
            }}).join('');
        }}

        document.addEventListener('DOMContentLoaded', () => {{ renderDashboard(); }});
    </script>
</body>
</html>
"""

with open('dashboard_alfabetizacao.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
    
print("Dashboard HTML atualizado gerado com sucesso!")
