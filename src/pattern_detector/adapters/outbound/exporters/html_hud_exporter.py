import json
import os
from ....domain.detection import DetectionReport
from ....ports.outbound.exporter_port import ExporterPort


class HtmlHudExporter(ExporterPort):
    def export(self, report: DetectionReport, output_path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        report_json = json.dumps(report.to_dict(), ensure_ascii=False)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DPX-Ruby | Ruby & Rails Architecture HUD</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #14080e;
            --card-bg: #26111c;
            --border-color: #4a152d;
            --primary: #fb7185;
            --primary-glow: rgba(251, 113, 133, 0.3);
            --ruby-red: #f43f5e;
            --rose-gold: #fda4af;
            --accent-green: #34d399;
            --accent-yellow: #fbbf24;
            --accent-red: #ef4444;
            --text-main: #fff1f2;
            --text-muted: #fecdd3;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }}
        body {{ background-color: var(--bg-dark); color: var(--text-main); line-height: 1.6; padding: 24px; }}
        .hud-container {{ max-width: 1500px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }}

        /* Top Header */
        .hud-header {{
            background: linear-gradient(135deg, rgba(38, 17, 28, 0.95), rgba(244, 63, 94, 0.15));
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(12px);
        }}
        .brand-title {{ display: flex; align-items: center; gap: 16px; }}
        .brand-logo {{
            font-size: 32px;
            background: linear-gradient(135deg, #fb7185, #f43f5e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
        }}
        .target-tag {{
            background: rgba(251, 113, 133, 0.1);
            color: var(--primary);
            border: 1px solid rgba(251, 113, 133, 0.3);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }}
        .metric-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            transition: all 0.2s ease;
        }}
        .metric-card:hover {{
            border-color: var(--primary);
            box-shadow: 0 4px 20px var(--primary-glow);
        }}
        .metric-label {{ font-size: 12px; text-transform: uppercase; color: var(--text-muted); font-weight: 600; letter-spacing: 0.5px; opacity: 0.8; }}
        .metric-value {{ font-size: 28px; font-weight: 800; color: var(--text-main); font-family: 'JetBrains Mono', monospace; }}

        /* Filter Controls */
        .filter-section {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
        }}
        .search-input {{
            background: rgba(20, 8, 14, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 16px;
            color: var(--text-main);
            font-size: 14px;
            width: 320px;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-input:focus {{ border-color: var(--primary); }}
        .pills-container {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .filter-pill {{
            background: rgba(74, 21, 45, 0.4);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .filter-pill.active, .filter-pill:hover {{
            background: rgba(251, 113, 133, 0.15);
            color: var(--primary);
            border-color: var(--primary);
        }}

        /* Findings Table */
        .findings-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            overflow: hidden;
        }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{
            background: #14080e;
            color: var(--text-muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 14px 20px;
            font-weight: 700;
            opacity: 0.9;
        }}
        td {{ padding: 14px 20px; border-top: 1px solid var(--border-color); font-size: 14px; vertical-align: middle; }}
        tr:hover {{ background: rgba(251, 113, 133, 0.04); }}

        .badge-cat {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', monospace;
        }}
        .cat-ruby_idiomatic {{ background: rgba(251, 113, 133, 0.15); color: #fb7185; border: 1px solid #fb7185; }}
        .cat-enterprise_rails {{ background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid #f43f5e; }}
        .cat-metaprogramming {{ background: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid #a855f7; }}
        .cat-creational {{ background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid #3b82f6; }}
        .cat-structural {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid #f59e0b; }}
        .cat-behavioral {{ background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid #34d399; }}
        .cat-security_hazards {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }}
        .cat-solid_principles {{ background: rgba(234, 179, 8, 0.15); color: #eab308; border: 1px solid #eab308; }}

        .confidence-bar {{
            width: 80px;
            height: 6px;
            background: #4a152d;
            border-radius: 3px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 8px;
        }}
        .confidence-fill {{ height: 100%; background: linear-gradient(90deg, #fb7185, #f43f5e); }}

        .btn-copy {{
            background: rgba(251, 113, 133, 0.1);
            color: var(--primary);
            border: 1px solid var(--primary);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .btn-copy:hover {{ background: var(--primary); color: #000; }}
    </style>
</head>
<body>
    <div class="hud-container">
        <!-- Top Header -->
        <header class="hud-header">
            <div class="brand-title">
                <span class="brand-logo">💎 DPX-Ruby</span>
                <span class="target-tag" id="headerPath">Ruby & Rails Analyzer</span>
            </div>
            <div>
                <button class="btn-copy" onclick="copyAiSummary()">🤖 Copy for AI Context</button>
            </div>
        </header>

        <!-- Metrics Grid -->
        <section class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Detections</div>
                <div class="metric-value" id="metricTotal">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Scanned Files</div>
                <div class="metric-value" id="metricFiles">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Execution Time</div>
                <div class="metric-value" id="metricTime">0.00s</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Security & Rails Hazards</div>
                <div class="metric-value" style="color: var(--accent-red)" id="metricHazards">0</div>
            </div>
        </section>

        <!-- Search and Filter Pills -->
        <section class="filter-section">
            <input type="text" class="search-input" id="searchInput" placeholder="Search patterns, classes, hazards..." oninput="filterResults()">
            <div class="pills-container" id="pillsContainer">
                <div class="filter-pill active" onclick="setCategoryFilter('ALL')">ALL</div>
            </div>
        </section>

        <!-- Findings Table -->
        <section class="findings-card">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Category</th>
                        <th>Pattern Type</th>
                        <th>Target Symbol</th>
                        <th>Confidence</th>
                        <th>Location</th>
                        <th>Summary</th>
                    </tr>
                </thead>
                <tbody id="findingsBody">
                    <!-- Injected via JS -->
                </tbody>
            </table>
        </section>
    </div>

    <script>
        const reportData = {report_json};
        let activeCategory = 'ALL';

        function initDashboard() {{
            document.getElementById('headerPath').innerText = reportData.target_path;
            document.getElementById('metricTotal').innerText = reportData.total_detections;
            document.getElementById('metricFiles').innerText = reportData.scanned_files_count;
            document.getElementById('metricTime').innerText = reportData.execution_time_seconds + 's';
            
            const hazards = reportData.category_counts['security_hazards'] || 0;
            document.getElementById('metricHazards').innerText = hazards;

            // Generate filter pills
            const pillsContainer = document.getElementById('pillsContainer');
            Object.keys(reportData.category_counts || {{}}).forEach(cat => {{
                const pill = document.createElement('div');
                pill.className = 'filter-pill';
                pill.innerText = `${{cat}} (${{reportData.category_counts[cat]}})`;
                pill.onclick = () => setCategoryFilter(cat);
                pillsContainer.appendChild(pill);
            }});

            renderTable(reportData.detections);
        }}

        function setCategoryFilter(cat) {{
            activeCategory = cat;
            document.querySelectorAll('.filter-pill').forEach(el => {{
                if (el.innerText.startsWith(cat) || (cat === 'ALL' && el.innerText === 'ALL')) {{
                    el.classList.add('active');
                }} else {{
                    el.classList.remove('active');
                }}
            }});
            filterResults();
        }}

        function filterResults() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            const filtered = reportData.detections.filter(d => {{
                const matchesCat = activeCategory === 'ALL' || d.category === activeCategory;
                const matchesQuery = d.target_name.toLowerCase().includes(query) ||
                    d.pattern_type.toLowerCase().includes(query) ||
                    d.summary.toLowerCase().includes(query) ||
                    d.location.file_path.toLowerCase().includes(query);
                return matchesCat && matchesQuery;
            }});
            renderTable(filtered);
        }}

        function renderTable(detections) {{
            const tbody = document.getElementById('findingsBody');
            tbody.innerHTML = '';
            detections.forEach((d, idx) => {{
                const tr = document.createElement('tr');
                const catClass = 'cat-' + d.category;
                const fileName = d.location.file_path.split('/').pop();
                
                tr.innerHTML = `
                    <td>${{idx + 1}}</td>
                    <td><span class="badge-cat ${{catClass}}">${{d.category}}</span></td>
                    <td style="font-family: 'JetBrains Mono'; font-weight: 600;">${{d.pattern_type}}</td>
                    <td><code style="color: var(--primary); font-weight: 600;">${{d.target_name}}</code></td>
                    <td>
                        <div class="confidence-bar"><div class="confidence-fill" style="width: ${{d.confidence.percentage}}%"></div></div>
                        <span style="font-size: 12px; font-weight: 700;">${{d.confidence.percentage}}%</span>
                    </td>
                    <td style="font-family: 'JetBrains Mono'; font-size: 12px; color: var(--text-muted);">${{fileName}}:${{d.location.line_number}}</td>
                    <td style="font-size: 13px; color: #cbd5e1;">${{d.summary}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function copyAiSummary() {{
            const btn = document.querySelector('.btn-copy');
            let text = "# 💎 DPX-Ruby Analysis Findings Summary\\n\\n";
            text += "- **Target Path**: " + reportData.target_path + "\\n";
            text += "- **Scanned Files**: " + reportData.scanned_files_count + "\\n";
            text += "- **Execution Time**: " + reportData.execution_time_seconds.toFixed(4) + "s\\n";
            text += "- **Total Detections**: " + reportData.total_detections + "\\n\\n";

            text += "## 📊 Category Breakdown\\n";
            for (const [cat, cnt] of Object.entries(reportData.category_counts || {{}})) {{
                text += "- **" + cat + "**: " + cnt + "\\n";
            }}

            text += "\\n## 🔍 Detections & Patterns\\n";
            reportData.detections.forEach((d, i) => {{
                const loc = d.location.file_path.split('/').pop() + ":" + d.location.line_number;
                text += (i + 1) + ". **[" + d.category + "] " + d.pattern_type + "** on `" + d.target_name + "` (" + d.confidence.percentage + "% confidence) at `" + loc + "`\\n";
                text += "   - *Summary*: " + d.summary + "\\n";
                if (d.evidence && d.evidence.length > 0) {{
                    d.evidence.forEach(ev => {{
                        text += "   - *Evidence*: " + ev.description + "\\n";
                    }});
                }}
            }});

            navigator.clipboard.writeText(text).then(() => {{
                const orig = btn.innerHTML;
                btn.innerHTML = '✔ Copied to Clipboard!';
                btn.style.background = 'var(--primary)';
                btn.style.color = '#000';
                setTimeout(() => {{
                    btn.innerHTML = orig;
                    btn.style.background = '';
                    btn.style.color = '';
                }}, 2500);
            }}).catch(err => {{
                console.error('Failed to copy', err);
            }});
        }}

        window.onload = initDashboard;
    </script>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
