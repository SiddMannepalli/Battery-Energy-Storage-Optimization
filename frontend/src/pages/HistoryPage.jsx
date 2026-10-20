import { useMemo } from 'react';
import { money, num, sum, runLabel } from '../format.js';
import { RED, baseOptions } from '../charts.js';
import ChartCanvas from '../components/ChartCanvas.jsx';
import { PageHeader, CardHeader, Kpi } from '../components/Layout.jsx';

export default function HistoryPage({ battery, runs, latest }) {
  const has = runs.length > 0;
  const best = has ? runs.reduce((m, r) => r.revenue > m.revenue ? r : m) : null;
  const worst = has ? runs.reduce((m, r) => r.revenue < m.revenue ? r : m) : null;

  const chart = useMemo(() => has ? {
    type: 'bar',
    data: { labels: runs.map(runLabel), datasets: [{ label: 'Net revenue', data: runs.map(r => r.revenue), backgroundColor: runs.map(r => r === latest ? '#635BFF' : r.revenue >= 0 ? '#C1C9D2' : RED) }] },
    options: baseOptions('$'),
  } : null, [runs, latest, has]);

  return (
    <section className="page active">
      <PageHeader title="Run History" sub={battery ? `${battery.name} · every optimization run` : ''} />
      <div className="kpi-grid">
        <Kpi tone="teal" label="Best Run" value={has ? money(best.revenue, 0) : '—'} sub={has && `${runLabel(best)} · ${best.date}`} />
        <Kpi tone="amber" label="Average Run" value={has ? money(sum(runs, 'revenue') / runs.length, 0) : '—'} sub="Net revenue per 24h run" />
        <Kpi tone="red" label="Worst Run" value={has ? money(worst.revenue, 0) : '—'} sub={has && `${runLabel(worst)} · ${worst.date}`} />
        <Kpi tone="blue" label="Total Runs" value={has ? runs.length : '—'} sub={has && `${new Set(runs.map(r => r.version)).size} versions`} />
      </div>
      <div className="chart-card mb">
        <CardHeader title="Net Revenue by Run" sub="Each bar is one optimization run" />
        <ChartCanvas config={chart} height="260px" />
      </div>
      <div className="chart-card">
        <CardHeader title="Runs" sub="Newest first" />
        <div className="table-scroll">
          <table className="data-table">
            <thead><tr><th>Run</th><th>Version</th><th>Date</th><th>Type</th><th className="num">Charged MWh</th><th className="num">Discharged MWh</th><th className="num">Net Revenue $</th></tr></thead>
            <tbody>
              {has ? [...runs].reverse().map(run => (
                <tr key={run.output_id}>
                  <td>#{run.output_id}</td><td>v{run.version}</td><td>{run.date}</td><td>{run.type}</td>
                  <td className="num">{num(run.charged / 1000)}</td><td className="num">{num(run.discharged / 1000)}</td>
                  <td className={`num ${run.revenue >= 0 ? 'rev-pos' : 'rev-neg'}`}>{money(run.revenue)}</td>
                </tr>
              )) : <tr><td colSpan="7" className="empty">No runs yet.</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
