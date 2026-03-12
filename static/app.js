/* ══════════════════════════════════════════════════════════════
   Multi-Agent Market Analysis Dashboard — Frontend Logic
   ══════════════════════════════════════════════════════════════ */

// ── State ────────────────────────────────────────────────────
let sentimentChart = null;
let pollInterval = null;
let currentReport = '';

// ── Init ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    loadDatasetStats();
    loadSavedReports();
});

// ── Dataset Stats ────────────────────────────────────────────
async function loadDatasetStats() {
    try {
        const res = await fetch('/api/dataset-stats');
        const data = await res.json();

        if (data.error) {
            console.error('Stats error:', data.error);
            return;
        }

        animateCounter('stat-total-val', data.total_reviews);
        animateCounter('stat-positive-val', data.positive_reviews);
        animateCounter('stat-negative-val', data.negative_reviews);
        animateCounter('stat-avg-len-val', data.avg_review_length, ' chars');

        renderSentimentChart(data.positive_reviews, data.negative_reviews);
    } catch (err) {
        console.error('Failed to load stats:', err);
    }
}

function animateCounter(elementId, target, suffix = '') {
    const el = document.getElementById(elementId);
    const duration = 1200;
    const start = performance.now();
    const startVal = 0;

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(startVal + (target - startVal) * eased);
        el.textContent = current.toLocaleString() + suffix;
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// ── Sentiment Chart ──────────────────────────────────────────
function renderSentimentChart(positive, negative) {
    const ctx = document.getElementById('sentimentChart').getContext('2d');

    if (sentimentChart) sentimentChart.destroy();

    sentimentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Negative'],
            datasets: [{
                data: [positive, negative],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)',
                ],
                borderWidth: 2,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: {
                            family: "'Inter', sans-serif",
                            size: 13,
                            weight: '500',
                        },
                        padding: 20,
                        usePointStyle: true,
                        pointStyleWidth: 12,
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(148, 163, 184, 0.2)',
                    borderWidth: 1,
                    cornerRadius: 10,
                    padding: 14,
                    titleFont: { family: "'Inter', sans-serif", weight: '600' },
                    bodyFont: { family: "'Inter', sans-serif" },
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed.toLocaleString()} (${pct}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                duration: 1000,
            }
        }
    });
}

// ── Analysis ─────────────────────────────────────────────────
async function startAnalysis() {
    const btn = document.getElementById('run-btn');
    const statusEl = document.getElementById('analysis-status');
    const queryInput = document.getElementById('query-input');

    btn.disabled = true;
    btn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin-icon"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        Analyzing...
    `;
    statusEl.classList.remove('hidden');

    const statusMessages = [
        { label: 'Initializing RAG Pipeline...', sub: 'Building vector embeddings' },
        { label: 'Retrieving Relevant Reviews...', sub: 'Querying ChromaDB' },
        { label: 'Sentiment Agent Working...', sub: 'Analyzing emotional patterns' },
        { label: 'Trend Agent Working...', sub: 'Extracting complaints & praise' },
        { label: 'Competitor Agent Working...', sub: 'Identifying market positioning' },
        { label: 'Strategist Agent Working...', sub: 'Generating recommendations' },
        { label: 'Compiling Final Report...', sub: 'Structuring insights' },
    ];

    let msgIndex = 0;
    const rotateStatus = setInterval(() => {
        msgIndex = (msgIndex + 1) % statusMessages.length;
        document.getElementById('status-label').textContent = statusMessages[msgIndex].label;
        document.getElementById('status-sub').textContent = statusMessages[msgIndex].sub;
    }, 8000);

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: queryInput.value }),
        });

        const data = await res.json();
        if (data.error) {
            alert('Error: ' + data.error);
            resetButton();
            clearInterval(rotateStatus);
            return;
        }

        // Poll for completion
        pollInterval = setInterval(async () => {
            try {
                const statusRes = await fetch('/api/analysis-status');
                const status = await statusRes.json();

                if (!status.running) {
                    clearInterval(pollInterval);
                    clearInterval(rotateStatus);

                    if (status.error) {
                        document.getElementById('status-label').textContent = 'Analysis Failed';
                        document.getElementById('status-sub').textContent = status.error;
                        resetButton();
                        return;
                    }

                    // Fetch result
                    const resultRes = await fetch('/api/analysis-result');
                    const result = await resultRes.json();

                    if (!result.error) {
                        displayReport(result.report);
                        currentReport = result.report;
                    }

                    statusEl.classList.add('hidden');
                    resetButton();
                    loadSavedReports();
                }
            } catch (e) {
                console.error('Poll error:', e);
            }
        }, 3000);

    } catch (err) {
        console.error('Analysis error:', err);
        alert('Failed to start analysis. Is the server running?');
        clearInterval(rotateStatus);
        resetButton();
    }
}

function resetButton() {
    const btn = document.getElementById('run-btn');
    btn.disabled = false;
    btn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        Start Analysis
    `;
}

// ── Report Display ───────────────────────────────────────────
function displayReport(markdown) {
    const section = document.getElementById('report-section');
    const content = document.getElementById('report-content');

    content.innerHTML = marked.parse(markdown);
    section.classList.remove('hidden');

    // Scroll into view
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function downloadReport() {
    if (!currentReport) return;

    const blob = new Blob([currentReport], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `market_analysis_${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ── Saved Reports ────────────────────────────────────────────
async function loadSavedReports() {
    try {
        const res = await fetch('/api/reports');
        const reports = await res.json();

        const container = document.getElementById('reports-list');

        if (!reports.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    <p>No saved reports yet</p>
                    <p class="empty-sub">Run an analysis to generate your first report</p>
                </div>
            `;
            return;
        }

        container.innerHTML = reports.map(r => `
            <div class="report-item" onclick="loadReport('${r.name}')">
                <div class="report-item-info">
                    <span class="report-item-name">${r.name}</span>
                    <span class="report-item-date">${new Date(r.created).toLocaleString()}</span>
                </div>
                <span class="report-item-size">${formatBytes(r.size)}</span>
            </div>
        `).join('');

    } catch (err) {
        console.error('Failed to load reports:', err);
    }
}

async function loadReport(name) {
    try {
        const res = await fetch(`/api/reports/${name}`);
        const data = await res.json();

        if (!data.error) {
            displayReport(data.content);
            currentReport = data.content;
        }
    } catch (err) {
        console.error('Failed to load report:', err);
    }
}

// ── Utilities ────────────────────────────────────────────────
function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}
