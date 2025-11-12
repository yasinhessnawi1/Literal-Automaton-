"""
Generate a standalone HTML page with the interactive visualization.
This converts the Dash app into a static HTML file that can be hosted on GitHub Pages.
"""

import os


def generate_html():
    """Generate a standalone HTML page with interactive controls."""

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tsetlin Machine Literal Automaton Stationary Distribution</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 2rem;
            background: linear-gradient(135deg, #000000 0%, #444444 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            color: #2d3748;
            margin-bottom: 0.5rem;
            font-size: 2rem;
        }

        .subtitle {
            color: #718096;
            margin-bottom: 2rem;
            font-size: 1rem;
        }

        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .control-group {
            background: #f7fafc;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }

        label {
            display: block;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }

        input[type="range"] {
            width: 100%;
            height: 6px;
            border-radius: 5px;
            background: #cbd5e0;
            outline: none;
            -webkit-appearance: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            transition: all 0.2s;
        }

        input[type="range"]::-webkit-slider-thumb:hover {
            background: #5568d3;
            transform: scale(1.2);
        }

        input[type="range"]::-moz-range-thumb {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
        }

        .value-display {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #4a5568;
        }

        .current-value {
            font-weight: bold;
            color: #667eea;
            font-size: 1rem;
        }

        #plot {
            margin: 2rem 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .distribution-values {
            background: #f7fafc;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
            border: 1px solid #e2e8f0;
        }

        .distribution-values h3 {
            color: #2d3748;
            margin-bottom: 1rem;
        }

        .values-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.75rem;
        }

        .value-item {
            background: white;
            padding: 0.75rem;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            border-left: 3px solid #667eea;
        }

        .derived-params {
            background: #edf2f7;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: #2d3748;
        }

        .github-link {
            text-align: center;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 2px solid #e2e8f0;
        }

        .github-link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }

        .github-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tsetlin Machine Literal Automaton</h1>
        <p class="subtitle">Stationary Distribution Visualization</p>

        <div class="controls">
            <div class="control-group">
                <label for="s-slider">Specificity (s)</label>
                <input type="range" id="s-slider" min="1" max="25" step="0.1" value="10">
                <div class="value-display">
                    <span>Range: 1.0 - 25.0</span>
                    <span class="current-value" id="s-value">10.0</span>
                </div>
            </div>

            <div class="control-group">
                <label for="ply-slider">P(L | Y)</label>
                <input type="range" id="ply-slider" min="0" max="1" step="0.01" value="0.5">
                <div class="value-display">
                    <span>Range: 0.0 - 1.0</span>
                    <span class="current-value" id="ply-value">0.50</span>
                </div>
            </div>

            <div class="control-group">
                <label for="py-slider">P(Y)</label>
                <input type="range" id="py-slider" min="0" max="1" step="0.01" value="0.5">
                <div class="value-display">
                    <span>Range: 0.0 - 1.0</span>
                    <span class="current-value" id="py-value">0.50</span>
                </div>
            </div>

            <div class="control-group">
                <label for="pnotl-slider">P(¬L | ¬Y)</label>
                <input type="range" id="pnotl-slider" min="0" max="1" step="0.01" value="0.5">
                <div class="value-display">
                    <span>Range: 0.0 - 1.0</span>
                    <span class="current-value" id="pnotl-value">0.50</span>
                </div>
            </div>
        </div>

        <div id="plot"></div>

        <div class="distribution-values">
            <h3>State Probabilities</h3>
            <div class="values-grid" id="distribution-list"></div>
        </div>

        <div class="derived-params" id="derived-params"></div>

        <div class="github-link">
            <p>
                View the source code on
                <a href="https://github.com/yasinhessnawi1/Literal-Automaton-" target="_blank">GitHub</a>
            </p>
        </div>
    </div>

    <script>
        // Computation functions (ported from Python)
        function stationaryDistribution(s, py, ply, pnotl_noty) {
            const pnotly = 1.0 - ply;
            const pnoty = 1.0 - py;
            const base = ply * py + pnotl_noty * pnoty;

            const terms = [
                Math.pow(py, 4) * Math.pow(pnotly, 7),
                Math.pow(py, 3) * Math.pow(pnotly, 6) * s * base,
                Math.pow(py, 2) * Math.pow(pnotly, 5) * Math.pow(s, 2) * Math.pow(base, 2),
                py * Math.pow(pnotly, 4) * Math.pow(s, 3) * Math.pow(base, 3),
                Math.pow(pnotly, 3) * Math.pow(s, 4) * Math.pow(base, 4),
                ply * Math.pow(pnotly, 2) * Math.pow(s, 5) * Math.pow(base, 4),
                Math.pow(ply, 2) * pnotly * Math.pow(s, 6) * Math.pow(base, 4),
                Math.pow(ply, 3) * Math.pow(s, 7) * Math.pow(base, 4)
            ];

            const total = terms.reduce((a, b) => a + b, 0);

            if (total === 0) {
                return terms.map(() => 1.0 / terms.length);
            }

            const alpha = 1.0 / total;
            return terms.map(term => alpha * term);
        }

        // Update visualization
        function updateVisualization() {
            const s = parseFloat(document.getElementById('s-slider').value);
            const ply = parseFloat(document.getElementById('ply-slider').value);
            const py = parseFloat(document.getElementById('py-slider').value);
            const pnotl_noty = parseFloat(document.getElementById('pnotl-slider').value);

            // Update value displays
            document.getElementById('s-value').textContent = s.toFixed(1);
            document.getElementById('ply-value').textContent = ply.toFixed(2);
            document.getElementById('py-value').textContent = py.toFixed(2);
            document.getElementById('pnotl-value').textContent = pnotl_noty.toFixed(2);

            // Calculate distribution
            const distribution = stationaryDistribution(s, py, ply, pnotl_noty);
            const states = ['π₁', 'π₂', 'π₃', 'π₄', 'π₅', 'π₆', 'π₇', 'π₈'];

            // Update plot
            const trace = {
                x: states,
                y: distribution,
                type: 'bar',
                marker: {
                    color: '#667eea',
                    line: {
                        color: '#5568d3',
                        width: 1.5
                    }
                },
                hovertemplate: '%{x}: %{y:.6f}<extra></extra>'
            };

            const layout = {
                title: {
                    text: 'Literal Automaton Stationary Distribution',
                    font: { size: 18, color: '#2d3748' }
                },
                xaxis: {
                    title: 'State',
                    titlefont: { size: 14, color: '#4a5568' },
                    tickfont: { size: 14 }
                },
                yaxis: {
                    title: 'Probability',
                    titlefont: { size: 14, color: '#4a5568' },
                    range: [0, Math.max(...distribution) * 1.1]
                },
                margin: { l: 60, r: 30, t: 60, b: 60 },
                plot_bgcolor: '#ffffff',
                paper_bgcolor: '#ffffff'
            };

            Plotly.newPlot('plot', [trace], layout, {
                responsive: true,
                displayModeBar: false
            });

            // Update distribution values
            const listHtml = distribution.map((val, i) =>
                `<div class="value-item">π${i+1} = ${val.toFixed(6)}</div>`
            ).join('');
            document.getElementById('distribution-list').innerHTML = listHtml;

            // Update derived parameters
            const pnotly = 1.0 - ply;
            const pnoty = 1.0 - py;
            const base = ply * py + pnotl_noty * pnoty;

            document.getElementById('derived-params').innerHTML =
                `P(¬L | Y) = ${pnotly.toFixed(4)}, P(¬Y) = ${pnoty.toFixed(4)}, B = ${base.toFixed(4)}`;
        }

        // Add event listeners
        document.getElementById('s-slider').addEventListener('input', updateVisualization);
        document.getElementById('ply-slider').addEventListener('input', updateVisualization);
        document.getElementById('py-slider').addEventListener('input', updateVisualization);
        document.getElementById('pnotl-slider').addEventListener('input', updateVisualization);

        // Initial render
        updateVisualization();
    </script>
</body>
</html>"""

    return html_content

if __name__ == '__main__':
    import os

    # Create docs directory
    os.makedirs('docs', exist_ok=True)

    # Generate HTML
    html = generate_html()

    # Write to file
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("✅ Static site generated successfully in docs/index.html")
